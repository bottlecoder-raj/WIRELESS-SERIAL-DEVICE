import serial

# CONFIGURATION
# If using USB cable to RPi: '/dev/ttyUSB0'
# If using GPIO pins: '/dev/ttyS0' or '/dev/ttyAMA0'
PORT = '/dev/ttyS0' 
BAUD = 115200
SAVE_AS = "received_from_pc.txt"

def receive_file():
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"Listening on {PORT}... Press Ctrl+C to stop.")

    with open(SAVE_AS, "wb") as f:
        receiving = True
        while receiving:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                
                if b"##EOF##" in data:
                    # Clean the EOF marker out of the final data
                    clean_data = data.replace(b"##EOF##", b"")
                    f.write(clean_data)
                    print("\nEnd of File marker received!")
                    receiving = False
                else:
                    f.write(data)
                    print(f"Receiving data... Total bytes saved.", end="\r")

    ser.close()
    print(f"File saved as: {SAVE_AS}")

if __name__ == "__main__":
    receive_file()