import json
import random
import os

# Path to configuration file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/plants.json')

# ==============================================================================
# HARDWARE SETTINGS (Raspberry Pi + MCP3008 ADC)
# ==============================================================================
# Capacitive sensors return LOWER raw values in water than in dry air.
AIR_VALUE = 0.82   # Raw value in dry air (example)
WATER_VALUE = 0.38 # Raw value submerged in water (example)

def read_moisture_hardware(channel=0):
    """
    Reads the physical sensor via the MCP3008 converter on a Raspberry Pi.
    Requires: pip install gpiozero spidev
    """
    try:
        from gpiozero import MCP3008
        sensor = MCP3008(channel=channel)
        raw = sensor.value
        
        # Convert raw voltage (0.0 - 1.0) into a percentage (0 - 100%)
        percentage = (AIR_VALUE - raw) / (AIR_VALUE - WATER_VALUE) * 100
        return round(max(0, min(100, percentage)), 1)
    except ImportError:
        print("⚠️ 'gpiozero' not found. Running on Mac/PC? Falling back to simulation.")
        return read_moisture_simulated({'current_moisture': 50})
    except Exception as e:
        print(f"⚠️ Hardware error: {e}")
        return 0.0

# ==============================================================================
# SIMULATION & LOGIC
# ==============================================================================
def read_moisture_simulated(plant):
    """
    Simulates soil drying out:
    Loses between 1% and 5% moisture per run.
    """
    current = plant.get('current_moisture', 50)
    decay = random.randint(1, 5)
    return max(0, current - decay)

def load_plants():
    """Loads plant profiles from the JSON configuration file."""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_PATH}")
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_plants(plants):
    """Saves the updated plant states back to the JSON file."""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(plants, f, indent=2)

def update_all_sensors(use_hardware=False):
    """
    Reads all plant sensors and updates the JSON database.
    Set use_hardware=True when running on a physical Raspberry Pi.
    """
    plants = load_plants()
    for plant in plants:
        if use_hardware:
            # Read real hardware sensor
            plant['current_moisture'] = read_moisture_hardware(channel=0)
        else:
            # Use simulation mode for local development
            plant['current_moisture'] = read_moisture_simulated(plant)
            
    save_plants(plants)
    return plants

def water_plant(plant_name):
    """Waters a specific plant and resets its moisture level to 100%."""
    plants = load_plants()
    for plant in plants:
        if plant['name'].lower() == plant_name.lower():
            plant['current_moisture'] = 100
            save_plants(plants)
            print(f"💦 Giesela watered {plant['name']}! Moisture is back at 100%.")
            return
    print(f"⚠️ Plant '{plant_name}' not found.")

if __name__ == "__main__":
    print("🔄 Testing sensor.py...")
    # Test run (defaults to simulation mode):
    updated = update_all_sensors(use_hardware=False)
    for p in updated:
        print(f"🪴 {p['name']}: {p['current_moisture']}% moisture")
