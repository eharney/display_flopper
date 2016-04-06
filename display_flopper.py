#!/usr/bin/python3
# Silly tool to jiggle monitors around in XFCE whe
# plugging in to/out of dock.
# EMH April 6 2016
# License: CC0

# inotify didn't seem to work w/ /sys/, thus, polling

import os
import time

# Thinkpad X1 carbon
device_root = '/sys/class/drm/card0/'
dock_device = 'card0-DP-4'
laptop_xrandr_device = 'eDP1'
external_monitor_xrandr_device = 'DP2-2'

def device_present():
    try:
        stat_result = os.stat(device_root + dock_device)
    except FileNotFoundError:
        print('device found')
        return False

    print('device not found')
    return True


previous_status = device_present()

while True:
    current_status = device_present()

    if previous_status != current_status:
        if current_status == True:
            # Monitor appeared
            print('Monitor appeared')
            os.system('xrandr --output %s --off' % laptop_xrandr_device)
            os.system('xrandr --output %s --pos 1920x1080+0+0 --auto' %
                      external_monitor_xrandr_device)
        else:
            # Monitor unplugged
            print('Monitor unplugged')
            os.system('xrandr --output %s --off' % external_monitor_xrandr_device)
            os.system('xrandr --output %s --pos 1920x1080+0+0 --auto' %
                      laptop_xrandr_device)


    previous_status = current_status
    time.sleep(2)
