import os
import ctypes
import keyboard
import time
import sys
import psutil
from cliutil.Permissions import getwindowsadmin
from cliutil.Selections import listselection
from cliutil.Questions import stringquestion
from cliutil.Questions import numberquestion
from cliutil.Questions import yesnoquestion
from cliutil.Configuration import writeconfiguration
from cliutil.Configuration import readfile
from glob import iglob as glob

# scriptpath = os.path.dirname(os.path.abspath(__file__))

if not getwindowsadmin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    exit()


def new_config():
    """
    Create a new configuration file
    :return: None
    """
    new_macro = stringquestion("Please input a trigger key", verify=True)[0]
    new_process = stringquestion("Please pick a process name to suspend", verify=True)
    new_duration = int(numberquestion("Please enter a duration in seconds to suspend the process for", verify=True))
    while True:
        new_name = stringquestion("What will this configuration be named", verify=True)
        if os.path.isfile(new_name + '.cfg'):
            if yesnoquestion("This configuration already exists! Overwrite it?"):
                writeconfiguration(new_name + '.cfg',
                                   {
                                       "macro": new_macro,
                                       "process": new_process,
                                       "duration": new_duration
                                   }, overwrite=True)
                return new_name + '.cfg'
            else:
                continue


def toggle_connection(process, duration):
    """
    Suspend the process for duration
    :return: None
    """
    x = os.popen('tasklist').read().strip().split("\n")
    for i in x:
        i = i.split()
        if i[0] == process:
            print(i)
            p = psutil.Process(int(i[1]))
            print("Suspending")
            p.suspend()
            time.sleep(duration)
            print("Resuming")
            p.resume()


configs = glob('*.cfg')
if len(configs) == 0:
    if yesnoquestion("No configs detected. Create one?"):
        variables = readfile(new_config())
    else:
        print("No config loaded or created. Exiting.")
        variables = None
        exit()
else:
    variables = listselection(configs, prompt="Please select a configuration", verify=True)
    variables = readfile(configs[variables])

# Start lagswitch loop
print("Macro key is: " + variables['macro'])
print("Suspending process: " + variables['process'])
print("For: " + str(variables['duration']) + " seconds")
while True:
    key = keyboard.read_key()
    if key == variables['macro']:
        toggle_connection(variables['process'], int(variables['duration']))
