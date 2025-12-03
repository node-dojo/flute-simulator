#!/usr/bin/env python3
"""
Generate an A4 note (440 Hz) as a WAV file
"""

import numpy as np
import wave
import struct

# A4 note specifications
frequency = 440.0  # Hz (A4)
duration = 2.0    # seconds
sample_rate = 44100  # samples per second

# Generate time array
t = np.linspace(0, duration, int(sample_rate * duration), False)

# Generate sine wave for A4
waveform = np.sin(2 * np.pi * frequency * t)

# Apply a gentle envelope to avoid clicks (fade in/out)
fade_samples = int(0.05 * sample_rate)  # 50ms fade
envelope = np.ones(len(waveform))
envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
waveform = waveform * envelope

# Normalize to 16-bit integer range
waveform = waveform * 0.5  # Reduce amplitude to avoid clipping
waveform_int = np.int16(waveform * 32767)

# Save as WAV file
filename = "A4_note.wav"
with wave.open(filename, 'w') as wav_file:
    wav_file.setnchannels(1)  # Mono
    wav_file.setsampwidth(2)   # 16-bit
    wav_file.setframerate(sample_rate)
    
    for sample in waveform_int:
        wav_file.writeframes(struct.pack('<h', sample))

print(f"Generated A4 note ({frequency} Hz)")
print(f"Duration: {duration} seconds")
print(f"Saved to: {filename}")
print(f"\nYou can play this file to hear what A4 sounds like.")

