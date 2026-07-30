import psutil
import platform
import time

BOOT_TIME = psutil.boot_time()


def get_system_info():
    uptime = int(time.time() - BOOT_TIME)

    return {
        "status": "Running",
        "cpu": psutil.cpu_percent(interval=0.1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "network_sent": round(psutil.net_io_counters().bytes_sent / (1024 * 1024), 2),
        "network_received": round(
            psutil.net_io_counters().bytes_recv / (1024 * 1024), 2
        ),
        "processes": len(psutil.pids()),
        "uptime": uptime,
        "system": platform.system(),
        "release": platform.release(),
        "python_version": platform.python_version(),
    }


def get_health():
    return {"status": "healthy"}
