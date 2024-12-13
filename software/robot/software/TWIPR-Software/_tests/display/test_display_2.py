from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont
import time
import threading


class Page:
    def __init__(self, width, height, name="Page"):
        """
        Initialize a page with a specified width and height.
        :param width: Width of the page
        :param height: Height of the page
        :param name: Name of the page
        """
        self.width = width
        self.height = height
        self.name = name
        self.image = Image.new("1", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)

    def draw_page(self):
        """Draw the static components of the page. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement draw_page")

    def update_page(self, frame):
        """Update dynamic components of the page. Override in subclasses."""
        raise NotImplementedError("Subclasses must implement update_page")


class ModePage(Page):
    def __init__(self, width, height, initial_mode="Idle"):
        """
        Initialize the Mode page.
        :param width: Width of the display
        :param height: Height of the display
        :param initial_mode: The initial mode to display
        """
        super().__init__(width, height, name="Mode Page")
        self.mode = initial_mode

    def set_mode(self, mode):
        """Set the current mode, redraw the page, and trigger a display update."""
        self.mode = mode
        self.draw_page()
        if hasattr(self, "display_image"):  # Check if `display_image` is available
            self.display_image(self.image)  # Update the display immediately

    def draw_page(self):
        """Draw the mode information in the middle of the screen."""
        # Clear the image by creating a new one
        self.image = Image.new("1", (self.width, self.height), 0)  # Clear screen (all black)
        self.draw = ImageDraw.Draw(self.image)  # Reinitialize the draw object

        font = ImageFont.load_default()

        # Prepare the text
        mode_text = f"Mode: {self.mode}"
        text_bbox = self.draw.textbbox((0, 0), mode_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Center the text
        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2

        # Draw the text
        self.draw.text((x, y), mode_text, font=font, fill=255)

    def update_page(self, frame):
        """
        Redraw the page during updates.
        This method is required for dynamic updates in the Display class.
        """
        self.draw_page()


class StatusPage(Page):
    def __init__(self, width, height):
        """Initialize the status page with dynamic elements."""
        super().__init__(width, height, name="Status Page")
        self.battery_level = "full"  # Options: "empty", "half", "full"
        self.battery_voltage = "16.8V"
        self.internet_connected = False
        self.user = "user"
        self.hostname = "hostname"
        self.ip_address = "0.0.0.0"
        self.ssid = "SSID"

    def set_battery(self, level, voltage):
        self.battery_level = level
        self.battery_voltage = voltage

    def set_internet_status(self, connected):
        self.internet_connected = connected

    def set_user_and_hostname(self, user, hostname):
        self.user = user
        self.hostname = hostname

    def set_ip_address(self, ip):
        self.ip_address = ip

    def set_ssid(self, ssid):
        self.ssid = ssid

    def draw_page(self):
        """Draw the static components of the status page."""
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Draw the header lines
        self._draw_header_lines()

        # Draw the status bar
        self._draw_status_bar()

        # Draw the three lines of information
        font = ImageFont.load_default()
        self.draw.text((0, 18), f"{self.user}@{self.hostname}", font=font, fill=255)
        self.draw.text((0, 30), f"IP: {self.ip_address}", font=font, fill=255)
        self.draw.text((0, 42), f"SSID: {self.ssid}", font=font, fill=255)

    def update_page(self, frame):
        """Redraw the page to reflect the current status."""
        self.draw_page()

    def _draw_header_lines(self):
        """Draw the lines above and below the header bar."""
        self.draw.line((0, 0, self.width, 0), fill=255)  # Line at the top
        self.draw.line((0, 14, self.width, 14), fill=255)  # Line below the header bar

    def _draw_status_bar(self):
        """Draw the status bar with battery and internet icons."""
        font = ImageFont.load_default()

        # Battery icon
        battery_x = 2
        battery_y = 2
        battery_width = 16
        battery_height = 8
        terminal_width = 2

        # Draw the battery outline
        self.draw.rectangle(
            (battery_x, battery_y, battery_x + battery_width, battery_y + battery_height),
            outline=255,
            fill=0,
        )

        # Draw the battery terminal
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

        # Fill the battery based on the level
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
        self.draw.text((battery_x + battery_width + terminal_width + 4, battery_y), self.battery_voltage, font=font,
                       fill=255)

        # Internet icon
        internet_x = battery_x + battery_width + terminal_width + 50
        if self.internet_connected:
            self.draw.ellipse((internet_x, battery_y, internet_x + 8, battery_y + 8), outline=255,
                              fill=255)  # Filled circle
        else:
            self.draw.ellipse((internet_x, battery_y, internet_x + 8, battery_y + 8), outline=255,
                              fill=0)  # Empty circle
            self.draw.line((internet_x, battery_y, internet_x + 8, internet_x + 8), fill=255, width=1)  # Cross line


class Display:
    def __init__(self, i2c_port=1, i2c_address=0x3C, fps=30, page_display_duration=2, page_border_thickness=3):
        """
        Initialize the SH1106 OLED display with multi-page support and threading.
        """
        self.serial = i2c(port=i2c_port, address=i2c_address)
        self.device = sh1106(self.serial)
        self.width = self.device.width
        self.height = self.device.height
        self.pages = {}
        self.current_page = None
        self.running = False
        self.frame = 0
        self.fps = fps
        self.thread = None
        self.page_display_duration = page_display_duration
        self.page_border_thickness = page_border_thickness

    def add_page(self, page):
        """Add a page to the display."""
        self.pages[page.name] = page
        if hasattr(page, "display_image"):
            page.display_image = self.display_image
        if self.current_page is None:
            self.current_page = page

    def change_page(self, name):
        """Change the current page to the specified name."""
        if name in self.pages:
            self.current_page = self.pages[name]

            # Pause updates
            self.running = False

            # Show the page name
            self._show_page_name(name)

            # Resume updates
            self.running = True

            # Draw the new page
            self.current_page.draw_page()
            self.display_image(self.current_page.image)

    def _show_page_name(self, name):
        """Display the page name in the center of the screen with a border."""
        image = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Draw the border
        for i in range(self.page_border_thickness):
            draw.rectangle((i, i, self.width - 1 - i, self.height - 1 - i), outline=255, fill=0)

        # Center the text
        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x = (self.width - text_width) // 2
        y = (self.height - text_height) // 2

        draw.text((x, y), name, font=font, fill=255)
        self.display_image(image)

        # Pause for display duration
        time.sleep(self.page_display_duration)

    def update(self):
        """Update the current page dynamically."""
        if self.current_page:
            self.current_page.update_page(self.frame)
            self.display_image(self.current_page.image)
            self.frame += 1

    def display_image(self, image):
        """Render the given image to the display."""
        self.device.display(image)

    def start(self):
        """Start the display thread."""
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the display thread."""
        self.running = False
        if self.thread:
            self.thread.join()

    def _run(self):
        """Thread function to update the display at the specified FPS."""
        while self.running:
            start_time = time.time()
            self.update()
            time.sleep(max(0, 1 / self.fps - (time.time() - start_time)))


if __name__ == "__main__":
    display = Display(fps=30)

    # Add the ModePage
    mode_page = ModePage(display.width, display.height, initial_mode="Idle")
    display.add_page(mode_page)

    # Add the StatusPage
    status_page = StatusPage(display.width, display.height)


    status_page.set_user_and_hostname("user", "raspberrypi")
    status_page.set_ip_address("192.168.1.2")
    status_page.set_ssid("MyWiFi")
    status_page.set_battery("half", "15.3V")
    status_page.set_internet_status(True)
    display.add_page(status_page)

    # Show the StatusPage first, then switch to the ModePage
    display.change_page("Status")
    display.start()

    # time.sleep(4)
    # display.change_page("Mode")

    try:
        while True:
            mode_page.set_mode("Stand-Alone")
            time.sleep(1)
            mode_page.set_mode("Host")
            time.sleep(1)
    except KeyboardInterrupt:
        display.stop()
