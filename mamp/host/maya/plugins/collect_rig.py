"""
"""
import pyblish.api


class CollectRig(pyblish.api.ContextPlugin):

    label = "Maya Rig"
    order = pyblish.api.CollectorOrder + 0.1
    hosts = ["maya"]
    targets = ["rig"]

    def process(self, context):
        from maya import cmds

        name = context.data["shot"]
        family = "rig"

        instance = context.create_instance(name, family=family)
        instance[:] = cmds.ls(["|all|rig", "|all|geo"], long=True)

