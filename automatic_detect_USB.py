import detectUSB
import pyudev

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by('block')
prev_action = ''

action, device = monitor.receive_device()
for device in iter(monitor.poll, None):
    if 'ID_FS_TYPE' in device:
        detectUSB.handleDeviceByAction(prev_action, device.action,device.get('ID_FS_LABEL'))
        print('{0} - {1}'.format(device.action,device.get('ID_FS_LABEL')))
        prev_action = device.action
