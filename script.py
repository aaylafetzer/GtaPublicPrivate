import subprocess
import os

scriptpath = os.path.dirname(os.path.abspath(__file__))
configs = []

print scriptpath

#Check for any config files
if not os.path.exists(scriptpath + '\\cfg\\'):
    os.makedirs(scriptpath + '\\cfg\\')
else:  #From the lack of a config directory we can assume no configs exist
    for i in os.listdir(scriptpath + '\\cfg\\'):
        if i.endswith('.conf'):
            configs.append(i)

#Create a new config file if none exist
if (len(configs) == 0):
    print("No config files found in directory. Would you like to make a new one?")

input()

subprocess.check_output('wmic nic get name, index')
