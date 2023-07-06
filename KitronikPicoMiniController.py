from machine import Pin, PWM
from time import sleep_ms

# The KitronikButton class enable the use of the 2 user input buttons on the board
class KitronikButton:
    def __init__(self, WhichPin):
        self.theButton = Pin(WhichPin, Pin.IN, Pin.PULL_DOWN)

    def pressed(self):
        return self.theButton.value()
    
    def irq(self, handler, trigger = Pin.IRQ_FALLING):
        if handler is None:
            self.theButton.irq(None)
            
        else:
            self.theButton.irq(handler, trigger)
    
# The KitronikBuzzer class enables control of the piezo buzzer on the board
class KitronikBuzzer:
    # Function is called when the class is initialised and sets the buzzer pin to GP2
    def __init__(self, WhichPin):
        self.buzzer = PWM(Pin(WhichPin))
        self.dutyCycle = 32767

    # Play a continous tone at a specified frequency
    def playTone(self, freq):
        if (freq < 30):
            freq = 30
        if (freq > 3000):
            freq = 3000
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(self.dutyCycle)

    # Play a tone at a speciied frequency for a specified length of time in ms
    def playTone_Length(self, freq, length):
        self.playTone(freq)
        sleep_ms(length)
        self.stopTone()

    # Stop the buzzer producing a tone
    def stopTone(self):
        self.buzzer.duty_u16(0)

class MiniController:
    def __init__(self):
        self.Up = KitronikButton(18)
        self.Down = KitronikButton(20)
        self.Left = KitronikButton(19)
        self.Right= KitronikButton(22)
        self.A = KitronikButton(10)
        self.B = KitronikButton(9)
        
        self.Buzzer = KitronikBuzzer(5)
