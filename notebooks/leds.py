import spidev
import time
import asyncio

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 8000000


BRIGHTNESS_LEVELS = {
    "off": 0,
    "very-low": 5,
    "low": 5,
    "mid": 15,
    "mid-high": 20,
    "full": 31
}

COLORS = {
    "blue": [255, 0, 0],
    "light_blue": [230, 216, 173],
    "magenta": [255, 0, 255],
    "yellow": [0, 255, 255],
    "green": [0, 255, 0],
    "light_green": [144, 238, 144],
    "orange": [0, 165, 255],
    "red": [0, 0, 255]
}


def set_led_color(color: dict, brightness_mode: dict):
    '''
    Following APA102 SPI Protocol
    # Start Frame: [0x00, 0x00, 0x00, 0x00]
    # Format: [brightness, Blue, Green, Red]
    # Brightness: 0b111xxxxx (0–31)
    # End Frame: [0xFF, 0xFF, 0xFF, 0xFF]
    '''
    data = []
    data += [0x00, 0x00, 0x00, 0x00]
    brightness = [0b11100000 | brightness_mode]
    for _ in range(3):  # 3 LEDs on the HAT
        data += brightness + color
    data += [0xFF, 0xFF, 0xFF, 0xFF]
    spi.xfer2(data)

# def breathe_color(color_name, cycles=3, step_delay=0.05, max_brightness:int = 31):
#     color = COLORS[color_name]
#     # Smooth brightness ramp up and down
#     brightness_values = list(range(0, max_brightness+1, 1)) + list(range(max_brightness, -1, -1))
#     for _ in range(cycles):
#         for b in brightness_values:
#             set_led_color(color, b)
#             time.sleep(step_delay)

# async def breathe_color_async(color_name, cycles, step_delay, max_brightness ):
#     loop = asyncio.get_running_loop()
#     await loop.run_in_executor(None, breathe_color, color_name, cycles, step_delay, max_brightness )


async def breathe_color_async(color_name, cycles=3, step_delay=0.05, max_brightness=31):
    color = COLORS[color_name]
    brightness_values = list(range(0, max_brightness+1)) + list(range(max_brightness, -1, -1))
    for _ in range(cycles):
        for b in brightness_values:
            set_led_color(color, b)
            await asyncio.sleep(step_delay)