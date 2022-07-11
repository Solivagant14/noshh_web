from flask import *
import json
from app.download import download
from app.remover import remove_silence
from app import in_file,out_file,JSON_FILE

async def sequence():
    download(url,in_file)
    remove_silence(in_file,out_file)

app = Flask(__name__)

@app.route('/',methods=['GET'])
def url():
    url = str(request.args.get('url'))  # /?url=URL
    download(url,in_file)
    remove_silence(in_file,out_file)    
    with open(JSON_FILE, "r") as jsonFile:
            data = json.loads(jsonFile.read())
    return data

if __name__ == '__main__':
    app.run()
