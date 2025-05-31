import pandas as pd
import numpy as np
import datetime

# Load Waypoints
WP_LIST = pd.read_csv("../01_create_map_material/doc/waypoints_modified_scaled.csv")

station_file = []

for index, (x, y, comm) in WP_LIST.iterrows():
    if comm != "WP" and not str(comm).startswith("Exit_"):
        station = {}
        time = input("Enter time for the station: "+comm)
        station['index'] = index
        station['time'] = time

        station_file.append(station)

print(station_file)

today = datetime.datetime.now()
scenarioFile = np.array(station_file, dtype=object)
np.save(f"station_files/altstadt_{today.year}-{today.month}-{today.day}-{today.hour}%{today.minute}",scenarioFile, allow_pickle=True)
