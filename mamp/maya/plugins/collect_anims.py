"""
"""
import pyblish.api


class CollectAnimClips(pyblish.api.ContextPlugin):

    label = "MAM Collect Anim Clips"
    order = pyblish.api.CollectorOrder
    hosts = ["maya"]

    def process(self, context):
        from maya import cmds

        name, family = context.data["shot"], "mam.anim.clip"

        wsdir = os.path.dirname(context.data["workspace_dir"])
        stage = os.path.join(wsdir, ".stage", family.rsplit(".", 1)[-1])

        instance = context.create_instance(name, family)
        instance.set_data["stage_dir"] = stage

        instance[:] = cmds.ls("{}_*_*_clip".format(name))


class CollectAnimComposition(pyblish.api.ContextPlugin):

    label = "MAM Collect Anim Compositions"
    order = pyblish.api.CollectorOrder
    hosts = ["maya"]

    def process(self, context):
        from maya import cmds

        # timeEditorBakeClips -sampleBy 1 -keepOriginalClip 1 -bakeToClip Baked -tti -2 ;
        name, family = context.data["shot"], "mam.anim.comp"

        wsdir = os.path.dirname(context.data["workspace_dir"])
        stage = os.path.join(wsdir, ".stage", family.rsplit(".", 1)[-1])

        instance = context.create_instance(name, family)
        instance.set_data["stage_dir"] = stage

        instance[:] = cmds.ls("{shot}_*_*_comp".format(name))
