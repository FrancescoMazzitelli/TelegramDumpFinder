import json


def init():
    fileJ = open('classes_and_files/settings_dark.json')
    settings = json.load(fileJ)
    return settings
