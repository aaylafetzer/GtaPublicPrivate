import importlib
import subprocess
import os
import ctypes
import keyboard
import time
import psutil
import sys
from pathlib import Path

scriptpath = os.path.dirname(os.path.abspath(__file__))
configs = []
macro = None
process = None
duration = None

try: #Check for admin rights
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

if (is_admin == False):
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    exit()

def config_scan():
    #Check for any config files
    if not os.path.exists(scriptpath + '\\cfg\\'):
        os.makedirs(scriptpath + '\\cfg\\')
    else:  #From the lack of a config directory we can assume no configs exist
        for i in os.listdir(scriptpath + '\\cfg\\'):
            if i.endswith('.cfg'):
                configs.append(i)

def new_config():
    global macro, adapter, duration
    #Make a new config file
    approved = False
    while (not approved):
        macro = input("Please input a key to be used as the trigger key (only the first key will be used): ")[:1]
    approved = False
    while (not approved):
        process = input("Please pick a process name to suspend: ")
        approved = True
    approved = False
    while (not approved):
        duration = input("Please enter a duration in seconds to suspend the process for: ")
        try:
            duration = int(duration)
            approved = True
        except:
            print("Please enter an integer answer")
    approved = False
    while (not approved):
        name = input("What would you like to call this configuration?: ")
        path = scriptpath + '\\cfg\\' + name + '.cfg'
        file = Path(path)
        if file.is_file():
            print("This file already exists!")
        else:
            print("Saving configuration: " + name + '.cfg')
            f = open(path, 'w')
            f.write("Macro:" + macro + '\n')
            f.write("Process:" + str(process) + '\n')
            f.write("Duration:" + str(duration) + '\n')
            f.close()
            approved = True

def load_config(path):
    global macro, process, duration
    f = open(path, 'r')
    macro = f.readline()[6:].strip()
    process = f.readline()[8:].strip()
    duration = int(f.readline()[9:].strip())

def toggle_connection():
    x = os.popen('tasklist').read().strip().split("\n")
    for i in x:
        i = i.split()
        if (i[0] == process):
            print(i)
            p = psutil.Process(int(i[1]))
            print("Suspending")
            p.suspend()
            time.sleep(duration)
            print("Resuming")
            p.resume()

config_scan()

#Create a new config file if none exist
if (len(configs) == 0):
    answer = input("No config files found in directory. Would you like to make a new one? Y/n: ")
    while True:
        if (answer == 'y' or answer == 'Y'):
            new_config()
            config_scan()
            break
        elif (answer == 'n' or answer == 'N'):
            print("No Config Files Found, Exiting")
            exit()
        else:
            print("Please input a y or an n")

#Pick a premade configuration
print("Please select a config to load")
for i in range(len(configs)):
    print(str(i) + ': ' + configs[i])
print(str(len(configs)) + ': Make a new config file')
while(True):
    answer = input()
    try:
        answer = int(answer)
        if (int(answer) == len(configs)):
            new_config()
            config_scan()
            exit()
        else:
            load_config(scriptpath + '\\cfg\\' + configs[answer])
        break
    except:
        print("Please give an integer answer")

#Start lagswitch loop
print("Macro key is: " + macro)
print("Suspending process: " + process)
print("For: " +  str(duration) + " seconds")
while (True):
    key = keyboard.read_key()
    if (key == macro):
        toggle_connection()
