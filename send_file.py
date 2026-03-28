import serial
import time
import os

# CONFIGURATION
PORT = 'COM3'  # Change this to your PC's ESP32 port
BAUD = 115200
FILE_TO_SEND = "transfer_test.txt"
CHUNK_SIZE = 240 

def send_file():
    if not os.path.exists(FILE_TO_SEND):
        print(f"Error: {FILE_TO_SEND} not found!")
        return

    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2) # Wait for ESP32 to reboot after connection

    print(f"Starting transfer of {FILE_TO_SEND}...")
    start_time = time.time()

    with open(FILE_TO_SEND, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            ser.write(chunk)
            # Short delay to let ESP-NOW process the packet
            time.sleep(0.05) 
            print(f"Sent {len(chunk)} bytes...", end="\r")

    # Send a unique EOF string so the Raspberry Pi knows to close the file
    ser.write(b"##EOF##")
    
    end_time = time.time()
    print(f"\nTransfer Complete in {round(end_time - start_time, 2)} seconds.")
    ser.close()

if __name__ == "__main__":
    send_file()