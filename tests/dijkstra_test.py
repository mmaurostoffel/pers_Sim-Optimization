import pandas as pd
import tkinter as tk
from tkinter import filedialog


def selectInputFile():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()
    return file_path


def readInputList(file):
    input = pd.read_csv(file)
    input = input.replace(to_replace='x', value=0, regex=True)

    return input








file = selectInputFile()
out = readInputList(file)

print(out.to_numpy())