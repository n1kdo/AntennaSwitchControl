from utils import upython

if not upython:
    from not_machine import machine
else:
    import machine

a_pins = [
    machine.Pin(13, machine.Pin.OUT, value=0),  # GP9 pin 17
    machine.Pin(12, machine.Pin.OUT, value=0),  # GP9 pin 16
    machine.Pin(11, machine.Pin.OUT, value=0),  # GP9 pin 5
    machine.Pin(10, machine.Pin.OUT, value=0),  # GP9 pin 14
    machine.Pin(9, machine.Pin.OUT, value=0),  # GP9 pin 12
    machine.Pin(8, machine.Pin.OUT, value=0),  # GP9 pin 11
    machine.Pin(7, machine.Pin.OUT, value=0),  # GP9 pin 10
    machine.Pin(6, machine.Pin.OUT, value=0),  # GP9 pin 9
]

# define pins for antenna switch port b
b_pins = [
    machine.Pin(27, machine.Pin.OUT, value=0),  # GP27 pin 32
    machine.Pin(26, machine.Pin.OUT, value=0),  # GP26 pin 31
    machine.Pin(21, machine.Pin.OUT, value=0),  # GP21 pin 27
    machine.Pin(20, machine.Pin.OUT, value=0),  # GP20 pin 26
    machine.Pin(19, machine.Pin.OUT, value=0),  # GP19 pin 25
    machine.Pin(18, machine.Pin.OUT, value=0),  # GP18 pin 24
    machine.Pin(17, machine.Pin.OUT, value=0),  # GP17 pin 22
    machine.Pin(16, machine.Pin.OUT, value=0),  # GP16 pin 21
]


def set_port_a(selected):
    for i in range(len(a_pins)):
        a_pins[i].off()
    a_pins[selected+1].on()


def set_port_b(selected):
    for i in range(len(b_pins)):
        b_pins[i].off()
    b_pins[selected+1].on()

