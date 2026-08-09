from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

latest_data = {}


@app.route("/api/monitor", methods=["POST"])
def receive_monitor_data():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "No monitoring data received"
        }), 400

    device_name = data.get("device_name")

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
    })


@app.route("/api/monitor/<device_name>", methods=["GET"])
def get_monitor_data(device_name):

    if device_name not in latest_data:
        return jsonify({
            "status": "error",
            "message": "Device not found"
        }), 404

    return jsonify(latest_data[device_name])


@app.route("/")
def home():

    return jsonify({
        "status": "online",
        "service": "Smart DevOps Monitoring API"
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )