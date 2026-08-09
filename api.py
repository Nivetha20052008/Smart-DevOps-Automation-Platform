from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Store latest monitoring data for each device
latest_data = {}


# -------------------------------------------------
# RECEIVE MONITORING DATA
# -------------------------------------------------

@app.route("/api/monitor", methods=["POST"])
def receive_monitor_data():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No monitoring data received"
        }), 400

    device_name = data.get("device_name")

    if not device_name:
        return jsonify({
            "status": "error",
            "message": "Device name is required"
        }), 400

    latest_data[device_name] = {
        "device_name": device_name,
        "cpu": data.get("cpu"),
        "memory": data.get("memory"),
        "disk": data.get("disk"),
        "status": data.get("status"),
        "updated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    }

    return jsonify({
        "status": "success",
        "message": "Monitoring data received"
    }), 200


# -------------------------------------------------
# GET ALL CONNECTED DEVICES
# -------------------------------------------------

@app.route("/api/monitor", methods=["GET"])
def get_all_monitor_data():

    return jsonify({
        "status": "success",
        "devices": list(latest_data.values())
    }), 200


# -------------------------------------------------
# GET SPECIFIC DEVICE
# -------------------------------------------------

@app.route("/api/monitor/<device_name>", methods=["GET"])
def get_monitor_data(device_name):

    if device_name not in latest_data:

        return jsonify({
            "status": "error",
            "message": "Device not found"
        }), 404

    return jsonify(
        latest_data[device_name]
    ), 200


# -------------------------------------------------
# API HOME
# -------------------------------------------------

@app.route("/")
def home():

    return jsonify({
        "status": "online",
        "service": "Smart DevOps Monitoring API"
    })


# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )