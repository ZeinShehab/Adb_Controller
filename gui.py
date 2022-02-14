#!/usr/bin/env python3

from logging import shutdown
import tkinter as tk

from ppadb import command
import device
import threading
import sys
import subprocess


# GLOBAL CONSTANTS
IP = "192.168.1.103"
PORT = 5555
WIDTH = 500
HEIGHT = 500

tv_box = device.Device(IP, PORT)

# INITIALIZE WINDOW
root = tk.Tk()
root.title("TV-Box")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Live screen share button
share = threading.Thread(target=tv_box.sharescreen)
share_btn = tk.Button(text="Live Screen", command=share.start)
canvas.create_window(200, 50, window=share_btn)

# Log button
log = threading.Thread(target=tv_box.get_log)
log_btn = tk.Button(text="Log", command=log.start)
canvas.create_window(300, 50, window=log_btn)

# Disconnect button
disconnect_btn = tk.Button(text="Disconnect", command=tv_box.disconnect)
canvas.create_window(50, 100, window=disconnect_btn)

# Connect button
connect_btn = tk.Button(text="Connect", command=tv_box.connect)
canvas.create_window(150, 100, window=connect_btn)

# Screenshot button
screenshot_btn = tk.Button(text="Screen Shot", command=tv_box.screenshot)
canvas.create_window(250, 100, window=screenshot_btn)

# Reboot button
reboot_btn = tk.Button(text="Reboot", command=tv_box.reboot)
canvas.create_window(350, 100, window=reboot_btn)

# Shutdown button
shutdown_btn = tk.Button(text="Shutdown", command=tv_box.shutdown)
canvas.create_window(450, 100, window=shutdown_btn)

# Pull Entry & Button
pull_entry = tk.Entry(root)
canvas.create_window(250, 225, window=pull_entry)

pull_btn = tk.Button(text="Pull", command= lambda: tv_box.pull(pull_entry.get()))
canvas.create_window(250, 275, window=pull_btn)

# Exit button
exit_btn = tk.Button(text="Exit", command=tv_box.exit)
canvas.create_window(250, 150, window=exit_btn)

# MAIN LOOP
root.mainloop()
