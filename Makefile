%.py: %.ksy
	ksc -t python $<

all: tmv71_channels.py
