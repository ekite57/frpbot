import json
import os

CUSTOM_CONFIG_PATH = "customconf.json"

def readConfig():
    if (
        os.path.exists(CUSTOM_CONFIG_PATH)
        and os.path.isfile(CUSTOM_CONFIG_PATH)
    ):
        try:
            conf = open(
                file = CUSTOM_CONFIG_PATH,
                mode = "r",
                encoding = "utf-8"
            )
            confContent = conf.read()
            confObject = json.loads(confContent)
            return confObject
        except Exception as e:
            print(f"error when opening custom config: {e}")

    elif (
        os.path.exists("config.json")
        and os.path.isfile("config.json")
    ):
        try:
            conf = open(
                file = "config.json",
                mode = "r",
                encoding = "utf-8"
            )
            confContent = conf.read()
            confObject = json.loads(confContent)
            return confObject
        except Exception as e:
            print(f"error when opening default config: {e}")

    else:
        print(f"cannot find either the default config file (config.json) or your custom config file ({CUSTOM_CONFIG_PATH}).")

def getConfig(confObject, confKey):
    if (confKey in confObject):
        return confObject.get(confKey)
    else:
        print(f"failed to get config: {confKey}")

if __name__ == "__main__":
    print("you are not supposed to run this - run main.py instead")
