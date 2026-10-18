#!/bin/bash
# usage: shot.sh url out.png WxH
google-chrome --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=$3 --virtual-time-budget=4000 --screenshot=$2 "$1" 2>/dev/null
