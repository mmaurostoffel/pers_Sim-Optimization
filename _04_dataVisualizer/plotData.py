import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np

TIME_PER_STEP = 0.3

def showFinalData(data):
    meta = data['metadata']
    stationList = meta['stationList']
    stationNames = [station['pname'] for station in stationList]
    stationTimes = [station['serv_time'] for station in stationList]
    sumStationTimes = sum(stationTimes)
    fullTime = meta['fullTime']
    stationOrder = meta['stationOrder']

    history = data['history']
    # Extract time and station wait times
    times = [entry['time'] * TIME_PER_STEP / 60 for entry in history]
    station_waits = list(zip(*[[wait * TIME_PER_STEP / 60 for wait in entry['stationWaitTimes']] for entry in history]))
    queueLengths = list(zip(*[entry['stationQueueLength'] for entry in history]))
    peopleOnField = list([entry['numPeopleOnField'] for entry in history])
    stack_data = list(queueLengths) + [peopleOnField]
    all_labels = stationNames + ['Im Freien']

    # Create a figure with two subplots (stacked vertically)
    fig, axs = plt.subplots(2, 1, figsize=(12, 10))

    # First subplot: Line plot for each station's wait times
    for i, wait_times in enumerate(station_waits):
        axs[0].plot(times, wait_times, label=f'{stationNames[i]}')
    axs[0].set_xlabel('Zeit [min]')
    axs[0].set_ylabel('Wartezeit [min]')
    axs[0].set_title('Stationen Wartezeiten über die Zeit')
    axs[0].legend(loc='upper right', ncol=2)
    axs[0].grid(True)

    # Second subplot: Stack plot for queue lengths
    axs[1].stackplot(times, *stack_data, labels=all_labels)
    axs[1].set_xlabel('Zeit [min]')
    axs[1].set_ylabel('Personenverteilung')
    axs[1].set_title('Personenverteilung über die Zeit')
    axs[1].legend(loc='upper right', ncol=2)
    axs[1].grid(True)

    # Add general info above both plots
    info_text = f"\n\nSimulations Info:"
    info_text = f"Gesamte Simulationszeit: {fullTime * TIME_PER_STEP / 60:.0f} min\n"
    info_text += f"Station-Sortierungs Typ: {stationOrder}\n"
    info_text += f"\nStationen Wartezeiten (Summe der Wartezeiten = {sumStationTimes* TIME_PER_STEP / 60:.0f} min):\n"
    counter=0


    for i, (name, time) in enumerate(zip(stationNames, stationTimes)):
        wait_min = time * TIME_PER_STEP / 60
        info_text += f"|{name.ljust(12)}: {wait_min:.0f} min".ljust(25)

        # Add a line break every N columns
        if (i + 1) % 5 == 0:
            info_text += "\n"


    fig.text(0.01, 0.98, "Simulations-Resultate Überblick", ha='left', va='top', fontsize=15, fontfamily='monospace')
    fig.text(0.01, 0.95, info_text, ha='left', va='top', fontsize=10, fontfamily='monospace')

    # Layout adjustment
    plt.tight_layout(rect=[0, 0, 1, 0.84])  # Leave space for the subtitle
    plt.show()

def percentOutside(data):
    history = data['history']
    times = [entry['time'] * TIME_PER_STEP / 60 for entry in history]
    peopleOnField = list([entry['numPeopleOnField'] for entry in history])
    plt.plot(times, peopleOnField)
    plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    # Open the file picker dialog
    file_path = filedialog.askopenfilename(title="Select a file")
    file = np.load(file_path, allow_pickle=True).item()
    showFinalData(file)
    #percentOutside(file)