import numpy as np
import pandas as pd

wp = pd.read_csv("doc/waypoints_modified_scaled.csv")
paths = pd.read_csv("doc/paths.csv")

# Create Adjacency Matrix
adj_matrix = np.zeros((len(wp), len(wp)), dtype=float)
df = pd.DataFrame(adj_matrix)

for i in range(len(paths)):
    curr = paths.iloc[i]
    #print(curr["point1"], curr["point2"], curr["comment"])

    p1 = curr["point1"]
    p2 = curr["point2"]

    p1_Korr = wp.iloc[p1-1]
    p2_Korr = wp.iloc[p2-1]
    #print(p1_Korr, p2_Korr)

    dist = np.sqrt(np.square(p1_Korr["x"] - p2_Korr["x"]) + np.square(p2_Korr["y"] - p1_Korr["y"]))
    print(p1, p2, dist)

    df.at[p1, p2] = round(dist,1)
    df.at[p2, p1] = round(dist,1)

print(df)
df.to_csv("doc/adjacencyMatrix", index=False)

