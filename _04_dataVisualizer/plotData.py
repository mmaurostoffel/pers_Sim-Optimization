import matplotlib.pyplot as plt
def showFinalData(data):
    history = data.history
    # Extract time and station wait times
    times = [entry['time'] for entry in history]
    station_waits = list(zip(*[entry['stationWaitTimes'] for entry in history]))

    # Plot each station's wait times
    plt.figure(figsize=(12, 6))
    for i, wait_times in enumerate(station_waits):
        plt.plot(times, wait_times, label=f'Station {i}')

    plt.xlabel('Time')
    plt.ylabel('Wait Time')
    plt.title('Station Wait Times Over Time')
    plt.legend(loc='upper right', ncol=2)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

