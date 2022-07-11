import json

JSON_FILE = "progress.json"
with open(JSON_FILE, 'w') as f:
    print("The json file is created")

with open(JSON_FILE, "w") as jsonFile:
    data = {
        "download":0,
        "audio":0,
        "video":0,
        "process":None
    }
    json.dump(data, jsonFile,indent=4)

# FILE = ''.join(random.choices(string.ascii_lowercase,k=7))
FILE = 'video'

in_file = '.temp/'+FILE+'_temp.webm'
out_file = 'noshh_vids/'+FILE+'.webm'
