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

    # Find halfway point
    total_sum_per_timestep = [sum(values) for values in zip(*stack_data)]
    initial_total_sum = total_sum_per_timestep[0]
    half_sum = initial_total_sum / 2
    target_index = next((i for i, val in enumerate(total_sum_per_timestep) if val <= half_sum),None)
    target_index = target_index * TIME_PER_STEP / 60

    threeQuarter_sum = initial_total_sum *0.75
    target_75_index = next((i for i, val in enumerate(total_sum_per_timestep) if val <= threeQuarter_sum), None)
    target_75_index = target_75_index * TIME_PER_STEP / 60
    print(target_75_index)

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

    # Plot vertical lines
    axs[0].axvline(x=target_index, color='red', linestyle='--', label='50%-Meilenstein')
    axs[0].text(target_index, axs[0].get_ylim()[1] * 0.9, '50%-Meilenstein', color='red',ha='center', va='bottom', backgroundcolor='white')
    axs[1].axvline(x=target_index, color='red', linestyle='--', label='50%-Meilenstein')
    axs[1].text(target_index, axs[1].get_ylim()[1] * 0.9, '50%-Meilenstein', color='red', ha='center', va='bottom',backgroundcolor='white')

    # Add general info above both plots
    info_text = f"\n\nSimulations Info:"
    info_text = f"Gesamte Simulationszeit: {fullTime * TIME_PER_STEP / 60:.0f} min\n"
    info_text += f"50% Meilenstein: {target_index:.0f} min\n"
    info_text += f"Station-Sortierungs Typ: {stationOrder}\n"
    info_text += f"\nStationen Wartezeiten (Summe der Wartezeiten = {sumStationTimes* TIME_PER_STEP / 60:.0f} min):\n"


    for i, (name, time) in enumerate(zip(stationNames, stationTimes)):
        wait_min = time * TIME_PER_STEP / 60
        info_text += f"|{name.ljust(12)}: {wait_min:.0f} min".ljust(25)

        if (i + 1) % 5 == 0:
            info_text += "\n"

    fig.text(0.01, 0.98, "Simulations-Resultate Überblick", ha='left', va='top', fontsize=15, fontfamily='monospace')
    fig.text(0.01, 0.93, info_text, ha='left', va='top', fontsize=10, fontfamily='monospace')

    # Layout adjustment
    plt.tight_layout(rect=[0, 0, 1, 0.80])
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