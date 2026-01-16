Process Monitor

Purpose:
Process Monitor helps users maintain a baseline of normal system activity by making it easy to view real‑time system information, running processes, and network behavior. Its simple interface replaces complex command‑line tools, allowing users to quickly spot suspicious programs or unusual system activity. The ability to export system data to a JSON file also makes it easier to request help from IT or security professionals by providing accurate, ready‑to‑share information.

Features:
- System Information: View OS details, CPU, RAM, and disk usage
- Process Monitoring: See active processes sorted by CPU usage
- Network Monitoring: Display active network interfaces and speeds
- Time Log: View system uptime and process uptimes
- Export to JSON: Save all system data to a JSON file

Requirements:
- Windows OS
- Python 3.x
- psutil
- requests
- tkinter (usually included with Python)

How to Run:
1. Install dependencies: pip install psutil requests
2. Run the application: python main.py
   OR double-click: Run System Monitor.bat

Files:
- main.py - Entry point, starts the application
- gui.py - GUI interface and main application logic
- sysinfo.py - Functions to gather system information
- monitor.py - Process monitoring and utility functions
- Run System Monitor.bat - Batch file to launch the application
- README.md - This file

Usage:
- Tab 1 (My System): View system specs and network interfaces. Click "Export to JSON" to save all data.
- Tab 2 (Processes): View running processes sorted by CPU usage
- Tab 3 (Time Log): View system uptime and individual process uptimes

Note: Error handling improvements needed for better user experience.

Potential Updates:

1. Cross-Platform Compatibility
- macOS support: Add error handling and platform checks for macOS systems
- Linux support: Test and verify network interface detection works properly on Linux
- Create shell scripts for Linux/Mac (.sh files) alongside the Windows .bat file

2. CPU Usage Notifications
- Alert popup/notification when CPU usage exceeds a configurable threshold (e.g., 80%, 90%)
- User-configurable threshold setting
- Option to show alerts for individual process CPU usage

3. Runtime Notifications
- Alert popup/notification when a process reaches a configurable runtime (e.g., 24 hours, 48 hours)
- User-configurable time threshold
- Option to alert only for specific processes

4. System Processes Toggle
- Toggle button to show/hide system processes
- Filter out system processes (e.g., Windows system services, kernel processes)
- Remember toggle state across sessions

Project Structure:

    Process-Monitor/
    │
    ├── main.py                        # Entry point; starts the application
    ├── gui.py                         # GUI interface and main application logic
    ├── sysinfo.py                     # System information functions
    ├── monitor.py                     # Process monitoring utilities
    │
    ├── Run System Monitor.bat         # Windows launcher
    ├── README.md                      # Documentation file
    │
    └── Screenshot.png                 # Application screenshot
