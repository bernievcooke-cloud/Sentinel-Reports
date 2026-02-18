#!/usr/bin/env python3
import os, platform, requests, sys
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import cm
from io import BytesIO

# ============================================================
# 1. DYNAMIC SETUP (INTEGRATED WITH HUB V3.17)
# ============================================================
# Hub passes 'PointLeo' as the first argument
LOC_NAME = sys.argv[1] if len(sys.argv) > 1 else "PhillipIsland"
PHONE = sys.argv[2] if len(sys.argv) > 2 else "None"

# Path Logic - Saving into the specific folder for that location
BASE_OUTPUT = r"C:\OneDrive\PublicReports\OUTPUT"
LOC_DIR = os.path.join(BASE_OUTPUT, LOC_NAME)
COORD_FILE = os.path.join(LOC_DIR, "coords.txt")

# Load Coords from the "Scout" deployed file
if os.path.exists(COORD_FILE):
    with open(COORD_FILE, "r") as f:
        coords = f.read().split(",")
        LAT, LON = float(coords[0]), float(coords[1])
else:
    # Default fallback to Phillip Island if no scout file exists
    LAT, LON = -38.50, 145.15  

FILENAME = f"Surf_{LOC_NAME}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
save_path = os.path.join(LOC_DIR, FILENAME)

# ============================================================
# 2. MASTER "X" LOGIC (National Standard)
# ============================================================
def check_x_factor(row):
    w, s, t = row['wind_direction_10m'], row['swell_wave_height'], row['tide_height']
    # General Logic: Offshore (W/NW) + Solid Swell + Mid-High Tide
    if (270 <= w <= 340) and (1.2 <= s <= 2.5) and (t >= 1.2):
        return "Peak Window"
    if (0.8 <= s <= 3.0) and (t >= 1.0):
        return "Session"
    return None

def deg_to_text(deg):
    if pd.isna(deg): return ""
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return dirs[int((deg + 11.25) // 22.5) % 16]

def fetch_surf_data():
    try:
        m_url = f"https://marine-api.open-meteo.com/v1/marine?latitude={LAT}&longitude={LON}&hourly=swell_wave_height,swell_wave_direction&timezone=auto"
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=wind_speed_10m,wind_direction_10m&timezone=auto"
        df_m = pd.DataFrame(requests.get(m_url).json()['hourly'])
        df_w = pd.DataFrame(requests.get(w_url).json()['hourly'])
        df = pd.merge(df_m, df_w, on="time")
        df['time'] = pd.to_datetime(df['time'])
        df['tide_height'] = 1.35 + 0.85 * np.sin(np.arange(len(df)) * (2 * np.pi / 12.4))
        return df
    except Exception as e:
        print(f"Fetch Error: {e}")
        return None

# ============================================================
# 3. CHARTING 
# ============================================================
def generate_daily(df, loc_title):
    now = datetime.now()
    day_df = df[df["time"].dt.date == now.date()].copy()
    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    ax2, ax3 = ax1.twinx(), ax1.twinx()
    ax3.spines.right.set_position(("axes", 1.08))

    l1, = ax1.plot(day_df["time"], day_df["swell_wave_height"], color="#1f77b4", lw=3.5, label="Swell (m)")
    l2, = ax2.plot(day_df["time"], day_df["wind_speed_10m"], color="#2ca02c", lw=1.5, ls="--", alpha=0.5, label="Wind (km/h)")
    l3, = ax3.plot(day_df["time"], day_df["tide_height"], color="#17becf", lw=1.5, alpha=0.3, label="Tide (m)")

    max_swell = day_df["swell_wave_height"].max()
    ax1.set_ylim(0, max_swell * 1.35) 

    day_df['active_x'] = day_df.apply(check_x_factor, axis=1)
    x_only = day_df.dropna(subset=['active_x'])
    
    for i, row in day_df.iterrows():
        label = row['active_x']
        if label:
            ax1.scatter(row["time"], row["swell_wave_height"], color="green", marker="x", s=100, zorder=10, lw=2)
            y_offset = -0.20 if row["swell_wave_height"] > (max_swell * 0.8) else 0.15
            ax1.text(row["time"], row["swell_wave_height"] + y_offset, f"{label}", 
                     color="green", fontweight="bold", ha="center", size=7)

    ax1.axvline(now, color="red", lw=2, label="Current Time")
    ax1.set_title(f"SURF STRATEGY: {loc_title.upper()}", fontweight="bold", fontsize=15)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    ax1.legend(handles=[l1, l2, l3], loc='upper left', fontsize=10)
    plt.tight_layout()
    
    buf = BytesIO(); plt.savefig(buf, format='png', dpi=140); plt.close(); buf.seek(0)
    return buf

def generate_weekly(df):
    fig, ax1 = plt.subplots(figsize=(11, 4.5))
    ax1.plot(df['time'], df['swell_wave_height'], color="#1f77b4", lw=2)
    ax1.set_title("7-DAY SWELL OUTLOOK", fontweight="bold", fontsize=12)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%a %d"))
    plt.tight_layout()
    buf = BytesIO(); plt.savefig(buf, format='png', dpi=140); plt.close(); buf.seek(0)
    return buf

# ============================================================
# 4. PDF BUILDER (Clean White Edition)
# ============================================================
def build_pdf(df):
    # Use the 'save_path' we defined at the top
    doc = SimpleDocTemplate(save_path, pagesize=A4, topMargin=0.5*cm, bottomMargin=0.5*cm)
    # ... rest of the function ...
    styles = getSampleStyleSheet()
    
    # White background table
    t = Table([['SENTINEL SYSTEM', f"LOCATION: {LOC_NAME.upper()}"]], colWidths=[5*cm, 13.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0),colors.black),
        ('TEXTCOLOR',(0,0),(0,0),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),
        ('BACKGROUND',(1,0),(1,0),colors.white), # PURE WHITE BACKGROUND
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey)
    ]))

    story = [
        Paragraph(f"<b>SURF STRATEGY REPORT</b>", styles["Title"]),
        t, Spacer(1, 10),
        Image(generate_daily(df, LOC_NAME), 19*cm, 9.5*cm), 
        Spacer(1, 15),
        Image(generate_weekly(df), 19*cm, 8.5*cm),
        Spacer(1, 10),
        Paragraph(f"<font size=8><b>Strategic Analysis:</b> Report generated for coordinates ({LAT}, {LON}). All times local to target location.</font>", styles["Normal"])
    ]
    doc.build(story)
    print(f"SUCCESS: Generated {FILENAME} in {LOC_DIR}")

if __name__ == "__main__":
    data = fetch_surf_data()
    if data is not None: 
        build_pdf(data)