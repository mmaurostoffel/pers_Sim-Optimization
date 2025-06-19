import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import dijkstra_algorithm as dj
import keyboard

# Set Debug Level
DEBUG_LEVEL = 2         # Set Debug level, 0 = No Debug Messages, 1 = some Debug messages, 2 = Full Debug messages and Target-Lines

# Define constants
CELL_PED = 2            # cell state: pedestrian
CELL_OBS = 0            # cell state: obstacle
CELL_EMP = 1            # cell state: empty

VIS_PAUSE = 0.000001    # time [s] between two visual updates
VIS_STEPS = 5           # stride [steps] between two visual updates
MAX_TIME = 5000         # Max Timesteps before the simulation stops
TIME_PER_STEP = 0.3     # The amount of real time that each time step symbolizes

STATION_ORDER = 0       # 1 = predefined, 1 = random, 2 = optimized

# Load Grid
emptyMap = np.load('../01_create_map_material/doc/matrixBaseOutput.npy')
old = emptyMap.copy()
new = old.copy()

GRIDSIZE_X = emptyMap.shape[0]
GRIDSIZE_Y = emptyMap.shape[1]

# Load adjacency matrix
ADJ_MATRIX = pd.read_csv('../01_create_map_material/doc/adjacencyMatrix')
ADJ_MATRIX = ADJ_MATRIX.replace(to_replace='x', value=0, regex=True)
ADJ_MATRIX = ADJ_MATRIX.map(pd.to_numeric, errors='coerce')
ADJ_MATRIX = ADJ_MATRIX.to_numpy()

# Load Waypoints
WP_LIST = pd.read_csv("../01_create_map_material/doc/waypoints_modified_scaled.csv")

# Load Waypoints
STATIONS = np.load("../02_createScenarios/station_files/altstadt_2025-5-30-19%10.npy", allow_pickle=True)


def reorderStations(stations):
    match STATION_ORDER:
        case 0:  # Sort the list
            return stations
        case 1:  # keep randomness from scenario Builder
            return stations
        case 2:  # Use optimization
            return stations

def getWaypoints(lastStation, nextStation):
    path, distance = dj.getWaypoints(ADJ_MATRIX, lastStation, nextStation)
    return path

def getWaypointIndex(x,y):
    index = WP_LIST[(WP_LIST['x'] == x) & (WP_LIST['y'] == y)].index[0]
    return index

def getWaypointCoords(index):
    row = WP_LIST.iloc[index]
    x = int(row['x'])
    y = int(row['y'])
    return [x,y]

def getStationTime(index):
    target_time = [item['time'] for item in STATIONS if item['index'] == index][0]
    return target_time

def checkTargetReached(x, y, x_target, y_target):
    if x == x_target and y == y_target:
        return True
    else:
        return False

def prettyPrint(person):
    string = "ID: "+ str(person['id']) + "curr: " + str(person['currentPos']) + ", target: [" + str(person['goal'][0])+", "+str(person['goal'][1])+"], wp: " + str(person['waypoints'])
    return string

def getPersonID(x,y):
    for index, item in enumerate(personalList):
        if item.get("currentPos") == [x, y]:
            return item.get("id")
    return -1

