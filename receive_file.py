import serial
import serial.tools.list_ports
import os

BAUD = 115200
SAVE_AS = "received_file.txt"

def find_rpi_port():
    # Priority 1: USB-to-Serial Adapters
    # Priority 2: Standard GPIO Serial (ttyS0 / ttyAMA0)
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.device:
            return port.device
    
    # Defaulting to GPIO if no USB serial is found
    if os.path.exists('/dev/ttyS0'): return '/dev/ttyS0'
    if os.path.exists('/dev/ttyAMA0'): return '/dev/ttyAMA0'
    return None

def receive_file():
    port = find_rpi_port()
    if not port:
        print("Error: Serial port not found on Raspberry Pi.")
        return

    ser = serial.Serial(port, BAUD, timeout=1)
    print(f"Listening on {port}...")

    with open(SAVE_AS, "wb") as f:
        while True:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                if b"##EOF##" in data:
                    f.write(data.replace(b"##EOF##", b""))
                    break
                f.write(data)
    
    print(f"File saved successfully as: {SAVE_AS}")
    ser.close()

if __name__ == "__main__":
    receive_file()