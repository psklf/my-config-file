## merge VOB
```
cat VOB_02_*.VOB > out.VOB
```

### split VOB file

process VOB first time

```
ffmpeg -analyzeduration 100M -probesize 100M -i VIDEO_TS/VTS_01_4.VOB  -codec:v copy -codec:a copy -codec:s copy -map 0:0 -map 0:1  -map 0:3 -map 0:4 -map 0:5 pre.VOB
```

split the output file

```
ffmpeg -analyzeduration 100M -probesize 100M -t 00:17:23 -i pre.VOB -codec:v copy -codec:a copy -codec:s copy -map 0 mainend.VOB
ffmpeg -ss 01:34:40 -analyzeduration 100M -probesize 100M -i src.VOB -codec:v copy -codec:a copy -codec:s copy  -map 0 crew.VOB
```

## subtitles:

```
mencoder <VOBFILE> -nosound -ovc frameno -o /dev/null -vobsuboutindex 0 -sid 0 -vobsubout <SUBFILE>

-vobsubid

mencoder VIDEO_TS/VIDEO_TS.IFO -nosound -ovc copy -o /dev/null -vobsubout subtitles -vobsuboutindex 2 -sid 2
```

## ffmpeg 264

grain: for old film

```
ffmpeg \
  -analyzeduration 100M -probesize 100M \
  -i output \
  -codec:v libx264 -b_strategy 2 -crf 18 -subq 11 -tune grain  \
  output.264
```

```
ffmpeg -analyzeduration 100M -probesize 100M -i main.VOB -ss 00:10:00 -t 00:02:00 -codec:v libx264 -b_strategy 2 -crf 18 -me_method umh  -x264opts deblock=-4:subme=11:no-fast-pskip=1:no-dct-decimate=1 -tune grain sample.264
```

x264:
```
 --b-adapt 2 --subme 11 --direct auto 

Keep stream 0:1 0:3 0:4 0:5 0:6
  -map 0:1 -map 0:3 -map 0:4 -map 0:5 -map 0:6 \
```

## Audio
```
ffmpeg -i out.VOB -map 0:2 -codec:a ac3 output.ac3
```

## mkvmerge

```
mkvmerge -o "Black.Snow.1990.PAL.DVDRip.x264.AC3-psklf.mkv" --title "Black.Snow.1990.PAL.DVDRip.x264.AC3-psklf" --chapters chapters.txt --default-duration 0:25fps --track-name 0:"H.264 Video  yuv420p 720x576 2685.6kbps" output.264 --language 0:chi --track-name 0:"AC3 Audio" output.ac3 --language 0:eng eng.idx
```
