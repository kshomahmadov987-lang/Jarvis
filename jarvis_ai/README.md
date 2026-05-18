# Jarvis AI Personal Assistant

A powerful, modular AI personal assistant inspired by Tony Stark's JARVIS.

## Features

- 🎤 **Voice Recognition** - Listen to voice commands using microphone input
- 🔊 **Text-to-Speech** - Speak responses using multiple TTS backends
- 📝 **Document Management** - Create and edit Word documents
- 📊 **Spreadsheet Support** - Create and read Excel files
- 💻 **System Monitoring** - Monitor CPU, RAM, and disk usage
- 🌤️ **Weather Updates** - Get current weather information
- 🧠 **Command Processing** - Natural language command matching with pattern support

## Quick Start

### Run Demo

```bash
cd /workspace
PYTHONPATH=/workspace python jarvis_ai/demo.py
```

### Run Interactive Assistant

```bash
cd /workspace
PYTHONPATH=/workspace python jarvis_ai/main.py
```

### Basic Usage

Once started, you can interact with Jarvis via text (or voice if audio hardware is available):

```
You: hello
Jarvis: Hello! I'm Jarvis, your personal AI assistant.

You: time
Jarvis: The current time is 02:45 PM

You: help
Jarvis: Available commands: create note, date, exit, goodbye, hello, help, ...
```

## Project Structure

```
jarvis_ai/
├── __init__.py           # Package initialization
├── main.py               # Main entry point
├── core/
│   ├── __init__.py
│   └── jarvis_core.py    # Main Jarvis orchestrator
├── engines/
│   ├── __init__.py
│   ├── audio_engine.py   # Voice recognition
│   ├── speech_engine.py  # Text-to-speech
│   ├── command_processor.py  # Command matching
│   └── office_controller.py  # Document handling
├── utils/
│   ├── __init__.py
│   ├── system_monitor.py # System resource monitoring
│   └── weather.py        # Weather API integration
└── assets/               # Audio files, images, etc.
```

## Available Commands

### Built-in Commands
- `hello` - Greet Jarvis
- `time` - Get current time
- `date` - Get current date
- `status` - System status check
- `help` - Show available commands
- `exit` / `quit` / `goodbye` - Exit Jarvis

### Extended Commands (in main.py)
- `create note` - Create a quick note document
- `system status` - Detailed system resource report
- `weather` - Get weather information (requires API key)

## Configuration

### Weather API

To enable weather features, get a free API key from [OpenWeatherMap](https://openweathermap.org/api) and set it:

```bash
export OPENWEATHER_API_KEY=your_api_key_here
```

Or modify the `WeatherAPI` initialization in your code.

### Language Support

Jarvis supports multiple languages:

```python
from jarvis_ai import JarvisCore

# English
jarvis = JarvisCore(language="en")

# Spanish
jarvis = JarvisCore(language="es")

# Russian
jarvis = JarvisCore(language="ru")
```

## Customization

### Adding Custom Commands

```python
from jarvis_ai import JarvisCore

jarvis = JarvisCore()

def my_custom_command():
    jarvis.speak("This is my custom command!")

jarvis.register_command("custom", my_custom_command, aliases=["my command"])
```

### Using Pattern Matching

```python
def greet_person(name):
    jarvis.speak(f"Hello, {name}!")

jarvis.command_processor.register_pattern(r'greet (\w+)', greet_person)
# Now "greet John" will call greet_person("John")
```

## API Reference

### JarvisCore

The main class that orchestrates all components:

```python
jarvis = JarvisCore(name="Jarvis", language="en")
jarvis.speak("Hello!")
jarvis.listen()  # Returns recognized text
jarvis.process_command("hello")
jarvis.run()  # Start interactive loop
```

### AudioEngine

Handles microphone input:

```python
from jarvis_ai.engines import AudioEngine

audio = AudioEngine()
text = audio.listen()  # Listen and recognize speech
audio.record_audio("recording.wav", duration=5)  # Record to file
```

### SpeechEngine

Text-to-speech output:

```python
from jarvis_ai.engines import SpeechEngine

speech = SpeechEngine(language="en")
speech.speak("Hello world!")
speech.save_to_file("Hello!", "output.mp3")
```

### OfficeController

Document management:

```python
from jarvis_ai.engines import OfficeController

office = OfficeController()
office.create_word_document("report", "Content here", title="My Report")
office.create_excel_sheet("data", [[1, 2], [3, 4]], headers=["A", "B"])
```

## Troubleshooting

### No Audio Input
- Ensure microphone is connected and permissions are granted
- Install `pyaudio` and `speechrecognition` packages
- On Linux: `sudo apt-get install portaudio19-dev`

### No Speech Output
- Install `pyttsx3` for offline TTS or `gtts` for online TTS
- On Linux: `sudo apt-get install mpg123` for gTTS playback

### Import Errors
- Make sure you're running from the project root directory
- Verify all dependencies are installed: `pip install -r requirements.txt`

## License

MIT License - Feel free to use and modify for your projects.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

*"Sometimes you gotta run before you can walk."* - Tony Stark
