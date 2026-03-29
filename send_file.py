import serial
import serial.tools.list_ports
import time
import os
from tqdm import tqdm  # <--- New Import

# CONFIGURATION
BAUD = 115200
FILE_TO_SEND = "hello.txt"
CHUNK_SIZE = 240 

def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
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

    file_size = os.path.getsize(FILE_TO_SEND) # Get size for progress bar
    ser = serial.Serial(port, BAUD, timeout=1)
    time.sleep(2) 

    print(f"Starting transfer of {FILE_TO_SEND} ({file_size} bytes)...")
    
    # Initialize the progress bar
    with open(FILE_TO_SEND, "rb") as f, tqdm(
        total=file_size, unit='B', unit_scale=True, desc="Sending"
    ) as pbar:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            ser.write(chunk)
            pbar.update(len(chunk)) # Update bar based on bytes sent
            time.sleep(0.05) 
    
    ser.write(b"##EOF##")
    print("\nTransfer Complete.")
    ser.close()

if __name__ == "__main__":
    send_file()
