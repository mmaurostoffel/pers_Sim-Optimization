#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

GRIDSIZE_X = 35
GRIDSIZE_Y = 35
MAX_TIME = 500
NUM_PEDS = 400

CELL_PED = 1   # cell state: pedestrian
CELL_EMP = 0   # cell state: empty
CELL_OBS = -1  # cell state: obstacle

EXIT_X = GRIDSIZE_X+1       # x-coordinate of exit
EXIT_Y = int(GRIDSIZE_Y/2)  # y-coordinate of exit

VIS_PAUSE = 0.000001  # time [s] between two visual updates
VIS_STEPS = 2    # stride [steps] between two visual updates

OBS_obsSize = 6

# count pedestrians left in domain
def count_peds(grid):
    nped = 0
    for x in range(1, GRIDSIZE_X+1):
        for y in range(1, GRIDSIZE_Y+1):
            if grid[x,y] == CELL_PED:
                nped = nped + 1
    return nped

# compute average density [P/m2]
def comp_density(grid):
    dens = 0
    for x in range(1, GRIDSIZE_X+1):
        for y in range(1, GRIDSIZE_Y+1):
            if grid[x,y] == CELL_PED:
                npeds = 0
                for i in range(-1,2):
                    for j in range(-1,2):
                        if grid[x+i,y+j] == CELL_PED:
                            npeds = npeds + 1
                dens = dens + (npeds/1.44)
    if count_peds(grid) != 0:
        return (dens/count_peds(grid))
    else:
        return 0

# state transition t -> t + dt
def update(old, new):
    for x in range(1, GRIDSIZE_X+1):
        for y in range(1, GRIDSIZE_Y+1):
            if old[x,y] == CELL_PED:
                #EXIT_X, EXIT_Y
                delta_x = EXIT_X - x
                delta_y = EXIT_Y - y
                #print(delta_x, delta_y)

                move_x = 1 if delta_x > 0 else -1
                move_y = 1 if delta_y > 0 else -1
                #print(move_x, move_y)

                if np.abs(delta_x) > np.abs(delta_y):
                    #try to move in x first
                    if old[x+move_x][y] == CELL_EMP:
                        # write new Cell
                        new[x+move_x][y] = CELL_PED
                        # block new Cell on old grid
                        old[x+move_x][y] = CELL_OBS

                    elif old[x][y+move_y] == CELL_EMP:
                        # write new Cell
                        new[x][y+move_y] = CELL_PED
                        # block new Cell on old grid
                        old[x][y+move_y] = CELL_OBS
                    else:
                        new[x][y] = CELL_PED
                else:
                    #try to move in y first
                    if old[x][y+move_y] == CELL_EMP:
                        # write new Cell
                        new[x][y+move_y] = CELL_PED
                        # block new Cell on old grid
                        old[x][y+move_y] = CELL_OBS

                    elif old[x+move_x][y] == CELL_EMP:
                        # write new Cell
                        new[x+move_x][y] = CELL_PED
                        # block new Cell on old grid
                        old[x+move_x][y] = CELL_OBS
                    else:
                        new[x][y] = CELL_PED

def setObstacle(grid):
    for i in range(3):
        for j in range(3):
            for x in range(OBS_obsSize):
                for y in range(OBS_obsSize):
                    xStart = 6 + i *10
                    yStart = 6 + j * 10
                    grid[xStart + x,yStart + y] = CELL_OBS

    return grid


# allocate memory and initialise grids
old = np.zeros((GRIDSIZE_X+2, GRIDSIZE_Y+2), dtype=np.int32)
new = np.zeros((GRIDSIZE_X+2, GRIDSIZE_Y+2), dtype=np.int32)
old[:,0] = CELL_OBS   # boundary: south
old[:,-1] = CELL_OBS  # boundary: north
old[0,:] = CELL_OBS   # boundary: west
old[-1,:] = CELL_OBS  # boundary: east
old = setObstacle(old)
old[EXIT_X,EXIT_Y-1] = CELL_EMP  # exit
old[EXIT_X,EXIT_Y] = CELL_EMP    # exit
old[EXIT_X,EXIT_Y+1] = CELL_EMP  # exit
new = old.copy()

# set random starting points for pedestrians
for i in range(NUM_PEDS):
    while True:
        x = int(float(GRIDSIZE_X)*np.random.random())+1
        y = int(float(GRIDSIZE_Y)*np.random.random())+1
        if old[x,y] == CELL_EMP:
            old[x,y] = CELL_PED
            break

# run updates
time = 0
dens = []
plt.ion()
plt.imshow(np.rot90(old, 1))
plt.pause(VIS_PAUSE)
while count_peds(old) > 0 and time < MAX_TIME:
    new[1:GRIDSIZE_X+1,1:GRIDSIZE_Y+1] = CELL_EMP
    update(old, new)
    new[EXIT_X,EXIT_Y-1] = CELL_EMP  # clear exit
    new[EXIT_X,EXIT_Y] = CELL_EMP    # clear exit
    new[EXIT_X,EXIT_Y+1] = CELL_EMP  # clear exit
    old = new.copy()
    old = setObstacle(old)
    numpeds = count_peds(old)
    dens.append(comp_density(old))
    time = time + 1
    if time%VIS_STEPS == 0:
      plt.clf()
      plt.imshow(np.rot90(old, 1))
      plt.pause(VIS_PAUSE)
plt.ioff()
print(f'Evacuation of {NUM_PEDS} persons done in {time*0.3:.2f} seconds')

# plot density diagramm
x = np.linspace(0,time*.3,time)
plt.clf()
plt.xlabel('Zeit [s]')
plt.ylabel('Dichte [P/m2]')
plt.plot(x, dens, 'r-')
plt.show()
