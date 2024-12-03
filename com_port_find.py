import serial
import pyautogui
import time
import tkinter as tk
from tkinter import messagebox
from serial.tools import list_ports


def find_ch340_port():
    """Automatically detects and returns the port name of the USB-SERIAL CH340."""
    ports = list_ports.comports()
    for port in ports:
        if 'CH340' in port.description:
            return port.device  # e.g., COM5 or /dev/ttyUSB0 on Linux
    return None


print(find_ch340_port())