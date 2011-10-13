#!/bin/bash

killall fbsetbg >/dev/null 2>&1
DISPLAY=:0.0 fbsetbg $1 &
