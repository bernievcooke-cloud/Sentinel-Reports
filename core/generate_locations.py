import os

# --- HARD-CODED SETTINGS (No Imports Allowed) ---
# This bypasses the 'ModuleNotFoundError' entirely.
BASE_OUTPUT = r"C:\OneDrive\Public Reports A\OUTPUT"
# This is where the menu file will be saved
LOC_FILE = r"C:\OneDrive\Public Reports A\core\locations.py"

def sync_locations():
    locations = {}
    print(f"\n--- STANDALONE SCANNING: {BASE_OUTPUT} ---")

    if not os.path.exists(BASE_OUTPUT):
        print(f"ERROR: Folder not found at {BASE_OUTPUT}")
        print("Please check that your 'OUTPUT' folder is inside 'Public Reports A'")
        return

    # Loop through subfolders (Manly, PhillipIsland, etc.)
    for loc_name in os.listdir(BASE_OUTPUT):
        loc_path = os.path.join(BASE_OUTPUT, loc_name)
        
        if os.path.isdir(loc_path):
            coord_file = os.path.join(loc_path, "coords.txt")
            if os.path.exists(coord_file):
                with open(coord_file, "r") as f:
                    try:
                        coords_raw = f.read().strip()
                        if "," in coords_raw:
                            lat, lon = coords_raw.split(",")
                            locations[loc_name] = (float(lat.strip()), float(lon.strip()))
                            print(f"FOUND: {loc_name} -> ({lat.strip()}, {lon.strip()})")
                    except Exception as e:
                        print(f"SKIPPING {loc_name}: Format error in coords.txt")

    # Write the locations.py file directly
    with open(LOC_FILE, "w") as f:
        f.write("# Auto-generated - DO NOT EDIT MANUALLY\n")
        f.write("LOCATIONS = {\n")
        for name, coords in locations.items():
            f.write(f'    "{name}": ({coords[0]}, {coords[1]}),\n')
        f.write("}\n")

    print("-" * 30)
    print(f"SUCCESS: {len(locations)} locations written to core/locations.py")
    print("You can now open your Dashboard.\n")

if __name__ == "__main__":
    sync_locations()