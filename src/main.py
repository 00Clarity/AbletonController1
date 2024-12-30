#!/usr/bin/env python3
import os
import sys
import logging
import asyncio
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

from ableton.controller import AbletonController
from ableton.clip_creator import ClipCreator
from nlp.processor import CommandProcessor
from utils.music_theory import MusicTheory

def setup_logging():
    """Configure logging based on environment settings."""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', 'ableton_control.log')
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

async def process_musical_command(command: str, controller: AbletonController, 
                                clip_creator: ClipCreator, processor: CommandProcessor) -> None:
    """Process a musical command and create MIDI content."""
    # Force basic command processing
    processor.client = None
    
    function_name, params = await processor.process_command(command)
    
    if function_name == 'create_bassline':
        # Generate bassline notes using music theory
        notes = MusicTheory.generate_bassline(
            root=params.get('root', 'C'),
            scale_type=params.get('scale_type', 'minor'),
            pattern=params.get('pattern', 'walking'),
            length=params.get('length', 4)
        )
        
        # Create the bassline in a new clip
        clip_creator.create_bassline(0, 0, notes, track_name=f"{params.get('root')} {params.get('scale_type', 'minor').title()} Bass")
    else:
        # Handle other commands using the controller directly
        if hasattr(controller, function_name):
            method = getattr(controller, function_name)
            method(**params)
        else:
            raise ValueError(f"Unknown command: {function_name}")

async def main():
    """Main entry point for the Ableton Control application."""
    logger = setup_logging()
    logger.info("Starting Ableton Control AI...")
    
    try:
        # Initialize components
        controller = AbletonController()
        clip_creator = ClipCreator(controller)
        processor = CommandProcessor()
        
        logger.info("Ready to process commands. Type 'exit' to quit.")
        while True:
            command = input("> ").strip()
            if command.lower() == 'exit':
                break
            
            try:
                await process_musical_command(command, controller, clip_creator, processor)
                logger.info(f"Successfully processed command: {command}")
            except Exception as e:
                logger.error(f"Error processing command: {e}")
                print(f"Error: {str(e)}")
            
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
    finally:
        logger.info("Ableton Control AI terminated.")

if __name__ == "__main__":
    asyncio.run(main()) 