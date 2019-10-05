# Parsing the memory of a TM-V71A radio using Kaitai Struct

This is a simple example of how to use [Kaitai Struct][] to parse a memory dump from a [Kenwood TM-V71A][] radio.

[kaitai struct]: http://kaitai.io
[kennwood tm-v71a]: https://www.kenwood.com/usa/com/amateur/tm-v71a/

## Running the example

This assumes that you have a TM-V71 memory dump in a file named
`memdump.bin`.

Set up a Python virtual environment:

   virtualenv --python python3 .venv

Activate the virtual environment:

    . .venv/bin/activate

Install prerequisites:

    pip install -r requirements.txt

Run the example:

    python extract_channels.py memdump.bin

## Modifying the struct defnition

If you want to make changes to the struct definition in `tmv71_channels.ksy`, you'll need to [install the kaitai struct compiler][install], and use that to re-generate the Python module after you make changes:

    ksc -t python tmv71_channels.ksy

[install]: http://kaitai.io/#download
