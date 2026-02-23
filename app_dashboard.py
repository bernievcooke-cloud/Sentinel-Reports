#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
import requests 
import winsound
import os
import time

# --- CORE CONFIG (BERNIE'S LOCK) ---
TOKEN = "8775524209:AAFVIpICTK1_Z3guFU_sBqKQtBA8YRKYtpc"
MY_ID = "8394071679"
BASE_PATH = r"C:\OneDrive\Public Reports A\OUTPUT"
GITHUB_USER = "bernievcooke-cloud"
REPO = "Sentinel-Access"

try:
    from core.locations import LOCATIONS
    from core.report_wrapper import generate_report
    from core.cloud_sync import push_to_github
except ImportError:
    LOCATIONS = {"TriggPoint": [-31.87, 115.75], "BellsBeach": [-38.37, 144.28]}
    def generate_report(*args): return os.path.join(BASE_PATH, args[0], f"{args[0]}_Report.pdf")
    def push_to_github(): return True

class SentinelHub:
    def __init__(self, root):
        self.root = root
        self.root.title("SENTINEL EXECUTIVE STRATEGY HUB V3.38")
        self.root.geometry("1550x900")
        self.root.configure(bg="#0a0a0a")
        self.admin_mode = False 
        
        # Style for consistent dropdowns
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TCombobox", fieldbackground="black", background="#333", foreground="white")
        
        self.setup_ui()

    def write(self, msg):
        self.log.insert(tk.END, f"\n> {msg}")
        self.log.see(tk.END)
        self.root.update()

    def setup_ui(self):
        self.root.columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.root.rowconfigure(0, weight=1)

        # --- COLUMN 1: CONTROLS & CONFIG ---
        col1 = tk.Frame(self.root, bg="#161616")
        col1.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        tk.Label(col1, text="Admin Control", font=("Verdana", 18, "bold"), bg="#161616", fg="#00FFCC").pack(pady=15)
        self.admin_btn = tk.Button(col1, text="ENTER ADMIN MODE", bg="#333", fg="#00FFCC", command=self.toggle_admin)
        self.admin_btn.pack(fill="x", padx=40, pady=5)

        tk.Label(col1, text="REPORT TYPE", font=("Verdana", 10), bg="#161616", fg="gray").pack(pady=(15,0))
        self.type_menu = ttk.Combobox(col1, values=["Surf", "Sky"], state="readonly", font=("Consolas", 14))
        self.type_menu.pack(fill="x", padx=40, pady=5)
        self.type_menu.current(0)

        tk.Label(col1, text="EXISTING LOCATIONS", font=("Verdana", 10), bg="#161616", fg="gray").pack(pady=(15, 0))
        self.loc_dropdown = ttk.Combobox(col1, values=sorted(list(LOCATIONS.keys())), state="readonly", font=("Consolas", 14))
        self.loc_dropdown.pack(fill="x", padx=40, pady=5)
        self.loc_dropdown.current(0)

        tk.Label(col1, text="ADD NEW LOCATION", font=("Verdana", 10), bg="#161616", fg="#00BFFF").pack(pady=(15, 0))
        self.new_loc_entry = tk.Entry(col1, bg="black", fg="white", font=("Consolas", 14), justify="center")
        self.new_loc_entry.pack(fill="x", padx=40, pady=5)
        tk.Button(col1, text="SAVE LOCATION", bg="#005577", fg="white", command=self.add_location).pack(fill="x", padx=40, pady=5)

        tk.Label(col1, text="TARGET TELEGRAM ID", font=("Verdana", 10), bg="#161616", fg="#00FFCC").pack(pady=(15, 0))
        self.id_entry = tk.Entry(col1, bg="black", fg="#00FFCC", font=("Consolas", 16), justify="center")
        self.id_entry.insert(0, MY_ID) 
        self.id_entry.pack(fill="x", padx=40, pady=5, ipady=8)

        self.jolt_btn = tk.Button(col1, text="REFRESH & JOLT CLOUD", bg="#222", fg="white", command=lambda: push_to_github())
        self.jolt_btn.pack(fill="x", padx=40, pady=20)

        # --- COLUMN 2: PROGRESS ---
        col2 = tk.Frame(self.root, bg="#161616")
        col2.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        tk.Label(col2, text="system progress", font=("Verdana", 18, "bold"), bg="#161616", fg="#00FFCC").pack(pady=20)
        self.log = tk.Text(col2, height=22, bg="black", fg="#00FF00", font=("Consolas", 11), bd=0, padx=15, pady=15)
        self.log.pack(fill="x", padx=25, pady=5)
        self.main_btn = tk.Button(col2, text="INITIATE FULL PROCESS", bg="#0055ff", fg="white", height=2, font=("Verdana", 12, "bold"), command=self.start_thread)
        self.main_btn.pack(pady=10, padx=25, fill="x")

        # --- COLUMN 3: DATA FEEDS (RESTORED) ---
        col3 = tk.Frame(self.root, bg="#161616")
        col3.grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
        
        tk.Label(col3, text="LIVE FEED ALPHA", font=("Verdana", 10), bg="#161616", fg="gray").pack(pady=(10,0))
        self.feed_top = tk.Text(col3, height=16, bg="#080808", fg="#00FF00", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.feed_top.pack(fill="x", padx=25, pady=5)
        
        tk.Label(col3, text="LIVE FEED BETA", font=("Verdana", 10), bg="#161616", fg="gray").pack(pady=(10,0))
        self.feed_bottom = tk.Text(col3, height=16, bg="#080808", fg="#00BFFF", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.feed_bottom.pack(fill="x", padx=25, pady=5)

    def toggle_admin(self):
        if not self.admin_mode:
            pw = simpledialog.askstring("Admin", "Password:", show='*')
            if pw == "sentinel123":
                self.admin_mode = True
                self.admin_btn.config(text="EXIT ADMIN MODE", bg="#00FFCC", fg="black")
        else:
            self.admin_mode = False
            self.admin_btn.config(text="ENTER ADMIN MODE", bg="#333", fg="#00FFCC")

    def add_location(self):
        name = self.new_loc_entry.get().strip()
        if name:
            LOCATIONS[name] = [-32.0, 115.0]
            self.loc_dropdown['values'] = sorted(list(LOCATIONS.keys()))
            self.write(f"LOCATION ADDED: {name}")
            self.new_loc_entry.delete(0, tk.END)

    def start_thread(self):
        threading.Thread(target=self.run_process, daemon=True).start()

    def run_process(self):
        loc = self.loc_dropdown.get()
        rep_type = self.type_menu.get()
        self.write(f"STAGING: {loc} ({rep_type})...")
        try:
            pdf_path = generate_report(loc, rep_type, LOCATIONS[loc], BASE_PATH)
            if push_to_github():
                self.write("CLOUD SYNC ACTIVE. WAITING 70s...")
                for i in range(70, 0, -1):
                    self.main_btn.config(text=f"SYNCING ({i}s)")
                    time.sleep(1)
                self.dispatch_telegram(pdf_path, loc)
        except Exception as e:
            self.write(f"ERROR: {e}")
        self.main_btn.config(text="INITIATE FULL PROCESS", bg="#0055ff")

    def dispatch_telegram(self, pdf_path, loc):
        chat_id = self.id_entry.get().strip()
        self.write("UPLOADING PDF TO TELEGRAM...")
        url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
        
        try:
            with open(pdf_path, 'rb') as f:
                payload = {"chat_id": chat_id, "caption": f"✅ SENTINEL: {loc}"}
                files = {"document": f}
                resp = requests.post(url, data=payload, files=files, timeout=30)
            
            if resp.status_code == 200:
                self.write("DISPATCH SUCCESSFUL.")
                winsound.Beep(1200, 500)
            else:
                self.write(f"TELEGRAM ERROR: {resp.text}")
        except Exception as e:
            self.write(f"CONNECTION FAILED: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SentinelHub(root)
    root.mainloop()