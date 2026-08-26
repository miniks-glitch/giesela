import time
from gpiozero import OutputDevice

# GPIO 17 corresponds to physical Pin 11 on the Raspberry Pi
PUMP_PIN = 17

# Initialize the relay on Pin 17.
# active_high=False supports standard low-level trigger relay modules.
pump = OutputDevice(PUMP_PIN, active_high=False, initial_value=False)

def start_pump(seconds=3):
    """Turns on the physical water pump for the specified duration in seconds."""
    print(f"🌊 Turning pump ON for {seconds} seconds...")
    
    pump.on()           # Relay activates -> Pump starts
    time.sleep(seconds) # Wait while water is pumping
    pump.off()          # Relay deactivates -> Pump stops
    
    print("🌊 Watering complete. Pump is OFF.")

if __name__ == "__main__":
    # Run this file directly on your Raspberry Pi to test the pump:
    print("🧪 Running hardware test for the pump...")
    start_pump(seconds=2)
