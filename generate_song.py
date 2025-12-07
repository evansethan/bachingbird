import os
import sys
import torch
import torch.nn as nn
import numpy as np
import pickle
from fractions import Fraction
import music21
from helpers import nucleus_sample, DualMusicLSTM

# --- CONFIGURATION ---
MODEL_FILE = "output/oldmodel.pkl"
CACHE_FILE = "output/processed_midi.pkl"
OUTPUT_FILE = "output/output.mid"

# Generation Settings
NUM_NOTES = 64            # Length of song
TEMPERATURE_PITCH = 1.0   # Higher (1.2) = More creative/risky
TEMPERATURE_DUR = 1.1      # Higher (1.0) = Less repetitive rhythm
TOP_P = 0.9               # Nucleus sampling threshold
SEQUENCE_LENGTH = 128

def nucleus_sample(prediction, top_p):
    """Samples from the probability distribution using Nucleus Sampling."""
    probs = torch.nn.functional.softmax(prediction, dim=1).squeeze()
    sorted_probs, sorted_indices = torch.sort(probs, descending=True)
    cumulative_probs = torch.cumsum(sorted_probs, dim=0)
    
    sorted_indices_to_remove = cumulative_probs > top_p
    sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
    sorted_indices_to_remove[..., 0] = 0
    
    indices_to_remove = sorted_indices[sorted_indices_to_remove]
    probs[indices_to_remove] = 0
    probs = probs / probs.sum()
    return torch.multinomial(probs, 1).item()

# --- 2. SETUP & LOAD ---

# Detect Device
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"🚀 Using Device: {device.type.upper()}")

# Load Processed Data (Vocabularies)
if not os.path.exists(CACHE_FILE):
    raise FileNotFoundError(f"Error: {CACHE_FILE} not found. Run the training script first!")
with open(CACHE_FILE, 'rb') as f:
    data = pickle.load(f)
    int_to_pitch = data['int_to_pitch']
    int_to_dur = data['int_to_dur']
    # We need the original sequences to seed the generation
    input_pitches = data['pitches'] 
    input_durs = data['durs']
    pitch_to_int = data['pitch_to_int'] # Needed for sequence conversion
    dur_to_int = data['dur_to_int']

# Load Model
if not os.path.exists(MODEL_FILE):
    raise FileNotFoundError(f"Error: {MODEL_FILE} not found. Train the model first!")
print(f"✅ Loading model from {MODEL_FILE}...")
with open(MODEL_FILE, 'rb') as f:
    model = pickle.load(f)
model.to(device)
model.eval()

# --- 3. GENERATION ---
print("🎹 Starting generation...")

# Create a sequence of IDs to seed the generation
all_pitch_ids = [pitch_to_int[p] for p in input_pitches if p in pitch_to_int]
all_dur_ids = [dur_to_int[d] for d in input_durs if d in dur_to_int]

# Start with a random slice of the training data
start_idx = np.random.randint(0, len(all_pitch_ids) - SEQUENCE_LENGTH - 1)
curr_p_seq = all_pitch_ids[start_idx : start_idx + SEQUENCE_LENGTH]
curr_d_seq = all_dur_ids[start_idx : start_idx + SEQUENCE_LENGTH]

generated_pitches = []
generated_durs = []

for i in range(NUM_NOTES):
    t_p = torch.tensor([curr_p_seq], dtype=torch.long).to(device)
    t_d = torch.tensor([curr_d_seq], dtype=torch.long).to(device)
    
    with torch.no_grad():
        pred_p, pred_d = model(t_p, t_d)
    
    # Apply Temperature
    pred_p = pred_p / TEMPERATURE_PITCH
    pred_d = pred_d / TEMPERATURE_DUR
    
    # Sample new tokens
    idx_p = nucleus_sample(pred_p, top_p=TOP_P)
    idx_d = nucleus_sample(pred_d, top_p=TOP_P)
    
    # Convert back to human-readable format
    generated_pitches.append(int_to_pitch[idx_p])
    generated_durs.append(int_to_dur[idx_d])
    
    # Update sequence for the next prediction step
    curr_p_seq.append(idx_p)
    curr_d_seq.append(idx_d)
    curr_p_seq = curr_p_seq[1:]
    curr_d_seq = curr_d_seq[1:]

# --- 4. RECONSTRUCT & SAVE MIDI ---
output_stream = music21.stream.Stream()
print("🎵 Converting tokens to MIDI...")

for p, d in zip(generated_pitches, generated_durs):
    try:
        # Handle fractional durations
        dur_val = float(Fraction(d)) if '/' in d else float(d)
            
        if '.' in p: # Chord
            el = music21.chord.Chord(p.split('.'))
        else: # Note
            el = music21.note.Note(p)
            
        el.duration.quarterLength = dur_val
        output_stream.append(el)
    except Exception as e:
        pass # Silently skip invalid tokens

output_stream.write('midi', fp=OUTPUT_FILE)
print(f"✅ Success! Generated music saved to {OUTPUT_FILE}")