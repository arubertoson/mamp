"""
"""
import pyblish.api


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

        pattern = "{}_*_*_clip".format(shot)

        clips = cmds.ls(pattern, type="timeEditorAnimSource") 
        if not len(clips) > 0:
            return self.log.info("No objects with pattern: {}".format(pattern))

        stage = os.path.abspath(os.path.join(context.data["stage_dir"], family.replace(".", "/")))

        for clip in clips:
            shot, variant, blend, anim_type = clip.split("_") 

            duration = cmds.getAttr(clip+".duration")

            name = "{variant}::{blend} [{duration}]".format(**locals())

            instance = context.create_instance(name, family=family + "." + anim_type)
            instance.set_data("stage_dir", value=stage)
            instance.set_data("geo", value=cmds.ls("{shot}:geo".format(**locals())))

            self.log.info("collecting {clip}".format(clip=clip))
            instance[:] = [clip]
