
## 1 Demux

### 1.1 DVD

#### Merge VOB
```
cat VOB_02_*.VOB > out.VOB
```

process VOB first time

```
ffmpeg -analyzeduration 100M -probesize 100M -i VIDEO_TS/VTS_01_4.VOB  -codec:v copy -codec:a copy -codec:s copy -map 0:0 -map 0:1  -map 0:3 -map 0:4 -map 0:5 pre.VOB
```

split the output file

```
ffmpeg -analyzeduration 100M -probesize 100M -t 00:17:23 -i pre.VOB -codec:v copy -codec:a copy -codec:s copy -map 0 mainend.VOB
ffmpeg -ss 01:34:40 -analyzeduration 100M -probesize 100M -i src.VOB -codec:v copy -codec:a copy -codec:s copy  -map 0 crew.VOB
```
####  Subtitles of DVD

```
mencoder <VOBFILE> -nosound -ovc frameno -o /dev/null -vobsuboutindex 0 -sid 0 -vobsubout <SUBFILE>

-vobsubid

mencoder VIDEO_TS/VIDEO_TS.IFO -nosound -ovc copy -o /dev/null -vobsubout subtitles -vobsuboutindex 2 -sid 2
```

### 1.2 BluRay

#### Split and merge bluray

Get file infomation:

```
tsMuxeR ./PLAYLIST/00003.mpls
```

create tsdemuxer.meta
```
MUXOPT --demux
S_HDMV/PGS, ./PLAYLIST/00004.mpls, track=4608
S_HDMV/PGS, ./PLAYLIST/00004.mpls, lang=eng, track=4609
A_LPCM, ./PLAYLIST/00004.mpls, track=4352
V_MPEG4/ISO/AVC, ./PLAYLIST/00004.mpls, track=4113

A_DTS, "./BDMV/PLAYLIST/00001.mpls", track=4352, down-to-dts
A_AC3, "./BDMV/PLAYLIST/00001.mpls", track=4353, down-to-ac3
```

Run
```
tsMuxeR tsdemuxermain.meta demux
```

```
ffmpeg -analyzeduration 500M -probesize 4096M -i demux/00003.track_4113.264  -ss 00:05:00 -t 00:00:10 -c copy srcsample1.264
```

### Chapters

```
# demux chapters and subs
# if don't want subs add -S
mkvmerge -A -S -D ./PLAYLIST/00003.mpls -o chapters.mkv
# extract
mkvextract chapters "chapters.mkv" > chapters.xml
```

## 2 Encode video by ffmpeg/x264

### x264 Encode

x264 (w/ vspipe)

First, get lossless 264 video file

```
vspipe  -y clip.vpy - | x264 --demuxer y4m - --qp 0 -o samplesrc.264
```

Use Vapoursynth to filter and x264 to encode

Set correct crop size

```
# crop
video = core.std.Crop(video, left=0, right=0, top=0, bottom=0)
```

Final command:

```
vspipe --y4m encodetest.vpy - | x264 --demuxer y4m - \
--preset slow --tune film \
--me umh --subme 11 --direct auto psy_rd=1.15:0.0 --no-dct-decimate --no-fast-pskip --no-dct-decimate \
--bframes 7 --b-adapt 2 --deblock -3:-3 --ref 12 \
--crf 18 --aq-mode 2 --qcomp 0.8 --no-mbtree 1 \
--output sampledst.264
```

#### x264 Settings

##### Qcomp

Qcomp determines your encoding strategy. Given the fact that the default qcomp is 0.6, when I say “Qcomp = 0.8” I am telling my encoder this “Hey, just because a frame is P or B, doesn’t mean that they are to be given too much of a step-motherly treatment”. When I say “Qcomp = 0.4”, P-frames and B-frames deteriorate much more than the I-frame.

Thus - in our example, when Qcomp was 0, the P and B frames were very information-light.

Warning: If you turn mbtree on for encodes which use qcomps less than 0.7, you must be very very sure that the source isn’t grainy or complex or else you will end up destroying your encode. Turn it off with –no-mbtree; since mbtree is enabled by default.

##### ref
ref: The max –ref value can be calculated as follows:

For –level 4.1, according to the H.264 standard, the max DPB (Decoded Picture Buffer) size is 12,288 kilobytes. Since each frame is stored in YV12 format, or 1.5 bytes per pixel, a 1920x1088 frame is 1920 x 1088 x 1.5 = 3133440 bytes = 3060 kilobytes. 12,288 / 3060 kilobytes = 4.01568627, so you can use a maximum of 4 reference frames. Remember, round both dimensions up to a mod16 value when doing the math, even if you’re not encoding mod16!

For level 4.1 MaxDpbMbs is 32768

Macro Block size is 16x16 so 1920 / 16 = 120, 1080 / 16 = 68.
For example, for an HDTV picture that is 1,920 samples wide (PicWidthInMbs = 120) and 1,080 samples high (FrameHeightInMbs = 68), a Level 4 decoder has a maximum DPB storage capacity of floor(32768/(120x68)) = 4 frames (or 8 fields). Thus, the value 4 is shown in parentheses in the table above in the right column of the row for Level 4 with the frame size 1920×1080.

For level 5 MaxDpbMbs is 110400, same res--> 13.5

##### aq

