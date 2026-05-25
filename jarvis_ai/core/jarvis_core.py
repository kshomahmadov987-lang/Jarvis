"""
Jarvis AI Personal Assistant - Core Engine
Main orchestrator for all Jarvis modules
"""

import os
from typing import Optional, Callable, Dict, List
from datetime import datetime


class JarvisCore:
    """
    Main Jarvis AI Personal Assistant class.
    Orchestrates voice recognition, speech synthesis, command processing,
    and system integrations.
    """
    
    DEFAULT_WAKE_WORDS = ["jarvis", "hey"]
    
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
        self.command_aliases: Dict[str, str] = {}
        self._initialize_modules()
        self._register_default_commands()
        
    def _initialize_modules(self):
        """Initialize all subsystem modules."""
        self.audio_engine = None
        self.speech_engine = None
        self.command_processor = None
        self.office_controller = None
        
        module_initializers = [
            ("Audio engine", self._init_audio_engine),
            ("Speech engine", self._init_speech_engine),
            ("Command processor", self._init_command_processor),
            ("Office controller", self._init_office_controller),
        ]
        
        for module_name, init_func in module_initializers:
            try:
                init_func()
            except ImportError:
                print(f"[WARNING] {module_name} not available")
    
    def _init_audio_engine(self):
        """Initialize the audio engine module."""
        from jarvis_ai.engines.audio_engine import AudioEngine
        self.audio_engine = AudioEngine()
    
    def _init_speech_engine(self):
        """Initialize the speech engine module."""
        from jarvis_ai.engines.speech_engine import SpeechEngine
        self.speech_engine = SpeechEngine(language=self.language)
    
    def _init_command_processor(self):
        """Initialize the command processor module."""
        from jarvis_ai.engines.command_processor import CommandProcessor
        self.command_processor = CommandProcessor()
    
    def _init_office_controller(self):
        """Initialize the office controller module."""
        from jarvis_ai.engines.office_controller import OfficeController
        self.office_controller = OfficeController()
            
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
        
    def register_command(self, phrase: str, handler: Callable, aliases: List[str] = None):
        """
        Register a custom command handler with optional aliases.
        
        Args:
            phrase: Voice phrase to trigger the command
            handler: Function to call when phrase is detected
            aliases: List of alternative phrases that map to this command
        """
        self.commands[phrase.lower()] = handler
        
        if aliases:
            for alias in aliases:
                self.command_aliases[alias.lower()] = phrase.lower()
        
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
        for word in self.DEFAULT_WAKE_WORDS + [self.name.lower()]:
            if command.startswith(word):
                command = command[len(word):].strip()
                break
                
        # Check for alias mapping
        if command in self.command_aliases:
            command = self.command_aliases[command]
        
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
