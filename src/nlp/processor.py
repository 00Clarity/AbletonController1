import os
import logging
import json
from openai import OpenAI
import re
from typing import Dict, Any, Optional, Tuple, List
from src.utils.music_theory import MusicTheory

logger = logging.getLogger(__name__)

class CommandProcessor:
    """Process natural language commands into Ableton control actions."""
    
    def __init__(self):
        """Initialize the command processor."""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        if self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key)
        else:
            self.client = None
        
        # Define command patterns and their corresponding actions
        self.command_patterns = {
            'tempo': {
                'function': 'set_tempo',
                'params': ['bpm']
            },
            'play': {
                'function': 'start_playback',
                'params': []
            },
            'stop': {
                'function': 'stop_playback',
                'params': []
            },
            'trigger clip': {
                'function': 'trigger_clip',
                'params': ['track', 'clip']
            },
            'volume': {
                'function': 'set_track_volume',
                'params': ['track', 'volume']
            },
            'pan': {
                'function': 'set_track_pan',
                'params': ['track', 'pan']
            },
            'mute': {
                'function': 'mute_track',
                'params': ['track']
            },
            'solo': {
                'function': 'solo_track',
                'params': ['track']
            },
            'create bassline': {
                'function': 'create_bassline',
                'params': ['root', 'scale_type', 'pattern', 'length']
            }
        }
    
    async def process_command(self, command: str) -> Tuple[str, Dict[str, Any]]:
        """Process a natural language command into an action and parameters."""
        try:
            if self.client:
                return await self._process_with_gpt(command)
            else:
                return self._process_basic(command)
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            raise
    
    async def _process_with_gpt(self, command: str) -> Tuple[str, Dict[str, Any]]:
        """Process command using GPT for more advanced understanding."""
        system_prompt = """
        You are an Ableton Live control system. Convert natural language commands into specific actions.
        Available actions:
        - set_tempo(bpm: float)
        - start_playback()
        - stop_playback()
        - trigger_clip(track: int, clip: int)
        - set_track_volume(track: int, volume: float)
        - set_track_pan(track: int, pan: float)
        - mute_track(track: int)
        - solo_track(track: int)
        - create_bassline(root: str, scale_type: str = 'minor', pattern: str = 'walking', length: int = 4)
        
        For musical commands, understand:
        - Notes: C, C#, D, D#, E, F, F#, G, G#, A, A#, B
        - Scales: major, minor, harmonic_minor, melodic_minor
        - Patterns: simple, octave, walking, arpeggio
        
        Respond with JSON containing 'function' and 'parameters'.
        Example: {"function": "create_bassline", "parameters": {"root": "G", "scale_type": "minor", "pattern": "walking", "length": 4}}
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": command}
            ]
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            return result['function'], result['parameters']
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error parsing GPT response: {e}")
            return self._process_basic(command)
    
    def _process_basic(self, command: str) -> Tuple[str, Dict[str, Any]]:
        """Basic command processing without GPT."""
        command = command.lower()
        
        # Handle musical commands first
        if 'bassline' in command:
            params = {'root': 'C', 'scale_type': 'minor', 'pattern': 'walking', 'length': 4}
            
            # Extract root note
            note_match = re.search(r'in ([A-Ga-g]#?)\s*(major|minor)?', command)
            if note_match:
                params['root'] = note_match.group(1).upper()
                if note_match.group(2):
                    params['scale_type'] = note_match.group(2).lower()
            
            # Extract pattern
            for pattern in MusicTheory.BASS_PATTERNS.keys():
                if pattern in command:
                    params['pattern'] = pattern
                    break
            
            return 'create_bassline', params
        
        # Handle other commands
        for pattern, action in self.command_patterns.items():
            if pattern in command:
                params = {}
                
                # Extract numeric values
                words = command.split()
                for word in words:
                    try:
                        value = float(word)
                        # Assign value to first unassigned parameter
                        for param in action['params']:
                            if param not in params:
                                params[param] = value
                                break
                    except ValueError:
                        continue
                
                return action['function'], params
        
        raise ValueError(f"Could not understand command: {command}") 