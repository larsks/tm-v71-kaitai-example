# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Tmv71Channels(KaitaiStruct):

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
            self.rx_step = self._io.read_u1()
            self.mod = self._root.Modulation(self._io.read_u1())
            self.flags = self._root.ChannelFlags(self._io, self, self._root)
            self.tone_frequency = self._io.read_u1()
            self.ctcss_frequency = self._io.read_u1()
            self.dcs_frequency = self._io.read_u1()
            self.tx_offset_raw = self._io.read_u4le()
            self.tx_step = self._io.read_u1()
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
        def tx_offset(self):
            if hasattr(self, '_m_tx_offset'):
                return self._m_tx_offset if hasattr(self, '_m_tx_offset') else None

            self._m_tx_offset = (self.tx_offset_raw / 1000000.0)
            return self._m_tx_offset if hasattr(self, '_m_tx_offset') else None

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


