from langchain_community.document_loaders import YoutubeLoader


def transcription_song(url_song: str) -> str | None:
    print("--- [YOUTUBE LOADER] ---")

    try:
        loader = YoutubeLoader.from_youtube_url(
            url_song,
            add_video_info=True,
            language=["es", "en"]
        )

        docs = loader.load()

        if not docs:
            print("No se encontró ninguna transcripción.")
            return None

        video_info = docs[0].metadata

        print(f"Título: {video_info.get('title')}")
        print(f"Autor: {video_info.get('author')}")

        transcript = docs[0].page_content

        print(f"Fragmento: {transcript[:200]}...")

        return transcript

    except Exception as e:
        print(
            f"⚠️ Error obteniendo la transcripción: {e}"
        )
        return None

# Prueba de que la funcion funciona y trae la cancion 
if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
    transcription_song(url)