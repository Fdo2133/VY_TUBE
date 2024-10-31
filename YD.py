import yt_dlp
import streamlit as st
import ffmpeg
import os

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.streams = None
    
    def load_video_info(self):
        try:
            ydl_opts = {'format': 'bestvideo+bestaudio/best'}  # Combina la mejor calidad de video y audio
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.info = ydl.extract_info(self.url, download=False)
            st.success("Video cargado con éxito.")
        except Exception as e:
            st.error("Error al cargar el video.")
            st.stop()

    def download(self):
        try:
            ydl_opts = {'format': 'bestvideo+bestaudio/best'}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            st.success("Descarga completada con éxito.")
            self.convert_to_mp4_720p()  # Llama a la función de conversión
        except Exception as e:
            st.error("Error al descargar el video.")

    def convert_to_mp4_720p(self):
        # Encuentra el último archivo descargado
        video_files = [f for f in os.listdir() if f.endswith('.mkv') or f.endswith('.webm') or f.endswith('.mp4')]
        if not video_files:
            st.error("No se encontró ningún archivo de video para convertir.")
            return
        
        latest_video = max(video_files, key=os.path.getctime)  # Obtiene el archivo más reciente
        output_file = f"{os.path.splitext(latest_video)[0]}_720p.mp4"  # Nombre del archivo de salida

        # Usar ffmpeg para convertir el video a 720p
        try:
            ffmpeg.input(latest_video).output(output_file, vf='scale=1280:720').run(overwrite_output=True)
            st.success(f"Conversión a 720p completada: {output_file}")
        except Exception as e:
            st.error("Error al convertir el video.")

if __name__ == "__main__":
    st.title("Descargador de videos de YouTube")
    url = st.text_input("Ingrese la url del video a descargar")

    if url:
        downloader = YouTubeDownloader(url)
        downloader.load_video_info()
        if downloader.info:
            if st.button("Descargar video"):
                downloader.download()