aq-mode

Adaptive Quantization Mode

Default: 1

Without AQ, x264 tends to underallocate bits to lower details sections. AQ is used to better distribute the available bits between all macroblocks in the video. This setting changes what scope AQ re-arranges bits in:

    0: Do not use AQ at all.
    1: Allow AQ to redistribute bits within each frame.
    2: Allow AQ to redistribute bits across the whole video.
    3: Auto-variance AQ with bias to dark scenes.

Recommendation: Default

aq-strength

Adaptive Quantization Strength

Default: 1.0

Sets the strength of AQ bias towards low detail ('flat') macroblocks. Negative values are not allowed. Values more than a couple of hundred percent off from 1.0 are probably a bad idea.

Recommendation: Default

##### psy rd

2 / 3 choose

#### compare screenshot

use [`ffinfo_screen.py`](ffinfo_screen.py) to generate screenshots.

#### backup stuff
My samples

**Rip an old Chinese film**

noisy DVD:
- Crop didn't change sar so use same sar as origin
- For this grain film using qcomp 1.3

```
vspipe --y4m encodetest.vpy - | x264 --demuxer y4m - \
         --preset veryslow --tune grain --sar 8:9 --me umh --subme 11 \
         --direct auto psy_rd=0.9:0.0 --no-dct-decimate --no-fast-pskip --no-dct-decimate \
         --bframes 7 --b-adapt 2 --deblock -3:-3 --ref 4 --crf 18 \
         --aq-mode 2 --qcomp 1.3 --no-mbtree 1 --aq-strength 0.7 \
         -o dst.264 > log.txt 2>&1 &
```

**Rip a new film**

```
ffmpeg -analyzeduration 100M -probesize 100M -i VIDEO_TS/VTS01.VOB -ss 00:13:00 -t 00:02:00 -codec:v libx264 -preset slow  -x264-params "crf=18:me=umh:bframes=5:deblock=-4:subme=11:no-fast-pskip=1:no-dct-decimate=1" sample.264

ffmpeg -analyzeduration 100M -probesize 100M -i main.VOB  -codec:v libx264 -preset veryslow  -x264-params "me=umh:deblock=-3:subme=11:no-fast-pskip=1:no-dct-decimate=1:qcomp=0.65:bframes=5:crf=18" main.264
```

## 3 Enocde Audio

```
ffmpeg -i out.VOB -map 0:2 -codec:a ac3 output.ac3

ffmpeg -analyzeduration 100M -probesize 100M -i main.VOB -map 0:2 -codec:a ac3 main5.1-side.ac3 -map 0:3 -codec:a ac3 mainstereo.ac3

# bd audio: 2-channels use flac
ffmpeg -i demux/00003.track_4352.wav -codec:a flac demux/00003.track_4352.flac

# get DTS core from DTS-MA dca_core bitstream filter:
ffmpeg -i DTS-HD_MA.dts -bsf:a dca_core -c:a copy TS-Core.dts
```

## 4 REMUX by mkvmerge

```
mkvmerge -o "Black.Snow.1990.PAL.DVDRip.x264.AC3-psklf.mkv" --title "Black.Snow.1990.PAL.DVDRip.x264.AC3-psklf" --chapters chapters.txt --default-duration 0:25fps --track-name 0:"H.264 Video  yuv420p 720x576 2685.6kbps" output.264 --language 0:chi --track-name 0:"AC3 Audio" output.ac3 --language 0:eng eng.idx

mkvmerge -o Time.To.Die.2007.DVDRip.x264.AC3-psklf.mkv --title "Time.To.Die.2007.DVDRip.x264.AC3-psklf" --default-duration 0:25fps --track-name 0:"H.264 Video" main.264 --language 0:pol --track-name 0:"AC-3 5.1 Audio" main51.ac3 --language 0:pol --track-name 0:"AC-3 stereo Audio" mainstereo.ac3 --chapters chapters.txt --language 0:chi Time.To.Die.2007.DVDRip.XviD-RESERVED.chs.srt --language 0:eng Time.To.Die.2007.DVDRip.XviD-RESERVED.english.srt

mkvmerge -o Rebels.of.the.Neon.God.1080p.BluRay.FLAC.x264-psklf.mkv --title "Rebels.of.the.Neon.God.1080p.BluRay.FLAC.x264-psklf" --compression 0:none --track-name 0:"H.264 / 1080p / 24fps / Advanced Profile 5" 00003rip.track_4113.264 --compression 0:none --language 0:chi --track-name 0:"Chinese / FLAC / 2.0 / 16 bits" demux/00003.track_4352.flac --chapters demux/00003chapters.xml --language 0:chi demux/00003.track_4608.sup --language 0:eng demux/00003.track_4609.sup

```
## Tips

```
mkvmerge -o temp.mkv --subtitle-tracks 2 ChungKing.Express.1994.1080p.BluRay.DTS.x264-psklf.mkv # select track 2
mkvmerge -o output.mkv -s '!3' input.mkv # remove  subtitle track  3

# slice s sample
ffmpeg -analyzeduration 100M -probesize 100M -i My.Life.as.McDull.2001.1080p.BluRay.DTS5.1.x264-psklf.mkv -ss 00:10:00 -t 00:03:00 -c copy -map 0 sample.mkv
```


