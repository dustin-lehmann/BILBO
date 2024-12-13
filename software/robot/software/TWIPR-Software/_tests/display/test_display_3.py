import random
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont
import time
import threading





class Page:
    def __init__(self, width, height, name="Page", border=False, show_title=True):
        """
        Initialize a page with a specified width and height.
        :param width: Width of the page
        :param height: Height of the page
        :param name: Name of the page
        :param border: Whether to render a 1px border around the page
        :param show_title: Whether to show the page title before rendering
        """
        self.width = width
        self.height = height
        self.name = name
        self.border = border  # Enable or disable page border
        self.show_title = show_title  # Enable or disable showing the title screen
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def draw_page(self):
        """
        Draw the static components of the page.
        Child classes should override this method to draw their content.
        """
        raise NotImplementedError("Subclasses must implement draw_page")

    def update_page(self, frame):
        """
        Update the dynamic components of the page.
        The default behavior includes rendering a border if enabled.
        """
        # Clear the page before drawing
        self.image = Image.new("1", (self.width, self.height), 0)  # Clear screen
        self.draw = ImageDraw.Draw(self.image)  # Reinitialize draw object

        # Render border if enabled
        if self.border:
            self.draw.rectangle(
                (0, 0, self.width - 1, self.height - 1),
                outline=255,
                fill=0,
            )

        # Allow child classes to render their content
        self.draw_page()


