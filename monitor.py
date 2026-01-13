# monitor.py
from typing import Dict, List
import psutil
import time
import datetime


#unit conversions
def bytes_to_mb(b: float) -> float:
    return round(b / (1024 ** 2), 2)

def bytes_to_gb(b: float) -> float:
    return round(b / (1024 ** 3), 2)

def bytes_to_mbps(delta_bytes: float, delta_seconds: float) -> float:
    #converts to mbps
    if delta_seconds <= 0:
        return 0.0
    return (delta_bytes * 8.0) / (1e6 * delta_seconds)

#formatting hh:mm:ss
def fmt_hhmmss(seconds: float) -> str:
    seconds = max(0, int(seconds))
    hrs, rem = divmod(seconds, 3600)
    mins, secs = divmod(rem, 60)
    return f"{hrs:02}:{mins:02}:{secs:02}"

def current_timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# prepare cpu percent measurements, first read always returns 0 so need to call this first
def prep_cpu_perc():
    for p in psutil.process_iter():
        try:
            p.cpu_percent(None)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
#40 most cpu demanding processes
def list_processes(limit: int = 40) -> List[Dict[str, float]]:
    # get number of logical cpus (threads) for percentage calculation
    num_logical_cpus = psutil.cpu_count(logical=True) or 1
    
    rows: List[Dict[str, float]] = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            info = p.info
            # cpu_percent() returns percentage across all cores (can be > 100)
            # divide by num_logical_cpus to get percentage of total threads (0-100%)
            cpu = p.cpu_percent() / num_logical_cpus
            # cap at 100% to ensure it never goes over
            cpu = min(cpu, 100.0)
            mem_mb = bytes_to_mb(info['memory_info'].rss) if info.get('memory_info') else 0.0
            rows.append({
                "pid": info.get('pid', 0),
                "name": info.get('name', 'N/A'),
                "cpu_percent": cpu,
                "memory_mb": mem_mb,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    rows.sort(key=lambda r: r['cpu_percent'], reverse=True)
    return rows[:max(1, limit)]

#uptime of processes
def get_time_log_rows() -> List[Dict[str, str]]:

    out: List[Dict[str, str]] = []
    now = time.time()
    for proc in psutil.process_iter(['pid', 'name', 'create_time']):
        try:
            ct = proc.info.get('create_time')
            if not ct:
                continue
            uptime_sec = max(0, now - ct)
            out.append({
                "pid": proc.info.get('pid', 0),
                "name": proc.info.get('name', 'N/A'),
                "uptime_hhmmss": fmt_hhmmss(uptime_sec),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    out.sort(key=lambda r: r['pid'], reverse=True)
    return out
