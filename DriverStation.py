import bluetooth
import time
import _thread as thread
import pygame

searchtime = 2

def loading(s,randint):
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    while s+1 > 0:
        print(" .",end="")
        time.sleep(1)
        s -=1
    print("\nDetected %s joysticks: " % (pygame.joystick.get_count())+str(joysticks)+"\n")
    return joysticks

def findDevices():
    try:
        nearby_devices = bluetooth.discover_devices(duration=searchtime, lookup_names=True, flush_cache=True, lookup_class=False)
        print("\n\nFound %d devices" % len(nearby_devices))
        i = 0
        for addr, name in nearby_devices:
            i+=1
            try:
                print(str(i)+": %s - %s" % (addr, name))
            except UnicodeEncodeError:
                print(str(i)+": %s - %s" % (addr, name.encode('utf-8', 'replace')))
        return nearby_devices
    except:
        print("\nError finding robots")

print("MiniFRC Driver Station v1.0\n")
print("Booting...",end="")
joysticks = thread.start_new_thread(loading,(searchtime,1))
devices = findDevices()

