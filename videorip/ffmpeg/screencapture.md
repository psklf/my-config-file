Analyse video

```
ffprobe  main.VOB -select_streams v   -show_frames | grep -E 'pict_type|coded_picture_number|pkt_pts_time' > allframes.txt

```
Sometimes need offset frame num.



```
ffmpeg -analyzeduration 100M -probesize 100M -i Ermo.1994.DVDRip.x264.AC3-psklf.mkv -f image2 -vf "select='eq(n\,20000)+eq(n\,30000)+eq(n\,40000)'",showinfo -vsync 0 -frames:v 3 encodenew%3d.png

```

With image size control
```
ffmpeg -analyzeduration 100M -probesize 100M -i main.VOB  -f image2 -vf "select='eq(n\,20000)+eq(n\,40000)+eq(n\,13613)',scale=1024:576",showinfo -vsync 0 -frames:v 3 source%3d.png

```


