def download_audio(video_url, token):
    """Download audio and return direct MP3 URL, avoiding m3u8 playlists."""
    try:
        unique_id = str(uuid.uuid4())[:8]
        output_template = os.path.join(DOWNLOAD_FOLDER, f"audio_{unique_id}.%(ext)s")
        
        # Updated options to force a direct, playable mp3 URL
        ydl_opts = {
            # Force direct HTTP/HTTPS protocol, avoiding HLS (m3u8)
            'format': '(bestaudio/best)[protocol~="^https?$"]', 
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128', # 128kbps is faster and good for streaming
            }],
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,           # Ensure we only get a single track
            # Add this to mimic a mobile client, sometimes yields better URLs
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            # The final filename after conversion
            mp3_filename = output_template.replace('%(ext)s', 'mp3')
            
            # Ensure the file exists and is not an m3u8 playlist
            if os.path.exists(mp3_filename) and not mp3_filename.endswith('.m3u8'):
                tokens[token] = {
                    'file_path': mp3_filename,
                    'timestamp': time.time(),
                    'title': info.get('title', 'audio'),
                    'ready': True
                }
                return True
            else:
                print(f"Error: File not created or is wrong format: {mp3_filename}")
                return False
                
    except Exception as e:
        print(f"Download error: {str(e)}")
        return False