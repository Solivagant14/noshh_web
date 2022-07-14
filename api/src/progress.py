import json

#function to assign the values to json file
def progress(percentage=0, process=None, json_file=''):
    with open(json_file, "r") as jsonFile:
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

    with open(json_file, "w") as jsonFile:
        json.dump(data, jsonFile,indent=4)