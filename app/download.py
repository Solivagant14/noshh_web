import yt_dlp
from app.progress import progress

#A hook which reads the progress value
def my_hook(d):
    if d['status'] == 'downloading':
        percentage = int(float(d['_percent_str'].strip()[:-1]))
        progress(percentage, process="download")

#logger class which gives access to read the terminal output of yt_dlp
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

#function to download a url and store at a path
def download(url,output):
    ydl_opts = {
    'outtmpl': output,
    'progress_hooks': [my_hook],
    'logger': MyLogger(),
    }   

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    