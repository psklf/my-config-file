# Screenshot by ffmpeg

With image size control or correct DAR. Try to resize width and keep origin height
```
# set frame number
ffmpeg -analyzeduration 100M -probesize 100M -i main.VOB  -f image2 -vf "select='eq(n\,20000)+eq(n\,40000)+eq(n\,13613)',scale=iw*sar:ih",showinfo -vsync 0 -frames:v 3 source%3d.png

# set even resolution and faster seek
ffmpeg -analyzeduration 600M -probesize 600M -ss 00:10:00 -i in.mkv -f image2 -vf "scale='trunc(ih*dar/2)*2:trunc(ih/2)*2',setsar=1/1",showinfo -vsync 0 -frames:v 1 shot001.png

    # Make pixels square by combining scale and setsar:
    scale='trunc(ih*dar):ih',setsar=1/1

    # Make pixels square by combining scale and setsar, making sure the resulting resolution is even (required by some codecs):
    scale='trunc(ih*dar/2)*2:trunc(ih/2)*2',setsar=1/1
```

Analyse video

```
ffprobe  main.VOB -select_streams v   -show_frames | grep -E 'pict_type|coded_picture_number|pkt_pts_time' > allframes.txt

```
Sometimes need offset frame num.

With frame num and type:
```
ffmpeg -analyzeduration 1024M -probesize 2048M -i demux/00001.track_4113.264 \
           -vf "drawtext=fontfile='/usr/share/fonts/urw-base35/NimbusSans-Regular.t1': \
text='frame %{frame_num} pic type %{pict_type}^Lsource': \
x=20:y=20: fontcolor=white: fontsize=30: box=1: boxcolor=black: boxborderw=5" -c:v libx264 -qp 0 srctemp.264
```