class ModePage(Page):
    def __init__(self, width, height, initial_mode="Idle"):
        """
        Initialize the Mode page.
        :param width: Width of the display
        :param height: Height of the display
        :param initial_mode: The initial mode to display
        """
        super().__init__(width, height, name="Mode", border=True, show_title=True)
        self.mode = initial_mode

    def set_mode(self, mode):
        """Set the current mode and redraw the page."""
        self.mode = mode

    def draw_page(self):
        """Draw the mode information in the middle of the screen."""
        font = ImageFont.load_default()

        i = random.randint(10, 20)
        # Prepare the text
        mode_text = f"Mode: {self.mode} + {i}"
        text_bbox = self.draw.textbbox((0, 0), mode_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Center the text
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2

        # Draw the text
        self.draw.text((x, y), mode_text, font=font, fill=255)


class StatusPage(Page):
    def __init__(self, width, height):
        """
        Initialize the Status page with dynamic elements.
        """
        super().__init__(width, height, name="Status Page", border=True, show_title=True)
        self.battery_level = "full"  # Options: "empty", "half", "full"
        self.battery_voltage = "16.8V"
        self.internet_connected = False
        self.joystick = False  # Whether the joystick is connected (True = filled, False = crossed out)
        self.user = "user"
        self.hostname = "hostname"
        self.ip_address = "0.0.0.0"
        self.ssid = "SSID"
        self.mode = "Idle"

    def set_battery(self, level, voltage):
        """Set the battery level and voltage."""
        self.battery_level = level
        self.battery_voltage = voltage

    def set_internet_status(self, connected):
        """Set the internet connection status."""
        self.internet_connected = connected

    def set_joystick_status(self, connected):
        """Set the joystick connection status."""
        self.joystick = connected

    def set_user_and_hostname(self, user, hostname):
        """Set the user and hostname."""
        self.user = user
        self.hostname = hostname

    def set_ip_address(self, ip):
        """Set the IP address."""
        self.ip_address = ip

    def set_ssid(self, ssid):
        """Set the WiFi SSID."""
        self.ssid = ssid

    def set_mode(self, mode):
        """Set the current mode."""
        self.mode = mode

    def draw_page(self):
        """Draw the Status page."""
        font = ImageFont.load_default()

        # Header Bar
        self._draw_status_bar(font)

        # Text block starting y-coordinate, shifted up by 3 pixels
        start_y = 15

        # Four lines of information
        self.draw.text((5, start_y), f"{self.user}@{self.hostname}", font=font, fill=255)
        self.draw.text((5, start_y + 12), f"IP: {self.ip_address}", font=font, fill=255)
        self.draw.text((5, start_y + 24), f"SSID: {self.ssid}", font=font, fill=255)
        self.draw.text((5, start_y + 36), f"Mode: {self.mode}", font=font, fill=255)

    def _draw_status_bar(self, font):
        """Draw the header bar with battery, internet, and joystick icons."""
        # Battery Icon
        battery_x = 2
        battery_y = 2
        battery_width = 16
        battery_height = 8
        terminal_width = 2

        # Draw battery outline
        self.draw.rectangle(
            (battery_x, battery_y, battery_x + battery_width, battery_y + battery_height),
            outline=255,
            fill=0,
        )

        # Draw battery terminal
        self.draw.rectangle(
            (
                battery_x + battery_width,
                battery_y + 2,
                battery_x + battery_width + terminal_width,
                battery_y + battery_height - 2,
            ),
            outline=255,
            fill=255,
        )

        # Fill battery based on level
        if self.battery_level == "empty":
            fill_width = 0
        elif self.battery_level == "half":
            fill_width = (battery_width - 2) // 2
        elif self.battery_level == "full":
            fill_width = battery_width - 2

        if fill_width > 0:
            self.draw.rectangle(
                (
                    battery_x + 1,
                    battery_y + 1,
                    battery_x + 1 + fill_width,
                    battery_y + battery_height - 1,
                ),
                outline=255,
                fill=255,
            )

        # Battery voltage text
        self.draw.text((battery_x + battery_width + terminal_width + 4, battery_y - 2), self.battery_voltage, font=font,
                       fill=255)

        # Internet status icon
        internet_x = battery_x + battery_width + terminal_width + 50
        if self.internet_connected:
            self.draw.ellipse((internet_x, battery_y, internet_x + 8, battery_y + 8), outline=255,
                              fill=255)  # Filled circle
        else:
            self.draw.ellipse((internet_x, battery_y, internet_x + 8, battery_y + 8), outline=255,
                              fill=0)  # Empty circle
            self.draw.line((internet_x, battery_y, internet_x + 8, internet_x + 8), fill=255, width=1)  # Cross line

        # Joystick status icon
        joystick_x = internet_x + 20
        joystick_y = battery_y
        if self.joystick:
            self.draw.rectangle(
                (joystick_x, joystick_y, joystick_x + 8, joystick_y + 8), outline=255, fill=255
            )  # Filled rectangle
        else:
            self.draw.rectangle(
                (joystick_x, joystick_y, joystick_x + 8, joystick_y + 8), outline=255, fill=0
            )  # Empty rectangle
            self.draw.line((joystick_x, joystick_y, joystick_x + 8, joystick_y + 8), fill=255)  # Cross line
            self.draw.line((joystick_x + 8, joystick_y, joystick_x, joystick_y + 8), fill=255)  # Cross line

        # Line under the status bar
        self.draw.line((0, battery_y + battery_height + 2, self.width, battery_y + battery_height + 2), fill=255)


class DefaultPage(Page):
    def __init__(self, width, height):
        """Initialize a blank default page."""
        super().__init__(width, height, name="Default Page", border=False, show_title=False)

    def draw_page(self):
        """Draw nothing, keeping the page blank."""
        pass


if __name__ == "__main__":
    display = Display(fps=60)

    # Add the ModePage with border enabled
    mode_page = ModePage(display.width, display.height, initial_mode="Idle")
    display.add_page(mode_page)

    status_page = StatusPage(display.width, display.height)
    status_page.set_user_and_hostname("user", "raspberrypi")
    status_page.set_ip_address("192.168.1.2")
    status_page.set_ssid("MyWiFi")
    status_page.set_battery("half", "15.3V")
    status_page.set_internet_status(True)
    display.add_page(status_page)

    # Start the display and test page transitions
    display.start()

    display.change_page("Status Page")

    try:
        while True:
            status_page.set_battery(level='half', voltage=f"{16.8} V")
            time.sleep(1)
    except KeyboardInterrupt:
        display.stop()
