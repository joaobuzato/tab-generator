from tkinter import Tk, Label, Button
from tkinter import filedialog
import numpy as np
import os
import librosa
from scipy.signal import find_peaks, medfilt
import csv

# Diretório atual do script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretório raiz do projeto (subindo um nível)
ROOT_DIR = os.path.dirname(CURRENT_DIR)

def read_frequencies():
    file_path = f"{ROOT_DIR}/frequencies.csv"
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convertendo os valores de FrequencyMin e FrequencyMax para float
            row['FrequencyMin'] = float(row['FrequencyMin'])
            row['FrequencyMax'] = float(row['FrequencyMax'])
            data.append(row)
    return data

FREQUENCIES = read_frequencies()

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        frequencies = extract_frequencies(file_path)
        print(frequencies)

def frequency_to_note(frequency):
    for note_freq in FREQUENCIES:
        if frequency >= note_freq["FrequencyMin"] and frequency <= note_freq['FrequencyMax']: 
            return { "note": note_freq['Note'], "octave":note_freq['Octave'] }

    return None



def extract_frequencies(file_path):
    y, sr = librosa.load(file_path)
    # Remoção de ruído
    y = librosa.effects.remix(y, intervals=librosa.effects.split(y, top_db=20))
    
    # PEGAR O TEMPO DA FAIXA DE AUDIO 
    # Calcular o hop_length baseado no tempo da faixa de audio

    # STFT
    stft_result = np.abs(librosa.stft(y, hop_length=1000))
    frequencies = librosa.fft_frequencies(sr=sr)

    peak_frequencies = []
    for frame in stft_result.T:
        peaks, _ = find_peaks(frame, height=4, threshold=4, prominence=2, width=2)
        peak_frequencies.extend(frequencies[peaks])

   # Suavização das frequências dominantes
    peak_frequencies = medfilt(peak_frequencies, kernel_size=5)

    notes = []
    for freq in peak_frequencies:
        print(freq)
        print(frequency_to_note(round(freq,4)))
        notes.append(frequency_to_note(round(freq,4)))

    
    print(notes)
    return notes


# extract_frequencies(f"{ROOT_DIR}/D#DG#G.mp3")
# window = Tk()
# window.title("Screen")
# window.config(padx=50, pady=50)

# window_label = Label(window, text="Insira seu Audio")
# window_label.grid(row=0, column=0)
# open_file_button = Button(window, text="Open File", command=open_file)
# open_file_button.grid(row=0, column=1)
# window.config(padx=50, pady=50)
# window.mainloop()

