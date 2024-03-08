# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai

aai.settings.api_key = "7e3a73239ae84d1583fa5625a66cfef5"
transcriber = aai.Transcriber()

transcript = transcriber.transcribe(
    "https://storage.googleapis.com/aai-web-samples/news.mp4"
)
# transcript = transcriber.transcribe("./my-local-audio-file.wav")

print(transcript.text)
