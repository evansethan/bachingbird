#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Downloading model.pkl from Dropbox..."
# REPLACE THE URL BELOW with your specific Dropbox link ending in dl=1
curl -L "https://www.dropbox.com/scl/fi/foy2yhb65vwti497mchjy/model.pkl?rlkey=lnfg8zhktq44mhe8h98zg6bxm&st=vo5wln3c&dl=1" -o model.pkl

echo "Build finished!"