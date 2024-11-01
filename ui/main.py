from tkinter import Tk, Label, Button
from tkinter import filedialog
import numpy as np
import os
import librosa
from scipy.signal import medfilt

# Diretório atual do script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretório raiz do projeto (subindo um nível)
ROOT_DIR = os.path.dirname(CURRENT_DIR)

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        frequencies = extract_frequencies(file_path)
        print(frequencies);

def frequency_to_midi(frequency):
    if frequency <= 0:
        return float('inf')
    return 69 + 12 * np.log2(frequency / 440.0)

def midi_to_note_name(midi_note):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (midi_note // 12) - 1
    note = note_names[midi_note % 12]
    return f"{note}{octave}"

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
    stft_result = np.abs(librosa.stft(y, hop_length=12000))
    frequencies = librosa.fft_frequencies(sr=sr)

    dominant_frequencies = []
    for frame in stft_result.T:
        dominant_frequencies.append(float(frequencies[np.argmax(frame)]))

    # Suavização das frequências dominantes
    dominant_frequencies = medfilt(dominant_frequencies, kernel_size=3)

    notes = [frequency_to_note_name(freq) for freq in dominant_frequencies]
    return notes

window = Tk()
window.title("Screen")
window.config(padx=50, pady=50)

window_label = Label(window, text="Insira seu Audio")
window_label.grid(row=0, column=0)
open_file_button = Button(window, text="Open File", command=open_file)
open_file_button.grid(row=0, column=1)
window.config(padx=50, pady=50)
window.mainloop()

