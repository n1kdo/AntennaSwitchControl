#
# antennas_selected_data.py -- antenna selected data class.
#

__author__ = 'J. B. Otterson'
__copyright__ = 'Copyright 2026 J. B. Otterson N1KDO.'
__version__ = '0.0.1'  # 2026-01-01

#
# Copyright 2026 J. B. Otterson N1KDO.
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



from cached_config_data import CachedConfigData

ANTENNAS_SELECTED_FILE = 'data/antennas_selected.json'

_KEY0 = '0'
_KEY1 = '1'
_KEY_ERROR = 'key must be int 0 or 1'
_VALUE_ERROR = 'value must be int 0 to 8'

class AntennasSelectedData(CachedConfigData):
    def __init__(self):
        super().__init__(ANTENNAS_SELECTED_FILE)

    @staticmethod
    def _default_config_data():
        return {_KEY0:1, _KEY1:2}

    def __getitem__(self, key):
        if key == 0:
            return self.get_item(_KEY0)
        elif key == 1:
            return self.get_item(_KEY1)
        else:
            raise KeyError(_KEY_ERROR)

    def __setitem__(self, key, value):
        if not isinstance(value, int) or not (0 <= value <= 8):
            raise ValueError(_VALUE_ERROR)
        if key == 0:
            self.set_item(_KEY0, value)
        elif key == 1:
            self.set_item(_KEY1, value)
        else:
            raise KeyError(_KEY_ERROR)
