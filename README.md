🚀 ESP-NOW Wireless Serial Bridge (USB)
Version: 1.0.0 (Baseline)

Author: Raj Narayan

This project creates a "Wireless USB Cable" using two ESP32 microcontrollers. It uses the ESP-NOW protocol to provide a high-speed, low-latency transparent serial bridge for transferring text files from a PC to a Raspberry Pi without a Wi-Fi network.

🛠 Features
Zero Wi-Fi Overhead: No routers or handshakes; uses direct 2.4GHz packets.

Auto-Port Detection: Python scripts automatically find the ESP32 on both Windows and Linux.

Visual Progress: Real-time progress bar on the PC side during file transfer.

V3.0+ SDK Compatible: Firmware updated for the latest Espressif Arduino Core.

Large File Handling: Automatically fragments data into 240-byte packets.

📂 Project Structure
Based on the current workspace:
<p>
.
├── esp32_code.ino          # Main Symmetric Bridge Firmware
├── MAC_Address_tester.ino  # Utility to find ESP32 MAC addresses
├── send_file.py            # PC-side Sender Script (with Progress Bar)
├── receive_file.py         # RPi-side Receiver Script
├── hello.txt               # Sample text file for testing
├── README.md               # Project Documentation
└── LICENSE                 # Project License
</p>
⚙️ Essential Raspberry Pi Setup
To use the GPIO Serial Pins (8 & 10) on the Raspberry Pi:

Run sudo raspi-config.

Navigate to: Interface Options -> Serial Port.

Login shell over serial? -> NO.

Hardware serial port enabled? -> YES.

Reboot the Pi.

🚀 Quick Start
Find MACs: Upload MAC_Address_tester.ino to both boards and note the addresses.

Flash Bridge: Update broadcastAddress in esp32_code.ino with the partner's MAC and upload.

Listen: On the Pi, run python3 receive_file.py.
        On the Pc, run python receive_file.py.

Send: On the PC, run python send_file.py.
      On the Pi, run python3 receive_file.py.

-> Do check for ports and filename for both the systems to avoid any issue.


👤 Contributor
Raj Narayan

To show appreciation, do mail or direct message on LinkedIn
