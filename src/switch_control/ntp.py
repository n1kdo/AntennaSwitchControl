#
# NTP client for MicroPython and CPython
# This module provides a function to get the current time from an NTP server.
#
__author__ = 'J. B. Otterson'
__copyright__ = 'Copyright 2024, 2025 J. B. Otterson N1KDO.'
__version__ = '0.0.9'
#
# Copyright 2024, 2025, J. B. Otterson N1KDO.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import socket
import struct
import sys
import time

_IS_MICROPYTHON = sys.implementation.name == 'micropython'

if _IS_MICROPYTHON:
    import micro_logging as logging
    from machine import RTC
    _rtc = RTC()
else:
    import logging
    _rtc = None
    def const(i):
        return i

_UNIX_EPOCH = const(2208988800)  # 1970-01-01 00:00:00
_NTP_PORT = const(123)
_BUF_SIZE = const(1024)
_NTP_MSG = b'\x1b' + b'\0' * 47
_SOCKET_TIMEOUT = const(5)
_STRUCT_FORMAT = '!12I'

def get_ntp_time(host='pool.ntp.org'):
    sock = None
    try:
        address = socket.getaddrinfo(host, _NTP_PORT)[0][-1]
        # connect to server
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(_SOCKET_TIMEOUT)
        sock.sendto(_NTP_MSG, address)
        msg = sock.recvfrom(_BUF_SIZE)[0]
        sock.close()

        t = struct.unpack(_STRUCT_FORMAT, msg)[10] - _UNIX_EPOCH
        tt = time.gmtime(t)
        if _IS_MICROPYTHON:
            # set the RTC
            try:
                _rtc.datetime((tt[0], tt[1], tt[2], tt[6], tt[3], tt[4], tt[5], 0))
            except OSError as ose:
                logging.exception('OSError', 'ntp.get_ntp_time', ose)
        return tt
    except OSError as ose:
        logging.exception('OSError', 'ntp.get_ntp_time', ose)
        return None
    finally:
        if sock:
            sock.close()


def main():
    ntp_time = get_ntp_time()
    print('ntptime: ', ntp_time)
    tt = time.gmtime()
    print('gmtime:  ', tt)
    dt = f'{tt[0]:04d}-{tt[1]:02d}-{tt[2]:02d}T{tt[3]:02d}:{tt[4]:02d}:{tt[5]:02d}+00:00'
    print(dt)


if __name__ == '__main__':
    main()
