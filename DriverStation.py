'''
Mini FRC Drivers Station V1.1

Requirements:
Made in Python 3.4
Uses Pygame and Pyserial

This program is for grabbing data from joysticks to control arduinos connected to bluetooth
'''
import serial
import time
import pygame
print("MiniFRC Driver Station v1.0\n")
print("Booting...")
pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print("\nDetected %s joystick(s): " % (pygame.joystick.get_count())+str(joysticks)) 

for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    for i in range(0,5):
        events = pygame.event.get()
        time.sleep(0.1)
    name = joystick.get_name()
    print("\nJoystick name: %s" % (name))
    
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

    hats = joystick.get_numhats()
    print("Number of hats: %s" % (hats))
    
    for l in range( hats ):
        hat = joystick.get_hat( l )
        print("Hat %s value: %s" % (l, hat))

if pygame.joystick.get_count() >0:
    com = "COM"
    com += str(input("Please enter the robot COM port: "))
    try:
        s = serial.Serial(str(com), 9600,timeout = 2) #we pretend the robot is on a usb port
        print("Connected to robot!")
        joystick_one = pygame.joystick.Joystick(0) #initiate first joystick
        joystick_one.init()
        axes = joystick.get_numaxes()
        Clock = pygame.time.Clock()
        while 1:
            events = pygame.event.get() #update pygame internally
            package = ""
            for j in range( axes ):
                package += (str(round(joystick.get_axis( j ),1)) +";")
            #package+= str(joystick.get_button(0)) + ";"     this is an example of adding buttons to the package
            print(package)
            s.write(bytes(package,'utf-8'))
            Clock.tick(20) #driver station tested and run at 20FPS, results may vary at other framerates.
    except Exception as e:
        print("Couldn't connect to the robot on this port, here's the problem: \n\n"+str(e))

else:
    print("No joysticks found, closing...")

    
