import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Define constants
CELL_PED = 2   # cell state: pedestrian
CELL_OBS = 0  # cell state: obstacle
CELL_EMP = 1   # cell state: empty

VIS_PAUSE = 0.000001  # time [s] between two visual updates
VIS_STEPS = 2    # stride [steps] between two visual updates
MAX_TIME = 200

# Load Grid
emptyMap = np.load('../01_create_map_material/doc/matrixBaseOutput.npy')
old = emptyMap.copy()
new = old.copy()

GRIDSIZE_X = emptyMap.shape[0]
GRIDSIZE_Y = emptyMap.shape[1]


################## Temporary ##################
EXIT_X = GRIDSIZE_X
EXIT_Y = GRIDSIZE_Y / 2
################## Temporary ##################

# Read starting Positions from scenario file
scenario = pd.read_csv("../02_createScenarios/scenario_files/altstadt_50_5_2025-5-18-13%10.csv")
for index,row in scenario.iterrows():
    x,y = row["startingPos"].strip("[]").split(",")
    old[int(x), int(y)] = CELL_PED

#def update(old, new):
#    print("")

def update(old, new):
    for x in range(1,GRIDSIZE_X-1):
        for y in range(1,GRIDSIZE_Y-1):
            if old[x, y] == CELL_PED:
                x_dist = x-EXIT_X
                x_move = 1 if x_dist > 0 else -1
                y_dist = y-EXIT_Y
                y_move = 1 if y_dist > 0 else -1
                if abs(x_dist) > abs(y_dist):
                    if old[(x + x_move), y] == CELL_EMP:
                        new[(x + x_move), y] = CELL_PED
                        old[(x + x_move), y] = CELL_OBS
                    elif old[x, (y + y_move)] == CELL_EMP:
                        new[x, (y + y_move)] = CELL_PED
                        old[x, (y + y_move)] = CELL_OBS
                    else:
                        new[x, y] = CELL_PED
                        old[x, y] = CELL_OBS
                else:
                    if old[x, (y + y_move)] == CELL_EMP:
                        new[x, (y + y_move)] = CELL_PED
                        old[x, (y + y_move)] = CELL_OBS
                    elif old[(x + x_move), y] == CELL_EMP:
                        new[(x + x_move), y] = CELL_PED
                        old[(x + x_move), y] = CELL_OBS
                    else:
                        new[x, y] = CELL_PED
                        old[x, y] = CELL_OBS


time = 0
dens = []

colors = ["black", "white", "green"]
cmap = ListedColormap(colors)
plt.ion()
#plt.imshow(old, cmap=cmap, interpolation='nearest')
plt.imshow(old[100:50, 1:100], cmap=cmap, interpolation='nearest')
plt.pause(VIS_PAUSE)
while time < MAX_TIME:
    new = emptyMap.copy()
    update(old, new)
    old = new.copy()
    time = time + 1
    if time%VIS_STEPS == 0:
      plt.clf()
      #plt.imshow(old, cmap=cmap, interpolation='nearest')
      plt.imshow(old[100:500, 1:100], cmap=cmap, interpolation='nearest')
      plt.pause(VIS_PAUSE)
plt.ioff()

# while count_peds(old) > 0 and time < MAX_TIME:







