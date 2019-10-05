# Parsing the memory of a TM-V71A radio using Kaitai Struct

This is a simple example of how to use [Kaitai Struct][] to parse a memory dump
from a [Kenwood TM-V71A][] radio. It will read the list of channels from the
memory dump and emit the list as a CSV file.

[kaitai struct]: http://kaitai.io
[kennwood tm-v71a]: https://www.kenwood.com/usa/com/amateur/tm-v71a/

## Running the example

This assumes that you have a TM-V71 memory dump in a file named `memdump.bin`.
There is an example `memdump.bin` included in this repository that is not a
complete memory dump, but it does have data at the locations expected by this
code.

Set up a Python virtual environment:

    virtualenv --python python3 .venv

Activate the virtual environment:

    . .venv/bin/activate

Install prerequisites:

    pip install -r requirements.txt

Run the example:

    python extract_channels.py memdump.bin

## Modifying the struct defnition

If you want to make changes to the struct definition in `tmv71_channels.ksy`,
you'll need to [install the kaitai struct compiler][install], and use that to
re-generate the Python module after you make changes:

    ksc -t python tmv71_channels.ksy

[install]: http://kaitai.io/#download

## Example output

```
$ python extract_channels.py memdump.bin
name,rx_freq,rx_step,flags.shift,flags.split,flags.admit,mod,tone_frequency,ctcss_frequency,dcs_frequency,tx_step,extended_flags.flags.lockout
MRABEL,145.430,5,down,False,ctcss,fm,146.20,146.20,023,0,False
MRABBY,146.820,5,down,False,tone,fm,146.20,88.50,023,0,False
MRAQCY,146.670,5,down,False,ctcss,fm,146.20,146.20,023,0,False
MRALWL,442.250,25,up,False,tone,fm,88.50,88.50,023,0,False
MRAMRW,449.925,5,down,False,ctcss,fm,88.50,88.50,023,0,False
MRAWES,442.700,5,up,False,ctcss,fm,88.50,88.50,023,0,False
WRA2M,146.640,5,down,False,ctcss,fm,136.50,136.50,023,0,False
WRA70C,449.075,5,down,False,tone,fm,88.50,88.50,023,0,False
CWA 2M,145.110,5,down,False,tone,fm,110.90,88.50,023,0,False
CWA70C,447.575,5,down,False,tone,fm,110.90,88.50,023,0,False
```
