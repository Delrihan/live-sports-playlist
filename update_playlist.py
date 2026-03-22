import requests

def get_playlist():
    base_url = "https://streamed.pk/api"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://streamed.pk/"
    }
    
    playlist_content = "#EXTM3U\n"
    seen_urls = set()

    try:
        # সব ক্যাটাগরি নিয়ে আসা
        sports = requests.get(f"{base_url}/sports", headers=headers, timeout=15).json()
        categories = [{"id": "live", "name": "LIVE NOW"}] + sports

        for sport in categories:
            s_id = sport.get('id')
            s_name = sport.get('name', 'Sports')
            
            try:
                matches = requests.get(f"{base_url}/matches/{s_id}", headers=headers, timeout=15).json()
                for match in matches:
                    title = match.get('title', 'Live Match')
                    logo = match.get('poster', 'https://cdn-icons-png.flaticon.com/512/5351/5351486.png')
                    
                    for src in match.get('sources', []):
                        try:
                            res = requests.get(f"{base_url}/stream/{src['source']}/{src['id']}", headers=headers, timeout=10).json()
                            for s in res:
                                url = s.get('embedUrl')
                                if url and url not in seen_urls:
                                    seen_urls.add(url)
                                    playlist_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{s_name.upper()}", {title}\n{url}\n'
                        except: continue
            except: continue

        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print("Playlist generated successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    get_playlist()
