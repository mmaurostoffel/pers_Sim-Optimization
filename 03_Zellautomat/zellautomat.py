import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import dijkstra_algorithm as dj

# Define constants
CELL_PED = 2   # cell state: pedestrian
CELL_OBS = 0  # cell state: obstacle
CELL_EMP = 1   # cell state: empty

VIS_PAUSE = 0.000001  # time [s] between two visual updates
VIS_STEPS = 2    # stride [steps] between two visual updates
MAX_TIME = 200

STATION_ORDER = 0 # 1 = predefined, 1 = random, 2 = optimized

# Load Grid
emptyMap = np.load('../01_create_map_material/doc/matrixBaseOutput.npy')
old = emptyMap.copy()
new = old.copy()

GRIDSIZE_X = emptyMap.shape[0]
GRIDSIZE_Y = emptyMap.shape[1]

# Load adjacency matrix
adj_matrix = pd.read_csv('../01_create_map_material/doc/adjacencyMatrix')
adj_matrix = adj_matrix.replace(to_replace='x', value=0, regex=True)
adj_matrix = adj_matrix.map(pd.to_numeric, errors='coerce')
adj_matrix = adj_matrix.to_numpy()

# Load Waypoints
WP_LIST = pd.read_csv("../01_create_map_material/doc/waypoints_modified_scaled.csv")

def reorderStations(stations):
    match STATION_ORDER:
        case 0:  # Sort the list
            return stations
        case 1:  # keep randomness from scenario Builder
            return stations
        case 2:  # Use optimization
            return stations

def getWaypoints(lastStation, nextStation):
    path, distance = dj.getWaypoints(adj_matrix, lastStation, nextStation)
    return path

def getWaypointIndex(x,y):
    index = WP_LIST[(WP_LIST['x'] == x) & (WP_LIST['y'] == y)].index[0]
    return index

def getWaypointCoords(index):
    row = WP_LIST.iloc[index]
    x = row['x']
    y = row['y']
    return [x,y]

def checkTargetReached(x, y, x_target, y_target):
    if x == x_target and y == y_target:
        return True
    else:
        return False

# Read starting Positions from scenario file
personalList = []
# scenario = np.load("../02_createScenarios/scenario_files/altstadt_1_3_2025-5-23-15%21.npy", allow_pickle=True)
# scenario = np.load("../02_createScenarios/scenario_files/altstadt_1_3_2025-5-29-0%38.npy", allow_pickle=True)
scenario = np.load("../02_createScenarios/scenario_files/altstadt_1_3_2025-5-29-0%45.npy", allow_pickle=True)
for row in scenario:
    person = {}
    # Get Starting Pos
    x = row[0][0]
    y = row[0][1]
    person['currentPos'] = [x, y]
    # Place on Board
    old[int(x), int(y)] = CELL_PED

    # Get first Waypoint
    firstWp = row[1]
    startNode = getWaypointIndex(firstWp[0], firstWp[1])

    # Apply station orders
    row[1] = reorderStations(row[2])
    # Get stations
    person['stations'] = row[2]

    # Generate next Waypoints
    wp = getWaypoints(int(startNode), int(row[2][0][0]))
    person['waypoints'] = wp

    # Get next Goal
    goal = getWaypointCoords(wp[0])
    person['goal'] = goal

    # Add Person to personalList
    personalList.append(person)
    break

def updatePerson(old, new):
    for person in personalList:
        print("HELLO", person)
        x, y = person['currentPos']
        x_target, y_target = person['goal']

        if checkTargetReached(x, y, x_target, y_target):
            # Remove first wp in waypoints
            person['waypoints'].pop(0)

            # Set new goal
            goal = getWaypointCoords(person['waypoints'][0])
            person['goal'] = goal

            # Set new Target
            x_target, y_target = person['goal']

        if old[x, y] == CELL_PED:
            x_dist = x_target - x
            x_move = 1 if x_dist > 0 else -1
            y_dist = y_target - y
            y_move = 1 if y_dist > 0 else -1
            if abs(x_dist) > abs(y_dist):
                if old[(x + x_move), y] == CELL_EMP:
                    new[(x + x_move), y] = CELL_PED
                    old[(x + x_move), y] = CELL_OBS
                    person['currentPos'] = [(x + x_move), y]
                elif old[x, (y + y_move)] == CELL_EMP:
                    new[x, (y + y_move)] = CELL_PED
                    old[x, (y + y_move)] = CELL_OBS
                    person['currentPos'] = [x, (y + y_move)]
                else:
                    new[x, y] = CELL_PED
                    old[x, y] = CELL_OBS
            else:
                if old[x, (y + y_move)] == CELL_EMP:
                    new[x, (y + y_move)] = CELL_PED
                    old[x, (y + y_move)] = CELL_OBS
                    person['currentPos'] = [x, (y + y_move)]
                elif old[(x + x_move), y] == CELL_EMP:
                    new[(x + x_move), y] = CELL_PED
                    old[(x + x_move), y] = CELL_OBS
                    person['currentPos'] = [(x + x_move), y]
                else:
                    new[x, y] = CELL_PED
                    old[x, y] = CELL_OBS
        else:
            print("Person not found where she's supposed to be")

time = 0
dens = []

colors = ["black", "white", "red"]
cmap = ListedColormap(colors)
plt.ion()
plt.imshow(old, cmap=cmap, interpolation='nearest')
plt.pause(VIS_PAUSE)
while time < MAX_TIME:
    new = emptyMap.copy()
    updatePerson(old, new)
    old = new.copy()
    time = time + 1
    if time%VIS_STEPS == 0:
      plt.clf()
      plt.imshow(old, cmap=cmap, interpolation='nearest')
      plt.pause(VIS_PAUSE)
      plt.pause(0.1)
plt.ioff()

# while count_peds(old) > 0 and time < MAX_TIME:







