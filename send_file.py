import serial
import serial.tools.list_ports
import time
import os

# CONFIGURATION
BAUD = 115200
FILE_TO_SEND = "hello.txt"
CHUNK_SIZE = 240 

def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Looks for common ESP32 chip identifiers
        if "CP210" in port.description or "CH340" in port.description or "USB" in port.description:
            print(f"--- Found ESP32 on {port.device} ({port.description}) ---")
            return port.device
    return None

def send_file():
    port = find_esp32_port()
    if not port:
        print("Error: No ESP32 detected. Check your USB connection.")
        return

    if not os.path.exists(FILE_TO_SEND):
        print(f"Error: {FILE_TO_SEND} not found!")
        return

    ser = serial.Serial(port, BAUD, timeout=1)
    time.sleep(2) 

    print(f"Starting transfer of {FILE_TO_SEND}...")
    with open(FILE_TO_SEND, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            ser.write(chunk)
            time.sleep(0.05) 
    
    ser.write(b"##EOF##")
    print("\nTransfer Complete.")
    ser.close()

if __name__ == "__main__":
    send_file()