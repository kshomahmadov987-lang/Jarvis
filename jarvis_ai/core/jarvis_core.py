"""
Jarvis AI Personal Assistant - Core Engine
Main orchestrator for all Jarvis modules
"""

import os
import sys
from typing import Optional, Callable, Dict
from datetime import datetime


class JarvisCore:
    """
    Main Jarvis AI Personal Assistant class.
    Orchestrates voice recognition, speech synthesis, command processing,
    and system integrations.
    """
    
    def __init__(self, name: str = "Jarvis", language: str = "en"):
        """
        Initialize Jarvis core system.
        
        Args:
            name: The name to respond to (default: "Jarvis")
            language: Language code for speech processing (default: "en")
        """
        self.name = name
        self.language = language
        self.is_listening = False
        self.commands: Dict[str, Callable] = {}
        self._initialize_modules()
        self._register_default_commands()
        
    def _initialize_modules(self):
        """Initialize all subsystem modules."""
        self.audio_engine = None
        self.speech_engine = None
        self.command_processor = None
        self.office_controller = None
        self.visual_core = None
        
        try:
            from ..engines.audio_engine import AudioEngine
            self.audio_engine = AudioEngine()
        except ImportError:
            print("[WARNING] Audio engine not available")
            
        try:
            from ..engines.speech_engine import SpeechEngine
            self.speech_engine = SpeechEngine(language=self.language)
        except ImportError:
            print("[WARNING] Speech engine not available")
            
        try:
            from ..engines.command_processor import CommandProcessor
            self.command_processor = CommandProcessor()
        except ImportError:
            print("[WARNING] Command processor not available")
            
        try:
            from ..engines.office_controller import OfficeController
            self.office_controller = OfficeController()
        except ImportError:
            print("[WARNING] Office controller not available")
            
    def _register_default_commands(self):
        """Register built-in voice commands."""
        default_commands = {
            "hello": self._cmd_hello,
            "time": self._cmd_time,
            "date": self._cmd_date,
            "status": self._cmd_status,
            "help": self._cmd_help,
            "exit": self._cmd_exit,
            "quit": self._cmd_exit,
            "goodbye": self._cmd_exit,
        }
        self.commands.update(default_commands)
        
    def register_command(self, phrase: str, handler: Callable):
        """
        Register a custom command handler.
        
        Args:
            phrase: Voice phrase to trigger the command
            handler: Function to call when phrase is detected
        """
        self.commands[phrase.lower()] = handler
        
    def speak(self, text: str):
        """
        Make Jarvis speak using text-to-speech.
        
        Args:
            text: Text to synthesize and speak
        """
        if self.speech_engine:
            self.speech_engine.speak(text)
        else:
            print(f"{self.name}: {text}")
            
    def listen(self) -> Optional[str]:
        """
        Listen for voice input.
        
        Returns:
            Recognized text or None if listening failed
        """
        if self.audio_engine:
            return self.audio_engine.listen()
        return None
        
    def process_command(self, command: str) -> bool:
        """
        Process a voice/text command.
        
        Args:
            command: The command text to process
            
        Returns:
            True if command was recognized and executed, False otherwise
        """
        command = command.lower().strip()
        
        # Remove wake word if present
        wake_words = [self.name.lower(), "jarvis", "hey"]
        for word in wake_words:
            if command.startswith(word):
                command = command[len(word):].strip()
                break
                
        # Execute command handler
        if command in self.commands:
            try:
                self.commands[command]()
                return True
            except Exception as e:
                self.speak(f"Error executing command: {str(e)}")
                return False
        else:
            self.speak(f"Command '{command}' not recognized. Say 'help' for available commands.")
            return False
            
    def run(self, wake_word: str = "jarvis"):
        """
        Start the main Jarvis loop.
        
        Args:
            wake_word: Word to activate Jarvis (default: "jarvis")
        """
        self.speak(f"{self.name} online. How may I assist you?")
        self.is_listening = True
        
        try:
            while self.is_listening:
                if self.audio_engine:
                    text = self.listen()
                    if text:
                        print(f"You said: {text}")
                        if wake_word.lower() in text.lower():
                            self.process_command(text)
                else:
                    # Fallback to text input if audio not available
                    text = input("You: ").strip()
                    if text:
                        self.process_command(text)
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()
            
    def shutdown(self):
        """Gracefully shutdown Jarvis."""
        self.is_listening = False
        self.speak("Shutting down. Goodbye!")
        
    # Default Command Handlers
    def _cmd_hello(self):
        """Respond to hello greeting."""
        self.speak(f"Hello! I'm {self.name}, your personal AI assistant.")
        
    def _cmd_time(self):
        """Tell current time."""
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        self.speak(f"The current time is {time_str}")
        
    def _cmd_date(self):
        """Tell current date."""
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        self.speak(f"Today is {date_str}")
        
    def _cmd_status(self):
        """Report system status."""
        self.speak("All systems operational. Ready to assist.")
        
    def _cmd_help(self):
        """Show available commands."""
        commands_list = ", ".join(sorted(self.commands.keys()))
        self.speak(f"Available commands: {commands_list}")
        
    def _cmd_exit(self):
        """Exit Jarvis."""
        self.speak("Goodbye!")
        self.is_listening = False
