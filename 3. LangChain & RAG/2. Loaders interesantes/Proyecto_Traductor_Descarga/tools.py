import subprocess
import whisper

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

    model = whisper.load_model("base")

    print("🎙️ Transcribiendo...")

    result = model.transcribe(audio_path)
    return result["text"]


def pipeline(url: str):
    audio = download_audio(url)
    text = transcribe_audio(audio)
    return text   # 👈 IMPORTANTE: SOLO TEXTO
