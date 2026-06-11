import subprocess
import whisper

YOUTUBE_URL = "https://www.youtube.com/watch?v=hmjfuuuRRYU"

def download_audio(url: str, output_name="audio.mp3"):
    print("⬇️ Descargando audio...")

    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", output_name,
        url
    ]

    subprocess.run(command, check=True)

    return output_name

def transcribe_audio(audio_path: str):
    print("🧠 Cargando Whisper...")

    model = whisper.load_model("medium")

    print("🎙️ Transcribiendo...")

    result = model.transcribe(audio_path)

    text = result["text"]

    # guardar archivo
    with open("transcripcion.txt", "w", encoding="utf-8") as f:
        f.write(text)

    return text

def pipeline(url: str):
    audio_file = download_audio(url)
    text = transcribe_audio(audio_file)

    print("\n====================")
    print("TRANSCRIPCIÓN FINAL")
    print("====================\n")
    print(text)


if __name__ == "__main__":
    pipeline(YOUTUBE_URL)