import logging
import socket
from pythonosc import udp_client
from pythonosc import osc_message_builder

logger = logging.getLogger(__name__)

class AbletonController:
    """Control Ableton Live via OSC."""
    
    def __init__(self, host="127.0.0.1", port=11000):
        """Initialize the controller."""
        self.client = udp_client.SimpleUDPClient(host, port)
        logger.info(f"Initialized Ableton controller on {host}:{port}")
        # Send test message to verify connection
        self.test_connection()
    
    def test_connection(self):
        """Test the connection to Ableton Live."""
        try:
            self.send_command("/live/test")
            logger.info("Successfully connected to Ableton Live")
        except Exception as e:
            logger.error(f"Could not connect to Ableton Live: {e}")
            raise
    
    def send_command(self, address, *args):
        """Send an OSC command to Ableton Live."""
        try:
            logger.debug(f"Sent command: {address} {args}")
            self.client.send_message(address, args if args else None)
        except Exception as e:
            logger.error(f"Error sending command: {e}")
            raise
    
    def create_midi_track(self):
        """Create a new MIDI track."""
        self.send_command("/live/song/create_midi_track", -1)  # -1 = end of list
    
    def set_track_name(self, track_index: int, name: str):
        """Set track name."""
        self.send_command("/live/track/set/name", track_index, name)
    
    def create_clip(self, track: int, clip: int, length: float):
        """Create a new MIDI clip."""
        self.send_command("/live/clip_slot/create_clip", track, clip, length)
    
    def add_clip_note(self, track: int, clip: int, note: int, 
                     start_time: float, duration: float, velocity: int = 100):
        """Add a MIDI note to a clip."""
        self.send_command("/live/clip/add/notes", track, clip, note, start_time, duration, velocity, 0)  # Last 0 is for mute=False
    
    def clear_clip(self, track: int, clip: int):
        """Clear all notes from a MIDI clip."""
        self.send_command("/live/clip/remove/notes", track, clip)
    
    def trigger_clip(self, track: int, clip: int):
        """Trigger a clip to play."""
        self.send_command("/live/clip/fire", track, clip)
    
    def stop_clip(self, track: int, clip: int):
        """Stop a clip."""
        self.send_command("/live/clip/stop", track, clip)
    
    def set_tempo(self, bpm: float):
        """Set the song tempo."""
        self.send_command("/live/song/set/tempo", bpm)
    
    def start_playback(self):
        """Start session playback."""
        self.send_command("/live/song/start_playing")
    
    def stop_playback(self):
        """Stop session playback."""
        self.send_command("/live/song/stop_playing")
    
    def set_track_volume(self, track: int, volume: float):
        """Set track volume (0.0 to 1.0)."""
        self.send_command("/live/track/set/volume", track, volume)
    
    def set_track_pan(self, track: int, pan: float):
        """Set track panning (-1.0 to 1.0)."""
        self.send_command("/live/track/set/panning", track, pan)
    
    def mute_track(self, track: int):
        """Mute a track."""
        self.send_command("/live/track/set/mute", track, 1)
    
    def unmute_track(self, track: int):
        """Unmute a track."""
        self.send_command("/live/track/set/mute", track, 0)
    
    def solo_track(self, track: int):
        """Solo a track."""
        self.send_command("/live/track/set/solo", track, 1)
    
    def unsolo_track(self, track: int):
        """Unsolo a track."""
        self.send_command("/live/track/set/solo", track, 0) 