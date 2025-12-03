#!/usr/bin/env python3
"""
Calculate base note range for a 200mm total length flute
with 20-30mm inner diameter
"""

import math

# Constants
c = 343.0  # Speed of sound in m/s at 20°C
total_length = 0.200  # 200mm in meters

# Diameter range
diameters = [0.020, 0.030]  # 20mm and 30mm

# Bore length range (accounting for slow air chamber ~30-50mm and block ~10mm)
# Conservative: 200 - 50 - 10 = 140mm
# Optimistic: 200 - 30 - 10 = 160mm
bore_lengths = [0.140, 0.150, 0.160]  # 140mm, 150mm, 160mm

# Musical note frequencies (4th octave for reference)
note_frequencies = {
    'C4': 261.63,
    'C#4': 277.18,
    'D4': 293.66,
    'D#4': 311.13,
    'E4': 329.63,
    'F4': 349.23,
    'F#4': 369.99,
    'G4': 392.00,
    'G#4': 415.30,
    'A4': 440.00,
    'A#4': 466.16,
    'B4': 493.88,
    'C5': 523.25,
    'C#5': 554.37,
    'D5': 587.33,
    'D#5': 622.25,
    'E5': 659.25,
    'F5': 698.46,
    'F#5': 739.99,
    'G5': 783.99,
    'G#5': 830.61,
    'A5': 880.00,
}

def find_closest_note(freq):
    """Find the closest musical note to a given frequency"""
    closest_note = None
    min_diff = float('inf')
    
    for note, note_freq in note_frequencies.items():
        diff = abs(freq - note_freq)
        if diff < min_diff:
            min_diff = diff
            closest_note = note
    
    # Calculate cents difference
    cents = 1200 * math.log2(freq / note_frequencies[closest_note])
    return closest_note, cents

def calculate_k1(D, L):
    """Calculate K1 end correction factor"""
    if L == 0:
        return 0.3
    return 0.3 + 0.2 * math.sqrt(D / L)

def calculate_k2(D, L):
    """Calculate K2 end correction factor"""
    if L == 0:
        return 0.6
    return 0.6 + 0.1 * math.sqrt(D / L)

def calculate_fundamental_frequency(D, L):
    """Calculate fundamental frequency for given diameter and bore length"""
    # Calculate end correction factors
    K1 = calculate_k1(D, L)
    K2 = calculate_k2(D, L)
    
    # Calculate end corrections
    delta_L1 = K1 * D
    delta_L2 = K2 * D
    total_delta_L = delta_L1 + delta_L2
    
    # Calculate effective length
    Leff = L + total_delta_L
    
    # Calculate fundamental frequency
    f0 = c / (4 * Leff)
    
    return f0, Leff, K1, K2, total_delta_L

print("=" * 80)
print("BASE NOTE RANGE CALCULATION FOR 200MM TOTAL LENGTH FLUTE")
print("=" * 80)
print(f"\nTotal Length: {total_length*1000:.0f} mm")
print(f"Speed of Sound: {c} m/s (at 20°C)")
print("\n" + "=" * 80)

results = []

for D in diameters:
    print(f"\n{'='*80}")
    print(f"INNER DIAMETER: {D*1000:.0f} mm ({D*1000/25.4:.2f} inches)")
    print(f"{'='*80}\n")
    
    for L in bore_lengths:
        f0, Leff, K1, K2, delta_L = calculate_fundamental_frequency(D, L)
        note, cents = find_closest_note(f0)
        
        # Calculate allocated space
        slow_air_chamber = total_length - L - 0.010  # Assuming 10mm for block
        
        print(f"Bore Length: {L*1000:.0f} mm")
        print(f"  Slow Air Chamber: ~{slow_air_chamber*1000:.0f} mm")
        print(f"  K1: {K1:.3f}, K2: {K2:.3f}")
        print(f"  End Correction: {delta_L*1000:.2f} mm")
        print(f"  Effective Length: {Leff*1000:.2f} mm")
        print(f"  Fundamental Frequency: {f0:.2f} Hz")
        print(f"  Closest Note: {note} ({cents:+.1f} cents)")
        print()
        
        results.append({
            'diameter_mm': D*1000,
            'bore_length_mm': L*1000,
            'frequency': f0,
            'note': note,
            'cents': cents
        })

print("=" * 80)
print("SUMMARY: BASE NOTE RANGE")
print("=" * 80)

# Find min and max frequencies
frequencies = [r['frequency'] for r in results]
min_freq = min(frequencies)
max_freq = max(frequencies)

min_note, min_cents = find_closest_note(min_freq)
max_note, max_cents = find_closest_note(max_freq)

print(f"\nMinimum Base Note: {min_freq:.2f} Hz → {min_note} ({min_cents:+.1f} cents)")
print(f"Maximum Base Note: {max_freq:.2f} Hz → {max_note} ({max_cents:+.1f} cents)")

print(f"\nNote Range: Approximately {min_note} to {max_note}")

# Show best configurations
print("\n" + "=" * 80)
print("RECOMMENDED CONFIGURATIONS")
print("=" * 80)

# Sort by frequency
results_sorted = sorted(results, key=lambda x: x['frequency'])

print("\nLowest Note (20mm diameter, 160mm bore):")
lowest = results_sorted[0]
print(f"  {lowest['note']} at {lowest['frequency']:.2f} Hz")

print("\nHighest Note (30mm diameter, 140mm bore):")
highest = results_sorted[-1]
print(f"  {highest['note']} at {highest['frequency']:.2f} Hz")

print("\n" + "=" * 80)

