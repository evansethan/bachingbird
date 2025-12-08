# Bachingbird

![Bachingbird Logo](./logo.jpg)

Bachingbird is a web application that uses a deep learning model to generate musical chorales in the style of Johann Sebastian Bach. It provides a simple interface to compose new, original pieces of music with the click of a button.

## Features

- **AI-Powered Music Generation**: Utilizes a custom Dual LSTM neural network (one for pitch, one for duration) trained on Bach's chorales to produce authentic-sounding music.
- **Interactive Web Interface**: Built with Streamlit, the app offers a simple and intuitive user experience.
- **Music Visualization**: Features an embedded MIDI player with a piano-roll visualizer to see and hear the generated music in real-time.
- **MIDI Export**: Allows you to download the generated chorales as standard MIDI (.mid) files for use in other music software.
- **Organ Timbre**: The generated music is set to a Church Organ instrument, mimicking the sound of Bach's era.

## How It Works

The application uses a pre-trained PyTorch model (`DualMusicLSTM`) loaded from `data/model.pkl`. This model was trained on a processed dataset of Bach's chorales (`data/processed_midi.pkl`).

When a user clicks "Generate New Chorale":
1.  A random seed sequence is selected from the original dataset.
2.  The model iteratively predicts the next pitch and duration using nucleus sampling to create a new musical sequence.
3.  The `music21` library assembles this sequence into a complete musical score.
4.  The score is converted into a MIDI file, which is then presented to the user for playback and download.

## Getting Started

Follow these instructions to run Bachingbird on your local machine.

### Prerequisites

- Python 3.8+
- `pip`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/bachingbird.git
    cd bachingbird
    ```

2.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Launch the Streamlit app:**
    ```bash
    streamlit run app.py
    ```

2.  **Open your web browser:**
    Navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

3.  **Generate Music:**
    Click the "Generate New Chorale" button to compose your first piece!

## Project Structure

```
.
├── app.py                  # The main Streamlit web application
├── helpers.py              # Contains the PyTorch model definition (DualMusicLSTM)
├── requirements.txt        # Python package dependencies
├── data/
│   ├── model.pkl           # Pre-trained PyTorch model
│   └── processed_midi.pkl  # Processed MIDI data used for training and seeding
└── logo.jpg                # Project logo
```
