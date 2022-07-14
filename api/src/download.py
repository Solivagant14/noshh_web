import yt_dlp
from .progress import progress
import functools

#A hook which reads the progress value
def my_hook(d,json_file):
    if d['status'] == 'downloading':
        percentage = int(float(d['_percent_str'].strip()[:-1]))
        progress(percentage, process="download",json_file=json_file)

#logger class which gives access to read the terminal output of yt_dlp
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

#function to download a url and store at a path
def download(url,output,jsonfile):
    ydl_opts = {
    'outtmpl': output,
    'progress_hooks': [functools.partial(my_hook, json_file=jsonfile)],
    'logger': MyLogger(),
    }   
    with yt_dlp.YoutubeDL(ydl_opts) as ydl: #ydl_opts
        ydl.download([url])
    