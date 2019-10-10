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
  tables:
    type: tables
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
  tables:
    doc: |
      This is a value-only collection of tables used to map
      numeric constants in the channel data into actual values.
    instances:
      step_size:
        value: >-
          [5, 6.25, 28.33, 10, 12.5, 15, 20, 25, 30, 50, 100]
      tone_frequency:
        value: >-
          [67, 69.3, 71.9, 74.4, 77, 79.7, 82.5, 85.4, 88.5, 91.5,
          94.8, 97.4, 100, 103.5, 107.2, 110.9, 114.8, 118.8, 123,
          127.3, 131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 162.2,
          167.9, 173.8, 179.9, 186.2, 192.8, 203.5, 240.7, 210.7,
          218.1, 225.7, 229.1, 233.6, 241.8, 250.3, 254.1]
      dcs_code:
        value: >-
          [23, 25, 26, 31, 32, 36, 43, 47, 51, 53, 54, 65, 71, 72, 73,
           74, 114, 115, 116, 122, 125, 131, 132, 134, 143, 145, 152,
           155, 156, 162, 165, 172, 174, 205, 212, 223, 225, 226, 243,
           244, 245, 246, 251, 252, 255, 261, 263, 265, 266, 271, 274,
           306, 311, 315, 325, 331, 332, 343, 346, 351, 356, 364, 365,
           371, 411, 412, 413, 423, 431, 432, 445, 446, 452, 454, 455,
           462, 464, 465, 466, 503, 506, 516, 523, 565, 532, 546, 565,
           606, 612, 624, 627, 631, 632, 654, 662, 664, 703, 712, 723,
           731, 732, 734, 743, 754]
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
      These flags are included in byte 6 of the channel entry.
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
      - id: rx_step_raw
        type: u1
      - id: mod
        type: u1
        enum: modulation
      - id: flags
        type: channel_flags
      - id: tone_frequency_raw
        type: u1
      - id: ctcss_frequency_raw
        type: u1
      - id: dcs_code_raw
        type: u1
      - id: tx_offset_raw
        type: u4
      - id: tx_step_raw
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
      rx_step:
        value: _root.tables.step_size[rx_step_raw]
      tone_frequency:
        value: _root.tables.tone_frequency[tone_frequency_raw]
      ctcss_frequency:
        value: _root.tables.tone_frequency[ctcss_frequency_raw]
      dcs_code:
        value: _root.tables.dcs_code[dcs_code_raw]
      tx_offset:
        value: tx_offset_raw / 1000000.0
      tx_step:
        value: "tx_step_raw == 0xff ? 0 : tx_step_raw"
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
