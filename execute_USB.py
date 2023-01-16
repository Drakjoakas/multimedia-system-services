
import subprocess
import os
import detectUSB

def execute():
    print('Running execute function')
    getUserProc = subprocess.Popen(['whoami'],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    user, err = getUserProc.communicate()
    user = user.decode('ascii')[:-1]

    connected_devices = os.listdir('/media/{}'.format(user))
    print("HOLA")
    print(connected_devices)
    if len(connected_devices) > 0:
        name = connected_devices[-1]
        detectUSB.handleDeviceByAction('add', 'change', name)
