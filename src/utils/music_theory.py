from typing import List, Tuple
import random

class MusicTheory:
    # Note mappings (MIDI note numbers)
    NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    # Scale patterns (steps between notes)
    SCALE_PATTERNS = {
        'major': [2, 2, 1, 2, 2, 2, 1],
        'minor': [2, 1, 2, 2, 1, 2, 2],
        'harmonic_minor': [2, 1, 2, 2, 1, 3, 1],
        'melodic_minor': [2, 1, 2, 2, 2, 2, 1],
        'dorian': [2, 1, 2, 2, 2, 1, 2],
        'phrygian': [1, 2, 2, 2, 1, 2, 2],
        'lydian': [2, 2, 2, 1, 2, 2, 1],
        'mixolydian': [2, 2, 1, 2, 2, 1, 2],
    }
    
    # Common chord progressions
    PROGRESSIONS = {
        'minor': [
            [1, 4, 5, 1],  # i-iv-v-i
            [1, 6, 4, 5],  # i-VI-iv-v
            [1, 4, 7, 5],  # i-iv-VII-v
            [1, 6, 3, 7],  # i-VI-III-VII
        ]
    }
    
    # Bass patterns (relative to root note, in steps)
    BASS_PATTERNS = {
        'simple': [(0, 1.0)],  # Root note, full length
        'octave': [(0, 0.5), (12, 0.5)],  # Root and octave
        'walking': [(0, 0.25), (7, 0.25), (12, 0.25), (7, 0.25)],  # Walking bass
        'arpeggio': [(0, 0.25), (4, 0.25), (7, 0.25), (12, 0.25)],  # Arpeggio
    }
    
    @classmethod
    def get_note_number(cls, note: str, octave: int = 4) -> int:
        """Convert note name and octave to MIDI note number."""
        note = note.upper()
        base_note = cls.NOTES.index(note)
        return base_note + (octave + 1) * 12

    @classmethod
    def get_scale(cls, root: str, scale_type: str = 'minor', octave: int = 4) -> List[int]:
        """Get MIDI note numbers for a scale."""
        if scale_type not in cls.SCALE_PATTERNS:
            raise ValueError(f"Unknown scale type: {scale_type}")
        
        notes = []
        current_note = cls.get_note_number(root, octave)
        notes.append(current_note)
        
        for interval in cls.SCALE_PATTERNS[scale_type]:
            current_note += interval
            notes.append(current_note)
        
        return notes

    @classmethod
    def get_chord(cls, root_note: int, chord_type: str = 'minor') -> List[int]:
        """Get MIDI note numbers for a chord."""
        if chord_type == 'minor':
            return [root_note, root_note + 3, root_note + 7]
        elif chord_type == 'major':
            return [root_note, root_note + 4, root_note + 7]
        elif chord_type == 'diminished':
            return [root_note, root_note + 3, root_note + 6]
        elif chord_type == 'augmented':
            return [root_note, root_note + 4, root_note + 8]
        else:
            raise ValueError(f"Unknown chord type: {chord_type}")

    @classmethod
    def generate_bassline(cls, root: str, scale_type: str = 'minor', 
                         pattern: str = 'walking', length: int = 4) -> List[Tuple[int, float]]:
        """Generate a bassline pattern.
        
        Args:
            root: Root note (e.g., 'G')
            scale_type: Type of scale ('minor', 'major', etc.)
            pattern: Type of bass pattern
            length: Length in bars
            
        Returns:
            List of (MIDI note, duration) tuples
        """
        scale = cls.get_scale(root, scale_type)
        base_pattern = cls.BASS_PATTERNS.get(pattern, cls.BASS_PATTERNS['simple'])
        
        # Generate the full bassline by repeating and varying the pattern
        bassline = []
        for _ in range(length):
            # Add some variation every other bar
            if _ % 2 == 1:
                # Occasionally use a different scale degree as root
                root_note = random.choice(scale[:5])  # Use first 5 notes of scale
                current_pattern = [(note + (root_note - scale[0]), dur) 
                                 for note, dur in base_pattern]
            else:
                current_pattern = base_pattern
            
            bassline.extend(current_pattern)
        
        return bassline 