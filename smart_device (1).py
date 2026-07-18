# ============================================================
#  Smart Device Management System
#  EL 162 / 234 – Object Oriented Programming
#  Author : Robert Kofitiah 
#  Date   : July 2026
# ============================================================


# ─────────────────────────────────────────────────────────────
#  PARENT CLASS
# ─────────────────────────────────────────────────────────────

class SmartDevice:
    """
    Base class for all smart home devices.
    Encapsulates device_id and power_status as private attributes.
    All child classes inherit from this class.
    """

    def __init__(self, name, device_id):
        # Public attribute — accessible directly
        self.name = name

        # Private attributes — only accessible via getters/setters
        # We validate device_id immediately on creation
        if not device_id or device_id.strip() == "":
            raise ValueError("Device ID cannot be empty.")
        self.__device_id = device_id
        self.__power_status = False   # All devices start powered OFF

    # ── Getter for device_id (read-only — no setter on purpose) ──
    @property
    def device_id(self):
        """Return the device ID. Cannot be changed after creation."""
        return self.__device_id

    # ── Getter for power_status ───────────────────────────────
    @property
    def power_status(self):
        """Return True if device is ON, False if OFF."""
        return self.__power_status

    # ── Setter for power_status (private — only used internally) ─
    def __set_power_status(self, status):
        """Internal method to change power status safely."""
        if not isinstance(status, bool):
            raise TypeError("Power status must be True or False.")
        self.__power_status = status

    # ── Public Methods ────────────────────────────────────────
    def turn_on(self):
        """Turn the device on."""
        if self.__power_status:
            print(f"  [{self.name}] is already ON.")
        else:
            self.__set_power_status(True)
            print(f"  [{self.name}] has been turned ON.")

    def turn_off(self):
        """Turn the device off."""
        if not self.__power_status:
            print(f"  [{self.name}] is already OFF.")
        else:
            self.__set_power_status(False)
            print(f"  [{self.name}] has been turned OFF.")

    def display_info(self):
        """Display general information about the device."""
        status = "ON" if self.__power_status else "OFF"
        print(f"\n  ── Device Info ──────────────────")
        print(f"  Name        : {self.name}")
        print(f"  Device ID   : {self.__device_id}")
        print(f"  Power Status: {status}")


# ─────────────────────────────────────────────────────────────
#  CHILD CLASS 1 — SecurityCamera
# ─────────────────────────────────────────────────────────────

class SecurityCamera(SmartDevice):
    """
    A security camera that can record footage.
    Inherits name, device_id, and power_status from SmartDevice.
    Adds: recording_status (bool)
    """

    def __init__(self, name, device_id):
        # Call parent constructor using super()
        super().__init__(name, device_id)
        self.recording_status = False   # Camera starts NOT recording

    def start_recording(self):
        """Begin recording. Device must be ON first."""
        if not self.power_status:
            print(f"  [{self.name}] Cannot record — device is OFF. Turn it on first.")
        elif self.recording_status:
            print(f"  [{self.name}] is already recording.")
        else:
            self.recording_status = True
            print(f"  [{self.name}] Recording STARTED.")

    def stop_recording(self):
        """Stop recording."""
        if not self.recording_status:
            print(f"  [{self.name}] is not currently recording.")
        else:
            self.recording_status = False
            print(f"  [{self.name}] Recording STOPPED.")

    def display_info(self):
        """Display camera-specific info, extending parent display_info."""
        super().display_info()   # Call parent method first
        rec = "YES" if self.recording_status else "NO"
        print(f"  Recording   : {rec}")
        print(f"  ────────────────────────────────")


# ─────────────────────────────────────────────────────────────
#  CHILD CLASS 2 — SmartLight
# ─────────────────────────────────────────────────────────────

class SmartLight(SmartDevice):
    """
    A smart light with adjustable brightness (0–100).
    Inherits name, device_id, and power_status from SmartDevice.
    Adds: brightness (int, 0 to 100)
    """

    def __init__(self, name, device_id, brightness=50):
        super().__init__(name, device_id)
        # Validate brightness on creation
        self.__brightness = 0
        self.brightness = brightness   # Use the setter for validation

    # ── Getter for brightness ─────────────────────────────────
    @property
    def brightness(self):
        return self.__brightness

    # ── Setter for brightness — enforces 0–100 rule ───────────
    @brightness.setter
    def brightness(self, value):
        if not isinstance(value, int):
            raise TypeError("Brightness must be an integer.")
        if value < 0 or value > 100:
            raise ValueError("Brightness must be between 0 and 100.")
        self.__brightness = value

    def increase_brightness(self, amount=10):
        """Increase brightness by a given amount (default 10). Max is 100."""
        if not self.power_status:
            print(f"  [{self.name}] Cannot adjust brightness — device is OFF.")
            return
        new_value = min(self.__brightness + amount, 100)
        self.brightness = new_value
        print(f"  [{self.name}] Brightness increased to {self.__brightness}%.")

    def decrease_brightness(self, amount=10):
        """Decrease brightness by a given amount (default 10). Min is 0."""
        if not self.power_status:
            print(f"  [{self.name}] Cannot adjust brightness — device is OFF.")
            return
        new_value = max(self.__brightness - amount, 0)
        self.brightness = new_value
        print(f"  [{self.name}] Brightness decreased to {self.__brightness}%.")

    def display_info(self):
        """Display light-specific info, extending parent display_info."""
        super().display_info()
        print(f"  Brightness  : {self.__brightness}%")
        print(f"  ────────────────────────────────")


