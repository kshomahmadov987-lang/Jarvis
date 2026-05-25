#!/usr/bin/env python3
"""
Jarvis AI Personal Assistant - Main Entry Point
Run this script to start Jarvis
"""

import sys
from typing import Callable

from jarvis_ai import JarvisCore


def main():
    """Main entry point for Jarvis AI."""
    print("=" * 50)
    print("       JARVIS AI PERSONAL ASSISTANT")
    print("=" * 50)
    print()
    
    # Initialize Jarvis
    jarvis = JarvisCore(name="Jarvis", language="en")
    
    # Register additional custom commands
    def create_note():
        """Create a quick note."""
        if not jarvis.office_controller:
            jarvis.speak("Office controller not available.")
            return
            
        print("\n[NOTE MODE] Enter your note (type 'done' to finish):")
        lines = []
        while True:
            line = input("> ")
            if line.lower() == 'done':
                break
            lines.append(line)
            
        content = "\n".join(lines)
        filepath = jarvis.office_controller.create_word_document(
            "quick_note", 
            content, 
            title="Quick Note"
        )
        if filepath:
            jarvis.speak(f"Note saved to {filepath}")
        else:
            jarvis.speak("Failed to save note. Word support may not be available.")
            
    def system_status():
        """Report detailed system status."""
        try:
            from jarvis_ai.utils.system_monitor import SystemMonitor
            monitor = SystemMonitor()
            report = monitor.get_status_report()
            jarvis.speak(f"System status: {report}")
        except ImportError:
            jarvis.speak("System monitor not available.")
            
    def check_weather(city: str = "London"):
        """Check weather for a city."""
        try:
            from jarvis_ai.utils.weather import WeatherAPI
            weather = WeatherAPI()
            if weather.api_key:
                report = weather.get_weather_report(city)
                jarvis.speak(report)
            else:
                jarvis.speak("Weather API key not configured. Set OPENWEATHER_API_KEY environment variable.")
        except ImportError:
            jarvis.speak("Weather service not available.")
    
    # Register custom commands with aliases
    jarvis.register_command("create note", create_note, aliases=["make note", "new note"])
    jarvis.register_command("system status", system_status, aliases=["status report", "check system"])
    jarvis.register_command("weather", lambda: check_weather("London"), aliases=["check weather"])
    
    # Start Jarvis
    print("Starting Jarvis...")
    print("Type 'help' for available commands or 'exit' to quit.")
    print()
    
    try:
        jarvis.run(wake_word="jarvis")
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        jarvis.shutdown()
        
    print("\nThank you for using Jarvis AI!")


if __name__ == "__main__":
    main()
