import requests

def get_live_playlist():
    matches_url = "https://streamed.pk/api/matches/live"
    playlist_content = "#EXTM3U\n"
    
    try:
        matches = requests.get(matches_url).json()
        for match in matches:
            title = match.get('title', 'Unknown Match')
            sources = match.get('sources', [])
            for src in sources:
                s_name = src.get('source')
                s_id = src.get('id')
                stream_api = f"https://streamed.pk/api/stream/{s_name}/{s_id}"
                streams = requests.get(stream_api).json()
                for s in streams:
                    lang = s.get('language', 'English')
                    url = s.get('embedUrl')
                    playlist_content += f"#EXTINF:-1 group-title='Live Sports', {title} [{s_name.upper()}] ({lang})\n"
                    playlist_content += f"{url}\n"
        
        with open("playlist.m3u", "w", encoding="utf-8") as f:
            f.write(playlist_content)
        print("Playlist updated!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_live_playlist()
