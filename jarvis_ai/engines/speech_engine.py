"""
Speech Engine for Jarvis AI
Handles text-to-speech synthesis
"""

import os
from typing import Optional


class SpeechEngine:
    """
    Handles text-to-speech output.
    Supports multiple TTS backends.
    """
    
    def __init__(self, language: str = "en", rate: int = 150):
        """
        Initialize speech engine.
        
        Args:
            language: Language code (default: "en")
            rate: Speech rate in words per minute (default: 150)
        """
        self.language = language
        self.rate = rate
        self._gtts_available = False
        self._pyttsx3_available = False
        self._initialize_tts()
        
    def _initialize_tts(self):
        """Initialize text-to-speech libraries."""
        # Try gTTS (Google Text-to-Speech)
        try:
            from gtts import gTTS
            self._gtts_available = True
            print("[SPEECH] gTTS initialized successfully")
        except ImportError:
            print("[WARNING] gTTS not installed. Online TTS disabled.")
            
        # Try pyttsx3 (offline TTS)
        try:
            import pyttsx3
            try:
                self._engine = pyttsx3.init()
                self._engine.setProperty('rate', self.rate)
                voices = self._engine.getProperty('voices')
                # Try to set voice based on language
                for voice in voices:
                    if self.language.lower() in voice.languages or self.language[:2].lower() in voice.id.lower():
                        self._engine.setProperty('voice', voice.id)
                        break
                self._pyttsx3_available = True
                print("[SPEECH] pyttsx3 initialized successfully")
            except RuntimeError as e:
                # eSpeak not installed - common in containers
                print(f"[WARNING] pyttsx3 initialization failed: {e}")
                self._engine = None
        except ImportError:
            print("[WARNING] pyttsx3 not installed. Offline TTS disabled.")
            self._engine = None
            
    def speak(self, text: str, blocking: bool = True) -> bool:
        """
        Speak the given text.
        
        Args:
            text: Text to synthesize and speak
            blocking: If True, wait until speech completes
            
        Returns:
            True if successful, False otherwise
        """
        if not text:
            return False
            
        # Prefer offline TTS (pyttsx3) for speed
        if self._pyttsx3_available:
            try:
                print(f"[SPEECH] Speaking: {text}")
                self._engine.say(text)
                if blocking:
                    self._engine.runAndWait()
                return True
            except Exception as e:
                print(f"[ERROR] pyttsx3 failed: {e}")
                
        # Fallback to gTTS
        if self._gtts_available:
            try:
                from gtts import gTTS
                import tempfile
                
                print(f"[SPEECH] Speaking (gTTS): {text}")
                tts = gTTS(text=text, lang=self.language, slow=False)
                
                # Save to temporary file and play
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                    temp_file = fp.name
                    
                tts.save(temp_file)
                
                # Play audio based on OS
                if os.name == 'nt':  # Windows
                    os.system(f'start /min wmplayer "{temp_file}"')
                else:  # Linux/Mac
                    try:
                        import subprocess
                        subprocess.call(['mpg123', '-q', temp_file])
                    except FileNotFoundError:
                        subprocess.call(['aplay', temp_file])
                        
                # Cleanup
                try:
                    os.unlink(temp_file)
                except:
                    pass
                    
                return True
            except Exception as e:
                print(f"[ERROR] gTTS failed: {e}")
                
        # No TTS available
        print(f"[SPEECH] No TTS engine available. Text: {text}")
        return False
        
    def save_to_file(self, text: str, filename: str) -> bool:
        """
        Save speech to an audio file.
        
        Args:
            text: Text to synthesize
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        if not self._gtts_available:
            print("[ERROR] gTTS required for saving to file")
            return False
            
        try:
            from gtts import gTTS
            tts = gTTS(text=text, lang=self.language, slow=False)
            tts.save(filename)
            print(f"[SPEECH] Saved to {filename}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save speech: {e}")
            return False
            
    def list_voices(self):
        """List available voices."""
        if self._pyttsx3_available:
            voices = self._engine.getProperty('voices')
            print("Available voices:")
            for i, voice in enumerate(voices):
                print(f"  {i}: {voice.name} ({voice.id})")
        else:
            print("No offline voices available")
