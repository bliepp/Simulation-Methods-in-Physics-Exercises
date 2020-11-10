#!/usr/bin/env python3
#
#
#

def data2file(outfile, time, x, v):
    out = "\t".join(["{:.2f}"]*5).format(
            time, x[0], x[1], v[0], v[1])
    outfile.write(out + "\n")