def updatePerson(old, new):
    removeList = []
    for person in personalList:
        if time % VIS_STEPS == 0:
            if DEBUG_LEVEL == 1: print(prettyPrint(person))
            if DEBUG_LEVEL == 2: print(person)

        x, y = person['currentPos']
        x_target, y_target = person['goal']

        if checkTargetReached(x, y, x_target, y_target):
            # Remove first wp in waypoints
            person['waypoints'].pop(0)

            # station reached
            if len(person['waypoints']) == 0:
                # => Check for Exit and remove if it is one
                if person['stations'][0] in EXIT_LIST:
                    if DEBUG_LEVEL > 0: print("Exit reached -> removing person")
                    removeList.append(person)
                else:
                    # => Add to remove List. Remove from stations list. Refill wp list. Add to station queue.
                    if DEBUG_LEVEL > 0: print("station reached")
                    # Add to remove List
                    removeList.append(person)

                    # Remove from stations list.
                    currentStation = person['stations'][0]
                    person['stations'].pop(0)

                    # Refill wp list.
                    wp = getWaypoints(currentStation, person['stations'][0])
                    person['waypoints'] = wp

                    for entry in stationList:
                        if entry['index'] == currentStation:
                            entry['queue'].append(person)
                            if entry['current_serv_time'] == 0:
                                entry['current_serv_time'] += int(entry['serv_time'])
                            break
                continue

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
            print(f"Person {person['id']} not found where she's supposed to be")

    # Remove all People on removeList from personalList
    for item in removeList:
        personalList.remove(item)

    # Tick StationList
    for entry in stationList:
        # Decrease all current_serv_time by 1
        if entry['current_serv_time'] > 0:
            entry['current_serv_time'] -= 1

        # if current_serv_time reached 0 add it back to personalList
        if entry['current_serv_time'] == 0 and len(entry['queue']) > 0:
            # Check if reentry point is occupied
            currX, currY = entry['queue'][0]['currentPos']
            if old[int(currX), int(currY)] == CELL_PED:
                # Location occupied: Wait another turn
                entry['current_serv_time'] = 1
            else:
                # Location empty: Place person back on field
                new[int(currX), int(currY)] = CELL_PED
                personalList.append(entry['queue'][0])
                # Remove from StationList
                entry['queue'].pop(0)
                if len(entry['queue']) > 0:
                    entry['current_serv_time'] += int(entry['serv_time'])


def checkPeopleRemaining():
    if len(personalList) == 0:
        for station in stationList:
            if len(station['queue']) > 0:
                return True
    else:
        return True
    return False

def saveTickInfo(currHistory):
    tick = {}
    tick['time'] = time
    tick['numPeopleOnField'] = len(personalList)
    stationWaitTimes = []
    stationQueueLength = []
    for station in stationList:
        stationWaitTimes.append(station['current_serv_time'])
        stationQueueLength.append(len(station['queue']))
    tick['stationWaitTimes'] = stationWaitTimes
    currHistory.append(tick)
    return currHistory


# Initialize personalList
personalList = []
# one person (1)
# scenario = np.load("../02_createScenarios/scenario_files/altstadt_1_3_2025-5-29-0%45.npy", allow_pickle=True)
# one person (2)
# scenario = np.load("../02_createScenarios/scenario_files/altstadt_1_3_2025-5-31-17%53.npy", allow_pickle=True)
# ten people
# scenario = np.load("../02_createScenarios/scenario_files/altstadt_10_3_2025-5-29-0%49.npy", allow_pickle=True)
# 100 people
scenario = np.load("../02_createScenarios/scenario_files/altstadt_100_5_2025-6-19-20%31.npy", allow_pickle=True)
id = 1
for row in scenario:
    person = {}
    # Set static Index
    person['id'] = id
    id += 1
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
    row[2] = reorderStations(row[2])
    # Get stations
    # person['stations'] = row[2]
    person['stations'] = [item[0] for item in row[2]]

    # Generate next Waypoints
    wp = getWaypoints(int(startNode), int(row[2][0][0]))
    person['waypoints'] = wp

    # Get next Goal
    goal = getWaypointCoords(wp[0])
    person['goal'] = goal

    # Add Person to personalList
    personalList.append(person)

# Initialize Station List
stationList = []
EXIT_LIST = []
for index, (x, y, comm) in WP_LIST.iterrows():
    if comm != "WP":
        if not str(comm).startswith("Exit_"):
            station = {}
            station['index'] = index
            station['pos'] = [x, y]
            station['name'] = comm
            station['pname'] = str(comm).replace("_", " ")
            station['serv_time'] = getStationTime(index)
            station['current_serv_time'] = 0
            station['queue'] = []

            stationList.append(station)
        else:
            EXIT_LIST.append(index)



