from tkinter import Tk, Label, Button
from tkinter import filedialog
import numpy as np
import os
import librosa
from scipy.signal import find_peaks, medfilt

# Diretório atual do script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretório raiz do projeto (subindo um nível)
ROOT_DIR = os.path.dirname(CURRENT_DIR)

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        frequencies = extract_frequencies(file_path)
        print(frequencies)

def midi_to_note_name(midi_note):
    print(f"MIDI NOTE {midi_note}")
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_note // 12) - 1
    note = note_names[midi_note % 12]
    return f"{note}{octave}"


def frequency_to_midi(frequency):
    if frequency <= 0:
        return float('inf')
    return (12 * np.log2(frequency / 440.0)) + 69


def frequency_to_note_name(frequency):
    midi_note = frequency_to_midi(frequency)
    if midi_note == float('inf'):
        return "Invalid frequency"
    return midi_to_note_name(round(midi_note))

def extract_frequencies(file_path):
    y, sr = librosa.load(file_path)
    # Remoção de ruído
    y = librosa.effects.remix(y, intervals=librosa.effects.split(y, top_db=20))
    
    # STFT
    stft_result = np.abs(librosa.stft(y, hop_length=4096))
    frequencies = librosa.fft_frequencies(sr=sr)

    peak_frequencies = []
    for frame in stft_result.T:
        peaks, _ = find_peaks(frame, height=4, threshold=5, prominence=1)
        peak_frequencies.extend(frequencies[peaks])

   # Suavização das frequências dominantes
    peak_frequencies = medfilt(peak_frequencies, kernel_size=3)

    midi_notes = [frequency_to_note_name(freq) for freq in peak_frequencies]
    print(midi_notes)
    return midi_notes


extract_frequencies(f"{ROOT_DIR}/ADEA.mp3")
# window = Tk()
# window.title("Screen")
# window.config(padx=50, pady=50)

# window_label = Label(window, text="Insira seu Audio")
# window_label.grid(row=0, column=0)
# open_file_button = Button(window, text="Open File", command=open_file)
# open_file_button.grid(row=0, column=1)
# window.config(padx=50, pady=50)
# window.mainloop()

