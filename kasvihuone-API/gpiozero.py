"""Dummy gpiozero library for testing."""

class LED:
    def __init__(pinnumber: int):
        self.pinnumber = pinnumber
    def on(self):
        print(f"LED {self.pinnumber} on")
    def off(self):
        print(f"LED {self.pinnumber} off")