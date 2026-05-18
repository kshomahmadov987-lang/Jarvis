#!/usr/bin/env python3
"""
Simple demo script to test Jarvis AI functionality
Run this to see Jarvis in action
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jarvis_ai import JarvisCore


def demo():
    """Run a demonstration of Jarvis capabilities."""
    
    print("=" * 60)
    print("           JARVIS AI PERSONAL ASSISTANT - DEMO")
    print("=" * 60)
    print()
    
    # Initialize Jarvis
    jarvis = JarvisCore(name="Jarvis", language="en")
    
    print("\n--- Testing Basic Commands ---\n")
    
    # Test commands
    commands_to_test = [
        "hello",
        "time", 
        "date",
        "status",
        "help"
    ]
    
    for cmd in commands_to_test:
        print(f"\n[USER] {cmd}")
        jarvis.process_command(cmd)
        
    # Test Office Controller
    print("\n--- Testing Document Creation ---\n")
    
    if jarvis.office_controller:
        print("[USER] Create a test document")
        
        doc_path = jarvis.office_controller.create_word_document(
            filename="demo_report",
            content="This is a test document created by Jarvis AI.",
            title="Demo Report"
        )
        
        if doc_path:
            print(f"[JARVIS] Document created at: {doc_path}")
            
        # Create Excel sheet
        excel_path = jarvis.office_controller.create_excel_sheet(
            filename="demo_data",
            data=[
                ["Item", "Quantity", "Price"],
                ["Apple", 10, 1.50],
                ["Banana", 20, 0.75],
                ["Orange", 15, 1.25]
            ],
            headers=["Item", "Quantity", "Price"]
        )
        
        if excel_path:
            print(f"[JARVIS] Spreadsheet created at: {excel_path}")
            
    # Test System Monitor
    print("\n--- Testing System Monitor ---\n")
    
    try:
        from jarvis_ai.utils.system_monitor import SystemMonitor
        monitor = SystemMonitor()
        
        if monitor._psutil_available:
            report = monitor.get_status_report()
            print(f"[SYSTEM] {report}")
        else:
            print("[SYSTEM] psutil not available")
    except Exception as e:
        print(f"[ERROR] System monitor test failed: {e}")
        
    # Test Weather (if API key available)
    print("\n--- Testing Weather Service ---\n")
    
    try:
        from jarvis_ai.utils.weather import WeatherAPI
        weather = WeatherAPI()
        
        if weather.api_key:
            report = weather.get_weather_report("London")
            print(f"[WEATHER] {report}")
        else:
            print("[WEATHER] No API key configured (set OPENWEATHER_API_KEY)")
    except Exception as e:
        print(f"[ERROR] Weather test failed: {e}")
        
    print("\n" + "=" * 60)
    print("              DEMO COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("\nJarvis AI is ready to use!")
    print("Run 'python main.py' to start the interactive assistant.")
    print()


if __name__ == "__main__":
    demo()
