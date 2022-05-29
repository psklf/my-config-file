from vapoursynth import core

core.std.LoadPlugin(path="/usr/local/lib/libffms2.so")

# video = core.ffms2.Source(source='demux/00000.track_4113.264')
video = core.ffms2.Source(source='dst.264')
clip = core.std.SelectEvery(clip = video, cycle = 30000, offsets = range(20000, 20120))
clip = core.std.AssumeFPS(clip, fpsnum=video.fps.numerator, fpsden=video.fps.denominator)

# crop
clip = core.std.Crop(clip, left=0, right=0, top=0, bottom=0)

clip.set_output()
# video = core.ffms2.Source(source='samplesrc.264')
# video.set_output()
