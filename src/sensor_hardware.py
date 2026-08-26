import time
from gpiozero import MCP3008

# ==============================================================================
# Calibration
# put the sensor in the air -> AIR_VALUE
# put the sensor into the water -> WATER_VALUE
# Capacitive sensors yield a LOWER value in water than in air.
# ==============================================================================
AIR_VALUE = 0.82   # value at the air (example)
WATER_VALUE = 0.38 # value into water (example)

# Sensor at MCP3008 channel 0 
sensor_channel = MCP3008(channel=0)

def read_raw_value():
    """reads raw value of MCP3008 (Wert zwischen 0.0 und 1.0)."""
    return sensor_channel.value

def get_moisture_percentage():
    """
   convert moisture into percentage (0% = dry, 100% = wet).
    """
    raw = read_raw_value()
    
    # scale & switch (low value = wet)
    percentage = (AIR_VALUE - raw) / (AIR_VALUE - WATER_VALUE) * 100
    
    # 
    clamped_percentage = max(0, min(100, percentage))
    return round(clamped_percentage, 1)

if __name__ == "__main__":
    print("🌱 Giesela Hardware-Sensor test sensor start...")
    print("press Strg+C to end.\n")
    
    try:
        while True:
            raw = read_raw_value()
            moisture = get_moisture_percentage()
            print(f"📊 raw value: {raw:.3f} | moisture: {moisture}%")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nmesurement end.")
