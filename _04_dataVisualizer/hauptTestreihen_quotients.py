import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# testreihe 1 und 2
files = {
    "Gesamte Simulationszeit 1. Testreihe": "doc/nachBesprechung/210min/fullTimes.csv",
    "50% Meilensteine 1. Testreihe": "doc/nachBesprechung/210min/halfTimes.csv",
    "Gesamte Simulationszeit 2. Testreihe": "doc/nachBesprechung/220min/fullTimes.csv",
    "50% Meilensteine 2. Testreihe": "doc/nachBesprechung/220min/halfTimes.csv",
    "Gesamte Simulationszeit 3. Testreihe": "doc/nachBesprechung/21min/fullTimes.csv",
    "50% Meilensteine 3. Testreihe": "doc/nachBesprechung/21min/halfTimes.csv",
    "Gesamte Simulationszeit 4. Testreihe": "doc/nachBesprechung/21minAll/fullTimes.csv",
    "50% Meilensteine 4. Testreihe": "doc/nachBesprechung/21minAll/halfTimes.csv",
}

people_counts = [10, 50, 100, 200, 500]
colors = ['blue', 'blue', 'red', 'red', 'green', 'green', 'orange', 'orange']
quotients = {}

# Quotienten berechnen
for key, path in files.items():
    df = pd.read_csv(path, header=None)
    quot = df.iloc[:, 0] / df.iloc[:, -1]
    quotients[key] = quot

plt.figure(figsize=(12, 7))
counter = 0

for key, q in quotients.items():
    if counter % 2 == 0:  # Nur "Gesamte Simulationszeit" Linien
        plt.plot(people_counts, q, 'o-', label=key, color=colors[counter])

        # Durchschnitt berechnen und Linie zeichnen
        avg = np.mean(q)
        plt.hlines(avg, people_counts[0], people_counts[-1], color=colors[counter], linestyle='--', linewidth=1.5)

        # Marker und Text am rechten Rand der Linie
        plt.plot(people_counts[-1], avg, 's', color=colors[counter])
        #plt.text(people_counts[-1] + 10, avg, f'{avg:.2f}', va='center', fontsize=12, color=colors[counter])

        print(key)
        print(avg)

    counter += 1

plt.xlabel('Anzahl Personen')
plt.ylabel('Quotient (Vordefinierte Stationeliste / dynamische Stationeliste)')
plt.title('Quotient (Vordefinierte Stationeliste / dynamische Stationeliste)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
