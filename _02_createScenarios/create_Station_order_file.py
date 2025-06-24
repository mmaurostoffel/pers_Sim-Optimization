import datetime
import numpy as np

station_order = [94, 91, 90, 97, 95, 89, 98, 92, 96, 93]

today = datetime.datetime.now()
np.save(f"statio_order_fils/altstadt_STATION_ORDER_{today.year}-{today.month}-{today.day}-{today.hour}%{today.minute}",station_order, allow_pickle=True)