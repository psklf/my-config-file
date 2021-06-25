import sys
import os
import functools
import vapoursynth as vs

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


video = core.ffms2.Source(source='samplesrc.264')
# video = core.std.AssumeFPS(video, fpsnum=video.fps.numerator, fpsden=video.fps.denominator)
video = FrameInfo(video,"src")

encode = core.ffms2.Source(source='sampledst.264')
encode = FrameInfo(encode,"encode")

out = core.std.Interleave([video,encode]) # 交叉帧
out = open_clip(out)

save_path = "./screenshots"
if not os.path.exists(save_path):
    os.mkdir(save_path)

imwri = core.imwri
out = imwri.Write(out, 'PNG', os.path.join(save_path, '%d.png'))
for frame in [700, 1000, 1500, 2000, 2500]:
    print("Write to {:s} {:d}".format(save_path, frame) )
    out.get_frame(frame)
    out.get_frame(frame+1)

