from vapoursynth import core

core.std.LoadPlugin(path="/usr/local/lib/libffms2.so")


# clip source video
video = core.ffms2.Source(source='demux/00001.track_4113.264')
# clip = core.std.SelectEvery(clip = video, cycle = 25000, offsets = range(20000, 20120))
# clip = core.std.AssumeFPS(clip, fpsnum=video.fps.numerator, fpsden=video.fps.denominator)

# crop
video = core.std.Crop(video, left=0, right=0, top=0, bottom=0)

# clip.set_output()
video.set_output()

# encode param test
# video = core.ffms2.Source(source='samplesrc.264')
# video.set_output()
