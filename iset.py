# Get Settings. Little opticos utility
import json

path = None


def create(path):
    with open(path, "w") as obj:
        app = {
            "conf_ver":1,
            "backend":"gwsl",
            "acrylic_enabled":True,
            "theme":"dark",
            "assocs":{}
               }

        json.dump(app, obj, indent=True)
        obj.close()





def read():
    with open(path, "r") as obj:
        current = json.load(obj)
        obj.close()
        return current


def set(json_f):
    with open(path, "w") as obj:
        json.dump(json_f, obj, indent=True)
        obj.close()
