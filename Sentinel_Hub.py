import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, time

# --- DYNAMIC PATHING (The Fix) ---
# This finds the folder where THIS script is saved (C:\OneDrive\PublicReports)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_PATH, "OUTPUT")

class SentinelHub:
    def __init__(self, root):
        self.root = root
        self.root.title("Sentinel Command V3.32")
        self.root.geometry("1400x850")
        self.root.configure(bg="#001d3d")
        
        self.admin_sidebar = tk.Frame(self.root, bg='white', width=380, padx=25, pady=25)
        self.admin_sidebar.pack(side="left", fill="y")
        self.admin_sidebar.pack_propagate(False)

        self.preview_area = tk.Frame(self.root, bg='#f1f3f5', padx=30, pady=25)
        self.preview_area.pack(side="right", expand=True, fill="both")
        
        self.setup_admin_panel()
        self.setup_preview_area()

    def get_existing_locations(self):
        if not os.path.exists(OUTPUT_DIR): return ["Torquay"]
        return sorted([d for d in os.listdir(OUTPUT_DIR) if os.path.isdir(os.path.join(OUTPUT_DIR, d))])

    def setup_admin_panel(self):
        tk.Label(self.admin_sidebar, text="SYSTEM ADMIN", font=("Helvetica", 20, "bold"), bg="white", fg="#001d3d").pack(anchor="w")
        tk.Frame(self.admin_sidebar, height=3, bg="#ffc300", width=120).pack(anchor="w", pady=(5, 30))

        tk.Button(self.admin_sidebar, text="🔄 REFRESH SYSTEM", font=("Helvetica", 10, "bold"), 
                  bg="#f8f9fa", relief="groove", pady=12, command=self.refresh_locations).pack(fill="x", pady=(0, 40))

        tk.Label(self.admin_sidebar, text="TARGET LOCATION", font=("Helvetica", 10, "bold"), bg="white", fg="#adb5bd").pack(anchor="w")
        self.loc_var = tk.StringVar()
        style = ttk.Style()
        style.configure("Large.TCombobox", font=("Helvetica", 14))
        self.loc_drop = ttk.Combobox(self.admin_sidebar, textvariable=self.loc_var, style="Large.TCombobox")
        self.loc_drop['values'] = self.get_existing_locations()
        self.loc_drop.pack(fill="x", pady=(5, 35), ipady=10)

        tk.Button(self.admin_sidebar, text="PREPARE SURF STRATEGY", bg="#001d3d", fg="white", 
                  font=("Helvetica", 12, "bold"), pady=18, command=lambda: self.trigger_worker("surf_worker.py")).pack(fill="x", pady=10)
        
        tk.Button(self.admin_sidebar, text="PREPARE SKY STRATEGY", bg="#003566", fg="white", 
                  font=("Helvetica", 12, "bold"), pady=18, command=lambda: self.trigger_worker("sky_worker.py")).pack(fill="x", pady=5)

        self.status_label = tk.Label(self.admin_sidebar, text="SYSTEM IDLE", font=("Helvetica", 10, "italic"), 
                                    bg="#f8f9fa", fg="#6c757d", pady=25, relief="sunken", bd=1)
        self.status_label.pack(fill="x", pady=40)

        self.pay_btn = tk.Button(self.admin_sidebar, text="💳 DISPATCH TO WHATSAPP", bg="#ffc300", fg="#001d3d", 
                                 font=("Helvetica", 13, "bold"), state="disabled", pady=25, command=self.dispatch_to_phone)
        self.pay_btn.pack(fill="x", side="bottom")

    def setup_preview_area(self):
        tk.Label(self.preview_area, text="STRATEGIC ANALYSIS PREVIEW", font=("Helvetica", 16, "bold"), bg="#f1f3f5", fg="#001d3d").pack(anchor="w")
        self.charts_container = tk.Frame(self.preview_area, bg="#f1f3f5")
        self.charts_container.pack(expand=True, fill="both", pady=20)
        self.upper_chart = tk.Frame(self.charts_container, bg="white", bd=1, relief="solid")
        self.upper_chart.pack(expand=True, fill="both", pady=(0, 15))
        self.lower_chart = tk.Frame(self.charts_container, bg="white", bd=1, relief="solid")
        self.lower_chart.pack(expand=True, fill="both")

    def refresh_locations(self):
        self.loc_drop['values'] = self.get_existing_locations()
        self.status_label.config(text="LOCATIONS UPDATED", fg="green")

    def trigger_worker(self, script_name):
        loc = self.loc_var.get().strip()
        if not loc: return
        
        # FULL PATH to the script (This prevents the 'No such file' error)
        script_path = os.path.join(BASE_PATH, script_name)
        
        self.pay_btn.config(state="disabled", text="GENERATING...", bg="#adb5bd")
        self.status_label.config(text=f"⚙️ EXECUTING {script_name.upper()}...", fg="#001d3d")
        
        threading.Thread(target=self.handshake_loop, args=(script_path, loc), daemon=True).start()

    def handshake_loop(self, script_path, loc):
        subprocess.Popen(['python', script_path, loc])
        target_dir = os.path.join(OUTPUT_DIR, loc)
        
        for i in range(20):
            self.status_label.config(text=f"⚙️ HANDSHAKE: SCANNING {loc} ({i+1}s)")
            if os.path.exists(target_dir):
                files = [f for f in os.listdir(target_dir) if f.endswith(".pdf")]
                if files:
                    self.root.after(0, lambda: self.worker_verified(loc))
                    return
            time.sleep(1)
        self.root.after(0, lambda: self.status_label.config(text="❌ HANDSHAKE TIMEOUT", fg="red"))

    def worker_verified(self, loc):
        self.status_label.config(text=f"✅ {loc.upper()} VERIFIED ON DISK", fg="#2ca02c")
        self.pay_btn.config(state="normal", text="💳 DISPATCH TO WHATSAPP", bg="#25d366", fg="white")

    def dispatch_to_phone(self):
        loc = self.loc_var.get().strip()
        # Use the Cloud script ONLY
        sender_path = os.path.join(BASE_PATH, "twilio_sender.py")
        subprocess.Popen(['python', sender_path, loc])
        
        self.pay_btn.config(text="☁️ CLOUD DISPATCHED", state="disabled", bg="#001d3d")
        self.status_label.config(text="✅ TWILIO MESSAGE FIRED", fg="blue")

if __name__ == "__main__":
    root = tk.Tk()
    app = SentinelHub(root)
    root.mainloop()