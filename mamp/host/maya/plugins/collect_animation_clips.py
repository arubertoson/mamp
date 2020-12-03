"""
"""
import pyblish.api

from mamp.utils import increment_version_at


class CollectAnimClips(pyblish.api.ContextPlugin):
    """Collect Animation Clips


    """

    label = "Animation Clips"
    order = pyblish.api.CollectorOrder + 0.1
    hosts = ["maya"]
    targets = ["animation"]

    def process(self, context):
        import os
        from maya import cmds

        family = "animation"
        shot = context.data["shot"]
        datatype = "clip"

        pattern = "{shot}_*_*_{datatype}".format(**locals())

        clips = cmds.ls(pattern, type="timeEditorAnimSource")
        if not len(clips) > 0:
            return self.log.info("No objects with pattern: {}".format(pattern))

        stage = os.path.abspath(os.path.join(context.data["stage_dir"], datatype))

        rig = "{}:all".format(shot)
        if not cmds.objExists(rig):
            raise RuntimeError("Rig does not exist, or wrong namespace")

        for clip in clips:
            _, anim, variant, _ = clip.split("_")

            duration = cmds.getAttr(clip + ".duration")

            name = "{anim}::{variant} [{duration}]".format(**locals())

            instance = context.create_instance(name, family=family + "." + datatype)

            dirname = increment_version_at(os.path.join(stage, anim, variant))
            instance.set_data("stage_dir", value=dirname)

            instance.set_data("geo", value=cmds.ls("{shot}:geo".format(**locals())))

            self.log.info("collecting {clip}".format(**locals()))
            instance.data["members"] = [clip] + [rig]

            instance[:] = [clip]
