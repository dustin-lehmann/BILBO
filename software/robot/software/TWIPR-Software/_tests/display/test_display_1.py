import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont


class Display:
    def __init__(self, width=128, height=64, i2c_address=0x3C):
        """
        Initialize the SH1106 OLED display using Adafruit's SSD1306 library.
        :param width: Width of the display (default is 128)
        :param height: Height of the display (default is 64)
        :param i2c_address: I2C address of the display (default is 0x3C)
        """
        self.width = width
        self.height = height
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.display = SSD1306_I2C(self.width, self.height, self.i2c, addr=i2c_address)

        # Initialize a blank image for drawing
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def clear(self):
        """Clear the display."""
        self.display.fill(0)
        self.display.show()

    def display_image(self):
        """Render the current image to the display."""
        self.display.image(self.image)
        self.display.show()

    def testFunction(self):
        """
        Display test content on the OLED:
        - Text
        - Geometric shapes
        """
        # Clear the display
        self.clear()

        # Draw some text
        font = ImageFont.load_default()
        self.draw.text((5, 5), "Hello, SH1106!", font=font, fill=255)

        # Draw some geometric shapes
        self.draw.rectangle((10, 20, 50, 40), outline=255, fill=0)  # Rectangle
        self.draw.ellipse((60, 20, 100, 40), outline=255, fill=0)   # Ellipse
        self.draw.line((0, 50, 127, 50), fill=255, width=1)         # Horizontal line

        # Render the image
        self.display_image()


# Example usage
if __name__ == "__main__":
    display = Display()
    display.testFunction()
