import requests

def get_full_auto_playlist():
    base_url = "https://streamed.pk/api"
    playlist_content = "#EXTM3U\n"
    seen_ids = set() # ডুপ্লিকেট ম্যাচ বাদ দেওয়ার জন্য

    try:
        # ১. সব স্পোর্টস ক্যাটাগরি টেনে আনা
        print("Fetching all available sports categories...")
        sports_response = requests.get(f"{base_url}/sports", timeout=15).json()
        
        # 'live' ক্যাটাগরি ডিফল্ট হিসেবে যোগ করা (কারণ এটি অনেক সময় লিস্টে থাকে না)
        categories = [{"id": "live", "name": "Live Events"}] + sports_response

        for sport in categories:
            sport_id = sport.get('id')
            sport_name = sport.get('name')
            
            print(f"Fetching matches for: {sport_name}...")
            
            try:
                # ২. নির্দিষ্ট স্পোর্টসের সব ম্যাচ নেওয়া
                matches = requests.get(f"{base_url}/matches/{sport_id}", timeout=15).json()
                
                for match in matches:
                    m_unique_id = match.get('id')
                    if m_unique_id in seen_ids:
                        continue
                    seen_ids.add(m_unique_id)

                    title = match.get('title', 'Live Match')
                    # পোস্টার বা লোগো নেওয়া
                    logo = match.get('poster', 'https://cdn-icons-png.flaticon.com/512/5351/5351486.png')
                    sources = match.get('sources', [])
                    
                    for src in sources:
                        s_source = src.get('source')
                        s_id = src.get('id')
                        
                        # ৩. প্রতিটি সোর্সের স্ট্রিম লিঙ্ক ফেচ করা
                        try:
                            stream_api = f"{base_url}/stream/{s_source}/{s_id}"
                            streams = requests.get(stream_api, timeout=10).json()
                            
                            for s in streams:
                                lang = s.get('language', 'English')
                                hd = "HD" if s.get('hd') else "SD"
                                url = s.get('embedUrl')
                                
                                # M3U ফরম্যাটে ডাটা সাজানো
                                playlist_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{sport_name}", {title} [{s_source.upper()}] ({lang} - {hd})\n'
                                playlist_content += f"{url}\n"
                        except:
                            continue
            except:
                continue

        # ৪. ফাইল সেভ করা
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print(f"Successfully created playlist with {len(seen_ids)} matches!")

    except Exception as e:
        print(f"Critical Error: {e}")

if __name__ == "__main__":
    get_full_auto_playlist()
