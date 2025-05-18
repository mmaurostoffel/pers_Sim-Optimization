import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

'''
05/05/2025	12/05/2025	Zellautomat
06/05/2025	13/05/2025	Ausgangslagen
07/05/2025	14/05/2025	Adjazenzmatrizen
08/05/2025	15/05/2025	Path-Finding
09/05/2025	16/05/2025	Test Path-Finding
10/05/2025	17/05/2025	Endprodukt
11/05/2025	18/06/2025	Test Endprodukt
12/05/2025	25/07/2025	Resultat/Doku

Start Master 5. Mai
Ende Master 25.Juli
'''




# Sample task data with (Task Name, Start Date, End Date)
tasks = [
    ("Resultat/Doku", "5-5-2025", "25-7-2025"),
    ("Test Endprodukt", "12-6-2025", "5-7-2025"),
    ("Endprodukt", "7-6-2025", "17-6-2025"),
    ("Test Path-Finding", "30-5-2025", "7-6-2025"),
    ("Path-Finding", "24-5-2025", "1-6-2025"),
    ("Adjazenzmatrizen", "5-5-2025", "24-5-2025"),
    ("Ausgangslagen", "5-5-2025", "20-5-2025"),
    ("Zellautomat", "5-5-2025", "17-5-2025"),
]
# Convert string dates to datetime objects
def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, "%d-%m-%Y")

tasks = [(task[0], str_to_date(task[1]), str_to_date(task[2])) for task in tasks]

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 5))

# Plot tasks
y_pos = range(len(tasks))
for i, (task, start, end) in enumerate(tasks):
    p = ax.barh(task, (end - start).days, left=start, color='skyblue', edgecolor='black')
    ax.bar_label(p, label_type='center')

# Format x-axis
ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))  # Tick every 5 days
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
ax.axvline(str_to_date("25-7-2025"), color='red', linestyle="--", linewidth=2, label="Ende Master")
plt.text(str_to_date("14-7-2025"),6.5,"Meilenstein 3:\nEnde Master\n", c='r')
ax.axvline(str_to_date("07-06-2025"), color='red', linestyle="--", linewidth=2, label="Abschluss der Zellautomaten")
plt.text(str_to_date("08-06-2025"),6.5,"Meilenstein 2:\nAbschluss des \nPath-Finding", c='r')
ax.axvline(str_to_date("24-05-2025"), color='red', linestyle="--", linewidth=2, label="Abschluss des Path-Finding")
plt.text(str_to_date("25-05-2025"),6.5,"Meilenstein 1:\nAbschluss des \nZellautomaten", c='r')



plt.xticks(rotation=45)
plt.xlabel("Datum")
plt.ylabel("Arbeitsschritte")
plt.title("Meilensteine Masterarbeit")
plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("gantt_chart.png")