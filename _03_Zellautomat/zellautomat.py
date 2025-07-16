import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
import dijkstra_algorithm as dj
import keyboard
from _04_dataVisualizer.plotData import showFinalData
import datetime
import random

# Set Debug Level
DEBUG_LEVEL = 0             # Set Debug level, 0 = No Debug Messages, 1 = some Debug messages, 2 = Full Debug messages and Target-Lines
PLOT_MARKERS = True         # Can be ued to turn of the plotting of the markers to analyze specific parts of the map

# Define constants
CELL_PED = 2                # cell state: pedestrian
CELL_OBS = 0                # cell state: obstacle
CELL_EMP = 1                # cell state: empty

VIS_PAUSE = 0.000001        # time [s] between two visual updates
VIS_STEPS = 10          # stride [steps] between two visual updates
STEP_UPDATES = 1000         # stride [steps] between two visual updates
MAX_TIME = 5000             # Max Timesteps before the simulation stops
TIME_PER_STEP = 0.3         # The amount of real time (in seconds) that each time step symbolizes

SET_PERSON_VISIBILITY = 10  # If this Value is set to a number other than -1 this person will be made more visible

STATION_ORDER = 4
# 0 = predefined, 1 = predefined with random start, 2 = random, 3 = optimized at Start, 4 = optimized after every Station
match STATION_ORDER:
    case 0:
        STATION_ORDER_NAME = "Vordefinierte Liste"
        USE_FIRST_STATION_AS_START = True
    case 1:
        STATION_ORDER_NAME = "Vordefinierte Liste mit zufälliger Startstation"
        USE_FIRST_STATION_AS_START = True
    case 2:
        STATION_ORDER_NAME = "Zufälliger Ablauf"
        USE_FIRST_STATION_AS_START = False
    case 3:
        STATION_ORDER_NAME = "Am Start optimierte Liste"
        USE_FIRST_STATION_AS_START = False
    case 4:
        STATION_ORDER_NAME = "dynamisch optimierte Liste"
        USE_FIRST_STATION_AS_START = False

# Load Grid
emptyMap = np.load('../_01_create_map_material/doc/matrixBaseOutput.npy')
old = emptyMap.copy()
new = old.copy()

GRIDSIZE_X = emptyMap.shape[0]
GRIDSIZE_Y = emptyMap.shape[1]

# Load adjacency matrix
ADJ_MATRIX = pd.read_csv('../_01_create_map_material/doc/adjacencyMatrix')
ADJ_MATRIX = ADJ_MATRIX.replace(to_replace='x', value=0, regex=True)
ADJ_MATRIX = ADJ_MATRIX.map(pd.to_numeric, errors='coerce')
ADJ_MATRIX = ADJ_MATRIX.to_numpy()

# Load Waypoints
WP_LIST = pd.read_csv("../_01_create_map_material/doc/waypoints_modified_scaled.csv")

# Load Station Times
# STATIONS = np.load("../_02_createScenarios/station_files/altstadt_TEST_SETUP_2025-6-21-18%44.npy", allow_pickle=True)
STATIONS = np.load("../_02_createScenarios/station_files/21min_altstadt__2025-6-28-1%27.npy", allow_pickle=True)

# Load Station Order
STATIC_STATION_ORDER = np.load("../_02_createScenarios/statio_order_fils/altstadt_STATION_ORDER_2025-6-21-19%2.npy", allow_pickle=True)

def reorderStations(stations):
    endStation = stations[-1]
    restStations = stations[:-1]

    match STATION_ORDER:
        case 0:  # Sort the list
            sorted_stations = sorted(restStations, key=lambda x: list(STATIC_STATION_ORDER).index(x[0]))
            stations = sorted_stations + [endStation]
            return stations
        case 1:  # Sort the list with random start
            sorted_stations = sorted(restStations, key=lambda x: list(STATIC_STATION_ORDER).index(x[0]))
            element = random.choice(sorted_stations)
            sorted_stations.remove(element)
            sorted_stations.insert(0, element)
            stations = sorted_stations + [endStation]
            return stations
        case 2:  # keep randomness from scenario Builder
            return stations
        case 3:  # Use optimization
            sorted_stations = optimizeStations(restStations)
            stations = sorted_stations + [endStation]
            return stations
        case 4:  # Use dynamic optimization
            sorted_stations = optimizeStations(restStations)
            stations = sorted_stations + [endStation]
            return stations

