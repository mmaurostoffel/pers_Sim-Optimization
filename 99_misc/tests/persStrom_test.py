import numpy as np
import matplotlib.pyplot as plt

GRIDSIZE_X = 200
GRIDSIZE_Y = 35
MAX_TIME = 1000
NUM_PEDS = 300

CELL_PED_2 = 2   # cell state: pedestrian
CELL_PED_1 = 1   # cell state: pedestrian
CELL_EMP = 0   # cell state: empty
CELL_OBS = -1  # cell state: obstacle

VIS_PAUSE = 0.000001  # time [s] between two visual updates
VIS_STEPS = 2    # stride [steps] between two visual updates

# state transition t -> t + dt
def update(old, new):
    for x in range(GRIDSIZE_X):
        for y in range(1, GRIDSIZE_Y+1):
            if old[x,y] == CELL_PED_1 or old[x, y] == CELL_PED_2:
                if old[x, y] == CELL_PED_1:
                    # walking right
                    if old[(x+1) % GRIDSIZE_X, y] == CELL_EMP:
                        new[(x+1) % GRIDSIZE_X, y] = CELL_PED_1
                        old[(x + 1) % GRIDSIZE_X, y] = CELL_OBS
                    else:
                        if int(np.random.random() + 0.5) == 1:
                            move = 1
                        else:
                            move = -1
                        if old[x, y+move] == CELL_EMP:
                            new[x, y+move] = CELL_PED_1
                            old[x, y+move] = CELL_OBS
                        elif old[x, y-move] == CELL_EMP:
                            new[x, y-move] = CELL_PED_1
                            old[x, y-move] = CELL_OBS
                        else:
                            new[x, y] = CELL_PED_1
                            old[x, y] = CELL_OBS
                else:
                    # walking left
                    if old[(x-1+GRIDSIZE_X) % GRIDSIZE_X, y] == CELL_EMP:
                        new[(x-1+GRIDSIZE_X) % GRIDSIZE_X, y] = CELL_PED_2
                        old[(x - 1 + GRIDSIZE_X) % GRIDSIZE_X, y] = CELL_OBS
                    else:
                        if int(np.random.random() + 0.5) == 1:
                            move = 1
                        else:
                            move = -1
                        if old[x, y + move] == CELL_EMP:
                            new[x, y + move] = CELL_PED_2
                            old[x, y + move] = CELL_OBS
                        elif old[x, y - move] == CELL_EMP:
                            new[x, y - move] = CELL_PED_2
                            old[x, y - move] = CELL_OBS
                        else:
                            new[x, y] = CELL_PED_2
                            old[x, y] = CELL_OBS


# allocate memory and initialise grids
old = np.zeros((GRIDSIZE_X, GRIDSIZE_Y+2), dtype=np.int32)
new = np.zeros((GRIDSIZE_X, GRIDSIZE_Y+2), dtype=np.int32)
old[:,0] = CELL_OBS   # boundary: south
old[:,-1] = CELL_OBS  # boundary: north
new = old.copy()

# set random starting points for pedestrians
for i in range(NUM_PEDS):
    while True:
        x = int(float(GRIDSIZE_X)*np.random.random())
        y = int(float(GRIDSIZE_Y)*np.random.random())+1
        if old[x,y] == CELL_EMP:
            old[x,y] = CELL_PED_1
            break
    while True:
        x = int(float(GRIDSIZE_X)*np.random.random())
        y = int(float(GRIDSIZE_Y)*np.random.random())+1
        if old[x,y] == CELL_EMP:
            old[x,y] = CELL_PED_2
            break


# run updates
time = 0
dens = []
plt.ion()
plt.imshow(np.rot90(old, 1))
plt.pause(VIS_PAUSE)
while time < MAX_TIME:
    new[:, 1:GRIDSIZE_Y+1] = CELL_EMP
    update(old, new)
    old = new.copy()
    time = time + 1
    if time%VIS_STEPS == 0:
      plt.clf()
      plt.imshow(np.rot90(old, 1))
      plt.pause(VIS_PAUSE)
plt.ioff()

