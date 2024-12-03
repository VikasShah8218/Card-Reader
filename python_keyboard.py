import serial
import pyautogui
import time

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 9600

def listen_to_serial():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")
            type_data_as_keyboard(data)

def type_data_as_keyboard(data):
    pyautogui.write(data)
    # pyautogui.press('enter') 
 

if __name__ == "__main__":
    while True:
        type_data_as_keyboard("Hi I am Mr Shah")
        time.sleep(5)
