
import wave
import math
import struct
import os
import random

def generate_tone(filename, frequency, duration=0.05, volume=1.0):
    sample_rate = 44100
    n_samples = int(duration * sample_rate)
    
    os.makedirs("assets/sounds", exist_ok=True)
    
    wave_file = wave.open(filename, 'w')
    wave_file.setnchannels(1) # mono
    wave_file.setsampwidth(2) # 2 bytes per sample
    wave_file.setframerate(sample_rate)
    
    for i in range(n_samples):
        # Time point
        t = float(i) / sample_rate
        
        # Envelope: very fast attack, exponential decay
        decay_rate = 50.0 
        envelope = math.exp(-decay_rate * t)
        
        # Sine wave
        sample_val = math.sin(2 * math.pi * frequency * t)
        
        # Apply envelope and volume
        value = int(32767.0 * volume * envelope * sample_val)
        
        # Clip to 16-bit range just in case
        value = max(-32768, min(32767, value))
        
        data = struct.pack('<h', value)
        wave_file.writeframesraw(data)
        
    wave_file.close()

if __name__ == "__main__":
    # Generate "High Tick" (First beat) - Higher pitch, sharper
    generate_tone("assets/sounds/high.wav", 1200.0, 0.05)
    
    # Generate "Low Tick" (Other beats) - Lower pitch, hollower
    generate_tone("assets/sounds/low.wav", 800.0, 0.05)
    
    print("Generated assets/sounds/high.wav and assets/sounds/low.wav")
