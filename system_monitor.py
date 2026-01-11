
###GUI#####
class SystemMonitorGUI:
    def __init__(self, root):
        self.root=root
        self.root.title("System Monitor")

        self.notebook=ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        #expands notebook to fill the window horizontally+vertically

        self.tab1=ttk.Frame(self.notebook)
        self.tab2=ttk.Frame(self.notebook)
        self.tab3=ttk.Frame(self.notebook)
        #created 3 tabs as frames

        self.notebook.add(self.tab1, text="My System")
        self.notebook.add(self.tab2, text="Processes")
        self.notebook.add(self.tab3, text="Time Log")
        #added tabs to notebook with text labels

        self.build_tab1()
        self.build_tab2()
        self.build_tab3()

        self.refresh_static_sys_info()
        self.update_dynamic_processes()
        self.update_dynamic_time_log()

    ##### TAB 1 BUILD #####
    def build_tab1(self):
        #
        left=ttk.Frame(self.tab1, padding=10)
        left.pack(side='left', fill='y')

        #
        right=ttk.Frame(self.tab1, padding=10)
        right.pack(side='right', fill='y')

        self.sys_labels={}
        rows=[
            ("Operating System" or "OS"),
            ("Architecture" or "Arch"),
            ("Hostname" or "Host"),
            ("Kernel Version" or "Kernel"),
            ("CPU Model" or "cpu_model"),
            ("CPU Cores" or "cpu_cores"),
            ("CPU Threads" or "cpu_threads"),
            ("CPU Max Frequency (MHz)" or "cpu_freq_max"),
            ("CPU Current Frequency (MHz)" or "cpu_freq_cur"),
            ("CPU Usage (%)" or "cpu_usage"),
            ("RAM Total (GB)" or "ram_total"),
            ("RAM Used (GB)" or "ram_used"),
            ("RAM Free (GB)" or "ram_free"),
            ("Disk Total (GB)" or "disk_total"),
            ("Disk Used (GB)" or "disk_used"),
            ("Disk Free (GB)" or "disk_free"),
        ]

        #interface tree network info
        self.iface_tree=ttk.Treeview(
            right,
            columns=("iface", "IPv4", "MAC"),
            show='headings',
            height=10
        )
        self.iface_tree.heading("iface", text="Interface")
        self.iface_tree.heading("IPv4", text="IPv4 Address")
        self.iface_tree.heading("MAC", text="MAC Address")
        self.iface_tree.column("iface", width=150, anchor='w')
        self.iface_tree.column("IPv4", width=150, anchor='w')
        self.iface_tree.column("MAC", width=150, anchor='w')
        self.iface_tree.column("downspeedmbps", width=100, anchor='e')
        self.iface_tree.column("upspeedmbps", width=100, anchor='e')
        self.iface_tree.pack(fill='both', expand=True)

        yscroll=ttk.Scrollbar(self.right, orient='vertical', command=self.iface_tree.yview)
        self.iface_tree.configure(yscroll=yscroll.set)
        yscroll.pack(in_=self.iface_tree, relx=1.0, rely=0, relheight=1.0, anchor="ne")

    def get_sys_info():
    #OS 
    os_info=f"{platform.system()} {platform.release()}"
    arch= platform.architecture()[0] 
    #tells whether 32 or 64 bit
    hostname=socket.gethostname()
    kernel=platform.version()

    #CPU
    cpu_model=platform.processor()
    cpu_cores=psutil.cpu_count(logical=False)
    cpu_threads=psutil.cpu_count(logical=True)
    #CPU model, cores, threads
    cpu_freq=psutil.cpu_freq().max
    cpu_freq_cur=psutil.cpu_freq().current
    #CPU max,current frequency in MHz
    cpu_usage=psutil.cpu_percent(interval=1)
    #current CPU usage percentage

    #RAM
    ram=psutil.virtual_memory()
    ram_total=round(ram.total/(1024**3),2)
    ram_used=round(ram.used/(1024**3),2)
    ram_free=round(ram.available/(1024**3),2)
    #RAM total, used, free in GB

    #Storage
    if platform.system()=='Windows':
        disk=psutil.disk_usage('C:\\')
    else:
        disk=psutil.disk_usage('/')
    #Checks C:\\ or / based on OS
    disk_total=round(disk.total/(1024**3),2)
    disk_used=round(disk.used/(1024**3),2)
    disk_free=round(disk.free/(1024**3),2)
    #Storage total, used, free in GB

    ###Set labels
    self.sys_labels["os"].config(text=os_info)
    self.sys_labels["arch"].config(text=arch)
    self.sys_labels["hostname"].config(text=hostname)
    self.sys_labels["kernel"].config(text=kernel)
    self.sys_labels["cpu_model"].config(text=cpu_model)
    self.sys_labels["cpu_cores"].config(text=str(cpu_cores))
    self.sys_labels["cpu_threads"].config(text=str(cpu_threads))
    self.sys_labels["cpu_freq_max"].config(text=str(cpu_freq))
    self.sys_labels["cpu_freq_cur"].config(text=str(cpu_freq_cur))
    self.sys_labels["cpu_usage"].config(text=str(cpu_usage))
    self.sys_labels["ram_total"].config(text=str(ram_total))
    self.sys_labels["ram_used"].config(text=str(ram_used))
    self.sys_labels["ram_free"].config(text=str(ram_free))
    self.sys_labels["disk_total"].config(text=str(disk_total))
    self.sys_labels["disk_used"].config(text=str(disk_used))
    self.sys_labels["disk_free"].config(text=str(disk_free))


    ##network
    def get_network_info():
        ##delete previously stored network info
        for row in self.iface_tree.get_children():
            self.iface_tree.delete(row)
        
        ##collect macs af link is winows/macs, af packet is for linux
        AF_LINK = getattr(psutil, "AF_LINK", None)
        AF_PACKET = getattr(socket, "AF_PACKET", None)

        ##only shows active interfaces
        for iface, addrs in psutil.net_if_addrs().items():
            stats = psutil.net_if_stats().get(iface)
            if not stats or not stats.isup:
                continue

            ipv4 = None
            mac = None

            for addr in addrs:
                if addr.family == socket.AF_INET:      # IPv4
                    ipv4 = addr.address
                if addr.family == AF_LINK or addr.family == AF_PACKET:      # MAC
                    mac = addr.address
            self.iface_tree.insert("", "end", values=(iface, ipv4, mac))
        
        #public ip
        public_ip_display = getattr(self, "public_ip", "—")
        self.iface_tree.insert("", "end", values=("Public", public_ip_display, "N/A"))

        #up/down speed

    def get_public_ip():
        ip = "—"
        try:
            response = requests.get("https://api.ipify.org", timeout=5)
            if response.status_code == 200:
                ip = response.text
        except requests.RequestException:
            pass
        self.public_ip = ip
    
    def get_speed():
        counterstart=psutil.net_io_counters()
        time.sleep(1)
        counterfinish=psutil.net_io_counters()

        upspeedmbps=(counterfinish.bytes_sent - counterstart.bytes_sent)*8/1e6
        downspeedmbps=(counterfinish.bytes_recv - counterstart.bytes_recv)*8/1e6
        #Upload and download speed in Mbps

