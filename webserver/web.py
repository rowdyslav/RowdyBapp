from threading import Lock, Thread

from flask import Flask, jsonify, request

app = Flask(__name__)

hug_state = "idle"
initiator = None  # Идентификатор инициатора
lock = Lock()


@app.route("/start_hug", methods=["POST"])
def start_hug():
    global hug_state, initiator
    device_id = request.json.get("device_id")
    with lock:
        if hug_state != "hug_started":
            hug_state = "hug_started"
            initiator = device_id
            return jsonify({"status": "hug_started"}), 200
        return jsonify({"status": "already_hugging"}), 200


@app.route("/stop_hug", methods=["POST"])
def stop_hug():
    global hug_state, initiator
    device_id = request.json.get("device_id")
    with lock:
        if hug_state == "hug_started":
            hug_state = "hug_stopped"
            initiator = device_id
            return jsonify({"status": "hug_stopped"}), 200
        return jsonify({"status": "already_stopped"}), 200


@app.route("/check_hug", methods=["GET"])
def check_hug():
    global hug_state, initiator
    device_id = request.args.get("device_id")
    with lock:
        state = hug_state
        should_vibrate = state == "hug_started" and initiator != device_id
        should_cancel = state == "hug_stopped" and initiator != device_id
        hug_state = "idle" if hug_state == "hug_stopped" else hug_state
    return (
        jsonify(
            {
                "hug_state": state,
                "should_vibrate": should_vibrate,
                "should_cancel": should_cancel,
                "initiator": initiator,
            }
        ),
        200,
    )


def run_server():
    app.run(host="0.0.0.0", port=25565)


if __name__ == "__main__":
    server_thread = Thread(target=run_server)
    server_thread.start()
