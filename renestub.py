# usage: renestub.py <stub> <ne-exe>

from __future__ import print_function, division

import struct

import os
import os.path
import sys

def main():
    _NEWSTUBFILE = sys.argv[1]
    orig = sys.argv[2]
    _B = "<B"
    _W = "<H"
    _DW = "<I"
    gw = lambda offset: struct.unpack(_W, entire[offset:offset+2])[0]
    gew = lambda offset: gw(oldstubsize + offset)
    with open(orig, "rb") as f:
        entire = f.read()

    assert gw(0x18) >= 0x40, "no NE file"
    oldstubsize = gw(0x3c)
    print("oldstubsize", oldstubsize)
    assert gw(oldstubsize) == 0x454e, "no NE file"
    shift = gew(0x32)
    print("shift", shift)

    with open(_NEWSTUBFILE, "rb") as f:
        stub = bytearray(f.read())

    newstubsize = len(stub)
    divisor = 1 << shift
    print("divisor", divisor)
    oldsects = oldstubsize // divisor
    print("old sects", oldsects)
    newsects = newstubsize // divisor
    if newstubsize > oldstubsize and oldsects == newsects:
        # make room for slightly larger stub
        newsects += 1
    print("distance", newsects - oldsects)

    def putw(offset, val):
        stub[offset:offset+2] = struct.pack(_W, val)

    newsize = len(entire) + ((newsects - oldsects) << shift)
    print("newsize", newsize)

    putw(2, newsize % 512)
    putw(4, (newsize + 511) >> 9)
    putw(0x3c, (newsects << shift) + (oldstubsize % divisor))

    bent = bytearray(entire[oldstubsize:])

    getew = lambda offset: struct.unpack(_W, bent[offset:offset+2])[0]
    def putew(offset, val):
        bent[offset:offset+2] = struct.pack(_W, val)

    geted = lambda offset: struct.unpack(_DW, bent[offset:offset+4])[0]
    def puted(offset, val):
        bent[offset:offset+4] = struct.pack(_DW, val)

    def puteb(offset, val):
        bent[offset:offset+1] = struct.pack(_B, val)

    # nonresident name offset
    puted(0x2c, geted(0x2c) + ((newsects - oldsects) << shift))
    # os type os/2
    puteb(0x36, 1)

    numsegs = getew(0x1c)
    print("numsegs", numsegs)

    segtable = getew(0x22)

    # segment offsets in file
    for seg in range(numsegs):
        print("seg start", seg, hex(getew(segtable + 8*seg) << shift))

        start = getew(segtable + 8*seg)
        if start:
            putew(segtable + 8*seg, start + newsects - oldsects)

    tmp = orig + ".tmp"
    with open(tmp, "wb") as tmpf:
        tmpf.write(stub)
        tmpf.write("\0" * (((newsects << shift) + (oldstubsize % divisor)) - len(stub)))
        tmpf.write(str(bent))
    os.rename(tmp, orig)

if __name__ == "__main__":
    main()
