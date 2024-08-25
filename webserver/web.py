import threading

from flask import Flask, request

app = Flask(__name__)

# Статус вибрации для всех подключённых устройств
status = []


@app.route("/send_hug", methods=["POST"])
def send_hug():
    global status
    # Устанавливаем флаг для всех устройств
    status = [True for _ in status]
    return "Hug sent!", 200


@app.route("/stop_hug", methods=["POST"])
def stop_hug():
    global status
    # Устанавливаем флаг остановки для всех устройств
    status = [False for _ in status]
    return "Hug stopped!", 200


@app.route("/register", methods=["POST"])
def register():
    global status
    # Регистрируем новое устройство
    status.append(False)
    return f"Registered successfully, ID: {len(status) - 1}", 200


@app.route("/check_hug", methods=["GET"])
def check_hug():
    user_id = int(request.args.get("id"))
    if status[user_id]:
        return "Hug received!", 200
    else:
        return "Stop hug", 200


def run_server():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()
