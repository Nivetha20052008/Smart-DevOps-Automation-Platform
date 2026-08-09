import time
import requests
import psutil
import socket

API_URL = "https://smart-devops-api.onrender.com/api/monitor"

DEVICE_NAME = socket.gethostname()


def get_system_data():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent

    if cpu >= 90 or memory >= 90 or disk >= 90:
        status = "CRITICAL"
    elif cpu >= 75 or memory >= 75 or disk >= 75:
        status = "WARNING"
    else:
        status = "HEALTHY"

    return {
        "device_name": DEVICE_NAME,
        "cpu": cpu,
        "memory": memory,
        "disk": disk,
        "status": status
    }


while True:

    try:
        data = get_system_data()

        response = requests.post(
            API_URL,
            json=data,
            timeout=10
        )

        print(
            f"Device: {DEVICE_NAME} | "
            f"CPU: {data['cpu']}% | "
            f"RAM: {data['memory']}% | "
            f"Disk: {data['disk']}% | "
            f"Status: {data['status']}"
        )

    except Exception as error:

        print(
            f"Monitoring connection error: {error}"
        )

    time.sleep(5)