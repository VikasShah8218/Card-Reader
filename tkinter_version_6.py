import serial
import pyautogui
import time
import tkinter as tk
from tkinter import messagebox
from serial.tools import list_ports
from PIL import Image, ImageTk  # Import Pillow for image resizing
import time  # To introduce delays

# Increase the limit for allowed image pixels to avoid the decompression bomb warning
Image.MAX_IMAGE_PIXELS = None

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
            # print(f"{ser.port}: {decoded_data}")
            if decoded_data.startswith("1181"):
                manipulated_data = "1180" + decoded_data[4:]
            else:
                manipulated_data = decoded_data
            type_data_as_keyboard(manipulated_data)
        except:
            decoded_data = "---ERROR---"
            status_label.config(text="Decoding ERROR", fg="red")

            # print(data, f" is not Convertible")
    
    if listening:
        root.after(100, read_serial)

def type_data_as_keyboard(data):
    pyautogui.write(data)

def find_ch340_port():
    """Automatically detects and returns the port name of the USB-SERIAL CH340."""
    ports = list_ports.comports()
    for port in ports:
        if 'CH340' in port.description:
            return port.device  # e.g., COM5 or /dev/ttyUSB0 on Linux
    return None

def start_listening():
    global listening, ser
    SERIAL_PORT = find_ch340_port()
    
    if SERIAL_PORT is None:
        status_label.config(text="CH340 device not found", fg="red")
        return
    
    if ser is not None and ser.is_open:  # Check if the port is already open
        try:
            ser.close()  # Close the existing connection if open
            status_label.config(text=f"Previous connection to {SERIAL_PORT} closed", fg="blue")
            time.sleep(1)  # Give time to release the port
        except Exception as e:
            status_label.config(text=f"Failed to close connection: {str(e)}", fg="red")
    
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
            root.after(100, read_serial)
        except serial.SerialException as e:
            status_label.config(text=f"Please Reconnect the Reader and then Retry", fg="red")
            listening = False

def stop_listening():
    global listening, ser
    if listening:
        listening = False
        try:
            ser.close()  # Close the port properly
            ser = None  # Release the serial object
            status_label.config(text="Stopped Listening and released port", fg="red")
            time.sleep(1)  # Wait for the system to release the port
        except Exception as e:
            status_label.config(text=f"Error closing port: {str(e)}", fg="red")

    start_button.config(state='normal')
    stop_button.config(state='disabled')

# Create the main window
root = tk.Tk()
root.title("CARD Tracker")

# Add ESSI and Ministry of Defence logos at the top
logo_frame = tk.Frame(root)
logo_frame.pack(pady=10)

# Load the images using Pillow
essi_image = Image.open("essi-logo.png")  # Ensure ESSI.png is available
essi_image = essi_image.resize((450,150), Image.Resampling.LANCZOS)  # Resize to 150x150
essi_logo = ImageTk.PhotoImage(essi_image)

mod_image = Image.open("mod.png")  # Ensure MinistryOfDefence.png is available
mod_image = mod_image.resize((150, 150), Image.Resampling.LANCZOS)  # Resize to 150x150
mod_logo = ImageTk.PhotoImage(mod_image)

# Add the logos to the frame
essi_label = tk.Label(logo_frame, image=essi_logo)
essi_label.grid(row=0, column=0, padx=10)

mod_label = tk.Label(logo_frame, image=mod_logo)
mod_label.grid(row=0, column=1, padx=10)

# Add the software name label
software_name = tk.Label(root, text="CARD Tracker", font=("Arial", 24, "bold"))
software_name.pack(pady=10)

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