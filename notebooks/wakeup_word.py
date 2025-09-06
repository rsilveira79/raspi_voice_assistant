import pvporcupine
import pyaudio
import struct
import os

PICOVOICE_API_KEY = os.environ['PICOVOICE_API_KEY']

porcupine = pvporcupine.create(access_key=PICOVOICE_API_KEY,
                               keywords=['porcupine'])
pa = pyaudio.PyAudio()

def wakeup_word():
    pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    result = porcupine.process(pcm)
    if result >= 0:
        return True
    else:
        return False

async def wakeup_word_async():
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, wakeup_word)