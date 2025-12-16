import wmi
import time
import os
import json
import psutil
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "..", "logs", "usb_events.log")
FILE_LOG = os.path.join(BASE_DIR, "..", "logs", "file_activity.log")

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def log_file_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(FILE_LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def extract_vid_pid(pnp_id):
    vid = "UNKNOWN"
    pid = "UNKNOWN"
    for part in pnp_id.split("&"):
        if part.startswith("VEN_"):
            vid = part.replace("VEN_", "")
        if part.startswith("PROD_"):
            pid = part.replace("PROD_", "")
    return vid, pid

def get_connected_usb():
    c = wmi.WMI()
    devices = []
    for usb in c.Win32_DiskDrive(InterfaceType="USB"):
        devices.append({
            "name": usb.Caption,
            "pnp_id": usb.PNPDeviceID
        })
    return devices

def load_policy(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f).get("devices", [])

ALLOWLIST = load_policy(os.path.join(BASE_DIR, "..", "policy", "allowlist.json"))
BLOCKLIST = load_policy(os.path.join(BASE_DIR, "..", "policy", "blocklist.json"))

def check_policy(vid, pid):
    for d in BLOCKLIST:
        if d["vid"] == vid and d["pid"] == pid:
            return "BLOCKED"
    for d in ALLOWLIST:
        if d["vid"] == vid and d["pid"] == pid:
            return "ALLOWED"
    return "UNKNOWN"

def get_usb_mounts():
    mounts = []
    for part in psutil.disk_partitions(all=False):
        if "removable" in part.opts.lower():
            mounts.append(part.mountpoint)
    return mounts

def snapshot_files(path):
    snapshot = {}
    for root, _, files in os.walk(path):
        for f in files:
            full_path = os.path.join(root, f)
            try:
                snapshot[full_path] = os.path.getsize(full_path)
            except:
                pass
    return snapshot

usb_file_state = {}
previous_devices = get_connected_usb()
log_event("USB monitoring started")

while True:
    time.sleep(2)

    # ---- USB DEVICE MONITORING ----
    current_devices = get_connected_usb()

    for device in current_devices:
        if device not in previous_devices:
            vid, pid = extract_vid_pid(device["pnp_id"])
            status = check_policy(vid, pid)
            log_event(
                f"USB Connected | Device: {device['name']} | VID: {vid} | PID: {pid} | Status: {status}"
            )

    for device in previous_devices:
        if device not in current_devices:
            vid, pid = extract_vid_pid(device["pnp_id"])
            status = check_policy(vid, pid)
            log_event(
                f"USB Disconnected | Device: {device['name']} | VID: {vid} | PID: {pid} | Status: {status}"
            )

    previous_devices = current_devices

    # ---- FILE ACTIVITY MONITORING ----
    mounts = get_usb_mounts()

    for mount in mounts:
        if mount not in usb_file_state:
            usb_file_state[mount] = snapshot_files(mount)
            continue

        current_snapshot = snapshot_files(mount)
        previous_snapshot = usb_file_state[mount]

        for file in current_snapshot:
            if file not in previous_snapshot:
                log_file_event(
                    f"File Copied TO USB: {file} ({current_snapshot[file]} bytes)"
                )

        for file in previous_snapshot:
            if file not in current_snapshot:
                log_file_event(
                    f"File Deleted FROM USB: {file}"
                )

        usb_file_state[mount] = current_snapshot
