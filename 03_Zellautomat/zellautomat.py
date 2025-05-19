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

# Read starting Positions from scenario file
scenario = pd.read_csv("../02_createScenarios/scenario_files/altstadt_50_5_2025-5-18-13%10.csv")
for index,row in scenario.iterrows():
    x,y = row["startingPos"].strip("[]").split(",")
    old[int(x), int(y)] = CELL_PED


def update(old, new):
    print("")

def update(old, new):
    for x in range(GRIDSIZE_X):
        for y in range(GRIDSIZE_Y):
            if old[x, y] == CELL_PED:
                if old[(x + 1) % GRIDSIZE_X, y] == CELL_EMP:
                    new[(x + 1) % GRIDSIZE_X, y] = CELL_PED
                    old[(x + 1) % GRIDSIZE_X, y] = CELL_OBS
                else:
                    if old[x, y] == CELL_EMP:
                        new[x, y] = CELL_PED
                        old[x, y] = CELL_OBS
                    elif old[x, y] == CELL_EMP:
                        new[x, y] = CELL_PED
                        old[x, y] = CELL_OBS
                    else:
                        new[x, y] = CELL_PED
                        old[x, y] = CELL_OBS

time = 0
dens = []

colors = ["black", "white", "green"]
cmap = ListedColormap(colors)
plt.ion()
# plt.imshow(np.rot90(old, 1))
plt.imshow(old, cmap=cmap, interpolation='nearest')
plt.pause(VIS_PAUSE)
while time < MAX_TIME:
    new = emptyMap.copy()
    update(old, new)
    old = new.copy()
    time = time + 1
    if time%VIS_STEPS == 0:
      plt.clf()
      # plt.imshow(np.rot90(old, 1))
      plt.imshow(old, cmap=cmap, interpolation='nearest')
      plt.pause(VIS_PAUSE)
plt.ioff()

# while count_peds(old) > 0 and time < MAX_TIME:







