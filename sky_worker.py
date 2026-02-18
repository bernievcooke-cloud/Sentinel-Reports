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
# 1. DYNAMIC SETUP & PATH TARGETING
# ============================================================
LOC_NAME = sys.argv[1].strip() if len(sys.argv) > 1 else "LakeTyrrell"
PHONE = sys.argv[2] if len(sys.argv) > 2 else "None"

BASE_OUTPUT = r"C:\OneDrive\PublicReports\OUTPUT"
LOC_DIR = os.path.join(BASE_OUTPUT, LOC_NAME)
COORD_FILE = os.path.join(LOC_DIR, "coords.txt")

# Ensure the sub-folder exists
if not os.path.exists(LOC_DIR):
    os.makedirs(LOC_DIR)

# Load Coords
if os.path.exists(COORD_FILE):
    with open(COORD_FILE, "r") as f:
        coords = f.read().split(",")
        LAT, LON = float(coords[0]), float(coords[1])
else:
    LAT, LON = -35.31, 142.79  # Default Lake Tyrrell fallback

FILENAME = f"Sky_{LOC_NAME}_{datetime.now().strftime('%Y-%m-%d')}.pdf"
save_path = os.path.join(LOC_DIR, FILENAME)

# ============================================================
# 2. ASTRO LOGIC (Clarity & Visibility)
# ============================================================
def check_astro_window(row):
    cloud = row['cloud_cover']
    if cloud <= 15: return "CLEAR SKY"
    if cloud <= 30: return "PARTIAL"
    return None

def fetch_sky_data():
    try:
        w_url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=cloud_cover,visibility,relative_humidity_2m&timezone=auto"
        response = requests.get(w_url).json()
        df = pd.DataFrame(response['hourly'])
        df['time'] = pd.to_datetime(df['time'])
        return df
    except Exception as e:
        print(f"Sky Data Error: {e}")
        return None

# ============================================================
# 3. CHARTING
# ============================================================
def generate_sky_daily(df):
    now = datetime.now()
    day_df = df[df["time"].dt.date == now.date()].copy()
    fig, ax1 = plt.subplots(figsize=(11, 5.5))
    
    ax1.plot(day_df["time"], 100 - day_df["cloud_cover"], color="#4b0082", lw=3, label="Clarity %")
    ax1.fill_between(day_df["time"], 100 - day_df["cloud_cover"], color="#4b0082", alpha=0.1)

    day_df['win'] = day_df.apply(check_astro_window, axis=1)
    peaks = day_df.dropna(subset=['win'])
    for i, row in peaks.iterrows():
        ax1.scatter(row["time"], 100 - row["cloud_cover"], color="gold", marker="*", s=100, zorder=5)

    ax1.axvline(now, color="red", lw=2, label="Current Time")
    ax1.set_ylim(0, 110)
    ax1.set_title(f"ASTRO STRATEGY: {LOC_NAME.upper()}", fontweight="bold", fontsize=15)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.tight_layout()
    
    buf = BytesIO(); plt.savefig(buf, format='png', dpi=140); plt.close(); buf.seek(0)
    return buf

# ============================================================
# 4. PDF BUILDER (White Edition)
# ============================================================
def build_pdf(df):
    doc = SimpleDocTemplate(save_path, pagesize=A4, topMargin=0.5*cm, bottomMargin=0.5*cm)
    styles = getSampleStyleSheet()
    
    t = Table([['SKY STRATEGY', f"TARGET SITE: {LOC_NAME.upper()}"]], colWidths=[5*cm, 13.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(0,0),colors.black),
        ('TEXTCOLOR',(0,0),(0,0),colors.white),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),
        ('BACKGROUND',(1,0),(1,0),colors.white), 
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey)
    ]))

    story = [
        Paragraph(f"<b>NIGHT SKY STRATEGY REPORT</b>", styles["Title"]),
        t, Spacer(1, 15),
        Image(generate_sky_daily(df), 19*cm, 10*cm), 
        Spacer(1, 15),
        Paragraph(f"<b>Astro Analysis:</b> Targets identified by Gold Stars represent optimal clarity for long-exposure photography. Coords: {LAT}, {LON}.", styles["Normal"])
    ]
    doc.build(story)
    print(f"SUCCESS: Sky Report generated in {LOC_DIR}")

if __name__ == "__main__":
    data = fetch_sky_data()
    if data is not None: 
        build_pdf(data)