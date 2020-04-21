```
ffmpeg -analyzeduration 100M -probesize 100M -i Ermo.1994.DVDRip.x264.AC3-psklf.mkv -f image2 -vf "select='eq(n\,20000)+eq(n\,30000)+eq(n\,40000)'",showinfo -vsync 0 -frames:v 3 encodenew%3d.png

```
