import logging
from typing import List, Tuple, Optional
from .controller import AbletonController

logger = logging.getLogger(__name__)

class ClipCreator:
    """Handle MIDI clip creation and manipulation in Ableton Live."""
    
    def __init__(self, controller: AbletonController):
        """Initialize the clip creator."""
        self.controller = controller
    
    def ensure_midi_track(self, track_index: int, name: str = None) -> None:
        """Ensure a MIDI track exists at the given index."""
        try:
            # Create a new MIDI track
            self.controller.create_midi_track()
            
            # Set track name if provided
            if name:
                self.controller.set_track_name(track_index, name)
                
            logger.info(f"Created MIDI track at index {track_index}")
        except Exception as e:
            logger.warning(f"Could not create MIDI track: {e}")
    
    def create_midi_clip(self, track: int, clip: int, length: float) -> None:
        """Create a new MIDI clip."""
        try:
            self.controller.create_clip(track, clip, length)
            logger.info(f"Created MIDI clip at track {track}, slot {clip}")
        except Exception as e:
            if "already has a clip" in str(e):
                # Clear existing clip instead
                self.clear_clip(track, clip)
                # Try creating again
                self.controller.create_clip(track, clip, length)
            else:
                raise
    
    def add_midi_note(self, track: int, clip: int, note: int, 
                      start_time: float, duration: float, velocity: int = 100) -> None:
        """Add a MIDI note to a clip."""
        try:
            self.controller.add_clip_note(track, clip, note, start_time, duration, velocity)
        except Exception as e:
            logger.error(f"Error adding MIDI note: {e}")
            raise
    
    def clear_clip(self, track: int, clip: int) -> None:
        """Clear all notes from a MIDI clip."""
        self.controller.clear_clip(track, clip)
    
    def create_bassline(self, track: int, clip: int, notes: List[Tuple[int, float]], 
                       velocity: int = 100, track_name: str = "Bass") -> None:
        """Create a bassline in a MIDI clip."""
        try:
            # Ensure we have a MIDI track
            self.ensure_midi_track(track, track_name)
            
            # Calculate total length
            total_length = sum(duration for _, duration in notes)
            
            # Create or clear the clip
            try:
                self.create_midi_clip(track, clip, total_length)
            except Exception:
                logger.warning("Could not create clip, attempting to clear existing one")
                self.clear_clip(track, clip)
            
            # Add notes
            current_time = 0.0
            for note, duration in notes:
                try:
                    self.add_midi_note(track, clip, note, current_time, duration, velocity)
                    current_time += duration
                except Exception as e:
                    logger.error(f"Error adding note {note} at time {current_time}: {e}")
            
            # Trigger the clip
            self.controller.trigger_clip(track, clip)
            
        except Exception as e:
            logger.error(f"Error creating bassline: {e}")
            raise 