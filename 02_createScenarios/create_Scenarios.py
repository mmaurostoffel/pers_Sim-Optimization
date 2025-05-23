import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import random
import datetime
import breath_first_search as bfs

# Inputs
baseMap = np.load('../01_create_map_material/doc/matrixBaseOutput.npy')
wp = pd.read_csv("../01_create_map_material/doc/waypoints_modified_scaled.csv")

numPeople = 1      # defines how many people are in the scenario
numOfTasks = 3     # defines how many tasks a person is supposed to do

# Constants
CELL_OBS = 0
CELL_EMP = 1
CELL_PED = 2

def plot_matrix(matrix):
    #wall, path, waypoint, marker
    colors = ["black", "white", "green"]
    cmap = ListedColormap(colors)
    plt.imshow(matrix, cmap=cmap, interpolation='nearest')
    plt.axis('off')
    plt.show()

def extractExitsAndShopsFromWP(wp):
    exits = []
    shops = []
    for i in range(len(wp)):
        if wp.iloc[i]["comment"] != "WP":
            if wp.iloc[i]["comment"].startswith("Exit"):
                exits.append(wp.iloc[i])
            else:
                shops.append(wp.iloc[i])
    return exits, shops

def setOfWaypoint(wp):
        waypoints = []
        for index, row in wp.iterrows():
            x = int(row['x'])
            y = int(row['y'])
            waypoints.append((x, y))
        return waypoints

# Extract shops and exits from waypoint file
exits, shops = extractExitsAndShopsFromWP(wp)

scenarioFile = []
for i in range(numPeople):
    currentPerson = []

    # set random starting points for pedestrians
    while True:
        x = int(float(baseMap.shape[0])*np.random.random())
        y = int(float(baseMap.shape[1])*np.random.random())
        if baseMap[x, y] == CELL_EMP:
            baseMap[x, y] = CELL_PED
            break
    currentPerson.append([x, y])

    # Find the closest Waypoint to starting pos
    foundWP = bfs.find_closest_waypoint(baseMap, (x, y), setOfWaypoint(wp))
    currentPerson.append(foundWP)

    # Add Tasks
    tempShops = shops
    shopList = []
    for j in range(numOfTasks):
        elem = random.choice(tempShops)
        tempShops = [item for item in tempShops if not item.equals(elem)]
        shopList.append([elem.name,elem['x'], elem['y'],elem['comment']])

    # Add Exit
    exit = random.choice(exits)
    shopList.append([exit.name, exit['x'], exit['y'], exit['comment']])

    # Add ShopList to currentPerson
    currentPerson.append(shopList)

    # Add person to scenario file
    scenarioFile.append(currentPerson)


today = datetime.datetime.now()
scenarioFile = np.array(scenarioFile, dtype=object)
np.save(f"scenario_files/altstadt_{numPeople}_{numOfTasks}_{today.year}-{today.month}-{today.day}-{today.hour}%{today.minute}",scenarioFile, allow_pickle=True)

# also save as csv if neccessary
df = pd.DataFrame(scenarioFile)
df.to_csv(f"scenario_files/temp.csv", index=False)