def optimizeStations(stations):
    # Sort stations by full_serv_time
    stations_sorted = sorted(stationList, key=lambda x: x['full_serv_time'])

    # Return the indeces of the sorted stations
    index_sorted = [station['index'] for station in stations_sorted]

    # Sort the input stations acording to index_sorted
    #sorted_stations = sorted(stations, key=lambda y: list(index_sorted).index(y[0]))
    sorted_stations = sorted(stations,key=lambda y: index_sorted.index(y if isinstance(y, int) else y[0]))
    return sorted_stations

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

def update(old, new):
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
                elif old[x, (y + y_move)] == CELL_EMP and old[x, (y - y_move)] == CELL_EMP and old[(x + x_move), y] == CELL_PED:
                    if x_move == 1:
                        new[x, (y + y_move)] = CELL_PED
                        old[x, (y + y_move)] = CELL_OBS
                        person['currentPos'] = [x, (y + y_move)]
                    else:
                        new[x, (y - y_move)] = CELL_PED
                        old[x, (y - y_move)] = CELL_OBS
                        person['currentPos'] = [x, (y - y_move)]
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
                elif old[(x + x_move), y] == CELL_EMP and old[(x - x_move), y] == CELL_EMP and old[x, (y + y_move)] == CELL_PED:
                    if y_move == 1:
                        new[(x + x_move), y] = CELL_PED
                        old[(x + x_move), y] = CELL_OBS
                        person['currentPos'] = [(x + x_move), y]
                    else:
                        new[(x - x_move), y] = CELL_PED
                        old[(x - x_move), y] = CELL_OBS
                        person['currentPos'] = [(x - x_move), y]
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
                # If dynamic Station order active reorder stations
                if STATION_ORDER == 4:
                    # Reference Person data
                    person = entry['queue'][0]
                    # Reorder Stations
                    person['stations'] = reorderStations(person['stations'])
                    # Refill wp list.
                    wp = getWaypoints(entry['index'], person['stations'][0])
                    person['waypoints'] = wp
                    # Set new goal
                    goal = getWaypointCoords(person['waypoints'][0])
                    person['goal'] = goal

                personalList.append(entry['queue'][0])
                # Remove from StationList
                entry['queue'].pop(0)
                if len(entry['queue']) > 0:
                    entry['current_serv_time'] += int(entry['serv_time'])
        # Update Full Service Time
        if len(entry['queue']) > 0:
            entry['full_serv_time'] = int(entry['serv_time']) * (len(entry['queue'])-1) + entry['current_serv_time']

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
        stationWaitTimes.append(station['full_serv_time'])
        stationQueueLength.append(len(station['queue']))
    tick['stationWaitTimes'] = stationWaitTimes
    tick['stationQueueLength'] = stationQueueLength
    currHistory.append(tick)
    return currHistory

def applyStartShops(currentPerson):
    if USE_FIRST_STATION_AS_START:
        startShop = currentPerson['shoplist'][0]
        currentPerson['shoplist'].pop(0)

        start_Shop = pd.Series(
            data=[startShop[2], startShop[1], startShop[3]],
            index=['y', 'x', 'comment'],
            name=startShop[0]
        )
        currentPerson['startShop'] = start_Shop
        return currentPerson
    else:
        currentPerson['shoplist'].pop(0)
        return currentPerson

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
            station['full_serv_time'] = 0
            station['queue'] = []

            stationList.append(station)
        else:
            EXIT_LIST.append(index)


