#!/usr/bin/env python3
import os

# --- INTEGRATION WITH WORKERS ---
try:
    # This links to the cleaned surf_worker.py we just fixed
    from core.surf_worker import generate_report as surf_gen
except ImportError:
    def surf_gen(*args, **kwargs):
        raise Exception("Surf Worker (surf_worker.py) not found in /core")

def generate_report(location, report_type, coords, output_dir):
    """
    The Hub calls this function. 
    It decides whether to run the Surf engine or the Sky engine.
    """
    
    if report_type == "Surf":
        # Calls your strategy logic and PDF builder
        return surf_gen(location, report_type, coords, output_dir)
    
    elif report_type == "Sky":
        # Placeholder for your Sky/Aviation logic
        # For now, we return an error until the Sky worker is built
        raise Exception("Sky Report Engine is currently under construction.")
    
    else:
        raise Exception(f"Unknown Report Type: {report_type}")