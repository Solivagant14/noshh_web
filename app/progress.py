import json

FILE = "progress/progress.json"
#function to assign the values to json file
def progress(percentage=0, process=None):
    with open(FILE, "r") as jsonFile:
        data = json.loads(jsonFile.read())

    match process:
        case "download":
             data["download"] = percentage
        case "audio":
             data["audio"] = percentage
        case "video":
             data["video"] = percentage
        case "Done":
            pass
        case _:
            raise Exception("Process not Identified")

    data["process"] = process

    with open(FILE, "w") as jsonFile:
        json.dump(data, jsonFile,indent=4)