from tkinter import Tk, Label, Button
from tkinter import filedialog
import numpy as np
import os
import librosa
import matplotlib.pyplot as plt

# Diretório atual do script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Diretório raiz do projeto (subindo um nível)
ROOT_DIR = os.path.dirname(CURRENT_DIR)

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        frequencies = extract_frequencies(file_path)
        

def extract_frequencies(file_path):
    y, sr = librosa.load(file_path)
    stft_result = np.abs(librosa.stft(y))
    frequencies = librosa.fft_frequencies(sr=sr)
    dominant_frequencies = []
    for frame in stft_result.T:
        dominant_frequencies.append(int(frequencies[np.argmax(frame)]))
    print(dominant_frequencies)
    return dominant_frequencies

window = Tk()
window.title("Screen")
window.config(padx=50, pady=50)

window_label = Label(window, text="Insira seu Audio")
window_label.grid(row=0, column=0)
open_file_button = Button(window, text="Open File", command=open_file)
open_file_button.grid(row=0, column=1)
window.config(padx=50, pady=50)
window.mainloop()

