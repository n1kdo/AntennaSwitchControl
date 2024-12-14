#
# relays support for AntennaSwitchControl.
#

__author__ = 'J. B. Otterson'
__copyright__ = """
Copyright 2024, J. B. Otterson N1KDO.
Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:
  1. Redistributions of source code must retain the above copyright notice, 
     this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright notice, 
     this list of conditions and the following disclaimer in the documentation 
     and/or other materials provided with the distribution.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE 
OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.
"""
__version__ = '0.1.0'

from utils import upython
import micro_logging as logging

if not upython:
    from not_machine import machine
else:
    import machine

NUM_RELAYS = 8

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


def set_port(radio: int, port_selected: int):
    if 0 <= port_selected < NUM_RELAYS:
        pins = None
        if radio == 1:
            pins = a_pins
        elif radio == 2:
            pins = b_pins
        if pins is not None:
            for i in range(len(pins)):
                pins[i].off()
            if port_selected > 0:
                pins[port_selected - 1].on()
    else:
        logging.error(f'Invalid port_selected {port_selected}')
