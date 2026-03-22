import requests

def fetch_playlist():
    # লাইভ এবং সব স্পোর্টস ক্যাটাগরি
    cats = ['live', 'football', 'cricket', 'basketball', 'tennis']
    playlist_content = "#EXTM3U\n"
    seen_ids = set()

    for cat in cats:
        try:
            url = f"https://streamed.pk/api/matches/{cat}"
            matches = requests.get(url, timeout=10).json()
            
            for match in matches:
                m_id = match.get('id')
                if m_id in seen_ids: continue
                seen_ids.add(m_id)

                title = match.get('title', 'Live Match')
                # লোগো সেট করা (যদি API তে থাকে, নাহলে ডিফল্ট স্পোর্টস আইকন)
                logo = match.get('poster', 'https://cdn-icons-png.flaticon.com/512/5351/5351486.png')
                
                sources = match.get('sources', [])
                for src in sources:
                    s_name = src.get('source')
                    s_id = src.get('id')
                    
                    # স্ট্রিম ডাটা ফেচ করা
                    try:
                        s_url = f"https://streamed.pk/api/stream/{s_name}/{s_id}"
                        streams = requests.get(s_url, timeout=10).json()
                        
                        for i, s in enumerate(streams):
                            final_link = s.get('embedUrl')
                            lang = s.get('language', 'Unknown')
                            
                            # M3U ফরম্যাট উইথ লোগো এবং গ্রুপ
                            playlist_content += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{cat.upper()}", {title} ({s_name.upper()} - {lang})\n'
                            playlist_content += f"{final_link}\n"
                    except:
                        continue
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(playlist_content)
    print("Playlist Updated Successfully!")

if __name__ == "__main__":
    fetch_playlist()
