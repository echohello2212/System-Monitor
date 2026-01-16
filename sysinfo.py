# sysinfo.py
from typing import Dict, List, Optional, Tuple
import platform
import socket
import psutil
import requests

import monitor  # for unit conversions

def get_static_sys_info() -> Dict[str, object]:
    # get os info
    os_info = f"{platform.system()} {platform.release()}"
    arch    = platform.architecture()[0]
    hostname = socket.gethostname()
    kernel  = platform.version()

    # get cpu info
    cpu_model   = platform.processor()
    cpu_cores   = psutil.cpu_count(logical=False) or 0
    cpu_threads = psutil.cpu_count(logical=True) or cpu_cores
    freq        = psutil.cpu_freq() or None
    cpu_freq_max = freq.max if freq else 0.0
    cpu_freq_cur = freq.current if freq else 0.0

    # get ram info
    vm = psutil.virtual_memory()
    ram_total = monitor.bytes_to_gb(vm.total)
    ram_used  = monitor.bytes_to_gb(vm.used)
    ram_free  = monitor.bytes_to_gb(vm.available)

    # get disk info
    root = 'C:\\' if platform.system() == 'Windows' else '/'
    du = psutil.disk_usage(root)
    disk_total = monitor.bytes_to_gb(du.total)
    disk_used  = monitor.bytes_to_gb(du.used)
    disk_free  = monitor.bytes_to_gb(du.free)

    return {
        "os": os_info,
        "arch": arch,
        "hostname": hostname,
        "kernel": kernel,
        "cpu_model": cpu_model or "N/A",
        "cpu_cores": cpu_cores,
        "cpu_threads": cpu_threads,
        "cpu_freq_max": round(cpu_freq_max, 1),
        "cpu_freq_cur": round(cpu_freq_cur, 1),
        "cpu_usage": 0.0,  # filled dynamically in gui
        "ram_total": ram_total,
        "ram_used": ram_used,
        "ram_free": ram_free,
        "disk_total": disk_total,
        "disk_used": disk_used,
        "disk_free": disk_free,
    }

def get_cpu_usage_percent(interval: Optional[float] = None) -> float:
    # if interval is None, returns instant value (non-blocking)
    # if interval > 0, blocks for that duration and returns average
    try:
        return psutil.cpu_percent(interval=interval)
    except Exception:
        return 0.0
#helper function to get mac address family for network interfaces
def _af_link_family():
    AF_LINK = getattr(psutil, "AF_LINK", None)
    AF_PACKET = getattr(socket, "AF_PACKET", None)  # for linux compatibility
    return AF_LINK, AF_PACKET

def get_network_interfaces() -> List[Dict[str, Optional[str]]]:
    interfaces = []
    AF_LINK, AF_PACKET = _af_link_family()

    stats = psutil.net_if_stats()
    addrs = psutil.net_if_addrs()
    # collect only active interfaces with ipv4 and mac addresses
    for iface, addr_list in addrs.items():
        s = stats.get(iface)
        if not s or not s.isup:
            continue

        ipv4 = None
        mac = None
        for a in addr_list:
            if a.family == socket.AF_INET:
                ipv4 = a.address
            if (AF_LINK and a.family == AF_LINK) or (AF_PACKET and a.family == AF_PACKET):
                mac = a.address

        interfaces.append({"name": iface, "ipv4": ipv4, "mac": mac})
    return interfaces

def get_public_ip() -> str:
    try:
        resp = requests.get("https://api.ipify.org", timeout=4)
        if resp.status_code == 200:
            return resp.text.strip()
    except requests.RequestException:
        pass
    return "—"

def get_net_io_counters() -> Optional[Tuple[int, int]]:
    # returns total (bytes_sent, bytes_recv) or None if unavailable
    try:
        c = psutil.net_io_counters()
        return (c.bytes_sent, c.bytes_recv)
    except Exception:
        return None

def get_net_io_counters_per_interface() -> Optional[Dict[str, Tuple[int, int]]]:
    # returns dict of interface_name: (bytes_sent, bytes_recv) or None if unavailable
    try:
        counters = psutil.net_io_counters(pernic=True)
        result = {}
        for iface, c in counters.items():
            result[iface] = (c.bytes_sent, c.bytes_recv)
        return result
    except Exception:
        return None
