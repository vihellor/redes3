#!/usr/bin/env python

import rrdtool
ret = rrdtool.create("netP.rrd",
                     "--start",'N',
                     "--step",'300',
                     "DS:inoctets:COUNTER:600:U:U",
                     "DS:outoctets:COUNTER:600:U:U",
                     "RRA:AVERAGE:0.5:1:2016",
                     "RRA:HWPREDICT:1440:0.1:0.0035:288",
                     "RRA:SEASONAL:1d:0.1:2",
                     "RRA:DEVSEASONAL:1d:0.1:2",
                     "RRA:DEVPREDICT:5d:5",
                     "RRA:FAILURES:1d:7:9:5")

if ret:
    print rrdtool.error()

