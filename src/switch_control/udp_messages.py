__author__ = 'J. B. Otterson'
__copyright__ = """
Copyright 2025, J. B. Otterson N1KDO.
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
__version__ = '0.0.3'  # 2025-12-31

from utils import upython
import asyncio
import micro_logging as logging
import socket
from struct import calcsize, pack_into

'''
        payload = {'radio_1_antenna': antennas_selected[0],  # is int (0->8), could be uint8
                   'radio_2_antenna': antennas_selected[1],  # is int (0->8), could be uint8
                   'radio_names': config['radio_names'],     # 2x16 char limit from UI
                   'antenna_names': config['antenna_names'], # 8x20 char limit from UI
                   'antenna_bands': config['antenna_bands'], # 8x int, could be uint16
                   # 'hostname': config['hostname'],         # 64 char limit from UI
                   }
'''
# uint8 uint8 16s 16s 20s 20s 20s 20s 20s 20s 20s 20s hhhhhhhh64s
STATUS_BROADCAST_FMT = 'BB16s16s20s20s20s20s20s20s20s20shhhhhhhh64s'
STATUS_BROADCAST_SIZE = calcsize(STATUS_BROADCAST_FMT)


def calculate_broadcast_address(ip_address, netmask):
    # validate quick sanity of inputs
    try:
        ip_parts = [int(x) for x in ip_address.split('.')]
        mask_parts = [int(x) for x in netmask.split('.')]
        if len(ip_parts) != 4 or len(mask_parts) != 4:
            raise ValueError('invalid ip or netmask format')
    except Exception as ex:
        logging.error(f'calculate_broadcast_address: invalid input: {ex}', 'udp_messages:calculate_broadcast_address')
        raise

    ip_int = sum([int(x) << 8 * i for i, x in enumerate(reversed(ip_address.split('.')))])
    mask_int = sum([int(x) << 8 * i for i, x in enumerate(reversed(netmask.split('.')))])
    mask_mask = mask_int ^ 0xffffffff
    bcast_int = ip_int | mask_mask
    bcast_addr = ".".join(map(str, [
        ((bcast_int >> 24) & 0xff),
        ((bcast_int >> 16) & 0xff),
        ((bcast_int >> 8) & 0xff),
        (bcast_int & 0xff),
    ]))
    return bcast_addr

def _fit_and_encode(s, length):
    """Encode string to bytes, truncate or pad with NUL to length."""
    if s is None:
        s = ''
    b = s.encode('utf-8', 'ignore')[:length]
    if len(b) < length:
        b = b + (b'\x00' * (length - len(b)))
    return b


class SendBroadcasts:
    """
    class to send UDP status datagrams
    """

    def __init__(self, target_ip, target_port, config: dict, antennas_selected):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockaddr = socket.getaddrinfo(target_ip, target_port)[0][-1]
        self.config = config
        self.antennas_selected = antennas_selected
        self.buf = bytearray(STATUS_BROADCAST_SIZE)
        logging.info(f'Broadcast address is {target_ip}:{target_port}', 'udp_messages:SendBroadcasts()')
        logging.info(f'Starting status broadcasts', 'udp_messages:SendBroadcasts()')
        self.run = True

    def send(self, payload):
        self.socket.sendto(payload, self.sockaddr)

    async def send_datagrams(self):
        radio_names = self.config['radio_names']
        antenna_names = self.config['antenna_names']
        antenna_bands = self.config['antenna_bands']
        antennas_selected = self.antennas_selected
        hostname = self.config['hostname']
        buf = self.buf
        sleep = asyncio.sleep
        while self.run:
            try:
                pack_into(STATUS_BROADCAST_FMT, buf, 0,
                          int(antennas_selected[0]),
                          int(antennas_selected[1]),
                          _fit_and_encode(radio_names[0] if len(radio_names) > 0 else '', 16),
                          _fit_and_encode(radio_names[1] if len(radio_names) > 1 else '', 16),
                          _fit_and_encode(antenna_names[0] if len(antenna_names) > 0 else '', 20),
                          _fit_and_encode(antenna_names[1] if len(antenna_names) > 1 else '', 20),
                          _fit_and_encode(antenna_names[2] if len(antenna_names) > 2 else '', 20),
                          _fit_and_encode(antenna_names[3] if len(antenna_names) > 3 else '', 20),
                          _fit_and_encode(antenna_names[4] if len(antenna_names) > 4 else '', 20),
                          _fit_and_encode(antenna_names[5] if len(antenna_names) > 5 else '', 20),
                          _fit_and_encode(antenna_names[6] if len(antenna_names) > 6 else '', 20),
                          _fit_and_encode(antenna_names[7] if len(antenna_names) > 7 else '', 20),
                          int(antenna_bands[0]) if len(antenna_bands) > 0 else 0,
                          int(antenna_bands[1]) if len(antenna_bands) > 1 else 0,
                          int(antenna_bands[2]) if len(antenna_bands) > 2 else 0,
                          int(antenna_bands[3]) if len(antenna_bands) > 3 else 0,
                          int(antenna_bands[4]) if len(antenna_bands) > 4 else 0,
                          int(antenna_bands[5]) if len(antenna_bands) > 5 else 0,
                          int(antenna_bands[6]) if len(antenna_bands) > 6 else 0,
                          int(antenna_bands[7]) if len(antenna_bands) > 7 else 0,
                          _fit_and_encode(hostname, 64))
                # send the raw buffer
                self.send(buf)
            except Exception as ex:
                logging.error(f'Broadcast pack/send failed: {ex}', 'udp_messages:send_datagrams')
            await sleep(1.0)

    def stop(self):
        self.run = False
