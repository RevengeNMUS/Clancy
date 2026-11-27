import faulthandler
from faster_whisper import WhisperModel

faulthandler.enable()
model = WhisperModel("tiny", device="cpu", compute_type="float32", cpu_threads=1)
print("Loaded OK")