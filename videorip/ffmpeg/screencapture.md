With frame num and type:
```
ffmpeg -analyzeduration 1024M -probesize 2048M -i demux/00001.track_4113.264 \
           -vf "drawtext=fontfile='/usr/share/fonts/urw-base35/NimbusSans-Regular.t1': \
text='frame %{frame_num} pic type %{pict_type}^Lsource': \
x=20:y=20: fontcolor=white: fontsize=30: box=1: boxcolor=black: boxborderw=5" -c:v libx264 -qp 0 srctemp.264
```

```
ffmpeg -analyzeduration 100M -probesize 100M -i Ermo.1994.DVDRip.x264.AC3-psklf.mkv -f image2 -vf "select='eq(n\,20000)+eq(n\,30000)+eq(n\,40000)'",showinfo -vsync 0 -frames:v 3 encodenew%3d.png

```

With image size control or correct DAR
```
ffmpeg -analyzeduration 100M -probesize 100M -i main.VOB  -f image2 -vf "select='eq(n\,20000)+eq(n\,40000)+eq(n\,13613)',scale=1024:576",showinfo -vsync 0 -frames:v 3 source%3d.png

ffmpeg -analyzeduration 100M -probesize 100M -i main.VOB  -f image2 -vf "select='eq(n\,20000)+eq(n\,40000)+eq(n\,13613)',scale=iw*sar:ih",showinfo -vsync 0 -frames:v 3 source%3d.png
```
Analyse video

```
ffprobe  main.VOB -select_streams v   -show_frames | grep -E 'pict_type|coded_picture_number|pkt_pts_time' > allframes.txt

```
Sometimes need offset frame num.





