import json
import os
import platform
import socket
import subprocess

import psutil


GIB = 1024 ** 3


def computermodel():
    """Zit niet in de basisdata, dus apart opvragen per besturingssysteem."""
    try:
        if platform.system() == "Windows":
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"HARDWARE\DESCRIPTION\System\BIOS") as k:
                return (winreg.QueryValueEx(k, "SystemManufacturer")[0] + " " +
                        winreg.QueryValueEx(k, "SystemProductName")[0])
        if platform.system() == "Linux":
            with open("/sys/class/dmi/id/sys_vendor") as f1, \
                 open("/sys/class/dmi/id/product_name") as f2:
                return f1.read().strip() + " " + f2.read().strip()
        if platform.system() == "Darwin":
            return subprocess.check_output(["sysctl", "-n", "hw.model"], text=True).strip()
    except OSError:
        return None


def primair_ip():
    """IPv4-adres dat het OS gebruikt om internet te bereiken (default route).
    Een UDP-connect verstuurt geen pakketten."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def filter_info(data):
    # Opslag: de partitie met het besturingssysteem
    if platform.system() == "Windows":
        schijf = os.environ.get("SystemDrive", "C:") + "\\"
    else:
        schijf = "/"
    opslag = data["storage"].get(schijf, {})

    # Primaire interface: de interface die het uitgaande IPv4-adres heeft
    ip = primair_ip()
    mac = ipv6 = ipv6_ll = None
    for naam, info in data["network"]["interfaces"].items():
        adressen = [a["address"] for a in info["addrs"] if a["family"] == socket.AF_INET]
        if ip not in adressen:
            continue
        for a in info["addrs"]:
            adres = a["address"].split("%")[0]  # zone-index (%eth0) weghalen
            if a["family"] == psutil.AF_LINK:
                mac = adres.replace("-", ":").lower()
            elif a["family"] == socket.AF_INET6:
                if adres.startswith("fe80"):
                    ipv6_ll = adres
                else:
                    ipv6 = adres
        break

    freq = data["cpu"]["cpu_freq"]
    return {
        "computernaam": data["network"]["hostname"],
        "computermodel": computermodel(),
        "processor": data["cpu"]["processor"],
        "cpu_fysieke_cores": data["cpu"]["physical_cores"],
        "cpu_max_frequentie_mhz": freq["max"] if freq else None,
        "ram_totaal_gib": round(data["memory"]["total"] / GIB, 2),
        "opslag_bestandssysteem": opslag.get("fstype"),
        "opslag_capaciteit_gib": round(opslag["total"] / GIB, 2) if opslag else None,
        "mac_adres": mac,
        "ipv4_adres": ip,
        "ipv6_adres": ipv6,
        "ipv6_link_local": ipv6_ll,
    }


if __name__ == "__main__":
    print(json.dumps(filter_info(collect_system_info()), indent=2))