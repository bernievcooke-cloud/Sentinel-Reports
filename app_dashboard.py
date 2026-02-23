#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
import os
import requests 
import winsound
import time

# --- 1. CORE CONFIG ---
TELEGRAM_BOT_TOKEN = "8775524209:AAFVIpICTK1_Z3guFU_sBqKQtBA8YRKYtpc"
DEFAULT_CHAT_ID = "8394071679" # This is now editable on the dash
BASE_PATH = r"C:\OneDrive\Public Reports A\OUTPUT"
GITHUB_USER = "bernievcooke-cloud"
REPO = "Sentinel-Access"

try:
    from core.locations import LOCATIONS
except ImportError:
    LOCATIONS = {"TriggPoint": [-31.87, 115.75], "BellsBeach": [-38.37, 144.28]}

try:
    from core.report_wrapper import generate_report
    from core.cloud_sync import push_to_github
except ImportError:
    def generate_report(*args): return "dummy.pdf"
    def push_to_github(): return True

class SentinelHub:
    def __init__(self, root):
        self.root = root
        self.root.title("SENTINEL EXECUTIVE STRATEGY HUB V3.34")
        self.root.geometry("1550x900")
        self.root.configure(bg="#0a0a0a")
        
        self.admin_mode = False 
        self.current_report_url = ""
        self.last_pdf_path = ""
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TCombobox", fieldbackground="black", background="#333", foreground="white", arrowsize=25)
        
        self.setup_ui()

    def write(self, msg):
        self.log.insert(tk.END, f"\n> {msg}")
        self.log.see(tk.END)
        self.root.update()

    def setup_ui(self):
        self.root.columnconfigure((0, 1, 2), weight=1, uniform="col")
        self.root.rowconfigure(0, weight=1)

        # --- COLUMN 1: CONTROLS (UNLOCKED) ---
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
        if LOCATIONS: self.loc_dropdown.current(0)

        tk.Label(col1, text="ADD NEW LOCATION", font=("Verdana", 10), bg="#161616", fg="#00BFFF").pack(pady=(15, 0))
        self.new_loc_entry = tk.Entry(col1, bg="black", fg="white", font=("Consolas", 14), justify="center")
        self.new_loc_entry.pack(fill="x", padx=40, pady=5)
        
        tk.Button(col1, text="SAVE LOCATION", bg="#005577", fg="white", command=self.add_location).pack(fill="x", padx=40, pady=5)

        # FIXED: TELEGRAM ID / PHONE LINK BOX (FULLY EDITABLE)
        tk.Label(col1, text="TARGET TELEGRAM ID (EDITABLE)", font=("Verdana", 10), bg="#161616", fg="#00FFCC").pack(pady=(15, 0))
        self.id_entry = tk.Entry(col1, bg="black", fg="#00FFCC", font=("Consolas", 16), justify="center", insertbackground="white")
        self.id_entry.insert(0, DEFAULT_CHAT_ID) 
        self.id_entry.pack(fill="x", padx=40, pady=5, ipady=8)

        # INSTRUCTION BOX
        instr_frame = tk.Frame(col1, bg="#101010", highlightthickness=1, highlightbackground="#444")
        instr_frame.pack(fill="x", padx=30, pady=15)
        instructions = (
            "SYSTEM INSTRUCTIONS:\n\n"
            "1. Enter report type\n"
            "2. Select/Add location\n"
            "3. Confirm Telegram ID above\n"
            "4. Hit Initiate\n\n"
            "Report arrives on Telegram app."
        )
        tk.Label(instr_frame, text=instructions, font=("Verdana", 10), bg="#101010", fg="#bbbbbb", justify="left", padx=10, pady=10).pack()

        # --- COLUMN 2: PROGRESS ---
        col2 = tk.Frame(self.root, bg="#161616")
        col2.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

        # TELEGRAM INFO
        tg_info = tk.Frame(col2, bg="#001a33", highlightthickness=1, highlightbackground="#0055ff")
        tg_info.pack(fill="x", padx=25, pady=(20, 10))
        tk.Label(tg_info, text="Telegram required for dispatch", font=("Verdana", 10, "bold"), bg="#001a33", fg="white").pack(pady=(5,0))
        link = tk.Label(tg_info, text="Sign up: https://desktop.telegram.org", font=("Verdana", 8, "underline"), bg="#001a33", fg="#00FFCC", cursor="hand2")
        link.pack(pady=(0, 5))
        link.bind("<Button-1>", lambda e: webbrowser.open("https://desktop.telegram.org"))

        tk.Label(col2, text="system progress", font=("Verdana", 18, "bold"), bg="#161616", fg="#00FFCC").pack(pady=10)
        self.log = tk.Text(col2, height=18, bg="black", fg="#00FF00", font=("Consolas", 11), bd=0, padx=15, pady=15)
        self.log.pack(fill="x", padx=25, pady=5)
        
        self.main_btn = tk.Button(col2, text="INITIATE FULL PROCESS", bg="#0055ff", fg="white", height=2, font=("Verdana", 12, "bold"), command=self.run_process)
        self.main_btn.pack(pady=10, padx=25, fill="x")

        # --- COLUMN 3: DATA FEEDS ---
        col3 = tk.Frame(self.root, bg="#161616")
        col3.grid(row=0, column=2, sticky="nsew", padx=15, pady=15)
        self.feed_top = tk.Text(col3, height=18, bg="#080808", fg="#00FF00", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.feed_top.pack(fill="x", padx=25, pady=(40, 10))
        self.feed_bottom = tk.Text(col3, height=18, bg="#080808", fg="#00BFFF", font=("Consolas", 10), bd=0, padx=15, pady=15)
        self.feed_bottom.pack(fill="x", padx=25, pady=10)

    def toggle_admin(self):
        if not self.admin_mode:
            pw = simpledialog.askstring("Admin Access", "Enter Password:", show='*')
            if pw == "sentinel123":
                self.admin_mode = True
                self.admin_btn.config(text="EXIT ADMIN MODE", bg="#00FFCC", fg="black")
                self.write("ADMIN MODE ACTIVE")
        else:
            self.admin_mode = False
            self.admin_btn.config(text="ENTER ADMIN MODE", bg="#333", fg="#00FFCC")
            self.write("ADMIN MODE EXITED")

    def add_location(self):
        name = self.new_loc_entry.get().strip()
        if name:
            LOCATIONS[name] = [-32.0, 115.0]
            self.loc_dropdown['values'] = sorted(list(LOCATIONS.keys()))
            self.write(f"LOCATION ADDED: {name}")
            self.new_loc_entry.delete(0, tk.END)

    def run_process(self):
        loc = self.loc_dropdown.get()
        self.write(f"STAGING: {loc}...")
        try:
            self.last_pdf_path = generate_report(loc, self.type_menu.get(), LOCATIONS[loc], BASE_PATH)
            if push_to_github():
                self.current_report_url = f"https://{GITHUB_USER}.github.io/{REPO}/OUTPUT/{loc}/{os.path.basename(self.last_pdf_path)}"
                self.countdown(70)
        except Exception as e:
            self.write(f"ERROR: {e}")

    def countdown(self, s):
        if s > 0:
            self.main_btn.config(text=f"SYNCING ({s}s)", bg="#444", state="disabled")
            self.root.after(1000, lambda: self.countdown(s-1))
        else:
            self.main_btn.config(text="INITIATE FULL PROCESS", bg="#0055ff", state="normal")
            self.dispatch_telegram()

    def dispatch_telegram(self):
        chat_id = self.id_entry.get().strip()
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        self.write("AUTO-DISPATCHING PDF...")
        try:
            with open(self.last_pdf_path, 'rb') as f:
                payload = {"chat_id": chat_id, "caption": f"✅ SENTINEL: {self.loc_dropdown.get()}", "parse_mode": "Markdown"}
                files = {"document": f}
                resp = requests.post(url, data=payload, files=files)
            if resp.status_code == 200:
                self.write("DISPATCH SUCCESSFUL.")
                winsound.Beep(1000, 500)
            else:
                self.write(f"API ERROR: {resp.text}")
        except Exception as e:
            self.write(f"DISPATCH FAILED: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SentinelHub(root)
    root.mainloop()