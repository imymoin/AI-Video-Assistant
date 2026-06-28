from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source = "https://www.youtube.com/watch?v=7qZH3D7u-z8&t=2s"

chunks = process_input(source)

print(transcribe_all(chunks))