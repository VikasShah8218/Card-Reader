import serial
import pyautogui
import time
import tkinter as tk
from tkinter import messagebox

BAUD_RATE = 9600
listening = False
rate = 9600
ser = None

def decode_byte_sequence(data):
    STX = b'\x02'
    ETX = b'\x03'
    start_marker = data.find(STX) + 1 
    end_marker = data.find(ETX, start_marker) 
    payload = data[start_marker:end_marker]
    decoded_payload = payload.decode('ascii')
    return decoded_payload

def read_serial():
    global listening, ser
    if listening and ser and ser.in_waiting > 0:
        data = ser.read(ser.in_waiting)
        try:
            decoded_data = decode_byte_sequence(data)
            print(f"{ser.port}: {decoded_data}")
            if decoded_data.startswith("1181"):
                manipulated_data = "1180" + decoded_data[4:]
            else:
                manipulated_data = decoded_data
            type_data_as_keyboard(manipulated_data)
        except:
            decoded_data = "---ERROR---"
            print(data, f" is not Convertable")
    
    # Keep calling the function periodically
    if listening:
        root.after(100, read_serial)  # Run this again after 100 milliseconds

def type_data_as_keyboard(data):
    pyautogui.write(data)

def start_listening():
    global listening, ser
    SERIAL_PORT = port_entry.get()  
    if not listening:
        try:
            ser = serial.Serial(
                port=SERIAL_PORT,
                baudrate=rate,
                timeout=1,
                parity=serial.PARITY_NONE,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False
            )
            status_label.config(text=f"Connected to {SERIAL_PORT}", fg="green")
            listening = True
            start_button.config(state='disabled')
            stop_button.config(state='normal')
            root.after(100, read_serial)  # Start reading the serial data
        except serial.SerialException as e:
            status_label.config(text=f"Connection Failed: {str(e)}", fg="red")
            listening = False

def stop_listening():
    global listening, ser
    if listening:
        listening = False
        ser.close()
        start_button.config(state='normal')
        stop_button.config(state='disabled')
        status_label.config(text="Stopped Listening", fg="red")

# Create the main window
root = tk.Tk()
root.title("Serial Listener")

# Create entry for COM port input
port_label = tk.Label(root, text="Enter COM Port:")
port_label.pack(pady=5)

port_entry = tk.Entry(root)
port_entry.pack(pady=5)
port_entry.insert(0, 'COM20')

# Create buttons
start_button = tk.Button(root, text="Start Listening", command=start_listening)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Listening", command=stop_listening, state='disabled')
stop_button.pack(pady=10)

# Status label to show connection status
status_label = tk.Label(root, text="Not Connected", fg="red")
status_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()