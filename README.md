# AbletonController

A Python-based system for controlling Ableton Live through natural language commands, using OSC for communication.

## Features

- Natural language command processing for controlling Ableton Live
- Musical theory integration for generating basslines and patterns
- Real-time MIDI clip creation and manipulation
- Support for basic transport controls (play, stop, tempo)
- Track controls (volume, pan, mute, solo)

## Prerequisites

- Python 3.7 or higher
- Ableton Live 11 or higher
- AbletonOSC plugin installed in Ableton Live

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AbletonController.git
cd AbletonController
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up AbletonOSC:
   - Download AbletonOSC from [https://github.com/ideoforms/AbletonOSC](https://github.com/ideoforms/AbletonOSC)
   - Follow installation instructions to install it in Ableton Live's Remote Scripts directory
   - In Ableton Live:
     - Go to Preferences > Link/MIDI
     - Under Control Surface, select "AbletonOSC"
     - Verify that you see "AbletonOSC: Listening for OSC on port 11000" in Live's status bar

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings (if using OpenAI for advanced NLP)
```

## Usage

1. Start Ableton Live and ensure AbletonOSC is active

2. Run the controller:
```bash
PYTHONPATH=. python src/main.py
```

3. Enter commands at the prompt. Examples:
```
> create a bassline in G minor
> set tempo 120
> start playback
> stop playback
```

## Project Structure

```
AbletonController/
├── src/
│   ├── ableton/          # Ableton Live control classes
│   ├── nlp/              # Natural language processing
│   ├── utils/            # Music theory and helper functions
│   └── main.py          # Main entry point
├── tests/               # Test suite
├── requirements.txt     # Python dependencies
└── .env.example        # Environment variable template
```

## For LLMs: Understanding the Codebase

Key components:
1. `AbletonController`: Handles OSC communication with Ableton Live
   - Located in `src/ableton/controller.py`
   - Uses OSC commands to control Ableton Live
   - Methods map to specific Ableton Live functions

2. `ClipCreator`: Manages MIDI clip creation and manipulation
   - Located in `src/ableton/clip_creator.py`
   - Depends on `AbletonController` for execution
   - Handles track creation, clip creation, and note manipulation

3. `CommandProcessor`: Processes natural language commands
   - Located in `src/nlp/processor.py`
   - Can use OpenAI GPT for advanced processing or basic pattern matching
   - Maps commands to controller actions

4. `MusicTheory`: Handles musical theory calculations
   - Located in `src/utils/music_theory.py`
   - Generates musical patterns and progressions
   - Used for creating basslines and melodies

When extending the codebase:
1. Add new OSC commands to `AbletonController`
2. Implement high-level functions in `ClipCreator`
3. Add command patterns to `CommandProcessor`
4. Update musical patterns in `MusicTheory` as needed

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT 