"""
"""
import pyblish.api


RIG_NODE = "all"


class CollectRig(pyblish.api.ContextPlugin):

    label = "MAM Collect Rig"
    order = pyblish.api.CollectorOrder
    hosts = ["maya"]

    def process(self, context):
        from maya import cmds

        name, family = "roebuck", "mam.rig"

        wsdir = os.path.dirname(context.data["workspace_dir"])
        stage = os.path.join(wsdir, ".stage")

        instance = context.create_instance(name, family)
        instance.set_data["stage_dir"] = stage

        instance[:] = cmds.ls(name + ":" + RIG_NODE)
