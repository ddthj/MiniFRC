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

searchtime = 5 #how long we look for bluetooth devices, less than 4 seems to be unreliable

def loading(s,randint):
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    while s+1 > 0:
        print(" .",end="")
        time.sleep(1)
        s -=1
    
    print("\nDetected %s joystick(s): " % (pygame.joystick.get_count())+str(joysticks)+"\n")
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
        print("\nError finding available robots")

print("MiniFRC Driver Station v1.0\n")
print("Booting...",end="")
thread.start_new_thread(loading,(searchtime,1)) #grabs connected joysticks with pygame while bluetooth is still searching in the main thread
devices = findDevices() #finds bluetooth devices

for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    for i in range(0,5):
        events = pygame.event.get()
        time.sleep(0.1)
        #here we are updating the pygame events over and over to attempt to get joystick axis values

    name = joystick.get_name()
    print("\n\nJoystick name: %s" % (name))
    
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

#
#
'''
This is where we begin the user setup of the driver station.
We have a list of joysticks and a list of bluetooth devices that the user must select/configure
'''
#
#

robot = devices[int(input("Which device above is your robot? (enter number)"))-1]

driver_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
driver_socket.connect((str(robot[0]),7))
print("Connected!")
driver_socket.send("a")
print("Sent Message!")
driver_socket.close()












'''
#Debuging controller axis stuff:

if pygame.joystick.get_count() >0:
    joystick_one = pygame.joystick.Joystick(0)
    joystick_one.init()


while 1:
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                os._exit(1)
    axis = joystick_one.get_hat(0)
    print(axis)
    time.sleep(0.05)
'''
  
    
    
