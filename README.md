# MiniFRC
This is a Driver Station for controlling bluetooth arduino robots.

Basically it takes joystick inputs, converts them into a string, and sends that out over the COM port that your bluetooth robot is connected to

How to modify the package:

The package is the data sent out over bluetooth. by default all joystick axes are sent.
If you want to send joystick buttons, just do:

package+= str(joystick.get_button(x))+";" where x is the button you want to grab from
