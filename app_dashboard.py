#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import webbrowser
import urllib.parse
import os
import time
import pyautogui
import winsound
import re

# --- 1. CORE DATA & FAIL-SAFES ---
try:
    from core.locations import LOCATIONS
except ImportError:
    # Safe defaults if file is missing
    LOCATIONS = {"TriggPoint": (-31.87, 115.75), "BellsBeach": (-38.37, 144.28)}

try:
    from core.report_wrapper import generate_report
    from core.cloud_sync import push_to_github
except ImportError:
    def generate_report(*args): return "dummy.pdf"
    def push_to_github(): return True

GITHUB_USER = "bernievcooke-cloud"
REPO = "Sentinel-Access"
BASE_PATH = r"C:\OneDrive\Public Reports A\OUTPUT"

class SentinelHub:
    def __init__(self, root):
        self.root = root
        self.root.title("SENTINEL EXECUTIVE STRATEGY HUB V3.11")
        self.root.geometry("1450x850")
        self.root.configure(bg="#0a0a0a")
        self.current_report_url = ""
        self.setup_ui()
        self.root.after(200, self.force_focus)

    def write(self, msg):
        self.log.insert(tk.END, f"\n> {msg}")
        self.log.see(tk.END)
        self.root.update()

    def force_focus(self):
        self.phone_entry.focus_set()
        self.phone_entry.icursor(tk.END)

    def setup_ui(self):
        self.root.columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.root.rowconfigure(0, weight=1)

        # --- COLUMN 1: LEFT BAR ---
        col1 = tk.Frame(self.root, bg="#161616")
        col1.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        tk.Label(col1, text="Admin", font=("Verdana", 18, "bold"), bg="#161616", fg="#00FFCC").pack(pady=20)

        tk.Label(col1, text="REPORT TYPE", font=("Verdana", 10), bg="#161616", fg="gray").pack()
        self.type_menu = ttk.Combobox(col1, values=["Surf", "Sky"], state="readonly", font=("Consolas", 14))
        self.type_menu.pack(fill="x", padx=40, pady=5)
        self.type_menu.current(0)

        tk.Label(col1, text="LOCATIONS", font=("Verdana", 10), bg="#161616", fg="gray").pack(pady=(25, 0))
        self.loc_dropdown = ttk.Combobox(col1, values=sorted(list(LOCATIONS.keys())), state="readonly", font=("Consolas", 14))
        self.loc_dropdown.pack(fill="x", padx=40, pady=5)
        self.loc_dropdown.current(0)

        tk.Label(col1, text="TARGET PHONE", font=("Verdana", 10), bg="#161616", fg="gray").pack(pady=(25, 0))
        self.phone_entry = tk.Entry(col1, bg="black", fg="white", font=("Consolas", 14), justify="center", insertbackground="white", highlightthickness=1, highlightbackground="#333")
        self.phone_entry.insert(0, "61")
        self.phone_entry.pack(fill="x", padx=40, pady=5, ipady=10)

        instr_frame = tk.Frame(col1, bg="#101010", highlightthickness=1, highlightbackground="#444")
        instr_frame.pack(fill="x", padx=30, pady=25)
        instructions = "SYSTEM INSTRUCTIONS:\n\n1. Enter number & INITIATE.\n2. Sync takes approx 2 mins.\n3. DO NOT TOUCH mouse/keys\n   during WhatsApp dispatch."
        tk.Label(instr_frame, text=instructions, font=("Verdana", 8), bg="#101010", fg="#bbbbbb", justify="left", padx=10, pady=10).pack()

        # --- COLUMN 2: PROGRESS ---
        col2 = tk.Frame(self.root, bg="#161616")
        col2.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        tk.Label(col2, text="system progress", font=("Verdana", 18, "bold"), bg="#161616", fg="#00FFCC").pack(pady=20)
        self.log = tk.Text(col2, height=18, bg="black", fg="#00FF00", font=("Consolas", 11), bd=0, padx=15, pady=15)
        self.log.pack(fill="x", padx=25, pady=5)
        self.write("READY")

        self.main_btn = tk.Button(col2, text="INITIATE REPORT", bg="#0055ff", fg="white", height=2, font=("Verdana", 12, "bold"), command=self.run_process)
        self.main_btn.pack(pady=15, padx=25, fill="x")

        self.whatsapp_btn = tk.Button(col2, text="SEND TO WHATSAPP", bg="#222", fg="gray", height=2, font=("Verdana", 12, "bold"), state="disabled", command=self.dispatch)
        self.whatsapp_btn.pack(pady=5, padx=25, fill="x")

        # --- COLUMN 3: DATA FEEDS ---
        col3 = tk.Frame(self.root, bg="#161616")
        col3.grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
        self.feed_top = tk.Text(col3, height=15, bg="#080808", fg="#00FF00", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.feed_top.pack(fill="x", padx=25, pady=(40, 10))
        self.feed_top.insert("1.0", "[DATA FEED ALPHA ACTIVE]")
        self.feed_bottom = tk.Text(col3, height=15, bg="#080808", fg="#00BFFF", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.feed_bottom.pack(fill="x", padx=25, pady=10)
        self.feed_bottom.insert("1.0", "[DATA FEED BETA ACTIVE]")

    def run_process(self):
        loc = self.loc_dropdown.get()
        self.main_btn.config(state="disabled", text="PROCESSING...")
        self.write(f"STAGING: {loc}...")
        try:
            pdf_path = generate_report(loc, self.type_menu.get(), LOCATIONS[loc], BASE_PATH)
            if push_to_github():
                self.current_report_url = f"https://{GITHUB_USER}.github.io/{REPO}/OUTPUT/{loc}/{os.path.basename(pdf_path)}"
                self.write("CLOUD SYNC INITIATED...")
                self.countdown(70)
        except Exception as e:
            self.write(f"ERROR: {e}")
            self.main_btn.config(state="normal", text="INITIATE REPORT")

    def countdown(self, s):
        if s > 0:
            self.main_btn.config(text=f"SYNCING ({s}s)")
            self.root.after(1000, lambda: self.countdown(s-1))
        else:
            self.write("CLOUD STABLE. READY.")
            self.main_btn.config(state="normal", text="INITIATE REPORT")
            self.whatsapp_btn.config(state="normal", bg="#25D366", fg="white")

    def dispatch(self):
        raw_phone = self.phone_entry.get().strip()
        clean_phone = re.sub(r'[^0-9]', '', raw_phone)
        link = f"https://web.whatsapp.com/send?phone={clean_phone}&text={urllib.parse.quote(self.current_report_url)}"
        webbrowser.open(link)
        self.write("WAKING WHATSAPP (80s Wait)...")
        self.root.after(80000, self.robot_fire)

    def robot_fire(self):
        try:
            pyautogui.hotkey('alt', 'tab')
            time.sleep(5)
            w, h = pyautogui.size()
            
            # 1. Force Browser Focus (Click Top Left)
            pyautogui.click(x=w * 0.1, y=h * 0.1) 
            time.sleep(1)

            # 2. Navigation Hack: Shift+Tab usually forces focus to the chat box
            self.write("LOCKING CHAT BOX...")
            pyautogui.hotkey('shift', 'tab')
            time.sleep(1)
            
            # 3. Double-Fire Sequence
            self.write("FORCING DISPATCH...")
            pyautogui.write(" ") # Tiny space to wake the send button
            pyautogui.press('enter')
            time.sleep(1)
            
            # 4. Universal Tab-Enter backup
            pyautogui.press('tab')
            time.sleep(0.5)
            pyautogui.press('enter')
            
            time.sleep(10) # Outbox buffer
            pyautogui.hotkey('ctrl', 'w')
            self.write("DISPATCH SUCCESSFUL.")
            winsound.Beep(1200, 400)
        except Exception as e:
            self.write(f"ROBOT FAILED: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SentinelHub(root)
    root.mainloop()