import whisper
import os
import requests
from pydub import AudioSegment



WHISPER_MODEL = os.getenv("WHISPER_MODEL", "tiny")


_model = None


def load_model():

    global _model  

    if _model is None: 
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")
        _model = whisper.load_model(WHISPER_MODEL) 
        print("Whisper model loaded.")
    return _model 


def transcribe_chunk(chunk_path: str, translate : bool = False) -> str:

    model = load_model()  

    task = "translate" if translate else "transcribe"


    result = model.transcribe(chunk_path, task=task)
    
    return result["text"]

def transcribe_all(chunks: list, translate : bool = False) -> str:

    full_transcript = "" 


    for i, chunk in enumerate(chunks):  

        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")

        text = transcribe_chunk(chunk, translate=translate)  

        full_transcript += text + " "  

    print("Transcription complete.")

    return full_transcript.strip()  