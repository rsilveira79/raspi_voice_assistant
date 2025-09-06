import sounddevice as sd
from scipy.io import wavfile
import asyncio


def play_sound(file: str):

    samplerate, data = wavfile.read(file)
    sd.play(data, samplerate)
    sd.wait()

async def play_sound_async(path):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, play_sound, path)