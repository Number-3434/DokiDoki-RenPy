import os
import subprocess
import sys

import azure.cognitiveservices.speech as speechsdk
from flask import Flask, jsonify, request


def ensure_packages(packages):
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{package} not found. Installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Check packages
ensure_packages(["azure.cognitiveservices.speech", "dotenv", "flask"])

AZURE_KEY = "YOUR_KEY"
AZURE_REGION = "YOUR_REGION"

app = Flask(__name__)


@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text", "")
    filename = request.json.get("filename", "line.wav")

    # Configure Azure TTS
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_KEY, region=AZURE_REGION)
    speech_config.speech_synthesis_output_format = (
        speechsdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm
    )
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

    synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config
    )
    result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return jsonify({"status": "ok", "filename": filename})
    else:
        return jsonify({"status": "error", "reason": str(result.reason)}), 500


if __name__ == "__main__":
    # Optional: ensure output directory exists
    os.makedirs("tts_cache", exist_ok=True)
    app.run(port=5005)
