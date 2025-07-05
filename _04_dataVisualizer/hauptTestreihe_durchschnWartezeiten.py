import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd

TIME_PER_STEP = 0.3
GETDATA = 1

def getMean(data):
    history = data['history']
    # Extract time and station wait times
    station_waits = list(zip(*[[wait * TIME_PER_STEP / 60 for wait in entry['stationWaitTimes']] for entry in history]))
    all_waits = [wait for station in station_waits for wait in station]
    print(round(np.mean(all_waits),0))

def plotData():
    tr1 = pd.read_csv("doc/vorBesprechung/durchschnittsWartezeiten/tr1.csv", header=None).T
    tr2 = pd.read_csv("doc/vorBesprechung/durchschnittsWartezeiten/tr2.csv", header=None).T
    tr3 = pd.read_csv("doc/vorBesprechung/durchschnittsWartezeiten/tr3.csv", header=None).T

    numPeople = [10, 50, 100, 200, 500]
    stationOrders = ["Vordefinierte Liste", "dynamisch optimierte Liste"]

    plt.figure(figsize=(10, 6))
    plt.plot(numPeople, tr1.iloc[0], 'o-', color="blue", label=f"⌀ Wartezeiten TR1: {stationOrders[0]}")
    plt.plot(numPeople, tr1.iloc[1], 'o--', color="blue", label=f"⌀ Wartezeiten TR1: {stationOrders[1]}")
    plt.plot(numPeople, tr2.iloc[0], 'o-', color="orange", label=f"⌀ Wartezeiten TR2: {stationOrders[0]}")
    plt.plot(numPeople, tr2.iloc[1], 'o--', color="orange", label=f"⌀ Wartezeiten TR2: {stationOrders[1]}")
    plt.plot(numPeople, tr3.iloc[0], 'o-', color="green", label=f"⌀ Wartezeiten TR3: {stationOrders[0]}")
    plt.plot(numPeople, tr3.iloc[1], 'o--', color="green", label=f"⌀ Wartezeiten TR3: {stationOrders[1]}")
    plt.title("Durchschnittliche Wartezeiten der Testreihen 1, 2 und 3")
    plt.legend(loc="best")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    if GETDATA == 0:
        root = tk.Tk()
        root.withdraw()

        # Open the file picker dialog
        file_path = filedialog.askopenfilename(title="Select a file")
        file = np.load(file_path, allow_pickle=True).item()
        getMean(file)
    else:
        plotData()