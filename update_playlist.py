import requests
import json

def get_complete_playlist():
    base_url = "https://streamed.pk/api"
    # সোর্সগুলো ব্লক হওয়া এড়াতে হেডার ব্যবহার
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://streamed.pk/"
    }
    
    playlist_content = "#EXTM3U x-tvg-url=\"\"\n"
    seen_match_ids = set()

    try:
        # ১. সব স্পোর্টস ক্যাটাগরি লিস্ট ফেচ করা
        print("Fetching sports categories...")
        sports_data = requests.get(f"{base_url}/sports", headers=headers, timeout=15).json()
        
        # 'live' এবং 'all' ক্যাটাগরি যোগ করা যাতে কোনো কিছু মিস না হয়
        target_categories = [{"id": "live", "name": "LIVE NOW"}] + sports_data

        for sport in target_categories:
            s_id = sport.get('id')
            s_name = sport.get('name', 'Sports')
            
            print(f"Processing: {s_name}")
            
            try:
                # ২. নির্দিষ্ট ক্যাটাগরির ম্যাচগুলো নেওয়া
                matches = requests.get(f"{base_url}/matches/{s_id}", headers=headers, timeout=15).json()
                
                for match in matches:
                    m_id = match.get('id')
                    # ডুপ্লিকেট ম্যাচ বাদ দেওয়া
                    if m_id in seen_match_ids:
                        continue
                    seen_match_ids.add(m_id)

                    title = match.get('title', 'Live Event')
                    logo = match.get('poster', 'https://cdn-icons-png.flaticon.com/512/5351/5351486.png')
                    
                    # ৩. প্রতিটি ম্যাচের সোর্স থেকে স্ট্রিম লিঙ্ক বের করা
                    for source in match.get('sources', []):
                        try:
                            s_name_api = source.get('source')
                            s_id_api = source.get('id')
                            
                            stream_res = requests.get(f"{base_url}/stream/{s_name_api}/{s_id_api}", headers=headers, timeout=10).json()
                            
                            for stream in stream_res:
                                embed_url = stream.get('embedUrl')
                                lang = stream.get('language', 'Multi')
                                quality = "HD" if stream.get('hd') else "SD"
                                
                                # ৪. M3U ফরম্যাটে ডাটা রাইট করা (অ্যাড ব্লকার সাপোর্ট বাড়াতে হেডারসহ)
                                # অনেক প্লেয়ারে '|Referer=...' ফরম্যাট কাজ করে
                                final_link = f"{embed_url}|Referer=https://streamed.pk/&User-Agent=Mozilla/5.0"
                                
                                playlist_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{s_name.upper()}", {title} [{s_name_api.upper()}] ({lang} - {quality})\n'
                                playlist_content += f"{final_link}\n"
                        except:
                            continue
            except:
                continue

        # ৫. ফাইল রাইট করা
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(playlist_content)
        
        print(f"Update Successful! Total matches added: {len(seen_match_ids)}")

    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == "__main__":
    get_complete_playlist()
