import time
import threading
import pygame
import os
from PyQt6.QtCore import QObject, pyqtSignal

class Metronome(QObject):
    beat_signal = pyqtSignal(int)  # Signal emitted on every beat (current_beat)
    kp_ready = False

    def __init__(self):
        super().__init__()
        self.bpm = 120
        self.playing = False
        self.time_signature = 4  # 4 beats per bar
        self.current_beat = 0
        self._stop_event = threading.Event()
        self._thread = None
        
        # Initialize mixer
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        # Load sounds
        self.sound_high = None
        self.sound_low = None
        try:
            high_path = "assets/sounds/high.wav"
            low_path = "assets/sounds/low.wav"
            if os.path.exists(high_path) and os.path.exists(low_path):
                self.sound_high = pygame.mixer.Sound(high_path)
                self.sound_low = pygame.mixer.Sound(low_path)
                self.kp_ready = True
            else:
                print("Warning: sound files not found")
        except Exception as e:
            print(f"Error loading sounds: {e}")

    def _generate_beep(self):
        """Generates a simple square wave beep for the metronome click."""
        # Simple square wave generation
        frequency = 1000  # Hz
        duration = 0.05   # seconds
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        
        # Generate raw 16-bit PCM data
        # This is a bit low-level, but ensures we have *something* to play without external files.
        # However, for better quality, we usually wan't to load a file.
        # Let's try to simulate a simple sound object if possible or just warn.
        # Actually, pygame.sndarray (numpy) is good but requires numpy. 
        # Let's rely on a file placeholder or silent fallback for now to be safe, 
        # but the plan mentioned 'click.wav'.
        # For this step, I'll return None and handle it in play_click.
        return None

    def load_sound(self, file_path):
        try:
            self.sound = pygame.mixer.Sound(file_path)
            self.kp_ready = True
        except Exception as e:
            print(f"Error loading sound: {e}")
            self.kp_ready = False

    def set_bpm(self, bpm):
        self.bpm = bpm

    def set_time_signature(self, signature):
        self.time_signature = signature

    def start(self):
        if self.playing:
            return
        self.playing = True
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run)
        self._thread.start()

    def stop(self):
        if not self.playing:
            return
        self.playing = False
        self._stop_event.set()
        if self._thread:
            self._thread.join()
        self.current_beat = 0

    def _run(self):
        # Precise timing logic
        next_beat_time = time.perf_counter()
        while not self._stop_event.is_set():
            current_time = time.perf_counter()
            if current_time >= next_beat_time:
                self.beat_signal.emit(self.current_beat + 1)
                
                # Determine which sound to play
                is_downbeat = (self.current_beat == 0)
                self.play_click(is_downbeat)
                
                self.current_beat = (self.current_beat + 1) % self.time_signature
                
                # Calculate next beat time
                # 60 / BPM = seconds per beat
                interval = 60.0 / self.bpm
                next_beat_time += interval
                
                # Small sleep to prevent CPU hogging, but short enough to be precise
                sleep_time = next_beat_time - time.perf_counter()
                if sleep_time > 0:
                    time.sleep(sleep_time)
            else:
                 # Sleep a tiny bit to avoid busy waiting too much
                 time.sleep(0.001)

    def play_click(self, is_accent):
        if is_accent and self.sound_high:
            self.sound_high.play()
        elif not is_accent and self.sound_low:
            self.sound_low.play()
