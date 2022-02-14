#!/usr/bin/env python3

import subprocess
from ppadb.client import Client as AdbClient
import sys
import os


# GLOBAL CONSTANTS
LHOST = "127.0.0.1"
LPORT = 5037


class Device:
    def __init__(self, rhost, rport=5555, dname="emulator-5555"):
        subprocess.call(["adb", "start-server"])

        self.rhost = rhost
        self.rport = rport
        self.dname = dname
        self.client = AdbClient(host=LHOST, port=LPORT)
        self.dispatcher = {
            "disconnect":self.disconnect,
            "screenshot":self.screenshot
        }
        self.device = self.connect()

    # Connect to remote host
    def connect(self):
        print(f"* connecting to {self.rhost}:{self.rport}")

        if self.client.remote_connect(self.rhost, self.rport):
            print("* connected successfully")
        else:
            print(f"* unknown host {self.rhost}")
            sys.exit(0)    

        return self.client.device(f"{self.rhost}:{self.rport}")

    # Disconnect from remote host
    def disconnect(self):
        print(f"* disconnect {self.rhost}:{self.rport}")
        self.client.remote_disconnect(self.rhost, self.rport)

    # Take screenshot of remote host screen
    def screenshot(self):
        with open("screen.png", "wb") as fp:
            fp.write(self.device.screencap())
            print("* screenshot saved as screen.png")

    # Share live screen of remote host
    @staticmethod
    def sharescreen():
        os.system("adb exec-out screenrecord --output-format=h264 - | ffplay -framerate 60 -probesize 32 -sync video - > /dev/null 2>&1")

    # Pull file or folder from remote device to host device
    def pull(self, filepath="", filename=""):
        temp_file_name = ""
        
        for char in filepath[::-1]:
            if char != "/":
                temp_file_name += char

        filename = temp_file_name[::-1]

        self.device.pull(filepath, filename)

    # Push file or folder from host device to remote device
    def push(self, lpath, rpath):
        self.device.push(lpath, rpath)

    # Shutdown
    def shutdown(self):
        self.device.shell("shutdown -r now")

    # Reboot
    def reboot(self):
        self.device.shell("reboot")

    # Constantly write remote device log to log file
    def get_log(self, file=None, bytes=2048):
        print(f"* writing log to {file}")

        def dump_logcat(connection):
            while True:
                data = connection.read(bytes)

                if not data:
                    break

                if file:
                    log_file = open(file, "a+")
                    log_file.truncate(0)

                    print(data.decode('utf-8'), file=log_file)
                else:
                    print(data.decode("utf-8"))
    
            connection.close()        

        self.device.shell("logcat", handler=dump_logcat)

    # Exit
    def exit(self):
        self.disconnect()
        subprocess.call(["adb", "kill-server"])
        sys.exit(0)
