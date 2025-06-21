import pandas as pd
import numpy as np
import datetime

# Constant Definition
TEST_SETUP = 1

# Variable Setup
if TEST_SETUP == 1:
    short_time = 200 # == 1 Minute
    medium_time = 600 # == 3 Minutes
    long_time = 1000 # == 5 Minutes
else:
    short_time = 2000 # == 10 Minute
    medium_time = 6000 # == 30 Minutes
    long_time = 12000 # == 60 Minutes

# Load Waypoints
WP_LIST = pd.read_csv("../01_create_map_material/doc/waypoints_modified_scaled.csv")

station_file = []
station_order = []

print("Enter time for the station (1 = short, 2 = medium, 3 = long):")
for index, (x, y, comm) in WP_LIST.iterrows():
    if comm != "WP" and not str(comm).startswith("Exit_"):
        station = {}

        time = input(comm + " = ")
        station['index'] = index
        match time:
            case "1":
                station['time'] = short_time
            case "2":
                station['time'] = medium_time
            case "3":
                station['time'] = long_time
            case _:
                print("invalid Time")

        station_file.append(station)

print(station_file)

today = datetime.datetime.now()
scenarioFile = np.array(station_file, dtype=object)
if TEST_SETUP == 1:
    np.save(f"station_files/altstadt_TEST_SETUP_{today.year}-{today.month}-{today.day}-{today.hour}%{today.minute}",scenarioFile, allow_pickle=True)
else:
    np.save(f"station_files/altstadt_{today.year}-{today.month}-{today.day}-{today.hour}%{today.minute}",scenarioFile, allow_pickle=True)
