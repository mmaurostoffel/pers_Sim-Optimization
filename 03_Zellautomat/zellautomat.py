import numpy as np
import matplotlib.pyplot as plt

# Define constants
CELL_PED = 1   # cell state: pedestrian
CELL_EMP = 0   # cell state: empty
CELL_OBS = -1  # cell state: obstacle

VIS_PAUSE = 0.000001  # time [s] between two visual updates
VIS_STEPS = 2    # stride [steps] between two visual updates
MAX_TIME = 500

# Load Grid
old = np.load('../01_create_map_material/doc/matrixBaseOutput.npy')
new = old.copy()

GRIDSIZE_X = old.shape[0]
GRIDSIZE_Y = old.shape[1]

# Read starting Positions from scenario file


# Definitions
def count_peds(grid):
    nped = 0
    for x in range(1, GRIDSIZE_X+1):
        for y in range(1, GRIDSIZE_Y+1):
            if grid[x, y] == CELL_PED:
                nped = nped + 1
    return nped

# Main update Loop
time = 0
dens = []
# plt.ion()
plt.imshow(np.rot90(old, 1))
plt.pause(VIS_PAUSE)

# while count_peds(old) > 0 and time < MAX_TIME:


