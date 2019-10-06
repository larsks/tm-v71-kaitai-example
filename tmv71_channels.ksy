---
doc: |
  This Kaitai Struct will parse a list of channels from a memory dump from
  a TM-V71A radio.  You can produce such a dump using tm-v71-tools
  (https://github.com/larsks/tm-v71-tools):

      tmv71 memory read -o memdump.bin

meta:
  id: tmv71_channels
  title: "TMV71 Channels"
  license: GPL-3.0-or-later
  ks-version: 0.8
  endian: le

seq:
  - id: magic
    contents: [0x00, 0x4b]

instances:
  channels:
    pos: 0x1700
    type: channel(_index)
    repeat: expr
    repeat-expr: 1000

  # Names in the tm-v71a are padded with `0xff` bytes up to their
  # maxium length. By specifying both `size` and `terminator` we
  # consume the correct number of bytes and return a string that
  # does not contain the padding bytes.
  channel_names:
    pos: 0x5800
    type: str
    encoding: ascii
    terminator: 0xff
    size: 8
    repeat: expr
    repeat-expr: 1000

  channel_extended_flags:
    pos: 0xe00
    type: channel_extended_flags
    repeat: expr
    repeat-expr: 1000

types:
  channel:
    doc: |
      A channel encoded in the radio memory.

      Use the `data.deleted` member to check for deleted channels. A deleted
      channel is empty: it will not have any of the expected fields.
    params:
      - id: number
        type: u2
    seq:
      - id: rx_freq_raw
        type: u4
      - id: data
        type:
          switch-on: rx_freq_raw
          cases:
            0xffffffff: empty_channel
            _: channel_fields
    instances:
      # The `name` attribute maps to the appropriate index in the
      # top-level `channel_names` array.
      name:
        value: _root.channel_names[number]
      # The `extended_flags` attribute maps to the appropriate index
      # in the top-level `channel_extended_flags` array.
      extended_flags:
        value: _root.channel_extended_flags[number]
  channel_flags:
    doc: |
      These flags are included in bit 6 of the channel entry.
    seq:
      - id: unknown
        type: b1
      - id: admit
        type: b3
        enum: admit
      - id: reverse
        type: b1
      - id: split
        type: b1
      - id: shift
        type: b2
        enum: shift_direction
  empty_channel:
    doc: |
      Represents an empty/deleted channel.
    seq:
      - id: padding
        size: 12
    instances:
      deleted:
        value: true
  channel_fields:
    doc: |
      These are the actual channel entry attributes.

      We also bring in the channel name from the top-level
      `channel_names` array, and some extended flags from the
      `channel_extended_flags` array.
    seq:
      - id: rx_step
        type: u1
      - id: mod
        type: u1
        enum: modulation
      - id: flags
        type: channel_flags
      - id: tone_frequency
        type: u1
      - id: ctcss_frequency
        type: u1
      - id: dcs_frequency
        type: u1
      - id: tx_offset_raw
        type: u4
      - id: tx_step
        type: u1
      - id: padding
        type: u1
    instances:
      name:
        value: _parent.name
      extended_flags:
        value: _parent.extended_flags
      rx_freq:
        value: _parent.rx_freq_raw / 1000000.0
      tx_offset:
        value: tx_offset_raw / 1000000.0
      deleted:
        value: false
  extended_flag_bits:
    seq:
      - id: unknown
        type: b7
      - id: lockout
        type: b1
  channel_extended_flags:
    seq:
      - id: band
        type: u1
      - id: flags
        type: extended_flag_bits
enums:
  channel_band:
    5: vhf
    8: uhf
  shift_direction:
    0: simplex
    1: up
    2: down
  modulation:
    0: fm
    1: am
    2: nfm
  admit:
    0: none
    4: tone
    2: ctcss
    1: dcs
