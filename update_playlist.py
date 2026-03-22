import requests

def get_complete_playlist():
    base_url = "https://streamed.pk/api"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://streamed.pk/"
    }
    
    playlist_content = "#EXTM3U\n"
    seen_urls = set()

    try:
        # সব স্পোর্টস ক্যাটাগরি লিস্ট ফেচ করা
        print("Fetching categories...")
        sports_data = requests.get(f"{base_url}/sports", headers=headers, timeout=15).json()
        target_categories = [{"id": "live", "name": "LIVE NOW"}] + sports_data

        for sport in target_categories:
            s_id = sport.get('id')
            s_name = sport.get('name', 'Sports')
            
            try:
                matches = requests.get(f"{base_url}/matches/{s_id}", headers=headers, timeout=15).json()
                for match in matches:
                    title = match.get('title', 'Live Event')
                    logo = match.get('poster', 'https://cdn-icons-png.flaticon.com/512/5351/5351486.png')
                    
                    for source in match.get('sources', []):
                        try:
                            s_name_api = source.get('source')
                            s_id_api = source.get('id')
                            stream_res = requests.get(f"{base_url}/stream/{s_name_api}/{s_id_api}", headers=headers, timeout=10).json()
                            
                            for s in stream_res:
                                url = s.get('embedUrl')
                                if url and url not in seen_urls:
                                    seen_urls.add(url)
                                    lang = s.get('language', 'English')
                                    # M3U Format
                                    playlist_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{s_name.upper()}", {title} ({lang})\n'
                                    playlist_content += f"{url}\n"
                        except: continue
            except: continue

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print("Success: Playlist created!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_complete_playlist()
