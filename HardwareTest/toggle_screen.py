#!/usr/bin/python3

from subprocess import call 
import time

# Spegniamo il monitor
non_so = call(["xset","dpms","force","off"]);
print("Monitor off: %s" % time.ctime())
time.sleep(  1)
print("Monitor on : %s" % time.ctime())
non_so = call(["xset","dpms","force","on"]);




print(non_so)
