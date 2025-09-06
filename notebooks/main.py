import asyncio
from sound_processing import play_sound, play_sound_async
from leds import breathe_color_async
from rich import print
from rich.console import Console
import time
import os

# Wake Up
import pvporcupine
import pyaudio
import struct
import os

# Warnings
import warnings
from scipy.io.wavfile import WavFileWarning
warnings.filterwarnings("ignore", category=WavFileWarning)

console = Console()

PICOVOICE_API_KEY = os.environ['PICOVOICE_API_KEY']
porcupine = pvporcupine.create(access_key=PICOVOICE_API_KEY,
                               keywords=['porcupine'])
pa = pyaudio.PyAudio()
stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

## Functions
async def handle_wake_sequence():
    console.print("[magenta] Wake word detected!")
    await asyncio.gather(
        play_sound_async("audio/star_ding.wav"),
        breathe_color_async(color_name="magenta", cycles=3, step_delay=0.03, max_brightness=30)
    )

if __name__ =="__main__":
    console.rule("[green4] Hello from Porcupine![/]")

    while True:
        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        result = porcupine.process(pcm)
        if result >= 0:
            asyncio.run(handle_wake_sequence())
