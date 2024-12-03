import serial
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import messagebox

BAUD_RATE = 9600
listening = False
thread = None
rate = 9600

def decode_byte_sequence(data):
    STX = b'\x02'
    ETX = b'\x03'
    start_marker = data.find(STX) + 1 
    end_marker = data.find(ETX, start_marker) 
    payload = data[start_marker:end_marker]
    decoded_payload = payload.decode('ascii')
    return decoded_payload

def read_serial(port):
    global listening
    try:
        ser = serial.Serial(
            port=port,
            baudrate=rate,
            timeout=1,
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )
        status_label.config(text=f"Connected to {port}")
        print(f"Connected to {port}")
        while listening:
            if ser.in_waiting > 0:
                data = ser.read(ser.in_waiting)
                try:
                    decoded_data = decode_byte_sequence(data)
                    print(f"{port}: {decoded_data}")
                    if decoded_data.startswith("1181"):
                        manupulated_data = "1180" + decoded_data[4:]
                    else:
                        manupulated_data = decoded_data
                    type_data_as_keyboard(manupulated_data)
                except:
                    decoded_data = "---ERROR---"
                    print(data, f" is not Convertable")
            time.sleep(0.0001) 
    except serial.SerialException as e:
        status_label.config(text=f"Connection Failed: {str(e)}")
        print(f"Error: {str(e)}")
        listening = False

def type_data_as_keyboard(data):
    pyautogui.write(data)

def start_listening():
    global listening, thread, SERIAL_PORT
    SERIAL_PORT = port_entry.get()  
    if not listening:
        listening = True
        thread = threading.Thread(target=read_serial, args=(SERIAL_PORT,))
        thread.start()
        start_button.config(state='disabled')
        stop_button.config(state='normal')

def stop_listening():
    global listening
    if listening:
        listening = False
        thread.join()
        start_button.config(state='normal')
        stop_button.config(state='disabled')
        status_label.config(text="Stopped Listening")

root = tk.Tk()
root.title("Serial Listener")

port_label = tk.Label(root, text="Enter COM Port:")
port_label.pack(pady=5)

port_entry = tk.Entry(root)
port_entry.pack(pady=5)
port_entry.insert(0, 'COM20')

start_button = tk.Button(root, text="Start Listening", command=start_listening)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Listening", command=stop_listening, state='disabled')
stop_button.pack(pady=10)

status_label = tk.Label(root, text="Not Connected", fg="red")
status_label.pack(pady=10)

root.mainloop()
