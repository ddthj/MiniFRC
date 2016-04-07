'''
Mini FRC Drivers Station


Requirements:
Made in Python 3.4
Uses Pygame and Bluetooth

This program is for grabbing data from joysticks to control arduinos connected to bluetooth

Todo List:
- Actually connect over bluetooth
- set up grabbing values from the detected joysticks
- clean up functions/create new functions
- don't break it

'''
import bluetooth
import time
import _thread as thread
import pygame

searchtime = 5 #how long we look for bluetooth devices

def loading(s,randint):
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    while s+1 > 0:
        print(" .",end="")
        time.sleep(1)
        s -=1
    
    print("\nDetected %s joysticks: " % (pygame.joystick.get_count())+str(joysticks)+"\n")
    thread.exit()
    

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
thread.start_new_thread(loading,(searchtime,1)) #grabs connected joysticks with pygame while bluetooth is still searching in the main thread
devices = findDevices() #finds bluetooth devices

for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    #print(str(joystick))

    # Get the name from the OS for the controller/joystick
    name = joystick.get_name()
    print("\n\nJoystick name: %s" % (name))
    
    # Usually axis run in pairs, up/down for one, and left/right for
    # the other.
    axes = joystick.get_numaxes()
    print("Num of axes: %s" % (axes))
    
    for j in range( axes ):
        axis = joystick.get_axis( j )
        print("Axis %s value: %s" % (j, axis) )
        
    buttons = joystick.get_numbuttons()
    print("Number of buttons: %s"%(buttons))

    for k in range( buttons ):
        button = joystick.get_button( k )
        print("Button %s value: %s"%(k,button))
        
    # Hat switch. All or nothing for direction, not like joysticks.
    # Value comes back in an array.
    hats = joystick.get_numhats()
    print("Number of hats: %s" % (hats))
    
    for l in range( hats ):
        hat = joystick.get_hat( l )
        print("Hat %s value: %s" % (l, hat))
if pygame.joystick.get_count() >0:
    joystick_one = pygame.joystick.Joystick(0)
while 1:
    axis = joystick.get_axis(1)
    print(axis)
    
  
    
    
