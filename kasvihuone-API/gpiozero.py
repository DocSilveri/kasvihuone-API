"""Dummy gpiozero library for testing."""

class LED:
    def __init__(self, pinnumber: int):
        self.pinnumber = pinnumber
    def on(self):
        print(f"LED {self.pinnumber} on")
    def off(self):
        print(f"LED {self.pinnumber} off")
        
class MCP3008:
    def __init__(self, channel: int):
        self.channel = channel
        self.value = 0,5