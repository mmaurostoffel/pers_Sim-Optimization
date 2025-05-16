from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def analyze_image_brightness_grid(image_path, cell_size=10, threshold=230):
    # Bild öffnen und in Graustufen umwandeln
    image = Image.open(image_path).convert("L")  # "L" = grayscale

    width, height = image.size

    # Größe des Rasters
    cols = width // cell_size
    rows = height // cell_size

    # Ergebnis-Matrix
    result = np.zeros((rows, cols), dtype=int)

    # Durchlaufe jede Rasterzelle
    for row in range(rows):
        for col in range(cols):
            x0 = col * cell_size
            y0 = row * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            # Ausschnitt der Zelle
            cell = image.crop((x0, y0, x1, y1))
            avg_brightness = np.mean(np.array(cell))

            # Schwelle anwenden
            result[row, col] = 1 if avg_brightness > threshold else 0

    return result


def plot_matrix(matrix):
    #wall, path, waypoint, marker
    colors = ["black", "white", "green", "red"]
    cmap = ListedColormap(colors)
    plt.imshow(matrix, cmap=cmap, interpolation='nearest')
    plt.axis('off')
    plt.savefig("doc/matrix.png")
    plt.show()

def addWaypoints(matrix):
    wp = pd.read_csv("doc/waypoints_modified_scaled.csv")
    for item in wp.iterrows():
        x, y, comment = item[1]
        if comment != "WP":
            pointvalue = 2
        else:
            pointvalue = 3
        matrix = addCentralPoint(matrix, x, y, pointsize=3, pointvalue = pointvalue)
    return matrix

def addMarkers(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if i % 50 == 0 and j % 50 == 0:
                matrix = addPoint(matrix, j, i, pointsize=3, pointvalue=4)
    return matrix

def addPoint(matrix, x, y, pointsize = 2, pointvalue = 2):
    for i in range(pointsize):
        for j in range(pointsize):
            matrix[y+i][x+j] = pointvalue
    return matrix

def addCentralPoint(matrix, x, y, pointsize = 3, pointvalue = 2):
    for i in range(pointsize):
        for j in range(pointsize):
            matrix[y+i-1][x+j-1] = pointvalue
    return matrix


# Beispielanwendung
#matrix = analyze_image_brightness_grid("doc/Altstadt_detailiert_1000 - bearbeitet.jpg", cell_size=5)
matrix = analyze_image_brightness_grid("doc/Altstadt_detailiert_1000 - bearbeitet - skaliert.jpg", cell_size=5)
print(matrix)

print(matrix.shape)


# Add Waypoints
# matrix = addMarkers(matrix)
matrix = addWaypoints(matrix)
np.save("doc/matrixOutput", matrix, allow_pickle=True)

# Anwendung
plot_matrix(matrix)
