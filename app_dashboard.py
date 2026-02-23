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

# --- 1. DEFINE LOCATIONS & ENGINE FAIL-SAFES ---
try:
    from core.locations import LOCATIONS
except ImportError:
    LOCATIONS = {"BellsBeach": (-38.37, 144.28), "TriggPoint": (-31.87, 115.75)}

try:
    from core.report_wrapper import generate_report
    from core.cloud_sync import push_to_github
except ImportError:
    def generate_report(*args): return ""
    def push_to_github(): return False

# --- SYSTEM IDENTITY & PATHS ---
GITHUB_USER = "bernievcooke-cloud"
REPO = "Sentinel-Access"
BASE_PATH = r"C:\OneDrive\Public Reports A\OUTPUT"

class SentinelHub:
    def __init__(self, root):
        self.root = root
        self.root.title("SENTINEL EXECUTIVE STRATEGY HUB V3.95")
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
        self.root.focus_force()
        self.phone_entry.focus_set()
        self.phone_entry.icursor(tk.END)

    def setup_ui(self):
        self.root.columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.root.rowconfigure(0, weight=1)

        # --- COLUMN 1: LEFT BAR ---
        col1 = tk.Frame(self.root, bg="#161616")
        col1.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        tk.Label(col1, text="Admin", font=("Verdana", 18, "bold"), bg="#161616", fg="#00FFCC").pack(pady=(20, 20))

        tk.Label(col1, text="REPORT TYPE", font=("Verdana", 10), bg="#161616", fg="gray").pack()
        self.type_menu = ttk.Combobox(col1, values=["Surf", "Sky"], state="readonly", font=("Consolas", 14))
        self.type_menu.pack(fill="x", padx=40, pady=5)
        self.type_menu.current(0)

        tk.Label(col1, text="LOCATIONS", font=("Verdana", 10), bg="#161616", fg="gray").pack(pady=(25, 0))
        self.loc_dropdown = ttk.Combobox(col1, values=sorted(list(LOCATIONS.keys())), state="readonly", font=("Consolas", 14))
        self.loc_dropdown.pack(fill="x", padx=40, pady=5)
        if LOCATIONS: self.loc_dropdown.current(0)

        tk.Label(col1, text="TARGET PHONE", font=("Verdana", 10), bg="#161616", fg="gray").pack(pady=(25, 0))
        self.phone_entry = tk.Entry(col1, bg="black", fg="white", font=("Consolas", 14), 
                                    justify="center", highlightthickness=2, 
                                    highlightbackground="#00FFCC", bd=0,
                                    insertbackground="white", insertwidth=4)
        self.phone_entry.insert(0, "61")
        self.phone_entry.pack(fill="x", padx=40, pady=5, ipady=12)

        # --- INSTRUCTION BOX ---
        instr_frame = tk.Frame(col1, bg="#101010", highlightthickness=1, highlightbackground="#444")
        instr_frame.pack(fill="x", padx=30, pady=25)
        
        instructions = (
            "SYSTEM INSTRUCTIONS:\n\n"
            "1. Enter number & hit INITIATE.\n"
            "2. System will build & sync to Cloud.\n"
            "3. WhatsApp will trigger automatically.\n\n"
            "NOTE: Process takes ~2.5 minutes.\n"
            "DO NOT TOUCH mouse/keyboard once\n"
            "dispatch begins (Robot Mode)."
        )
        tk.Label(instr_frame, text=instructions, font=("Verdana", 8), bg="#101010", fg="#bbbbbb", justify="left", padx=10, pady=10).pack()

        self.reset_btn = tk.Button(col1, text="RESET SYSTEM", bg="#333", fg="white", font=("Verdana", 10, "bold"), command=self.reset_fields)
        self.reset_btn.pack(side="bottom", fill="x", padx=40, pady=20)

        # --- COLUMN 2: PROGRESS ---
        col2 = tk.Frame(self.root, bg="#161616")
        col2.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        tk.Label(col2, text="system progress", font=("Verdana", 18, "bold"), bg="#161616", fg="#00FFCC").pack(pady=(20, 20))
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
        self.feed_top.insert("1.0", "[DATA FEED ALPHA]")
        self.feed_bottom = tk.Text(col3, height=15, bg="#080808", fg="#00BFFF", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.feed_bottom.pack(fill="x", padx=25, pady=10)
        self.feed_bottom.insert("1.0", "[DATA FEED BETA]")

    def reset_fields(self):
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, "61")
        self.log.delete("1.0", tk.END)
        self.write("SYSTEM RESET. READY.")
        self.main_btn.config(state="normal", text="INITIATE REPORT", bg="#0055ff")
        self.whatsapp_btn.config(state="disabled", bg="#222")
        self.force_focus()

    def run_process(self):
        loc = self.loc_dropdown.get()
        self.main_btn.config(state="disabled", text="PROCESSING...", bg="#444")
        self.write(f"STAGING: {loc}...")
        
        try:
            coords = LOCATIONS.get(loc, (-31.87, 115.75)) # Defaulting to Trigg Point
            pdf_path = generate_report(loc, self.type_menu.get(), coords, BASE_PATH)
            
            if push_to_github():
                filename = os.path.basename(pdf_path)
                self.current_report_url = f"https://{GITHUB_USER}.github.io/{REPO}/OUTPUT/{loc}/{filename}"
                self.write("CLOUD SYNC INITIATED...")
                self.countdown(70)
        except Exception as e:
            self.write(f"ERROR: {e}")
            self.main_btn.config(state="normal", text="INITIATE REPORT", bg="#0055ff")

    def countdown(self, s):
        if s > 0:
            self.main_btn.config(text=f"SYNCING ({s}s)")
            self.root.after(1000, lambda: self.countdown(s-1))
        else:
            self.write("CLOUD STABLE. READY TO SEND.")
            self.main_btn.config(state="normal", text="INITIATE REPORT", bg="#0055ff")
            self.whatsapp_btn.config(state="normal", bg="#25D366", fg="white")

    def dispatch(self):
        raw_phone = self.phone_entry.get().strip()
        clean_phone = re.sub(r'[^0-9]', '', raw_phone) 
        msg = f"Sentinel Report: {self.current_report_url}"
        webbrowser.open(f"https://web.whatsapp.com/send?phone={clean_phone}&text={urllib.parse.quote(msg)}")
        
        self.write("WAKING WHATSAPP ENGINE...")
        self.write("WAITING FOR SYNC (75s)...")
        self.root.after(75000, self.robot_fire) # Bumped to 75s for safety

    def robot_fire(self):
        try:
            # A. HARD FOCUS BROWSER
            pyautogui.hotkey('alt', 'tab') 
            time.sleep(4)
            w, h = pyautogui.size()
            
            # B. SAFETY CLICK (TOP OF BROWSER)
            pyautogui.click(x=w * 0.5, y=h * 0.1) 
            time.sleep(1)
            
            # C. FOCUS INPUT FIELD
            pyautogui.click(x=w * 0.5, y=h * 0.92) 
            time.sleep(1)
            pyautogui.press('tab') # Fail-safe to land in input
            time.sleep(1)
            
            # D. THE FORCE-FIRE SEQUENCE
            for _ in range(7):
                pyautogui.press('enter')
                time.sleep(1.0)
            
            self.write("WAITING FOR SYNC HANDSHAKE...")
            time.sleep(8) # Extra buffer for message to leave the PC
            
            pyautogui.hotkey('ctrl', 'w') 
            self.write("DISPATCH SUCCESSFUL. SYSTEM IDLE.")
            winsound.Beep(1200, 400)
            
        except Exception as e:
            self.write(f"ROBOT ERROR: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SentinelHub(root)
    root.mainloop()