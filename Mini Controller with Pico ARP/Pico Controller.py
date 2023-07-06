from bluetooth import BLE
from time import sleep_ms
from KitronikPicoMiniController import *
from KitronikPicoWBluetooth import BLECentral
from machine import Pin

# Setup Mini Controller for Pico
controller = MiniController()
led = Pin("LED", Pin.OUT)

# Setup Bluetooth central
central = BLECentral(BLE())
notFound = False

# Set scan callback, to process the results of a scan
def onScan(addr_type, addr, name):
    global notFound
    if addr_type is not None:
        print("Found sensor:", addr_type, addr, name)
        central.connect()
    else:
        notFound = True
        print("No sensor found.")

central.scan(callback=onScan)

# Wait for connection...
while not central.isConnected():
    sleep_ms(100)
    while notFound:
        # Flash LED to show the peripheral has not been found
        led(1)
        sleep_ms(100)
        led(0)
        sleep_ms(100)

# Set read callback, to process start command
def readCallback(value):
    val = bytes(value).decode("utf-8")
    if val == "START":
        central.readCallback = None

central.readCallback = readCallback
central.read()

# Wait for start command to be read
while central.readCallback is not None:
    sleep_ms(50)

# Turn on LED to show the buggy is ready to be controlled
led(1)

# Loop while the controller is connected to the buggy
while central.isConnected():
    move = 0 # STOP

    if controller.Up.pressed():
        move = 1 # FORWARD
    if controller.Down.pressed():
        move = 2 # REVERSE
    if controller.Left.pressed():
        move = 3 # LEFT
    if controller.Right.pressed():
        move = 4 # RIGHT
    if controller.A.pressed():
        move = 5 # INCREASE SPEED
    if controller.B.pressed():
        move = 6 # DECREASE SPEED
    
    # Send the move command to the buggy
    config = bytes([move])
    central.write(config)

    sleep_ms(125)

# Turn off the LED to show its disconnected
led(0)