# Load Scenario File
scenario = np.load("../_02_createScenarios/scenario_files/new_Haupttestreihe/ALL_altstadt_500_10_0.9_2025-7-11-14%37.npy", allow_pickle=True)
# scenario = np.load("../_02_createScenarios/scenario_files/VersuchsScenarios/altstadt_500_5_0_2025-6-27-13%36.npy", allow_pickle=True)

# Pre-Fill full_serv_time of stations
peopleCount = {}
for currentPerson in scenario:
    # Apply station orders
    currentPerson['shoplist'] = reorderStations(currentPerson['shoplist'])
    if currentPerson['inStation'] == True:
        currentPerson = applyStartShops(currentPerson)
        startShop = currentPerson['startShop']
        for entry in stationList:
            if entry['index'] == startShop.name:
                if entry['index'] in peopleCount:
                    peopleCount[entry['index']] += 1
                else:
                    peopleCount[entry['index']] = 1

for key in peopleCount:
    for entry in stationList:
        if entry['index'] == key:
            entry['full_serv_time'] = int(entry['serv_time']) * peopleCount[key]


# Initialize personalList
personalList = []
id = 1
for currentPerson in scenario:
    person = {}
    # Set static Index
    person['id'] = id
    id += 1
    if currentPerson['inStation'] == False:
        # Get Starting Pos
        x,y = currentPerson['pos']
        person['currentPos'] = [x, y]
        # Place on Board
        old[int(x), int(y)] = CELL_PED

        # Get first Waypoint
        firstWp = currentPerson['closestWP']
        startNode = getWaypointIndex(firstWp[0], firstWp[1])
    else:
        startShop = currentPerson['startShop']
        x, y = startShop['x'], startShop['y']
        person['currentPos'] = [x, y]

        startNode = startShop.name

    # Apply station orders
    currentPerson['shoplist'] = reorderStations(currentPerson['shoplist'])

    # Get stations
    person['stations'] = [item[0] for item in currentPerson['shoplist']]

    # Generate next Waypoints
    wp = getWaypoints(int(startNode), int(currentPerson['shoplist'][0][0]))
    person['waypoints'] = wp

    # Get next Goal
    goal = getWaypointCoords(wp[0])
    person['goal'] = goal

    if currentPerson['inStation'] == False:
        # Add Person to personalList
        personalList.append(person)
    else:
        # Add Person to Station queue
        for entry in stationList:
            if entry['index'] == startShop.name:
                entry['queue'].append(person)
                if entry['current_serv_time'] == 0:
                    entry['current_serv_time'] += int(entry['serv_time'])
                entry['full_serv_time'] += int(entry['serv_time'])
                break



# Start Simulation Loop
time = 0
cmap = ListedColormap(['gray', 'white', 'red'])
norm = BoundaryNorm([0, 0.5, 1.5, 2.5], cmap.N)

