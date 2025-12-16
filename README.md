# USB Device Control & Monitoring Framework

A Windows-based endpoint security project that monitors USB device activity, applies allowlist/blocklist policies, and audits file transfers on removable storage devices to detect unauthorized usage and potential data exfiltration.

This project focuses on real hardware monitoring and policy-driven security decisions, similar to how enterprise endpoint protection systems operate.

---

## Features

- USB device connect and disconnect detection
- Vendor ID (VID) and Product ID (PID) extraction
- Allowlist / Blocklist based policy enforcement
- Real-time USB device activity logging
- File transfer auditing on removable drives
- Timestamped security logs for forensic analysis

---

## Project Motivation

USB devices are a common attack vector for:
- Data exfiltration
- Malware introduction
- Insider threats

This project demonstrates how endpoint systems can:
- Identify connected USB devices
- Decide whether a device is trusted
- Track file movement to and from removable storage

---

## Tech Stack

- OS: Windows
- Language: Python
- Libraries:
  - wmi
  - pywin32
  - psutil

---

## Project Structure

USB_Device_Control/
├── README.md
├── src/
│ └── usb_monitor.py
├── policy/
│ ├── allowlist.json
│ └── blocklist.json
├── logs/
│ ├── usb_events.log
│ └── file_activity.log
└── evidence/
└── sample_run.txt


---

## How to Run

1. Install dependencies
pip install wmi pywin32 psutil


2. Run the monitoring agent
python src/usb_monitor.py


3. Test the system
- Plug in a USB storage device
- Copy or delete files on the USB
- Remove the USB device

---

## Output

USB device logs (`logs/usb_events.log`)
USB Connected | VID: MASS | PID: STORAGE_DEVICE | Status: ALLOWED
USB Disconnected | VID: MASS | PID: STORAGE_DEVICE | Status: ALLOWED

File activity logs (`logs/file_activity.log`)
File Copied TO USB: G:\example.pdf (358295 bytes)
File Deleted FROM USB: G:\example.pdf


Devices are classified as:
- ALLOWED
- BLOCKED
- UNKNOWN

---

## Learning Outcomes

- Understanding USB hardware identification
- Implementing endpoint security policies
- Monitoring file system activity on removable media
- Designing security tools with real-world relevance

---

## Disclaimer

This project is intended strictly for educational and defensive purposes.
It does not block devices at the kernel level or modify system security policies.



