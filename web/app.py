from flask import Flask, render_template
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")

USB_LOG = os.path.join(LOG_DIR, "usb_events.log")
FILE_LOG = os.path.join(LOG_DIR, "file_activity.log")

def read_log(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return f.readlines()[::-1]

@app.route("/")
def index():
    usb_logs = read_log(USB_LOG)
    last_event = usb_logs[0] if usb_logs else "No USB activity yet"
    return render_template("index.html", last_event=last_event)

@app.route("/usb")
def usb():
    logs = read_log(USB_LOG)
    return render_template("usb.html", logs=logs)

@app.route("/files")
def files():
    logs = read_log(FILE_LOG)
    return render_template("files.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
