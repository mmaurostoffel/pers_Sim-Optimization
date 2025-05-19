import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Define constants
CELL_PED = 2   # cell state: pedestrian
CELL_OBS = 1  # cell state: obstacle
CELL_EMP = 0   # cell state: empty

VIS_PAUSE = 0.000001  # time [s] between two visual updates
VIS_STEPS = 2    # stride [steps] between two visual updates
MAX_TIME = 40

# Load Grid
emptyMap = np.load('../01_create_map_material/doc/matrixBaseOutput.npy')
old = emptyMap.copy()
new = old.copy()

GRIDSIZE_X = old.shape[0]
GRIDSIZE_Y = old.shape[1]

# Read starting Positions from scenario file
scenario = pd.read_csv("../02_createScenarios/scenario_files/altstadt_50_5_2025-5-18-13%10.csv")
for index,row in scenario.iterrows():
    x,y = row["startingPos"].strip("[]").split(",")
    old[int(x), int(y)] = CELL_PED


def update(old, new):
    print("")

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