def build_tab2(self):
    #
    topbar=ttk.Frame(self.tab2, padding=10,10,10,0)
    topbar.pack(fill="x")
    ttk.Label(topbar, text="Active Processes",
              font="SegoeUI 11 bold").pack(side="left")
    #
    collumns=("pid", "name", "cpu_percent", "memory_mb",)
    self.process_tree=ttk.Treeview(self.tab2, columns=collumns,
                                   show='headings', height=15)
    self.process_tree.pack(fill='both', expand=True,padx=10, pady=5,10)

    #
    self.process_tree.heading("pid", text="PID")
    self.process_tree.heading("name", text="Process Name")
    self.process_tree.heading("cpu_percent", text="CPU %")
    self.process_tree.heading("memory_mb", text="Memory (MB)")

    #
    self.process_tree.column("pid", width=80, anchor='center')
    self.process_tree.column("name", width=250, anchor='w')
    self.process_tree.column("cpu_percent", width=100, anchor='e')
    self.process_tree.column("memory_mb", width=120, anchor='e')

    #scrollbar
    yscroll=ttk.Scrollbar(self.tab2, orient='vertical', command=self.process_tree.yview)
    self.process_tree.configure(yscroll=yscroll.set)
    yscroll.pack(in_=self.process_tree, relx=1.0, rely=0, relheight=1.0, anchor="ne")

    #
    for p in psutil.process_iter():
        try:
            p.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    def update_process_dynamic(self):
        for row in self.process_tree.get_children():
            self.process_tree.delete(row)

        for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                self.process_tree.insert("", "end", values=(
                    p.info['pid'],
                    p.info['name'],
                    round(p.info['cpu_percent'], 2),
                    round(p.info['memory_info'].rss / (1024**2), 2)
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

            #sort by cpu percent
        rows.sort(key=lambda r: float(r[2]), reverse=True)
        for pid, name, cpu_percent, memory_mb in rows[:number_of_processes]:
            self.process_tree.insert("", "end", values=(pid, name, f"{cpu_percent:.1f}", f"{memory_mb:.1f}"))
            self.root.after(refresh_processes_ms, self.update_process_dynamic)

def build_tab3(self):
    container=ttk.Frame(self.tab3, padding=10)
    container.pack(fill='both', expand=True)

    ttk.Label(container, text="Time Log",
              font="SegoeUI 11 bold").pack(side="top", anchor="w")
    self.time_log_text=tk.Text(container, wrap='none', height=15)
    self.time_log_text.pack(fill='both', expand=True, pady=(5,0))

    #scrollbar
    yscroll=ttk.Scrollbar(container, orient='vertical',
                         command=self.time_log_text.yview)
    self.time_log_text.configure(yscroll=yscroll.set)
    yscroll.pack(in_=self.time_log_text, relx=1.0, rely=0, 
                relheight=1.0, anchor="ne")
    
    def update_time_log_dynamic(self):
        ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        now=time.time()
        rows=[]

        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                ct=proc.info['create_time']#process creation time
                if not ct:
                    continue
                uptime_sec=max(0, time.time() - ct)
                uptime_hrs=_fmt_hhmmss(uptime_sec)
                name=proc.info.get('name', 'N/A')
                pid=proc.info.get('pid', 'N/A')
                rows.append((pid, name, uptime_hrs))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        rows.sort(key=lambda r: r[0], reverse=True)

        #refresh list
        self.time_log_text.delete('1.0', tk.END)
        self.time_log_text.insert(tk.END, f"Uptime of Processes: {ts}\n")

        for uptime_hrs, pid, name in rows:
            self.time_log_text.insert(tk.END, f"PID: {pid} | Name: {name} | Uptime: {uptime_hrs}\n")
            self.time_log_text.see(tk.END)

        self.root.after(refresh_time_log_ms, self.update_time_log_dynamic)

#imports#
import psutil
import platform
import datetime
import time
import socket
import requests
import wmi #only for windows antivirus

refresh_processes_ms=5000 #5 seconds
refresh_time_log_ms=30000 #30 seconds
number_of_processes=40 #number of processes to show in process tab
def _fmt_hhmmss(seconds):
    hrs, rem = divmod(seconds, 3600)
    mins, secs = divmod(rem, 60)
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02}"

##### TAB 1 CONTENT #####
def get_sys_info(self):
    #OS 
    os_info=f"{platform.system()} {platform.release()}"
    arch= platform.architecture()[0] 
    #tells whether 32 or 64 bit
    hostname=socket.gethostname()
    kernel=platform.version()

    #CPU
    cpu_model=platform.processor()
    cpu_cores=psutil.cpu_count(logical=False)
    cpu_threads=psutil.cpu_count(logical=True)
    #CPU model, cores, threads
    cpu_freq=psutil.cpu_freq().max
    cpu_freq_cur=psutil.cpu_freq().current
    #CPU max,current frequency in MHz
    cpu_usage=psutil.cpu_percent(interval=1)
    #current CPU usage percentage

    #RAM
    ram=psutil.virtual_memory()
    ram_total=round(ram.total/(1024**3),2)
    ram_used=round(ram.used/(1024**3),2)
    ram_free=round(ram.available/(1024**3),2)
    #RAM total, used, free in GB

    #Storage
    if platform.system()=='Windows':
        disk=psutil.disk_usage('C:\\')
    else:
        disk=psutil.disk_usage('/')
    #Checks C:\\ or / based on OS
    disk_total=round(disk.total/(1024**3),2)
    disk_used=round(disk.used/(1024**3),2)
    disk_free=round(disk.free/(1024**3),2)
    #Storage total, used, free in GB

    ###Set labels
    self.sys_labels["os"].config(text=os_info)
    self.sys_labels["arch"].config(text=arch)
    self.sys_labels["hostname"].config(text=hostname)
    self.sys_labels["kernel"].config(text=kernel)
    self.sys_labels["cpu_model"].config(text=cpu_model)
    self.sys_labels["cpu_cores"].config(text=str(cpu_cores))
    self.sys_labels["cpu_threads"].config(text=str(cpu_threads))
    self.sys_labels["cpu_freq_max"].config(text=str(cpu_freq))
    self.sys_labels["cpu_freq_cur"].config(text=str(cpu_freq_cur))
    self.sys_labels["cpu_usage"].config(text=str(cpu_usage))
    self.sys_labels["ram_total"].config(text=str(ram_total))
    self.sys_labels["ram_used"].config(text=str(ram_used))
    self.sys_labels["ram_free"].config(text=str(ram_free))
    self.sys_labels["disk_total"].config(text=str(disk_total))
    self.sys_labels["disk_used"].config(text=str(disk_used))
    self.sys_labels["disk_free"].config(text=str(disk_free))

    #refresh static
    self._refresh_interfaces_static()

    #Network
    def get_network_info():
      ip_public=requests.get("https://api.ipify.org").text

    counterstart=psutil.net_io_counters()
    time.sleep(1)
    counterfinish=psutil.net_io_counters()

    upspeedmbps=(counterfinish.bytes_sent - counterstart.bytes_sent)*8/1e6
    downspeed=(counterfinish.bytes_recv - counterstart.bytes_recv)*8/1e6
    #Upload and download speed in Mbps

    for iface, addrs in psutil.net_if_addrs().items():
        if psutil.net_if_stats()[iface].isup:      # only active adapters
            ipv4 = None
            mac = None

            for addr in addrs:
                if addr.family == socket.AF_INET:      # IPv4
                    ipv4 = addr.address
                if addr.family == psutil.AF_LINK:      # MAC
                    mac = addr.address
        network_info[iface] = {
            "ipv4": ipv4,
            "mac": mac
        }


    

    #Antivirus (Windows only), work on later.

##### TAB2 CONTENT #####
def get_process_info():
    for proc in psutil.process_iter():
        try: 
            proc.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    time.sleep(1)

    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'create_time']):#list of process with specific info
        try:
            cpu_thread_perc=proc.cpu_percent(None)
            cpu_sys_perc=cpu_thread_perc/cpu_threads #percentage of total CPU
            proc_mem=proc.info['memory_info'].rss / (1024**2) #Process ram in MB
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

        print(f"PID: {proc.info['pid']},
            Name: {proc.info['name']}, 
            CPU%: {cpu_sys}%, 
            Memory(MB): {proc_mem}"
            )
        ######correct f string later#####





##### TAB 3 CONTENT #####
def log_time_activity():
    ct=proc.info['create_time']#process creation time
    proc_uptime=datetime.datetime.now() - ct#process uptime (current time - creation time)
    print(f"{proc.info['pid']} {proc.info['name']} {proc_uptime}")###format later###







