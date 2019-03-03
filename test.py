import os

adapters = os.popen('wmic nic get name, index').read().split('\n\n')
for i in adapters:
    print(i)
answer = input("Please pick a network adapter to cut")
try:
    adapter = int(answer)
    for i in adapters:
        if (str(adapter) == i[:len(str(adapter))]):
            print("Selected adapter: " + ' '.join(i.split()[1:]))
            break
except:
    print("Please input a integer answer")
