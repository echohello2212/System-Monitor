import tkinter as tk
from tkinter import ttk

####Window setup####
def create_window():
    root=tk.Tk()
    root.title("Process Monitor")
    #root.geomery("widthxheight") if i want set window sizr
    #root.resizable(False, False) # to disable resizing the window
    #created actual window

    notebook=ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')
    #expands notebook to fill the window horizontally+vertically

    tab1=ttk.Frame(notebook)
    tab2=ttk.Frame(notebook)
    tab3=ttk.Frame(notebook)
    #created 3 tabs as frames

    notebook.add(tab1, text="My Computer")
    notebook.add(tab2, text="Processes")
    notebook.add(tab3, text="Time Log")
    #added tabs to notebook with text labels


import psutil
import platform
import datetime
import time
import socket
import requests
import wmi #only for windows antivirus

##### TAB 1 CONTENT #####
def get_sys_info():
    #OS 
    os_info=f"{platform.system()} {platform.release()}"
    arch= platform.architecture()[0] 
    #tells whether 32 or 64 bit
    hostname=socket.gethostname()
    kernel_version=platform.version()

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

        print(f"""
            Interface:{iface} 
            IPv4: {ipv4} 
            MAC: {mac},
            Public IP: {ip_public}
            Upload Speed: {upspeedmbps.2f} Mbps,
            Download Speed: {downspeed.2f} Mbps
            """)
    

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
            cpu_sys=cpu_thread_perc/cpu_threads #percentage of total CPU
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

