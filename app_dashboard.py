#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import urllib.parse
import os
import time
import pyautogui
import winsound
from datetime import datetime

# --- SYSTEM IDENTITY & PATHS ---
GITHUB_USER = "bernievcooke-cloud"
REPO = "Sentinel-Access"
BASE_PATH = r"C:\OneDrive\Public Reports A\OUTPUT"

# --- CORE INTEGRATION ---
try:
    from core.locations import LOCATIONS
    from core.report_wrapper import generate_report
    from core.cloud_sync import push_to_github
except ImportError:
    LOCATIONS = {"BellsBeach": (-38.37, 144.28)}

class SentinelHub:
    def __init__(self, root):
        self.root = root
        self.root.title("SENTINEL EXECUTIVE STRATEGY HUB V3.65")
        self.root.geometry("1450x850")
        self.root.configure(bg="#0a0a0a")

        self.current_report_url = ""
        self.setup_ui()
        
        # --- FLASHING CURSOR INITIALIZATION ---
        self.root.after(200, self.force_focus)

    def force_focus(self):
        """Forces the window to front and starts the flashing cursor at +61"""
        self.root.focus_force()  # Brings window to foreground
        self.phone_entry.focus_set()
        self.phone_entry.icursor(tk.END) # Places cursor after '61'

    def setup_ui(self):
        self.root.columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.root.rowconfigure(0, weight=1)

        # --- COLUMN 1: LEFT BAR (ADMIN & RESET) ---
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

        tk.Label(col1, text="NEW LOCATION (BLANK)", font=("Verdana", 10), bg="#161616", fg="#00FFCC").pack(pady=(25, 0))
        self.manual_loc = tk.Entry(col1, bg="black", fg="white", font=("Consolas", 14), justify="center", highlightthickness=2, highlightbackground="white", bd=0)
        self.manual_loc.pack(fill="x", padx=40, pady=5, ipady=12)

        tk.Label(col1, text="TARGET PHONE", font=("Verdana", 10), bg="#161616", fg="gray").pack(pady=(25, 0))
        # The 'insertofftime' and 'insertontime' ensure a visible, sharp blink
        self.phone_entry = tk.Entry(col1, bg="black", fg="white", font=("Consolas", 14), 
                                    justify="center", highlightthickness=2, 
                                    highlightbackground="#00FFCC", bd=0,
                                    insertbackground="white", insertwidth=4)
        self.phone_entry.insert(0, "61")
        self.phone_entry.pack(fill="x", padx=40, pady=5, ipady=12)

        # RESET BUTTON
        self.reset_btn = tk.Button(col1, text="RESET SYSTEM", bg="#333", fg="white", font=("Verdana", 10, "bold"), command=self.reset_fields)
        self.reset_btn.pack(side="bottom", fill="x", padx=40, pady=20)

        # --- COLUMN 2: MIDDLE BAR (SYSTEM PROGRESS) ---
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

        # --- COLUMN 3: RIGHT BAR ---
        col3 = tk.Frame(self.root, bg="#161616")
        col3.grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
        
        self.feed_top = tk.Text(col3, height=15, bg="#080808", fg="#00FF00", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.feed_top.pack(fill="x", padx=25, pady=(40, 10))
        self.feed_top.insert("1.0", "[DATA FEED ALPHA]")

        self.feed_bottom = tk.Text(col3, height=15, bg="#080808", fg="#00BFFF", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.feed_bottom.pack(fill="x", padx=25, pady=10)
        self.feed_bottom.insert("1.0", "[DATA FEED BETA]")

    def write(self, msg):
        self.log.insert(tk.END, f"\n> {msg}")
        self.log.see(tk.END)
        self.root.update()

    def reset_fields(self):
        self.manual_loc.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, "61")
        self.log.delete("1.0", tk.END)
        self.write("SYSTEM RESET. READY.")
        self.main_btn.config(state="normal", text="INITIATE REPORT", bg="#0055ff")
        self.whatsapp_btn.config(state="disabled", bg="#222")
        self.force_focus()

    def run_process(self):
        manual_name = self.manual_loc.get().strip()
        loc = manual_name if manual_name else self.loc_dropdown.get()
        
        if loc not in LOCATIONS:
            try:
                with open("core/locations.py", "a") as f:
                    f.write(f'\nLOCATIONS["{loc}"] = (-38.37, 144.28)')
                LOCATIONS[loc] = (-38.37, 144.28)
                self.write(f"LEARNED NEW SPOT: {loc}")
            except: pass

        self.main_btn.config(state="disabled", text="PROCESSING...", bg="#444")
        self.write(f"STAGING: {loc}...")
        
        try:
            coords = LOCATIONS.get(loc, (-38.37, 144.28))
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
        phone = self.phone_entry.get().strip()
        msg = f"Sentinel Report: {self.current_report_url}"
        
        # 1. Open browser (Starts from a closed state)
        webbrowser.open(f"https://web.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(msg)}")
        
        self.write("WAKING WHATSAPP ENGINE...")
        self.write("DO NOT TOUCH MOUSE OR KEYBOARD.")
        
        # 2. Give it 35 seconds to load the chat from a cold start
        self.root.after(35000, self.robot_fire)

    def robot_fire(self):
        try:
            # A. Grab the browser window
            pyautogui.hotkey('alt', 'tab') 
            time.sleep(2)
            
            # B. The Send Sequence (Triple-Tap for certainty)
            for _ in range(3):
                pyautogui.press('enter')
                time.sleep(2)
            
            # C. THE KILL SWITCH
            # This closes the WhatsApp tab immediately after sending.
            # Your browser stays open (if other tabs were open), but the evidence is gone.
            pyautogui.hotkey('ctrl', 'w') 
            
            winsound.Beep(1200, 400)
            self.write("DISPATCH SUCCESSFUL. DESKTOP CLEARED.")
            
        except Exception as e:
            self.write(f"ROBOT ERROR: {e}")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = SentinelHub(root)
    root.mainloop()