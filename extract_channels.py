#!/usr/bin/python3

'''This is an example application that uses the kaitai struct definition 
in tmv71_channels.ksy to extract a list of channels from a TM-V71 memory
dump.'''

import csv
import sys

import tmv71_channels

STEP_SIZE = [5, 6.25, 28.33, 10, 12.5, 15, 20, 25, 30, 50, 100]

TONE_FREQUENCY = [67, 69.3, 71.9, 74.4, 77, 79.7, 82.5, 85.4, 88.5, 91.5,
                  94.8, 97.4, 100, 103.5, 107.2, 110.9, 114.8, 118.8, 123,
                  127.3, 131.8, 136.5, 141.3, 146.2, 151.4, 156.7, 162.2,
                  167.9, 173.8, 179.9, 186.2, 192.8, 203.5, 240.7, 210.7,
                  218.1, 225.7, 229.1, 233.6, 241.8, 250.3, 254.1]

DCS_CODE = [23, 25, 26, 31, 32, 36, 43, 47, 51, 53, 54, 65, 71, 72, 73,
            74, 114, 115, 116, 122, 125, 131, 132, 134, 143, 145, 152,
            155, 156, 162, 165, 172, 174, 205, 212, 223, 225, 226, 243,
            244, 245, 246, 251, 252, 255, 261, 263, 265, 266, 271, 274,
            306, 311, 315, 325, 331, 332, 343, 346, 351, 356, 364, 365,
            371, 411, 412, 413, 423, 431, 432, 445, 446, 452, 454, 455,
            462, 464, 465, 466, 503, 506, 516, 523, 565, 532, 546, 565,
            606, 612, 624, 627, 631, 632, 654, 662, 664, 703, 712, 723,
            731, 732, 734, 743, 754]

extract_fields = [
    ('name', '{}'),
    ('rx_freq', '{:06.3f}'),
    ('rx_step', lambda val: STEP_SIZE[val]),
    ('flags.shift', '{.name}'),
    ('flags.split', '{}'),
    ('flags.admit', '{.name}'),
    ('mod', '{.name}'),
    ('tone_frequency', lambda val: '{:0.2f}'.format(TONE_FREQUENCY[val])),
    ('ctcss_frequency', lambda val: '{:0.2f}'.format(TONE_FREQUENCY[val])),
    ('dcs_frequency', lambda val: '{:03d}'.format(DCS_CODE[val])),
    ('tx_step', lambda val: STEP_SIZE[val] if val != 0xff else 0),
    ('extended_flags.flags.lockout', '{}'),
]


def resolve(obj, path):
    for p in path.split('.'):
        obj = getattr(obj, p)

    return obj


with open(sys.argv[1], 'rb') as image:
    mem = tmv71_channels.Tmv71Channels.from_io(image)

    writer = csv.writer(sys.stdout)
    writer.writerow(x[0] for x in extract_fields)
    for i, channel in enumerate(mem.channels):
        if channel.data.deleted:
            continue
        writer.writerow([
            x[1](resolve(channel.data, x[0])) if callable(x[1]) else
            x[1].format(resolve(channel.data, x[0])) for x in extract_fields
        ])
