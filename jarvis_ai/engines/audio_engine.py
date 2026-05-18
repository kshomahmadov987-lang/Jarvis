"""
Audio Engine for Jarvis AI
Handles microphone input and audio recording
"""

import os
from typing import Optional


class AudioEngine:
    """
    Handles audio input from microphone.
    Uses speech recognition libraries when available.
    """
    
    def __init__(self, sample_rate: int = 16000):
        """
        Initialize audio engine.
        
        Args:
            sample_rate: Audio sample rate in Hz (default: 16000)
        """
        self.sample_rate = sample_rate
        self.is_recording = False
        self._recognizer = None
        self._microphone = None
        self._initialize_speech_recognition()
        
    def _initialize_speech_recognition(self):
        """Initialize speech recognition library."""
        try:
            import speech_recognition as sr
            self._recognizer = sr.Recognizer()
            self._microphone = sr.Microphone(sample_rate=self.sample_rate)
            
            # Adjust for ambient noise
            with self._microphone as source:
                print("[AUDIO] Adjusting for ambient noise...")
                self._recognizer.adjust_for_ambient_noise(source, duration=1)
            print("[AUDIO] Microphone initialized successfully")
        except ImportError:
            print("[WARNING] speech_recognition not installed. Voice input disabled.")
        except Exception as e:
            print(f"[ERROR] Failed to initialize microphone: {e}")
            
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input and convert to text.
        
        Args:
            timeout: Maximum seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for the phrase
            
        Returns:
            Recognized text or None if failed
        """
        if not self._recognizer or not self._microphone:
            return None
            
        try:
            with self._microphone as source:
                print("[AUDIO] Listening...")
                audio = self._recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
            # Try Google Speech Recognition (free, no API key needed)
            try:
                text = self._recognizer.recognize_google(audio)
                print(f"[AUDIO] Recognized: {text}")
                return text
            except sr.UnknownValueError:
                print("[AUDIO] Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"[AUDIO] Recognition service error: {e}")
                return None
                
        except Exception as e:
            print(f"[AUDIO] Error during listening: {e}")
            return None
            
    def record_audio(self, filename: str = "recording.wav", duration: int = 5) -> bool:
        """
        Record audio to a file.
        
        Args:
            filename: Output filename
            duration: Recording duration in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self._microphone:
            return False
            
        try:
            import pyaudio
            import wave
            
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            
            p = pyaudio.PyAudio()
            stream = p.open(
                format=FORMAT,
                channels=CHANNELS,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=CHUNK
            )
            
            print(f"[AUDIO] Recording for {duration} seconds...")
            frames = []
            
            for _ in range(0, int(self.sample_rate / CHUNK * duration)):
                data = stream.read(CHUNK)
                frames.append(data)
                
            print("[AUDIO] Recording finished")
            
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Save to WAV file
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            print(f"[AUDIO] Saved to {filename}")
            return True
            
        except ImportError:
            print("[WARNING] pyaudio not installed. Cannot record audio.")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to record audio: {e}")
            return False
