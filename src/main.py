import json
import os
from sensor import read_moisture_hardware
from pump import start_pump

# Path to your plant configuration file
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../config/plants.json')
WATERING_DURATION = 3  # Seconds the pump will run per watering cycle

def load_plants():
    """Loads plant definitions from the config JSON file."""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_plants(plants):
    """Saves updated moisture levels back to the JSON file."""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(plants, f, indent=2)

def run_giesela():
    print("🌱 Giesela system started...")
    plants = load_plants()

    for plant in plants:
        name = plant['name']
        threshold = plant['threshold']
        
        # 1. Read the physical sensor value for the plant
        # (channel=0 reads the MCP3008 channel where your sensor is connected)
        current_moisture = read_moisture_hardware(channel=0)
        plant['current_moisture'] = current_moisture

        print(f"\n🪴 Checking {name}: Moisture is at {current_moisture}% (Min threshold: {threshold}%)")

        # 2. Decision logic: Water if moisture drops below threshold
        if current_moisture < threshold:
            print(f"🚨 ALERT: {name} needs water!")
            
            # Trigger physical pump
            start_pump(seconds=WATERING_DURATION)
            
            # Update moisture level after watering
            plant['current_moisture'] = 100
            print(f"💦 {name} has been watered successfully.")
        else:
            print(f"✅ OK: {name} has enough moisture.")

    # 3. Save the updated states back to config/plants.json
    save_plants(plants)

if __name__ == "__main__":
    run_giesela()
