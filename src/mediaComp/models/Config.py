import os
import json
'''
CONFIG_DICT = {
    "CONFIG_WRAPPIXELVALUES" : False,
    "CONFIG_MEDIA_PATH" : "",
    "CONFIG_SESSION_PATH" : "",
    "CONFIG_JES4PY_PATH" : ""
    }
CONFIG_FILENAME = ".jes4pyconf"

def getConfigVal(key):
    return CONFIG_DICT[key]

def setConfigVal(key, val):
    CONFIG_DICT[key] = val
    writeDict(CONFIG_DICT)

def initPath():
    import package
    CONFIG_DICT["CONFIG_JES4PY_PATH"] = os.path.dirname(package.__file__)

def initDict():
    filePath = os.path.join(os.path.expanduser("~"), CONFIG_FILENAME)
    if os.path.exists(filePath):
        curDict = readDict(filePath)
        global CONFIG_DICT
        pathDict = readDict(filePath)
        CONFIG_DICT["CONFIG_SESSION_PATH"]=pathDict["CONFIG_MEDIA_PATH"]
        CONFIG_DICT["CONFIG_MEDIA_PATH"]=pathDict["CONFIG_MEDIA_PATH"]

def writeDict(dict):
    filePath = os.path.join(os.path.expanduser("~"), CONFIG_FILENAME)
    f = open(filePath, "w")
    f.write(json.dumps(dict))
    f.close()

def readDict(filePath):
    f = open(filePath, "r")
    contents = f.read()
    dict = json.loads(contents)
    f.close()
    return dict
'''

CONFIG_FILENAME = ".mediaCompConfig.json"
DEFAULT_CONFIG = {
    "CONFIG_WRAPPIXELVALUES": False,
    "CONFIG_MEDIA_PATH": "",
    "CONFIG_SESSION_PATH": "",
    "CONFIG_MEDIACOMP_PATH": ""
}

class ConfigManager:
    def __init__(self):
        self.file_path = os.path.join(os.path.expanduser("~"), CONFIG_FILENAME)
        self.config = DEFAULT_CONFIG.copy()
        self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    stored = json.load(f)
                self.config.update(stored)
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")

    def _save(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save config: {e}")

    def get(self, key):
        return self.config.get(key, "")

    def set(self, key, value):
        self.config[key] = value
        self._save()

    def reset(self):
        self.config = DEFAULT_CONFIG.copy()
        self._save()

    def clearMediaPath(self):
        self.set("CONFIG_MEDIA_PATH", "")

    def getMediaPath(self, filename=""):
        base = self.get("CONFIG_MEDIA_PATH")
        return os.path.join(base, filename) if filename else base

    def setMediaPath(self, path):
        self.set("CONFIG_MEDIA_PATH", path)

    def getSessionPath(self):
        return self.get("CONFIG_SESSION_PATH")

    def setSessionPath(self, path):
        self.set("CONFIG_SESSION_PATH", path)

    def setMEDIACOMPPath(self):
        import mediaComp
        self.set("CONFIG_MEDIACOMP_PATH", os.path.dirname(mediaComp.__file__))

    def getMEDIACOMPPath(self):
        return self.get("CONFIG_MEDIACOMP_PATH")