import psutil
from datetime import datetime


def get_system_health():
    cpu = psutil.cpu_percent(interval=0.5)

    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    if cpu >= 90 or memory.percent >= 90 or disk.percent >= 90:
        status = "CRITICAL"

    elif cpu >= 75 or memory.percent >= 75 or disk.percent >= 75:
        status = "WARNING"

    else:
        status = "HEALTHY"

    return {
        "cpu": cpu,
        "memory": memory.percent,
        "disk": disk.percent,
        "status": status,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }