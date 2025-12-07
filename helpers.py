import os
import glob
import music21
import torch
import torch.nn as nn
import torch.nn.functional as F # Added F to simplify calls

DROPOUT = 0.5   

# --- DUAL EMBEDDING MODEL ---
class DualMusicLSTM(nn.Module):
    def __init__(self, n_pitch, n_dur, embed_pitch, embed_dur, hidden_size, num_layers):
        super(DualMusicLSTM, self).__init__()
        
        # Two Embedding Layers
        self.emb_pitch = nn.Embedding(n_pitch, embed_pitch)
        self.emb_dur = nn.Embedding(n_dur, embed_dur)
        
        # LSTM input size is the sum of both embeddings
        lstm_input_size = embed_pitch + embed_dur
        
        self.lstm = nn.LSTM(lstm_input_size, hidden_size, num_layers, batch_first=True, dropout=DROPOUT)
        
        # Two Output Heads
        self.pitch_head = nn.Linear(hidden_size, n_pitch)
        self.dur_head = nn.Linear(hidden_size, n_dur)

    def forward(self, x_p, x_d):
        e_p = self.emb_pitch(x_p)
        e_d = self.emb_dur(x_d)
        
        x = torch.cat((e_p, e_d), dim=2)
        
        lstm_out, _ = self.lstm(x)
        
        last_out = lstm_out[:, -1, :]
        
        out_pitch = self.pitch_head(last_out)
        out_dur = self.dur_head(last_out)
        
        return out_pitch, out_dur