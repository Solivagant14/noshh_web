import os
import shutil
import subprocess
from app.progress import progress
from moviepy.editor import VideoFileClip, concatenate_videoclips
from proglog import ProgressBarLogger

#logger class which gives access to read the terminal output of moviepy
class MyBarLogger(ProgressBarLogger):
    def callback(self, **changes):
        # Every time the logger is updated, this function is called
        if len(self.bars):
            title = next(reversed(self.bars.items()))[1]['title']
            percentage = int(next(reversed(self.bars.items()))[1]['index'] / next(reversed(self.bars.items()))[1]['total']*100)
            if(title == 'chunk'):
                progress(percentage, process="audio")
            if(title == 't'):
                progress(percentage, process="video")

logger = MyBarLogger()

#removes the silence and stores the edited video in a folder and deletes the in file
def remove_silence(in_file,out_file):
    in_file = in_file
    out_file = out_file

    def generate_timestamps():
        command = "sh script/detect_silence.sh {}".format(in_file)
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        return output.stdout.split('\n')[:-1]

    timestamps=generate_timestamps()
    silence_start=[]
    silence_duration=[]

    while len(timestamps)>0:
        silence_start.append(float(timestamps.pop(0)))
        silence_duration.append(float(timestamps.pop(0)))

    video = VideoFileClip(in_file)
    full_duration = video.duration
    clips = []
    length = len(silence_start)

    start = 0
    end = 0

    # print("Getting Clips Ready")
    for i in range(length):
        end = silence_start[i]
        clip = video.subclip(start, end)
        clips.append(clip)
        start = end+silence_duration[i]

    if full_duration>start:
        clip = video.subclip(start, full_duration)

    try:
        processed_video = concatenate_videoclips(clips)
    except ValueError:
        shutil.move(in_file,out_file)
        return

    processed_video.write_videofile(
        out_file,
        bitrate="50000k",
        logger=logger,
        temp_audiofile=".temp/audio_temp.ogg"
        )

    video.close()
    os.remove(in_file)