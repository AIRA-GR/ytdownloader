import streamlit as st
import yt_dlp
import os
import glob

st.set_page_config(page_title="Media Downloader", layout="centered")
st.title("Media Downloader")

url = st.text_input("Paste YouTube Link Here:")
fmt = st.selectbox("Format:", ["Video (MP4)", "Audio (MP3)"])
qual = st.selectbox("Quality:", ["High", "Medium", "Low"])

if st.button("Start Download", type="primary"):
    if not url:
        st.error("Please enter a URL.")
    else:
        output_dir = "temp_downloads"
        os.makedirs(output_dir, exist_ok=True)
        
        # Clean previous downloads
        for f in glob.glob(f"{output_dir}/*"):
            os.remove(f)

        ydl_opts = {'outtmpl': f'{output_dir}/%(title)s.%(ext)s', 'quiet': True}
        
        if fmt == 'Video (MP4)':
            ydl_opts['merge_output_format'] = 'mp4'
            if qual == 'High': ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
            elif qual == 'Medium': ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]/best'
            else: ydl_opts['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]/best'
        else:
            ydl_opts['format'] = 'bestaudio/best'
            kbps = '320' if qual == 'High' else ('192' if qual == 'Medium' else '128')
            ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': kbps}]

        try:
            with st.spinner("Downloading... Please wait."):
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            
            downloaded_files = glob.glob(f"{output_dir}/*")
            if downloaded_files:
                file_path = downloaded_files[0]
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Save to Device",
                        data=file,
                        file_name=os.path.basename(file_path),
                        mime="video/mp4" if fmt == 'Video (MP4)' else "audio/mpeg"
                    )
                st.success("Download Ready! Click the button above.")
        except Exception as e:
            st.error("Error: Process Failed. Please check the link.")
