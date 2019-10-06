# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Tmv71Channels(KaitaiStruct):
    """This Kaitai Struct will parse a list of channels from a memory dump from
    a TM-V71A radio.  You can produce such a dump using tm-v71-tools
    (https://github.com/larsks/tm-v71-tools):
    
        tmv71 memory read -o memdump.bin
    """

    class ChannelBand(Enum):
        vhf = 5
        uhf = 8

    class ShiftDirection(Enum):
        simplex = 0
        up = 1
        down = 2

    class Modulation(Enum):
        fm = 0
        am = 1
        nfm = 2

    class Admit(Enum):
        none = 0
        dcs = 1
        ctcss = 2
        tone = 4
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.ensure_fixed_contents(b"\x00\x4B")

    class ExtendedFlagBits(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown = self._io.read_bits_int(7)
            self.lockout = self._io.read_bits_int(1) != 0


    class Channel(KaitaiStruct):
        """A channel encoded in the radio memory.
        
        Use the `data.deleted` member to check for deleted channels. A deleted
        channel is empty: it will not have any of the expected fields.
        """
        def __init__(self, number, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.number = number
            self._read()

        def _read(self):
            self.rx_freq_raw = self._io.read_u4le()
            _on = self.rx_freq_raw
            if _on == 4294967295:
                self.data = self._root.EmptyChannel(self._io, self, self._root)
            else:
                self.data = self._root.ChannelFields(self._io, self, self._root)

        @property
        def name(self):
            if hasattr(self, '_m_name'):
                return self._m_name if hasattr(self, '_m_name') else None

            self._m_name = self._root.channel_names[self.number]
            return self._m_name if hasattr(self, '_m_name') else None

        @property
        def extended_flags(self):
            if hasattr(self, '_m_extended_flags'):
                return self._m_extended_flags if hasattr(self, '_m_extended_flags') else None

            self._m_extended_flags = self._root.channel_extended_flags[self.number]
            return self._m_extended_flags if hasattr(self, '_m_extended_flags') else None


    class ChannelExtendedFlags(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.band = self._io.read_u1()
            self.flags = self._root.ExtendedFlagBits(self._io, self, self._root)


    class EmptyChannel(KaitaiStruct):
        """Represents an empty/deleted channel.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.padding = self._io.read_bytes(12)

        @property
        def deleted(self):
            if hasattr(self, '_m_deleted'):
                return self._m_deleted if hasattr(self, '_m_deleted') else None

            self._m_deleted = True
            return self._m_deleted if hasattr(self, '_m_deleted') else None


    class ChannelFields(KaitaiStruct):
        """These are the actual channel entry attributes.
        
        We also bring in the channel name from the top-level
        `channel_names` array, and some extended flags from the
        `channel_extended_flags` array.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rx_step_raw = self._io.read_u1()
            self.mod = self._root.Modulation(self._io.read_u1())
            self.flags = self._root.ChannelFlags(self._io, self, self._root)
            self.tone_frequency_raw = self._io.read_u1()
            self.ctcss_frequency_raw = self._io.read_u1()
            self.dcs_code_raw = self._io.read_u1()
            self.tx_offset_raw = self._io.read_u4le()
            self.tx_step_raw = self._io.read_u1()
            self.padding = self._io.read_u1()

        @property
        def extended_flags(self):
            if hasattr(self, '_m_extended_flags'):
                return self._m_extended_flags if hasattr(self, '_m_extended_flags') else None

            self._m_extended_flags = self._parent.extended_flags
            return self._m_extended_flags if hasattr(self, '_m_extended_flags') else None

        @property
        def rx_freq(self):
            if hasattr(self, '_m_rx_freq'):
                return self._m_rx_freq if hasattr(self, '_m_rx_freq') else None

            self._m_rx_freq = (self._parent.rx_freq_raw / 1000000.0)
            return self._m_rx_freq if hasattr(self, '_m_rx_freq') else None

        @property
        def tone_frequency(self):
            if hasattr(self, '_m_tone_frequency'):
                return self._m_tone_frequency if hasattr(self, '_m_tone_frequency') else None

            self._m_tone_frequency = self._root.tables.tone_frequency[self.tone_frequency_raw]
            return self._m_tone_frequency if hasattr(self, '_m_tone_frequency') else None

        @property
        def dcs_code(self):
            if hasattr(self, '_m_dcs_code'):
                return self._m_dcs_code if hasattr(self, '_m_dcs_code') else None

            self._m_dcs_code = self._root.tables.dcs_code[self.dcs_code_raw]
            return self._m_dcs_code if hasattr(self, '_m_dcs_code') else None

        @property
        def tx_offset(self):
            if hasattr(self, '_m_tx_offset'):
                return self._m_tx_offset if hasattr(self, '_m_tx_offset') else None

            self._m_tx_offset = (self.tx_offset_raw / 1000000.0)
            return self._m_tx_offset if hasattr(self, '_m_tx_offset') else None

        @property
        def rx_step(self):
            if hasattr(self, '_m_rx_step'):
                return self._m_rx_step if hasattr(self, '_m_rx_step') else None

            self._m_rx_step = self._root.tables.step_size[self.rx_step_raw]
            return self._m_rx_step if hasattr(self, '_m_rx_step') else None

        @property
        def ctcss_frequency(self):
            if hasattr(self, '_m_ctcss_frequency'):
                return self._m_ctcss_frequency if hasattr(self, '_m_ctcss_frequency') else None

            self._m_ctcss_frequency = self._root.tables.tone_frequency[self.ctcss_frequency_raw]
            return self._m_ctcss_frequency if hasattr(self, '_m_ctcss_frequency') else None

        @property
        def name(self):
            if hasattr(self, '_m_name'):
                return self._m_name if hasattr(self, '_m_name') else None

            self._m_name = self._parent.name
            return self._m_name if hasattr(self, '_m_name') else None

        @property
        def deleted(self):
            if hasattr(self, '_m_deleted'):
                return self._m_deleted if hasattr(self, '_m_deleted') else None

            self._m_deleted = False
            return self._m_deleted if hasattr(self, '_m_deleted') else None

        @property
        def tx_step(self):
            if hasattr(self, '_m_tx_step'):
                return self._m_tx_step if hasattr(self, '_m_tx_step') else None

            self._m_tx_step = (0 if self.tx_step_raw == 255 else self.tx_step_raw)
            return self._m_tx_step if hasattr(self, '_m_tx_step') else None


    class ChannelFlags(KaitaiStruct):
        """These flags are included in bit 6 of the channel entry.
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown = self._io.read_bits_int(1) != 0
            self.admit = self._root.Admit(self._io.read_bits_int(3))
            self.reverse = self._io.read_bits_int(1) != 0
            self.split = self._io.read_bits_int(1) != 0
            self.shift = self._root.ShiftDirection(self._io.read_bits_int(2))


    class Tables(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass

        @property
        def step_size(self):
            if hasattr(self, '_m_step_size'):
                return self._m_step_size if hasattr(self, '_m_step_size') else None

            self._m_step_size = [5, 6.25, 28.33, 10, 12.5, 15, 20, 25, 30, 50, 100]
            return self._m_step_size if hasattr(self, '_m_step_size') else None

        @property
        def tone_frequency(self):
            if hasattr(self, '_m_tone_frequency'):
                return self._m_tone_frequency if hasattr(self, '_m_tone_frequency') else None

            self._m_tone_frequency = [67, 69.3, 71.9, 74.4, 77, 79.7, 82.5, 85.4, 88.5, 91.5, 94.8, 97.4, 100, 103.5, 107.2, 110.9, 114.8, 118.8, 123, 127.3, 131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 162.2, 167.9, 173.8, 179.9, 186.2, 192.8, 203.5, 240.7, 210.7, 218.1, 225.7, 229.1, 233.6, 241.8, 250.3, 254.1]
            return self._m_tone_frequency if hasattr(self, '_m_tone_frequency') else None

        @property
        def dcs_code(self):
            if hasattr(self, '_m_dcs_code'):
                return self._m_dcs_code if hasattr(self, '_m_dcs_code') else None

            self._m_dcs_code = [23, 25, 26, 31, 32, 36, 43, 47, 51, 53, 54, 65, 71, 72, 73, 74, 114, 115, 116, 122, 125, 131, 132, 134, 143, 145, 152, 155, 156, 162, 165, 172, 174, 205, 212, 223, 225, 226, 243, 244, 245, 246, 251, 252, 255, 261, 263, 265, 266, 271, 274, 306, 311, 315, 325, 331, 332, 343, 346, 351, 356, 364, 365, 371, 411, 412, 413, 423, 431, 432, 445, 446, 452, 454, 455, 462, 464, 465, 466, 503, 506, 516, 523, 565, 532, 546, 565, 606, 612, 624, 627, 631, 632, 654, 662, 664, 703, 712, 723, 731, 732, 734, 743, 754]
            return self._m_dcs_code if hasattr(self, '_m_dcs_code') else None


    @property
    def tables(self):
        if hasattr(self, '_m_tables'):
            return self._m_tables if hasattr(self, '_m_tables') else None

        self._m_tables = self._root.Tables(self._io, self, self._root)
        return self._m_tables if hasattr(self, '_m_tables') else None

    @property
    def channels(self):
        if hasattr(self, '_m_channels'):
            return self._m_channels if hasattr(self, '_m_channels') else None

        _pos = self._io.pos()
        self._io.seek(5888)
        self._m_channels = [None] * (1000)
        for i in range(1000):
            self._m_channels[i] = self._root.Channel(i, self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_channels if hasattr(self, '_m_channels') else None

    @property
    def channel_names(self):
        if hasattr(self, '_m_channel_names'):
            return self._m_channel_names if hasattr(self, '_m_channel_names') else None

        _pos = self._io.pos()
        self._io.seek(22528)
        self._m_channel_names = [None] * (1000)
        for i in range(1000):
            self._m_channel_names[i] = (KaitaiStream.bytes_terminate(self._io.read_bytes(8), 255, False)).decode(u"ascii")

        self._io.seek(_pos)
        return self._m_channel_names if hasattr(self, '_m_channel_names') else None

    @property
    def channel_extended_flags(self):
        if hasattr(self, '_m_channel_extended_flags'):
            return self._m_channel_extended_flags if hasattr(self, '_m_channel_extended_flags') else None

        _pos = self._io.pos()
        self._io.seek(3584)
        self._m_channel_extended_flags = [None] * (1000)
        for i in range(1000):
            self._m_channel_extended_flags[i] = self._root.ChannelExtendedFlags(self._io, self, self._root)

        self._io.seek(_pos)
        return self._m_channel_extended_flags if hasattr(self, '_m_channel_extended_flags') else None


