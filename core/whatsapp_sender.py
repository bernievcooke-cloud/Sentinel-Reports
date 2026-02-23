def dispatch(self):
        phone = self.phone_entry.get().strip()
        msg = f"Sentinel Report: {self.current_report_url}"
        # Force the browser to open
        webbrowser.open(f"https://web.whatsapp.com/send?phone={phone}&text={urllib.parse.quote(msg)}")
        self.write("WAITING FOR WHATSAPP INTERFACE...")
        # Increase wait time to 20s to ensure the 'Send' button is visible
        self.root.after(20000, self.robot_fire) 

    def robot_fire(self):
        # 1. Click the center of the screen to focus the browser
        w, h = pyautogui.size()
        pyautogui.click(x=w/2, y=h/2) 
        time.sleep(2) # Wait for focus
        
        # 2. Press Enter to send the text
        pyautogui.press('enter')
        time.sleep(2)
        
        # 3. Double-tap Enter just in case of a popup
        pyautogui.press('enter')
        
        winsound.Beep(1000, 400)
        self.write("DISPATCH COMMAND SENT.")