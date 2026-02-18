import os

# --- CONFIGURATION ---
BASE_PATH = r"C:\OneDrive\PublicReports"
OUTPUT_DIR = os.path.join(BASE_PATH, "OUTPUT")

# PRE-VALIDATED SURF DATABASE (One-Word Format for V3.17)
# Format: "State": {"LocationName": (Lat, Lon)}
SURF_MAP = {
    "VIC": {
        "BellsBeach": (-38.371, 144.282),
        "PhillipIsland": (-38.502, 145.148),
        "Torquay": (-38.333, 144.316),
        "PointLeo": (-38.423, 145.074),
        "PortFairy": (-38.384, 142.235)
    },
    "NSW": {
        "ByronBay": (-28.647, 153.633),
        "BondiBeach": (-33.890, 151.274),
        "ManlyBeach": (-33.800, 151.284),
        "Newcastle": (-32.927, 151.786),
        "Cronulla": (-34.058, 151.154)
    },
    "QLD": {
        "NoosaHeads": (-26.382, 153.095),
        "BurleighHeads": (-28.087, 153.454),
        "KirraBeach": (-28.167, 153.531),
        "SnapperRocks": (-28.163, 153.551),
        "SunshineBeach": (-26.397, 153.118)
    },
    "WA": {
        "MargaretRiver": (-33.955, 115.075),
        "Gnaraloo": (-23.821, 113.475),
        "Yallingup": (-33.641, 115.024),
        "Cottesloe": (-31.995, 115.751),
        "TriggPoint": (-31.878, 115.752)
    },
    "SA": {
        "Middleton": (-35.511, 138.711),
        "Waitpinga": (-35.632, 138.484),
        "Pondalowie": (-35.234, 136.837),
        "CactusBeach": (-32.083, 133.000)
    },
    "TAS": {
        "ShipsternBluff": (-43.212, 147.854),
        "CliftonBeach": (-42.986, 147.471),
        "EaglehawkNeck": (-43.018, 147.925)
    }
}

def deploy_locations():
    print("🛰️ SENTINEL SCOUT: DEPLOYING STRATEGIC LOCATIONS...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created Root: {OUTPUT_DIR}")

    count = 0
    for state, spots in SURF_MAP.items():
        print(f"\nProcessing {state}...")
        for name, coords in spots.items():
            # Create a placeholder folder for each location
            # This ensures the Hub's get_existing_locations() picks them up
            folder_path = os.path.join(OUTPUT_DIR, name)
            
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                # Create a small text file with the coordinates for the worker to read later
                with open(os.path.join(folder_path, "coords.txt"), "w") as f:
                    f.write(f"{coords[0]},{coords[1]}")
                print(f"  [+] Deployed: {name} {coords}")
                count += 1
            else:
                print(f"  [-] Already Active: {name}")

    print(f"\n✅ SUCCESS: {count} new locations are now ready in the Sentinel system.")

if __name__ == "__main__":
    deploy_locations()
    