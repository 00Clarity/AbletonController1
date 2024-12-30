import re
from typing import Union, Optional

def normalize_value(value: float, min_val: float, max_val: float) -> float:
    """Normalize a value to fit within a given range.
    
    Args:
        value: The value to normalize
        min_val: Minimum allowed value
        max_val: Maximum allowed value
    
    Returns:
        Normalized value within the specified range
    """
    return max(min_val, min(max_val, value))

def parse_track_number(track_str: str) -> Optional[int]:
    """Parse a track number from a string.
    
    Args:
        track_str: String containing track number (e.g., "track 1", "1")
    
    Returns:
        Track number as integer (0-based) or None if not found
    """
    # Try to extract number from string
    match = re.search(r'\d+', track_str)
    if match:
        # Convert to 0-based index
        return int(match.group()) - 1
    return None

def parse_clip_number(clip_str: str) -> Optional[int]:
    """Parse a clip number from a string.
    
    Args:
        clip_str: String containing clip number (e.g., "clip 1", "1")
    
    Returns:
        Clip number as integer (0-based) or None if not found
    """
    # Try to extract number from string
    match = re.search(r'\d+', clip_str)
    if match:
        # Convert to 0-based index
        return int(match.group()) - 1
    return None

def parse_volume(volume_str: str) -> Optional[float]:
    """Parse a volume value from a string.
    
    Args:
        volume_str: String containing volume value (e.g., "50%", "0.5")
    
    Returns:
        Volume as float (0.0 to 1.0) or None if not found
    """
    # Remove % sign if present
    volume_str = volume_str.replace('%', '')
    
    try:
        value = float(volume_str)
        # If value is between 0-100, assume it's a percentage
        if 0 <= value <= 100:
            value = value / 100
        return normalize_value(value, 0.0, 1.0)
    except ValueError:
        return None

def parse_pan(pan_str: str) -> Optional[float]:
    """Parse a pan value from a string.
    
    Args:
        pan_str: String containing pan value (e.g., "left", "right", "-50", "0.5")
    
    Returns:
        Pan as float (-1.0 to 1.0) or None if not found
    """
    # Handle text-based pan positions
    if 'left' in pan_str.lower():
        return -1.0
    if 'right' in pan_str.lower():
        return 1.0
    if 'center' in pan_str.lower() or 'middle' in pan_str.lower():
        return 0.0
    
    try:
        value = float(pan_str)
        # If value is between -100 and 100, assume it's a percentage
        if -100 <= value <= 100:
            value = value / 100
        return normalize_value(value, -1.0, 1.0)
    except ValueError:
        return None

def parse_tempo(tempo_str: str) -> Optional[float]:
    """Parse a tempo value from a string.
    
    Args:
        tempo_str: String containing tempo value (e.g., "120 bpm", "120")
    
    Returns:
        Tempo as float or None if not found
    """
    # Remove 'bpm' if present
    tempo_str = tempo_str.lower().replace('bpm', '').strip()
    
    try:
        value = float(tempo_str)
        return normalize_value(value, 20.0, 999.0)  # Ableton's tempo range
    except ValueError:
        return None 