# ─────────────────────────────────────────────────────────────
#  CHILD CLASS 3 — TemperatureSensor
# ─────────────────────────────────────────────────────────────

class TemperatureSensor(SmartDevice):
    """
    A temperature sensor that reads the current temperature.
    Inherits name, device_id, and power_status from SmartDevice.
    Adds: temperature (float, in degrees Celsius)
    """

    def __init__(self, name, device_id, temperature=25.0):
        super().__init__(name, device_id)
        self.temperature = temperature   # Current temperature in °C

    def read_temperature(self):
        """Read and display the current temperature. Device must be ON."""
        if not self.power_status:
            print(f"  [{self.name}] Cannot read temperature — device is OFF.")
        else:
            print(f"  [{self.name}] Current Temperature: {self.temperature:.1f} °C")

    def display_info(self):
        """Display sensor-specific info, extending parent display_info."""
        super().display_info()
        print(f"  Temperature : {self.temperature:.1f} °C")
        print(f"  ────────────────────────────────")


# ─────────────────────────────────────────────────────────────
#  HELPER — print a clean section separator
# ─────────────────────────────────────────────────────────────

def print_header(title):
    """Print a formatted section header for the menu."""
    print("\n" + "=" * 48)
    print(f"   {title}")
    print("=" * 48)


def print_menu():
    """Display the main menu options."""
    print_header("SMART DEVICE MANAGEMENT SYSTEM")
    print("  Select a Device:")
    print("  [1] Living Room Light   (SmartLight)")
    print("  [2] Front Door Camera   (SecurityCamera)")
    print("  [3] Bedroom Sensor      (TemperatureSensor)")
    print("  [0] Exit")
    print("-" * 48)


def device_menu(device):
    """
    Show the action menu for a selected device.
    Uses conditional statements and a loop to handle user choices.
    """
    while True:
        print(f"\n  ── Actions for: {device.name} ──")
        print("  [1] Display Device Info")
        print("  [2] Turn Device ON")
        print("  [3] Turn Device OFF")

        # Show extra options depending on device type
        if isinstance(device, TemperatureSensor):
            print("  [4] Read Temperature")
        elif isinstance(device, SmartLight):
            print("  [4] Increase Brightness")
            print("  [5] Decrease Brightness")
        elif isinstance(device, SecurityCamera):
            print("  [4] Start Recording")
            print("  [5] Stop Recording")

        print("  [0] Back to Main Menu")
        print("-" * 48)

        choice = input("  Enter your choice: ").strip()

        print()  # Blank line for readability

        if choice == "1":
            device.display_info()

        elif choice == "2":
            device.turn_on()

        elif choice == "3":
            device.turn_off()

        elif choice == "4":
            # Temperature Sensor
            if isinstance(device, TemperatureSensor):
                device.read_temperature()
            # Smart Light — increase brightness
            elif isinstance(device, SmartLight):
                try:
                    amount = int(input("  Enter amount to increase (default 10): ") or "10")
                    device.increase_brightness(amount)
                except ValueError:
                    print("  Invalid input. Please enter a whole number.")
            # Security Camera — start recording
            elif isinstance(device, SecurityCamera):
                device.start_recording()

        elif choice == "5":
            # Smart Light — decrease brightness
            if isinstance(device, SmartLight):
                try:
                    amount = int(input("  Enter amount to decrease (default 10): ") or "10")
                    device.decrease_brightness(amount)
                except ValueError:
                    print("  Invalid input. Please enter a whole number.")
            # Security Camera — stop recording
            elif isinstance(device, SecurityCamera):
                device.stop_recording()

        elif choice == "0":
            print("  Returning to main menu...")
            break

        else:
            print("  Invalid choice. Please try again.")


# ─────────────────────────────────────────────────────────────
#  MAIN PROGRAM — Create devices and run menu
# ─────────────────────────────────────────────────────────────

def main():
    """
    Entry point of the program.
    Creates one of each device type and launches the menu-driven interface.
    """

    # ── Create device objects ─────────────────────────────────
    living_room_light  = SmartLight("Living Room Light",  "SL-001", brightness=60)
    front_door_camera  = SecurityCamera("Front Door Camera", "SC-002")
    bedroom_sensor     = TemperatureSensor("Bedroom Sensor",  "TS-003", temperature=22.5)

    # Store all devices in a list for easy access
    devices = [living_room_light, front_door_camera, bedroom_sensor]

    # ── Main menu loop ────────────────────────────────────────
    while True:
        print_menu()
        choice = input("  Enter your choice: ").strip()

        if choice == "1":
            device_menu(devices[0])   # SmartLight

        elif choice == "2":
            device_menu(devices[1])   # SecurityCamera

        elif choice == "3":
            device_menu(devices[2])   # TemperatureSensor

        elif choice == "0":
            print_header("Goodbye! System shutting down.")
            print("  All devices have been safely deregistered.")
            print("=" * 48 + "\n")
            break

        else:
            print("\n  Invalid choice. Please enter 0, 1, 2, or 3.")


# ── Run the program ───────────────────────────────────────────
if __name__ == "__main__":
    main()
