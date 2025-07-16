import matplotlib.pyplot as plt
import pandas as pd

# Load and transpose
full_210 = pd.read_csv("doc/nachBesprechung/210min/fullTimes.csv", header=None).T
#quarter_210 = pd.read_csv("doc/nachBesprechung/210min/threeQuarterTimes.csv", header=None).T
half_210 = pd.read_csv("doc/nachBesprechung/210min/halfTimes.csv", header=None).T

full_220 = pd.read_csv("doc/nachBesprechung/220min/fullTimes.csv", header=None).T
#quarter_220 = pd.read_csv("doc/nachBesprechung/220min/threeQuarterTimes.csv", header=None).T
half_220 = pd.read_csv("doc/nachBesprechung/220min/halfTimes.csv", header=None).T

full_22 = pd.read_csv("doc/nachBesprechung/21min/fullTimes.csv", header=None).T
#quarter_22 = pd.read_csv("doc/nachBesprechung/22min/threeQuarterTimes.csv", header=None).T
half_22 = pd.read_csv("doc/nachBesprechung/21min/halfTimes.csv", header=None).T

full_22All = pd.read_csv("doc/nachBesprechung/21minAll/fullTimes.csv", header=None).T
#quarter_22 = pd.read_csv("doc/nachBesprechung/22min/threeQuarterTimes.csv", header=None).T
half_22All = pd.read_csv("doc/nachBesprechung/21minAll/halfTimes.csv", header=None).T


# Labels
numPeople = [10, 50, 100, 200, 500]

stationOrders = ["Vordefinierte Liste","Vordefinierte Liste mit zufälligem Start","Zufälliger Ablauf", "Am Start optimierte Liste", "dynamisch optimierte Liste"]
colors = ['blue', 'orange', 'green', 'red', "purple"]

# Plot
plt.figure(figsize=(10, 6))
for i in range(len(stationOrders)):
    plt.plot(numPeople, full_210.iloc[i], 'o-', color=colors[i], label=f"Gesamte Simulationszeit: {stationOrders[i]}")
# for i in range(len(stationOrders)):
#     plt.plot(numPeople, quarter_210.iloc[i], 'o--', color=colors[i], label=f"75% Meilenstein: {stationOrders[i]}")
for i in range(len(stationOrders)):
    plt.plot(numPeople, half_210.iloc[i], 'o-.', color=colors[i], alpha= 0.5, label=f"50% Meilenstein: {stationOrders[i]}")

plt.xlabel("Anzahl Personen")
plt.ylabel("Zeit [min]")
plt.title("Resultate der ersten Haupttestreihe")
plt.grid(True)
plt.legend(loc='best')
plt.tight_layout()
plt.xlim([0, 60])
plt.ylim([0, 2500])


plt.figure(figsize=(10, 6))
for i in range(len(stationOrders)):
    plt.plot(numPeople, full_220.iloc[i], 'o-', color=colors[i], label=f"Gesamte Simulationszeit: {stationOrders[i]}")
# for i in range(len(stationOrders)):
#     plt.plot(numPeople, quarter_220.iloc[i], 'o--', color=colors[i], label=f"75% Meilenstein: {stationOrders[i]}")
for i in range(len(stationOrders)):
    plt.plot(numPeople, half_220.iloc[i], 'o-.', color=colors[i],  alpha= 0.5, label=f"50% Meilenstein: {stationOrders[i]}")

plt.xlabel("Anzahl Personen")
plt.ylabel("Zeit [min]")
plt.title("Resultate der zweiten Haupttestreihe")
plt.grid(True)
plt.legend(loc='best')
plt.tight_layout()
#plt.xlim([0, 60])
#plt.ylim([0, 2500])


plt.figure(figsize=(10, 6))
for i in range(len(stationOrders)):
    plt.plot(numPeople, full_22.iloc[i], 'o-', color=colors[i], label=f"Gesamte Simulationszeit: {stationOrders[i]}")
# for i in range(len(stationOrders)):
#     plt.plot(numPeople, quarter_22.iloc[i], 'o--', color=colors[i], label=f"75% Meilenstein: {stationOrders[i]}")
for i in range(len(stationOrders)):
    plt.plot(numPeople, half_22.iloc[i], 'o-.', color=colors[i],  alpha= 0.5, label=f"50% Meilenstein: {stationOrders[i]}")

plt.xlabel("Anzahl Personen")
plt.ylabel("Zeit [min]")
plt.title("Resultate der dritten Haupttestreihe")
plt.grid(True)
plt.legend(loc='best')
plt.tight_layout()
plt.xlim([0, 110])
plt.ylim([0, 600])


plt.figure(figsize=(10, 6))
for i in range(len(stationOrders)):
    plt.plot(numPeople, full_22All.iloc[i], 'o-', color=colors[i], label=f"Gesamte Simulationszeit: {stationOrders[i]}")
# for i in range(len(stationOrders)):
#     plt.plot(numPeople, quarter_22.iloc[i], 'o--', color=colors[i], label=f"75% Meilenstein: {stationOrders[i]}")
for i in range(len(stationOrders)):
    plt.plot(numPeople, half_22All.iloc[i], 'o-.', color=colors[i],  alpha= 0.5, label=f"50% Meilenstein: {stationOrders[i]}")

plt.xlabel("Anzahl Personen")
plt.ylabel("Zeit [min]")
plt.title("Resultate der vierten Haupttestreihe")
plt.grid(True)
plt.legend(loc='best')
plt.tight_layout()
#plt.xlim([0, 110])
#plt.ylim([0, 300])
plt.show()