# Visualisierung vorbereiten
import matplotlib.gridspec as gridspec
fig = plt.figure(figsize=(18, 11))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])
ax = fig.add_subplot(gs[0])
ax_station = fig.add_subplot(gs[1])
plt.ion()
plt.tight_layout()
fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
fs_Title = 18
fs_Text = 13

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
    update(old, new)
    old = new.copy()
    time += 1

    if time % STEP_UPDATES == 0:
        print(time)

    if time % VIS_STEPS == 0:

        # Pedestrians
        ax.cla()
        ax.imshow(old, cmap=cmap, norm=norm)
        if PLOT_MARKERS:
            pedestrian_positions = np.argwhere(old == 2)
            for y, x in pedestrian_positions:
                currID = getPersonID(y, x)
                currAlpha = 1
                if SET_PERSON_VISIBILITY > -1:
                    if currID != SET_PERSON_VISIBILITY:
                        currAlpha = 0.2
                ax.plot(x, y, marker='o', color='red', alpha=currAlpha, markersize=10)
                ax.text(x+7, y-7, str(currID), color='black', alpha=currAlpha, fontsize=10,
                        ha='center', va='center', weight='bold')

            # Path lines
            for person in personalList:
                currID = person['id']
                currAlpha = 1
                if SET_PERSON_VISIBILITY > -1:
                    if currID != SET_PERSON_VISIBILITY:
                        currAlpha = 0.2
                ax.plot([person['currentPos'][1], person['goal'][1]], [person['currentPos'][0], person['goal'][0]], color='red', alpha=currAlpha, linewidth=2)

            # Station-status
            ax_station.clear()
            ax_station.axis('off')
            ax_station.set_title("Stationen & Status", fontsize=fs_Title, fontweight='bold')


            ax_station.text(0.5, 0.97, f"{STATION_ORDER_NAME}", fontsize=fs_Text, weight='bold',va='bottom', ha='center')
            ax_station.text(0.05, 0.9, f"ID:", fontsize=fs_Text, weight='bold', va='bottom', ha='left')
            ax_station.text(0.15, 0.9, f"Name:", fontsize=fs_Text, weight='bold', va='bottom', ha='left')
            ax_station.text(0.35, 0.9, f"Wartezeit\npro Person:", fontsize=fs_Text, weight='bold', va='bottom', ha='left')
            ax_station.text(0.55, 0.9, f"Momentane\nWartezeit", fontsize=fs_Text, weight='bold', va='bottom', ha='left')
            ax_station.text(0.72, 0.9, f"Gesamt\nWartezeit", fontsize=fs_Text, weight='bold',va='bottom', ha='left')
            ax_station.text(0.90, 0.9, f"Anzahl\nPersonen", fontsize=fs_Text, weight='bold',va='bottom', ha='left')

            for station in stationList:
                idx = int(station['index']) - 88
                # Add marker
                ax.plot(station['pos'][0], station['pos'][1], marker='o', color='green', markersize=15)
                ax.text(station['pos'][0], station['pos'][1], str(idx), color='white', fontsize=10, ha='center', va='center', weight='bold')

                persons_at_station = len(station['queue'])
                wait_time = station['current_serv_time']
                full_wait_time = station['full_serv_time']
                default_wait_time = station['serv_time']

                icons = 'o' * min(persons_at_station, 5)
                if persons_at_station > 5:
                    icons += f" +{persons_at_station - 5}"
                y_pos = 0.95 - idx * 0.09
                ax_station.text(0.05, y_pos, f"{idx}:", fontsize=fs_Text, weight='bold', va='center')
                ax_station.text(0.15, y_pos, f"{station['pname']}:", fontsize=fs_Text, weight='bold', va='center')
                ax_station.text(0.35, y_pos, f"{(default_wait_time* TIME_PER_STEP / 60):.0f} min", fontsize=fs_Text, va='center')
                ax_station.text(0.65, y_pos, f"{(wait_time* TIME_PER_STEP / 60):.1f} min", fontsize=fs_Text, va='center', ha='right')
                ax_station.text(0.80, y_pos, f"{(full_wait_time * TIME_PER_STEP / 60):.1f} min", fontsize=fs_Text, va='center', ha='right')
                ax_station.text(0.90, y_pos, icons, fontsize=fs_Text, va='center')


        plt.pause(VIS_PAUSE)

    peopleInSim = checkPeopleRemaining()
    history = saveTickInfo(history)

    # Exit from Loop
    if keyboard.is_pressed('q'):
        break

print(f"Simulation finished in {time} ticks")
plt.ioff()
plt.show()


# Daten-Speicherung
data = {}
metadata = {}
metadata['fullTime'] = time
metadata['stationOrder'] = STATION_ORDER_NAME
stationData = []
for currStation in stationList:
    station = {}
    station['index'] = currStation['index']
    station['pname'] = currStation['pname']
    station['serv_time'] = currStation['serv_time']
    stationData.append(station)
metadata['stationList'] = stationData

data['history'] = history
data['metadata'] = metadata

today = datetime.datetime.now()
data = np.array(data, dtype=object)
np.save(f"saved_simulations/newHaupttestreihe/altstadt_{today.year}-{today.month}-{today.day}-{today.hour}%{today.minute}", data, allow_pickle=True)

showFinalData(data.item())








