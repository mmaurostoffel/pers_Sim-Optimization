import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np

TIME_PER_STEP = 0.3


def percentOutside(data):
    history = data['history']
    times = [entry['time'] * TIME_PER_STEP / 60 for entry in history]
    peopleOnField = list([entry['numPeopleOnField'] for entry in history])
    plt.plot(times, peopleOnField)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    # Open the file picker dialog
    for i in range(5):
        file_path = filedialog.askopenfilename(title="Select a file")
        file = np.load(file_path, allow_pickle=True).item()

        percentOutside(file)
    plt.legend(["10%", "25%", "50%", "75%", "90%", ])
    plt.title("Anzahl Personen auf dem Simulationsgebiet über die Zeit")
    plt.xlabel('Zeit ins Simulations-Iterationen')
    plt.ylabel('Anzahl Personen auf dem Simulationsgebiet')
    plt.show()
