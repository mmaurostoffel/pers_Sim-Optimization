import pandas as pd

paths = pd.read_csv("doc/old/paths.csv")

newPaths = []

for i in range(len(paths)):
    curr = paths.iloc[i]
    p1 = curr["point1"]
    p2 = curr["point2"]
    comm = curr["comment"]

    newPaths.append([p1-1,p2-1,comm])

df = pd.DataFrame(newPaths, columns=["point1", "point2", "comment"])
df.to_csv("doc/paths.csv",index=False)