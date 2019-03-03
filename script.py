import importlib
import subprocess
import os
import ctypes
import keyboard
import time
from pathlib import Path

scriptpath = os.path.dirname(os.path.abspath(__file__))
configs = []
macro = None
adapter = None
duration = None

try: #Check for admin rights
    is_admin = os.getuid() == 0
except AttributeError:
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

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
    answer = input("No config files found in directory. Would you like to make a new one? Y/n: ")
    while True:
        if (answer == 'y' or answer == 'Y'):
            break
        elif (answer == 'n' or answer == 'N'):
            print("No Config Files Found, Exiting")
            exit()
        else:
            print("Please input a y or an n")
    #Make a new config file
    approved = False
    while (not approved):
        macro = input("Please input a key to be used as the trigger key: ")[:1]
        print(macro)
        answer = input("Does this macro seem right? Y/n: ")
        while True:
            if (answer == 'y' or answer == 'Y'):
                approved = True
                break
            elif (answer == 'n' or answer == 'N'):
                print("Restarting capture")
                break
            else:
                print("Please input a y or an n")
    approved = False
    while (not approved):
        adapters = os.popen('wmic nic get name, index').read().split('\n\n')
        for i in adapters:
            print(i)
        answer = input("Please pick a network adapter to cut: ")
        try:
            adapter = int(answer)
            for i in adapters:
                if (str(adapter) == i[:len(str(adapter))]):
                    print("Selected adapter: " + ' '.join(i.split()[1:]))
                    approved = True
                    break
            if (not approved):
                print("Please pick a number from the list")
        except:
            print("Please input a integer answer")
    approved = False
    while (not approved):
        duration = input("Please enter a duration in seconds to shut off the network adapter for: ")
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
            f.write("ShotKey:" + macro + '\n')
            f.write("Adapter:" + str(adapter) + '\n')
            f.write("Duration:" + str(duration) + '\n')
            f.close()
            approved = True

def load_config(path):
    global macro, adapter, duration
    f = open(path, 'r')
    macro = f.readline()[8:].strip()
    adapter = f.readline()[8:].strip()
    duration = int(f.readline()[9:].strip())

def toggle_connection():
    global adapter, duration
    print("Disable")
    os.system('wmic path win32_networkadapter where index=' + adapter + ' call disable')
    time.sleep(duration)
    os.system('wmic path win32_networkadapter where index=' + adapter + ' call enable')

config_scan()

#Create a new config file if none exist
if (len(configs) == 0):
    new_config()
    config_scan()

#Exit if script is not being run as admin
if (is_admin == False):
    print("This tool needs to be run as an administrator to work properly! Press any key to exit")
    exit()

#Pick a premade configuration
print("Please select a config to load")
for i in range(len(configs)):
    print(str(i) + ': ' + configs[i])
while(True):
    answer = input()
    try:
        answer = int(answer)
        load_config(scriptpath + '\\cfg\\' + configs[answer])
        break
    except:
        print("Please give an integer answer")

#Start lagswitch loop
print("Macro key is: " + macro)
while (True):
    firing = False
    key = keyboard.read_key()
    if (key == macro and not firing):
        firing = True
        firing = toggle_connection()
