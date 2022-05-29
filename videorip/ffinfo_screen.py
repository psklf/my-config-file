import sys
import os
import random
import functools
import vapoursynth as vs
from random import choice

core = vs.get_core()
core.std.LoadPlugin(path="/usr/local/lib/libffms2.so")

# 生成帧信息，并打入标签
def FrameInfo(clip, title,
              style="sans-serif,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,0,7,10,10,10,1"):
    import functools
    def FrameProps(n, clip):
        clip = core.sub.Subtitle(clip, "Frame " + str(n) + " of " + str(
            clip.num_frames) + "\nPicture type: " + clip.get_frame(n).props._PictType.decode(), style=style)
        return clip

    clip = core.std.FrameEval(clip, functools.partial(FrameProps, clip=clip))
    clip = core.sub.Subtitle(clip, ['\n \n \n' + title], style=style)
    return clip

def open_clip(clip) -> vs.VideoNode:
    return clip.resize.Spline36(format=vs.RGB24, matrix_in_s='709' if clip.height > 576 else '470bg',
                                transfer_in_s='709' if clip.height > 576 else '470bg',
                                primaries_in_s='709' if clip.height > 576 else '470bg',
                                prefer_props=True)

def resize_dar(clip, width, height):
    return core.resize.Spline36(clip, width, height)

video = core.ffms2.Source(source='samplesrc.264')
# video = core.ffms2.Source(source='demux/00000.track_4113.264')
# video = core.lsmas.LWLibavSource(source='samplesrc.264')
video = FrameInfo(video,"source")

# clip = core.std.SelectEvery(clip = video[8000:-8000], cycle = 10000, offsets = 80)
# clip = core.std.AssumeFPS(clip, fpsnum=video.fps.numerator, fpsden=video.fps.denominator)
# clip = FrameInfo(clip,"source")

# encode = core.ffms2.Source(source='sampledst.264')
# encode = core.ffms2.Source(source='sampledst.264')
encode = core.lsmas.LWLibavSource(source='sampledst.264')
encode = FrameInfo(encode,"encode")

# enc_clip = core.std.SelectEvery(clip = encode[8000:-8000], cycle = 10000, offsets = 80)
# enc_clip = core.std.AssumeFPS(enc_clip, fpsnum=encode.fps.numerator, fpsden=encode.fps.denominator)
# enc_clip = FrameInfo(enc_clip,"encode")

out = core.std.Interleave([video, encode]) # 交叉帧
# out = core.std.Interleave([video, enc_clip]) # 交叉帧
out = open_clip(out)

# resize if needed
# out = resize_dar(out, 626, 348)


save_path = "./screenshots"
if not os.path.exists(save_path):
    os.mkdir(save_path)

imwri = core.imwri
out = imwri.Write(out, 'PNG', os.path.join(save_path, '%d.png'))

print("src num frames ", video.num_frames)
length = video.num_frames
num = 5
frames = []
for _ in range(num):
    frames.append(random.choice(range(video.num_frames // 10, video.num_frames // 10 * 9)))

frames = set([x // 100 for x in frames])
while len(frames) < num:
    frames.add(choice(range(length // 10, length // 10 * 9)) // 100)

frames = [x * 100 for x in frames]

for frame in frames:
    print("Write to {:s} {:d}".format(save_path, frame * 2) )
    out.get_frame(frame * 2)
    out.get_frame(frame * 2 + 1)

