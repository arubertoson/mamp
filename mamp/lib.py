"""
"""
import os
import json


def get_template():
    with open("/mnt/g/project/marksman/config/templates.json") as f:
        data = json.load(f)

    return data["attributes"], data["templates"]

def collect_ogre_files():
    attr, temp = get_template()

    context = {
        "project": "marksman",
        "shot": "roebuck",
        "sequence": "char",
        "representation": "ogre"
    }

    context["asset"] = attr["asset"].format(**context)

    files = {}
    rig_files(temp["rig"], context, files)
    # anim_files(temp["anim"], context, files)
    # mat_files(temp["mat"], context, files)

    return files

def anim_files(tmp, context, files):
    context["step"] = "anim"
    context["datatype"] = "comp"

    ndict = {}
    ndict.update(context)
    root = tmp[:tmp.index("{anim}")].format(**context)
    for anim in os.listdir(root):
        root = tmp[:tmp.index("{variant}")].format(**context)
        for variant in os.listdir(root):


def rig_files(tmp, context, files):
    context["step"] = "rig"

    ndict = {}
    ndict.update(context)

    root = tmp[:tmp.index("{variant}")].format(**context)
    for variant in os.listdir(root):
        vpath = os.path.join(root, variant)

        version = max([v[1:] for v in os.listdir(vpath)])

        ndict.update({
            "variant": variant,
            "version": version,
        })

        path = tmp.format(**ndict) 

        files.setdefault(variant, {})["path"] = path
        files.setdefault(variant, [])["files"] = os.listdir(path)

    return

def main():
    print(collect_ogre_files())

if __name__ == "__main__":
    main()
