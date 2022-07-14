from flask import *
import json
from urllib.parse import parse_qs,urlparse
from src.run import Execute
from src.download import download

app = Flask(__name__)

@app.route('/',methods=['GET'])
def url():
    url = str(request.args.get('url'))  # /?url=URL
    # print(url)#parse_qs(urlparse(url).query)['v'][0])
    # download(url,'.temp/'+url[-5:])
    runner = Execute(url)
    runner.run()
    with open(runner.JSON_FILE, "r") as jsonFile:
            data = json.loads(jsonFile.read())
    return data

if __name__ == '__main__':
    app.run()
