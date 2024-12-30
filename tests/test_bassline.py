#!/usr/bin/env python3
import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ableton.controller import AbletonController
from src.ableton.clip_creator import ClipCreator
from src.nlp.processor import CommandProcessor
from src.utils.music_theory import MusicTheory

async def test_bassline_creation():
    """Test creating a bassline in G minor."""
    print("\nTesting bassline creation...")
    
    try:
        # Initialize components
        controller = AbletonController()
        clip_creator = ClipCreator(controller)
        processor = CommandProcessor()
        
        # Force basic command processing by setting client to None
        processor.client = None
        
        # Test command
        command = "create a bassline in G minor"
        print(f"\nProcessing command: {command}")
        
        # Process the command
        function_name, params = await processor.process_command(command)
        print(f"Parsed command: {function_name} with params {params}")
        
        if function_name == 'create_bassline':
            # Create a MIDI track first
            track_index = 0
            clip_creator.ensure_midi_track(track_index, "G Minor Bass")
            print(f"Created MIDI track at index {track_index}")
            
            # Generate and create the bassline
            notes = MusicTheory.generate_bassline(**params)
            print(f"Generated {len(notes)} notes for the bassline")
            
            # Create the clip with the notes
            clip_creator.create_bassline(track_index, 0, notes, track_name="G Minor Bass")
            print("Created and triggered bassline clip")
            
            print("\nTest completed successfully!")
        else:
            print(f"Error: Unexpected function {function_name}")
            
    except Exception as e:
        print(f"Error during test: {e}")
        raise  # Re-raise to see full traceback

if __name__ == "__main__":
    # Run the test
    asyncio.run(test_bassline_creation()) 