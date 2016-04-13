'''
Mini FRC Drivers Station


Requirements:
Made in Python 3.4
Uses Pygame and Bluetooth

This program is for grabbing data from joysticks to control arduinos connected to bluetooth

Todo List:
- Actually connect over bluetooth -DONE
- set up grabbing values from the detected joysticks -DONE
- clean up functions/create new functions - NO
- don't break it - MAYBE

'''

#
#
'''
This inits the joysticks and pygame, also tells user the current joystick setup
'''
#
#

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
        #here we are updating the pygame events over and over to attempt to get joystick axis values

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
This is where we begin talking to the robot

We grab the axis from the first joystick and package it to be sent the the arduino
'''
#
#


if pygame.joystick.get_count() >0:
    com = "COM"
    com += str(input("Please enter the robot COM port: "))
    try:
        s = serial.Serial(str(com), 9600,timeout = None)
        print("Connected to robot!")
        joystick_one = pygame.joystick.Joystick(0)
        joystick_one.init()
        axes = joystick.get_numaxes()
        Clock = pygame.time.Clock()
        while 1:
            Clock.tick(20)
            events = pygame.event.get()
            package = ""
            for j in range( axes ):
                package += str(joystick.get_axis( j ))
                package +=";"
            s.write(bytes(package,'utf-8'))
            

            '''
            message = s.read(size = 128)
            if message != b'':
                print(str(message))
            '''
    except Exception as e:
        print("Couldn't connect to the robot on this port, here's the problem: \n\n"+str(e))

else:
    print("No joysticks found, closing...")








#Debuging controller axis stuff:
#0 - left/right
#1 - forward/backward
#2 - throttle
#3 - yaw

'''
if pygame.joystick.get_count() >0:
    joystick_one = pygame.joystick.Joystick(0)
    joystick_one.init()
    axes = joystick.get_numaxes()
    while 1:
        time.sleep(0.2)
        events = pygame.event.get()
        print("\n\n")
        for j in range( axes ):
            axis = joystick_one.get_axis( j )
            print("Axis %s value: %s" % (j, axis) )

'''
    
    
