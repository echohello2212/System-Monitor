#main

# Ser bra ut! Se till att uppdatera din readme.md med Funktion, Syfte, Systemkrav, Instruktioner!

import tkinter as tk
from gui import SystemMonitorGUI

# refresh intervals in milliseconds
REFRESH_METRICS_MS   = 2000   # cpu usage + net speed
REFRESH_PROCESSES_MS = 5000   # process table
REFRESH_TIMELOG_MS   = 30000  # time log

def main():
    root = tk.Tk()
    root.title("Process Monitor")

    # create gui and pass refresh intervals
    app = SystemMonitorGUI(
        root,
        refresh_processes_ms=REFRESH_PROCESSES_MS,
        refresh_timelog_ms=REFRESH_TIMELOG_MS,
        refresh_metrics_ms=REFRESH_METRICS_MS,
    )

    root.mainloop()

if __name__ == "__main__":
    main()
