import json
from .download import download
from .remover import remove_silence
from .tools import uid

class Execute:
    def __init__(self,url):
        self.URL = url
        self.VIDEO = uid(url)
        self.JSON_FILE = 'progress/'+self.VIDEO+'_progress.json'

        self.in_file = '.temp/'+self.VIDEO+'.webm'
        self.out_file = 'noshh_vids/'+self.VIDEO+'.webm'

        with open(self.JSON_FILE, "w") as jsonFile:
            print("The json file is created")
            data = {
                "download":0,
                "audio":0,
                "video":0,
                "process":None
            }
            json.dump(data, jsonFile,indent=4)

    def run(self):
        download(self.URL,self.in_file,self.JSON_FILE)
        print(f'{self.VIDEO} Download Complete')
        remove_silence(self.in_file,self.out_file,self.VIDEO,self.JSON_FILE)
        print(f'{self.VIDEO} Processing Complete')

