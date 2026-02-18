import os

# --- CONFIGURATION ---
BASE_PATH = r"C:\OneDrive\PublicReports"
OUTPUT_DIR = os.path.join(BASE_PATH, "OUTPUT")

# TOP DARK-SKY & ASTRO LOCATIONS (One-Word Format)
SKY_MAP = {
    "VIC": {
        "LakeTyrrell": (-35.316, 142.795),     # Salt lake reflections
        "TwelveApostles": (-38.664, 143.103),  # Iconic silhouettes
        "WilsonsProm": (-39.022, 146.331),     # Southernmost dark sky
        "MountBuffalo": (-36.721, 146.775)     # High altitude clarity
    },
    "NSW": {
        "Warrumbungle": (-31.275, 149.001),    # Australia's first Dark Sky Park
        "MungoNationalPark": (-33.748, 143.081), # Desert landscapes
        "ParkesRadioScope": (-32.998, 148.263), # Iconic 'The Dish'
        "BrokenHill": (-31.953, 141.464)       # Outback clarity
    },
    "QLD": {
        "MountIsA": (-20.725, 139.492),        # Massive horizon
        "CarnarvonGorge": (-25.064, 148.232),  # Ancient sandstone
        "Whitsundays": (-20.211, 148.956),     # Clear island air
        "BunyaMountains": (-26.837, 151.597)    # High altitude/dark
    },
    "WA": {
        "ThePinnacles": (-30.604, 115.157),    # Alien landscape/Stars
        "LakeBallard": (-29.458, 121.217),     # Famous statues/Night sky
        "RoebuckBay": (-17.994, 122.316),      # "Staircase to the Moon"
        "WaveRock": (-32.444, 118.897)         # Granite silhouettes
    },
    "SA": {
        "RiverMurrayDarkSky": (-34.613, 139.553), # Certified Dark Sky Reserve
        "CooberPedy": (-29.013, 134.754),         # Mars-like terrain
        "WilpenaPound": (-31.498, 138.563),       # Ancient mountain range
        "KangarooIsland": (-35.775, 137.214)      # Pristine coastal darkness
    },
    "TAS": {
        "BayOfFires": (-41.171, 148.274),      # Red rocks vs Aurora
        "MountWellington": (-42.895, 147.237), # High above Hobart
        "BrunyIsland": (-43.332, 147.251),     # Southern Lights (Aurora)
        "CradleMountain": (-41.685, 145.923)   # Alpine reflections
    },
    "NT": {
        "Uluru": (-25.344, 131.036),           # The ultimate astro shot
        "DevilsMarbles": (-20.852, 134.263),   # Round boulders vs Milky Way
        "AliceSprings": (-23.698, 133.880)     # Center of the desert
    }
}

def deploy_night_spots():
    print("🌌 SENTINEL NIGHT-SCOUT: DEPLOYING ASTRO SITES...")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    count = 0
    for state, spots in SKY_MAP.items():
        print(f"\nProcessing {state}...")
        for name, coords in spots.items():
            folder_path = os.path.join(OUTPUT_DIR, name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                with open(os.path.join(folder_path, "coords.txt"), "w") as f:
                    f.write(f"{coords[0]},{coords[1]}")
                print(f"  [+] Deployed Night Site: {name}")
                count += 1
            else:
                # Update coords even if folder exists
                with open(os.path.join(folder_path, "coords.txt"), "w") as f:
                    f.write(f"{coords[0]},{coords[1]}")
                print(f"  [~] Updated Coords: {name}")

    print(f"\n✅ SUCCESS: {count} Night Photography sites added to the Command Hub.")

if __name__ == "__main__":
    deploy_night_spots()