# Start Simulation Loop
time = 0
cmap = ListedColormap(['gray', 'white', 'white'])
norm = BoundaryNorm([0, 0.5, 1.5, 2.5], cmap.N)

# Visualisierung vorbereiten
import matplotlib.gridspec as gridspec
fig = plt.figure(figsize=(18, 8))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
ax = fig.add_subplot(gs[0])
ax_station = fig.add_subplot(gs[1])
plt.ion()

# Simulationsschleife
peopleInSim = True
history = []
while peopleInSim:
    # Clear Console
    if DEBUG_LEVEL > 0:
        print("\n" * 100)
        for person in personalList:
            if DEBUG_LEVEL == 1: print(prettyPrint(person))
            if DEBUG_LEVEL == 2: print(person)
        if DEBUG_LEVEL == 2: print("STATION LIST = ", stationList)

    new = emptyMap.copy()
    updatePerson(old, new)
    old = new.copy()
    time += 1

    if time % VIS_STEPS == 0:

        # Pedestrians
        ax.cla()
        ax.imshow(old, cmap=cmap, norm=norm)
        pedestrian_positions = np.argwhere(old == 2)
        for y, x in pedestrian_positions:
            ax.plot(x, y, marker='o', color='red', markersize=10)
            ax.text(x+7, y-7, str(getPersonID(y, x)), color='black', fontsize=10,
                    ha='center', va='center', weight='bold')

        # Debug path lines
        if DEBUG_LEVEL > 0:
            for person in personalList:
                ax.plot([person['currentPos'][1], person['goal'][1]], [person['currentPos'][0], person['goal'][0]], color='red', linewidth=2)

        # Station-status
        ax_station.clear()
        ax_station.axis('off')
        ax_station.set_title("Stationen & Status", fontsize=12, fontweight='bold')
        
        for station in stationList:
            idx = int(station['index']) - 88
            # Add marker
            ax.plot(station['pos'][0], station['pos'][1], marker='o', color='green', markersize=15)
            ax.text(station['pos'][0], station['pos'][1], str(idx), color='white', fontsize=10,
                    ha='center', va='center', weight='bold')

            persons_at_station = len(station['queue'])
            wait_time = station['current_serv_time']

            icons = 'o' * min(persons_at_station, 5)
            if persons_at_station > 5:
                icons += f" +{persons_at_station - 5}"
            y_pos = 0.9 - idx * 0.09
            ax_station.text(0.05, y_pos, f"{idx}:", fontsize=10, weight='bold', va='center')
            ax_station.text(0.15, y_pos, f"{station['name']}:", fontsize=10, weight='bold', va='center')
            ax_station.text(0.45, y_pos, f"{wait_time:.1f} min", fontsize=10, va='center', ha='right')
            ax_station.text(0.55, y_pos, icons, fontsize=12, va='center')

        plt.pause(VIS_PAUSE)

    peopleInSim = checkPeopleRemaining()
    history = saveTickInfo(history)

    # Exit from Loop
    if keyboard.is_pressed('q'):
        break

plt.ioff()
plt.show()

print(f"Simulation finished in {time} ticks")
# print(history)

# Extract time and station wait times
times = [entry['time'] for entry in history]
station_waits = list(zip(*[entry['stationWaitTimes'] for entry in history]))

# Plot each station's wait times
plt.figure(figsize=(12, 6))
for i, wait_times in enumerate(station_waits):
    plt.plot(times, wait_times, label=f'Station {i}')

plt.xlabel('Time')
plt.ylabel('Wait Time')
plt.title('Station Wait Times Over Time')
plt.legend(loc='upper right', ncol=2)
plt.grid(True)
plt.tight_layout()
plt.show()





