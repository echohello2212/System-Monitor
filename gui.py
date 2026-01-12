
# gui.py
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Tuple
import time
import psutil

import sysinfo
import monitor

class SystemMonitorGUI:
    def __init__(self, root: tk.Tk, refresh_processes_ms: int = 5000, 
                 refresh_timelog_ms: int = 30000, refresh_metrics_ms: int = 2000):
        self.root = root
        self.refresh_processes_ms = refresh_processes_ms
        self.refresh_timelog_ms = refresh_timelog_ms
        self.refresh_metrics_ms = refresh_metrics_ms
        
        # init network tracking variabless for calculating network speed
        self.prev_net_io = None
        self.prev_net_ts = None

        self._build_notebook()
        self._build_tab1()
        self._build_tab2()
        self._build_tab3()
        
        # initial refresh calls
        self.refresh_static_sys_info()
        self.root.after(100, self.update_dynamic_metrics)
        self.root.after(100, self.update_dynamic_processes)
        self.root.after(100, self.update_dynamic_time_log)


    def _build_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="My System")
        self.notebook.add(self.tab2, text="Processes")
        self.notebook.add(self.tab3, text="Time Log")

    # tab1
    def _build_tab1(self):
        container = ttk.Frame(self.tab1, padding=10)
        container.pack(fill='both', expand=True)

        left = ttk.Frame(container)
        right = ttk.Frame(container)
        left.pack(side='left', fill='y', padx=(0, 10))
        right.pack(side='right', fill='both', expand=True)

        # labels
        rows = [
            ("Operating System", "os"),
            ("Architecture", "arch"),
            ("Hostname", "hostname"),
            ("Kernel Version", "kernel"),
            ("CPU Model", "cpu_model"),
            ("CPU Cores", "cpu_cores"),
            ("CPU Threads", "cpu_threads"),
            ("CPU Max Frequency (MHz)", "cpu_freq_max"),
            ("CPU Current Frequency (MHz)", "cpu_freq_cur"),
            ("CPU Usage (%)", "cpu_usage"),
            ("RAM Total (GB)", "ram_total"),
            ("RAM Used (GB)", "ram_used"),
            ("RAM Free (GB)", "ram_free"),
            ("Disk Total (GB)", "disk_total"),
            ("Disk Used (GB)", "disk_used"),
            ("Disk Free (GB)", "disk_free"),
        ]

        self.sys_labels: Dict[str, ttk.Label] = {}
        for r, (label, key) in enumerate(rows):
            ttk.Label(left, text=label).grid(row=r, column=0, sticky='w', pady=2)
            val_lbl = ttk.Label(left, text="—")
            val_lbl.grid(row=r, column=1, sticky='w', pady=2)
            self.sys_labels[key] = val_lbl

        # network interfaces tree on right side
        ttk.Label(right, text="Active Network Interfaces", font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        tree_frame = ttk.Frame(right)
        tree_frame.pack(fill='both', expand=True, pady=(5, 0))
        cols = ("iface", "IPv4", "MAC", "Down (Mbps)", "Up (Mbps)")
        self.iface_tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=10)
        for c in cols:
            self.iface_tree.heading(c, text=c)
        self.iface_tree.column("iface", width=150, anchor='w')
        self.iface_tree.column("IPv4", width=150, anchor='w')
        self.iface_tree.column("MAC", width=170, anchor='w')
        self.iface_tree.column("Down (Mbps)", width=110, anchor='e')
        self.iface_tree.column("Up (Mbps)", width=110, anchor='e')
        self.iface_tree.pack(side='left', fill='both', expand=True)

        yscroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.iface_tree.yview)
        self.iface_tree.configure(yscroll=yscroll.set)
        yscroll.pack(side='right', fill='y')

        # public ip label
        self.public_ip_var = tk.StringVar(value="Public IP: —")
        ttk.Label(right, textvariable=self.public_ip_var).pack(anchor='w', pady=(6, 0))

    def refresh_static_sys_info(self):
        info = sysinfo.get_static_sys_info()  # dict
        # fill left labels with system info
        for key, val in info.items():
            if key in self.sys_labels:
                self.sys_labels[key].config(text=str(val))

        # fill interfaces list with ipv4/mac addresses
        self._refresh_interfaces_static()

        # get public ip from api
        public_ip = sysinfo.get_public_ip()
        self.public_ip_var.set(f"Public IP: {public_ip}")

    def _refresh_interfaces_static(self):
        self.iface_tree.delete(*self.iface_tree.get_children())
        for iface in sysinfo.get_network_interfaces():
            self.iface_tree.insert("", "end",
                                   values=(iface["name"], iface["ipv4"] or "—", iface["mac"] or "—", "—", "—"))

    def update_dynamic_metrics(self):
        # calculate network up/down speed from counters
        # note: sys_info labels are now static and don't update
        now = time.time()
        counters = sysinfo.get_net_io_counters()
        if counters:
            sent, recv = counters
            if self.prev_net_io is not None and self.prev_net_ts is not None:
                delta_t = max(1e-3, now - self.prev_net_ts)
                up_mbps   = monitor.bytes_to_mbps(sent - self.prev_net_io[0], delta_t)
                down_mbps = monitor.bytes_to_mbps(recv - self.prev_net_io[1], delta_t)
                # update treeview with network speeds
                for iid in self.iface_tree.get_children():
                    vals = self.iface_tree.item(iid, "values")
                    if vals and vals[0] == "Total":
                        self.iface_tree.delete(iid)
                self.iface_tree.insert("", "end",
                    values=("Total", "—", "—", f"{down_mbps:.2f}", f"{up_mbps:.2f}"))

            self.prev_net_io = (sent, recv)
            self.prev_net_ts = now

        # schedule next refresh
        self.root.after(self.refresh_metrics_ms, self.update_dynamic_metrics)

    # tab2 
    def _build_tab2(self):
        topbar = ttk.Frame(self.tab2, padding=(10, 10, 10, 0))
        topbar.pack(fill="x")
        ttk.Label(topbar, text="Active Processes", font=('Segoe UI', 11, 'bold')).pack(side="left")

        columns = ("pid", "name", "cpu_percent", "memory_mb")
        tree_frame = ttk.Frame(self.tab2)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=(5, 10))
        self.process_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        self.process_tree.heading("pid", text="PID")
        self.process_tree.heading("name", text="Process Name")
        self.process_tree.heading("cpu_percent", text="CPU %")
        self.process_tree.heading("memory_mb", text="Memory (MB)")

        self.process_tree.column("pid", width=80, anchor='center')
        self.process_tree.column("name", width=300, anchor='w')
        self.process_tree.column("cpu_percent", width=100, anchor='e')
        self.process_tree.column("memory_mb", width=120, anchor='e')

        self.process_tree.pack(side='left', fill='both', expand=True)

        yscroll = ttk.Scrollbar(tree_frame, orient='vertical', command=self.process_tree.yview)
        self.process_tree.configure(yscroll=yscroll.set)
        yscroll.pack(side='right', fill='y')

        # prime cpu percent for processes, first read always returns 0 so need this
        monitor.prep_cpu_perc()

    def update_dynamic_processes(self):
        self.process_tree.delete(*self.process_tree.get_children())

        rows = monitor.list_processes()  # sorted by cpu descending
        for r in rows:
            self.process_tree.insert("", "end",
                                     values=(r["pid"], r["name"], f"{r['cpu_percent']:.1f}", f"{r['memory_mb']:.1f}"))
        self.root.after(self.refresh_processes_ms, self.update_dynamic_processes)

    # tab3 - time log
    def _build_tab3(self):
        container = ttk.Frame(self.tab3, padding=10)
        container.pack(fill='both', expand=True)

        ttk.Label(container, text="Time Log", font=('Segoe UI', 11, 'bold')).pack(side="top", anchor="w")
        text_frame = ttk.Frame(container)
        text_frame.pack(fill='both', expand=True, pady=(5, 0))
        self.time_log_text = tk.Text(text_frame, wrap='none', height=15)
        self.time_log_text.pack(side='left', fill='both', expand=True)

        yscroll = ttk.Scrollbar(text_frame, orient='vertical', command=self.time_log_text.yview)
        self.time_log_text.configure(yscroll=yscroll.set)
        yscroll.pack(side='right', fill='y')

    def update_dynamic_time_log(self):
        ts = monitor.current_timestamp()
        rows = monitor.get_time_log_rows()

        self.time_log_text.delete('1.0', tk.END)
        self.time_log_text.insert(tk.END, f"Uptime of Processes: {ts}\n")
        for r in rows:
            self.time_log_text.insert(
                tk.END,
                f"PID: {r['pid']} | Name: {r['name']} | Uptime: {r['uptime_hhmmss']}\n"
            )
        self.time_log_text.see(tk.END)

        self.root.after(self.refresh_timelog_ms, self.update_dynamic_time_log)
