from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

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
    plt.imshow(matrix, cmap='gray', interpolation='nearest')
    plt.axis('off')
    plt.savefig("doc/matrix.png")
    plt.show()



#Image Size: 2058 x 2931 Pixels

# Beispielanwendung
matrix = analyze_image_brightness_grid("doc/Altstadt_detailiert_1000 - bearbeitet.jpg", cell_size=10)
print(matrix)

# Anwendung
plot_matrix(matrix)
