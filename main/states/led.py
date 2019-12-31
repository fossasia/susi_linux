try:
    import spidev
except ImportError:
    print("No spidev, probably no raspi ...")
import subprocess
import sys
import os
from math import ceil

RGB_MAP = {'rgb': [3, 2, 1], 'rbg': [3, 1, 2], 'grb': [
    2, 3, 1], 'gbr': [2, 1, 3], 'brg': [1, 3, 2], 'bgr': [1, 2, 3]}


class LED_COLOR:

    # Constants
    MAX_BRIGHTNESS = 0b11111  # Safeguard: Set to a value appropriate for your setup
    LED_START = 0b11100000   # Three "1" bits, followed by 5 brightness bits

    def __init__(self, num_led, global_brightness=MAX_BRIGHTNESS,
                 order='rgb', bus=0, device=1, max_speed_hz=8000000):
        if (os.access("/proc/asound/cards", os.R_OK)):
            output = subprocess.check_output(
                ["cat", "/proc/asound/cards"]).decode(sys.stdout.encoding)
            self.seeed_attached = output.find("seeed") != -1
        else:
            self.seeed_attached = False
        if (not self.seeed_attached):
            return
        self.num_led = num_led  # The number of LEDs in the Strip
        order = order.lower()
        self.rgb = RGB_MAP.get(order, RGB_MAP['rgb'])
        # Limit the brightness to the maximum if it's set higher
        if global_brightness > self.MAX_BRIGHTNESS:
            self.global_brightness = self.MAX_BRIGHTNESS
        else:
            self.global_brightness = global_brightness

        self.leds = [self.LED_START, 0, 0, 0] * self.num_led  # Pixel buffer
        self.spi = spidev.SpiDev()  # Init the SPI device
        self.spi.open(bus, device)  # Open SPI port 0, slave device (CS) 1
        # Up the speed a bit, so that the LEDs are painted faster
        if max_speed_hz:
            self.spi.max_speed_hz = max_speed_hz

    def clock_start_frame(self):
        if (not self.seeed_attached):
            return
        """Sends a start frame to the LED strip.
        """
        self.spi.xfer2([0] * 4)  # Start frame, 32 zero bits

    def clock_end_frame(self):
        if (not self.seeed_attached):
            return
        self.spi.xfer2([0xFF] * 4)

        # Round up num_led/2 bits (or num_led/16 bytes)
        # for _ in range((self.num_led + 15) // 16):
        #    self.spi.xfer2([0x00])

    def clear_strip(self):
        if (not self.seeed_attached):
            return
        """ Turns off the strip and shows the result right away."""

        for led in range(self.num_led):
            self.set_pixel(led, 0, 0, 0)
        self.show()

    def set_pixel(self, led_num, red, green, blue, bright_percent=100):
        if (not self.seeed_attached):
            return
        """Sets the color of one pixel in the LED stripe.

        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer. Colors are passed individually.
        If brightness is not set the global brightness setting is used.
        """
        if led_num < 0:
            return  # Pixel is invisible, so ignore
        if led_num >= self.num_led:
            return  # again, invisible

        # Calculate pixel brightness as a percentage of the
        # defined global_brightness. Round up to nearest integer
        # as we expect some brightness unless set to 0
        brightness = int(ceil(bright_percent * self.global_brightness / 100.0))

        # LED startframe is three "1" bits, followed by 5 brightness bits
        ledstart = (brightness & 0b00011111) | self.LED_START

        start_index = 4 * led_num
        self.leds[start_index] = ledstart
        self.leds[start_index + self.rgb[0]] = red
        self.leds[start_index + self.rgb[1]] = green
        self.leds[start_index + self.rgb[2]] = blue

    def set_pixel_rgb(self, led_num, rgb_color, bright_percent=100):
        if (not self.seeed_attached):
            return
        """
        Sets the color of one pixel in the LED stripe.

        The changed pixel is not shown yet on the Stripe, it is only
        written to the pixel buffer.
        Colors are passed combined (3 bytes concatenated)
        If brightness is not set the global brightness setting is used.
        """
        self.set_pixel(led_num, (rgb_color & 0xFF0000) >> 16,
                       (rgb_color & 0x00FF00) >> 8, rgb_color & 0x0000FF, bright_percent)

    def rotate(self, positions=1):
        if (not self.seeed_attached):
            return
        """
        Rotate the LEDs by the specified number of positions.

        Treating the internal LED array as a circular buffer, rotate it by
        the specified number of positions. The number could be negative,
        which means rotating in the opposite direction.
        """
        cutoff = 4 * (positions % self.num_led)
        self.leds = self.leds[cutoff:] + self.leds[:cutoff]

    def show(self):
        if (not self.seeed_attached):
            return
        """
        Sends the content of the pixel buffer to the strip.

        Todo: More than 1024 LEDs requires more than one xfer operation.
        """
        self.clock_start_frame()
        # xfer2 kills the list, unfortunately. So it must be copied first
        # SPI takes up to 4096 Integers. So we are fine for up to 1024 LEDs.
        data = list(self.leds)
        while data:
            self.spi.xfer2(data[:32])
            data = data[32:]
        self.clock_end_frame()

    def cleanup(self):
        if (not self.seeed_attached):
            return
        """Release the SPI device; Call this method at the end"""
        self.spi.close()  # Close SPI port

    @staticmethod
    def combine_color(red, green, blue):
        """Make one 3 * 8 byte color value."""

        return (red << 16) + (green << 8) + blue

    def wheel(self, wheel_pos):
        """Get a color from a color wheel; Green -> Red -> Blue -> Green"""

        if wheel_pos > 255:
            wheel_pos = 255  # Safeguard
        if wheel_pos < 85:  # Green -> Red
            return self.combine_color(wheel_pos * 3, 255 - wheel_pos * 3, 0)
        if wheel_pos < 170:  # Red -> Blue
            wheel_pos -= 85
            return self.combine_color(255 - wheel_pos * 3, 0, wheel_pos * 3)
        # Blue -> Green
        wheel_pos -= 170
        return self.combine_color(0, wheel_pos * 3, 255 - wheel_pos * 3)
