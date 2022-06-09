import sys
from app import in_file,out_file
from app.download import download
from app.remover import remove_silence
from app.progress import progress

url = sys.argv[1]

download(url,in_file)
remove_silence(in_file,out_file)

progress(process="Done")
