import json

def run_giesela():
    print("🌱 Giesela ist gestartet...")
    with open('config/plants.json', 'r') as f:
        plants = json.load(f)

    for plant in plants:
        if plant['current_moisture'] < plant['threshold']:
            print(f"🚨 ALERT: {plant['name']} braucht Wasser! (Aktuell: {plant['current_moisture']}%, Minimum: {plant['threshold']}%)")
        else:
            print(f"✅ OK: {plant['name']} ist versorgt ({plant['current_moisture']}%).")

if __name__ == "__main__":
    run_giesela()
