#!/usr/bin/python3

'''This is an example application that uses the kaitai struct definition
in tmv71_channels.ksy to extract a list of channels from a TM-V71 memory
dump.'''

import csv
import sys

import tmv71_channels

extract_fields = [
    ('name', '{}'),
    ('rx_freq', '{:06.3f}'),
    ('rx_step', '{:0.2f}'),
    ('flags.shift', '{.name}'),
    ('flags.split', '{}'),
    ('flags.admit', '{.name}'),
    ('mod', '{.name}'),
    ('tone_frequency', '{:0.2f}'),
    ('ctcss_frequency', '{:0.2f}'),
    ('dcs_code', '{:03d}'),
    ('tx_step', '{}'),
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
