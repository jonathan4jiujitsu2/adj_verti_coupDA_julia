import broadlink
import tkinter as tk
from tkinter import messagebox

# Device details
DEVICE_IP = "192.168.1.55"
DEVICE_MAC = "e8:16:56:a1:72:15"
DEVICE_NAME = "VERGA1"

# Initialize the device
def connect_device():
    try:
        global device
        device = broadlink.hello(DEVICE_IP)
        device.auth()
        messagebox.showinfo("Success", f"Connected to {DEVICE_NAME} at {DEVICE_IP}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect to {DEVICE_NAME}: {e}")

# Enter learning mode
def enter_learning():
    try:
        device.enter_learning()
        messagebox.showinfo("Learning Mode", f"{DEVICE_NAME} is ready to learn IR signal.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to enter learning mode: {e}")

# Get learned IR packet
def get_ir_packet():
    try:
        packet = device.check_data()
        if packet:
            ir_codes[command_var.get()] = packet
            messagebox.showinfo("Success", f"IR code for '{command_var.get()}' learned and saved.")
        else:
            messagebox.showerror("Error", "No IR code received.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get IR packet: {e}")

# Send IR packet
def send_ir_command():
    try:
        command = command_var.get()
        if command in ir_codes:
            device.send_data(ir_codes[command])
            messagebox.showinfo("Success", f"Sent IR command: {command}")
        else:
            messagebox.showerror("Error", f"IR code for '{command}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send IR command: {e}")

# Initialize IR codes dictionary
ir_codes = {}

# Create the GUI window
root = tk.Tk()
root.title(f"{DEVICE_NAME} AC Controller")
root.geometry("400x400")

# Title
tk.Label(root, text=f"{DEVICE_NAME} AC Controller", font=("Arial", 16)).pack(pady=10)

# Connect device button
tk.Button(root, text="Connect to VERGA1", command=connect_device).pack(pady=5)

# Command options
commands = ["Power On", "Power Off", "Temp Up", "Temp Down", "Fan Speed", "Cool Mode", "Heat Mode"]
command_var = tk.StringVar(root)
command_var.set(commands[0])

# Dropdown menu
tk.Label(root, text="Select Command:").pack()
command_menu = tk.OptionMenu(root, command_var, *commands)
command_menu.pack(pady=5)

# Learning mode buttons
tk.Button(root, text="Enter Learning Mode", command=enter_learning).pack(pady=5)
tk.Button(root, text="Get IR Packet", command=get_ir_packet).pack(pady=5)

# Send IR command button
tk.Button(root, text="Send Command", command=send_ir_command).pack(pady=5)

# Exit button
tk.Button(root, text="Exit", command=root.destroy).pack(pady=10)

# Run the GUI
root.mainloop()
