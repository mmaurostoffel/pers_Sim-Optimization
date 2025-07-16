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

for key, path in files.items():
    df = pd.read_csv(path, header=None)
    quot = df.iloc[:, 0] / df.iloc[:, -1]
    quotients[key] = quot

# Vordefiniert / dynamisch -->

plt.figure(figsize=(10, 6))
counter = 0
for key, q in quotients.items():
    if counter == 0 or counter == 2 or counter == 4 or counter == 6:
        plt.plot(people_counts, q, 'o-', label=key, color=colors[counter])
    else:
        plt.plot(people_counts, q, 'o--', label=key, color=colors[counter])
    counter += 1
    print(key)
    print(np.mean(q))

plt.xlabel('Anzahl Personen')
plt.ylabel('Quotient (Vordefinierte Stationeliste / dynamische Stationeliste)')
plt.title('Quotient (Vordefinierte Stationeliste / dynamische Stationeliste)')
plt.legend()
plt.grid(True)
plt.show()
