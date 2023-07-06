from bluetooth import BLE
from time import sleep_ms
from PicoAutonomousRobotics import KitronikPicoRobotBuggy
from KitronikPicoWBluetooth import BLEPeripheral

# Setup Pico Autonomous Robotics Platform Buggy
buggy = KitronikPicoRobotBuggy()
# Set the buggy speed to 50%
speed = 50

# Set LEDs to red to show its turned on
for i in range(4):
    buggy.setLED(i, (100, 0, 0))
buggy.show()

# Setup Bluetooth peripheral
peripheral = BLEPeripheral(BLE())

# Wait for connection...
while not peripheral.isConnected():
    sleep_ms(100)

# Set LEDs to yellow to show a central device has connected
for i in range(4):
    buggy.setLED(i, (100, 100, 0))
buggy.show()

# Set write callback, to process a write event
def writeCallback(value):
    global received
    received = bytes(value)

received = None
peripheral.writeCallback = writeCallback

# Set read callback, to send start command
def readCallback():
    peripheral.readCallback = None
    return "START"

peripheral.readCallback = readCallback

# Wait for start command to be read
while peripheral.readCallback is not None:
    sleep_ms(50)

# Set LEDs to green to show the buggy is ready to be controlled
for i in range(4):
    buggy.setLED(i, (0, 100, 0))
buggy.show()

# Loop while the controller is connected to the buggy
while peripheral.isConnected():
    # When a message has been received from the controller
    if received is not None:
        config = received
        received = None

        move = config[0]

        if move == 1: # FORWARD
            buggy.motorOn("l", "f", speed)
            buggy.motorOn("r", "f", speed)
        elif move == 2: # REVERSE
            buggy.motorOn("l", "r", speed)
            buggy.motorOn("r", "r", speed)
        elif move == 3: # LEFT
            buggy.motorOn("l", "r", speed)
            buggy.motorOn("r", "f", speed)
        elif move == 4: # RIGHT
            buggy.motorOn("l", "f", speed)
            buggy.motorOn("r", "r", speed)
        elif move == 5: # INCREASE SPEED
            if speed < 100:
                speed += 10
        elif move == 6: # DECREASE SPEED
            if speed > 0:
                speed -= 10
        else: # STOP
            buggy.motorOff("l")
            buggy.motorOff("r")

    sleep_ms(50)

# Stop the buggy, controller disconnected
buggy.motorOff("l")
buggy.motorOff("r")

# Set LEDs to red to show its disconnected
for i in range(4):
    buggy.setLED(i, (100, 0, 0))
buggy.show()
