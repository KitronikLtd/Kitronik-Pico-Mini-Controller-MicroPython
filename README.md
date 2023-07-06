# Kitronik Mini Controller for Pico
This repo contains the MicroPython library file for the [Kitronik Mini Controller for Raspberry Pi Pico](https://kitronik.co.uk/5353).

To use the library you can save the `KitronikPicoMiniController.py` file onto the Pico so it can be imported.

While this controller can be used with a standard Pico, it is better suited for use with a Pico W which is then connected to another device and used to control it.

To use this controller with a standard Pico you could control other devices or sensors by connecting them to the broken out GPIO pins.

When using this controller with a Pico W you can connect it to other wireless devices, such as another Pico W, to control them wirelessly using the Mini Controller.

## Mini Controller with Pico ARP Example
Also in this repo is an example of how to use the Mini Controller with a Pico W to control the [Kitronik Autonomous Robotics Platform for Pico](https://kitronik.co.uk/5335). The ARP buggy can have a second Pico W plugged in to it allowing the Mini Controller to drive the ARP buggy over Bluetooth.

To learn more about Bluetooth on the Raspberry Pi Pico W checkout this [blog post](https://kitronik.co.uk/blogs/resources/the-raspberry-pi-pico-w-now-has-bluetooth-connectivity).

![Mini Controller for Pico controlling the Pico ARP wirelessly](MiniControllerWithARP.gif)

The example code for this can be found in the `Mini Controller with Pico ARP` folder.

Both Pico Ws need a copy of the [`KitronikPicoWBluetooth.py`](https://github.com/KitronikLtd/Kitronik-Pico-W-Bluetooth-MicroPython/blob/main/KitronikPicoWBluetooth.py) file saved onto them.

The Pico W for this Mini Controller also needs a copy of the `Pico Controller.py` file saved onto it, as well as the `KitronikPicoMiniController.py` library from this repo.

Then the Pico W for the ARP buggy needs a copy of the `Pico ARP.py` file saved onto it, as well as the [`PicoAutonomousRobotics.py`](https://github.com/KitronikLtd/Kitronik-Pico-Autonomous-Robotics-Platform-MicroPython/blob/main/PicoAutonomousRobotics.py) library.

## Using the KitronikPicoMiniController.py Library
### Setup the Mini Controller
To use the Mini Controller for Pico we first need to import the library and setup our controller. To initialise our controller we can use the `MiniController` class which will setup all of our buttons and the buzzer for us.
``` python
from KitronikPicoMiniController import *
# Setup Mini Controller for Pico
controller = MiniController()
```

### Detecting button presses
To detect when a button has been pressed on our Mini Controller we can use the `pressed` function on each of our buttons. As we don't know when a button is going to be pressed it is best to continuously check for them in a loop.

Inside of the loop we can then use a series of `if` statements to check when each button is being pressed. Inisde of each `if` statement we can respond to a button press by executing some code, such as playing a tone on the buzzer.
``` python
while True:
    if controller.Up.pressed():
        # Respond to Up button being pressed
    if controller.Down.pressed():
        # Respond to Down button being pressed
    if controller.Left.pressed():
        # Respond to Left button being pressed
    if controller.Right.pressed():
        # Respond to Right button being pressed
    if controller.A.pressed():
        # Respond to A button being pressed
    if controller.B.pressed():
        # Respond to B button being pressed
```

The Mini Controller has some of the GPIO pins broken out so we can access them and customise our controller. Two of these pins are at the top of the controller and could be used for adding left and right shoulder buttons.

To setup the two shoulder buttons we can use the `KitronikButton` class inside the Mini Controller library. When initialising the shoulder buttons we need to give the GPIO pin number as the input for where each of our buttons are connected to.
``` python
# Setup additional Left Shoulder button
LeftShoulder = KitronikButton(16)
# Setup additional Right Shoulder button
RightShoulder = KitronikButton(14)
```

We can now use the shoulder buttons like we would any of the default buttons on the Mini Controller.
``` python
if LeftShoulder.pressed():
    # Respond to Left Shoulder button being pressed
if RightShoulder.pressed():
    # Respond to Right Shoulder button being pressed
```

### Using the buzzer
To use the buzzer on our Mini Controller we have two different ways of playing a tone.

The first is to use the `playTone` function, then wait for a period of time, and finally use the `stopTone` function. In this code we ask the buzzer to play a tone at 500 Hz. Then we use the `sleep` function to wait for 1 second. And finally we stop playing the tone after we have waited for 1 second.
``` python
# Play tone at frequency 500 Hz
controller.Buzzer.playTone(500)
# Sleep for 1 second
sleep(1)
# Stop tone playing
controller.Buzzer.stopTone()
```

The second is to use the `playTone_Length` function. In this code we ask the buzzer to again play a tone at 500 Hz, but we also ask it to only play the tone for 50 milliseconds.
``` python
# Play tone at frequency 500 Hz for 50 milliseconds
controller.Buzzer.playTone_Length(500, 50)
```
