#!/usr/bin/sh
ffmpeg -analyzeduration 100M -probesize 100M -i main.VOB -codec:v libx264 -b_strategy 2 -crf 18 -me_method umh  -x264opts deblock=-4:subme=11:no-fast-pskip=1:no-dct-decimate=1 -tune grain main.264
