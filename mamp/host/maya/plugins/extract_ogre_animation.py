"""
"""
import pyblish.api

from mamp.utils import ensure_output_dir


class ExtractOgreAnimClip(pyblish.api.InstancePlugin):

    label = "Ogre Animation Clip"
    optional = True

    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = ["animation.clip"]
    targets = ["animation", "ogre"]

    temp_export_track = "ogre_clip_export"

    def process(self, instance):
        import os

        from maya import cmds, mel
        from pyblish_maya import maintained_selection

        from mamp.host.maya.export import ogre
        from mamp.host.maya.utils import temp_anim_comp

        dirname = os.path.join(instance.data["stage_dir"], "ogre")

        ensure_output_dir(dirname)

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        # Ogre Command
        cmd = ogre.OgreCommand(mel.eval)

        start_frame = 1.0

        with maintained_selection():
            cmds.select(instance.data["geo"])

            # XXX: Need to check if export exists
            with temp_anim_comp(self.temp_export_track) as comp:
                for clip in instance:
                    self.log.debug("Extracting Clip: {}".format(clip))

                    if not cmds.nodeType(clip) == "timeEditorAnimSource":
                        continue

                    id_ = cmds.timeEditorClip(
                        "export_clip",
                        animSource=clip,
                        startTime=1.0,
                        track="{}:0".format(comp),
                    )

                    # Add the clip to the ogre skel export
                    end = start_frame + cmds.getAttr(
                        "{clip}.duration".format(**locals())
                    )

                    anims = ogre.OgreSkelOption(clip, dirname)

                    # Although the skeleton file should retain the clip name we
                    # want to remove some noise from our internal animation
                    anim_name = clip.split("_")[1:-1]
                    if anim_name[-1] == "base":
                        anim_name.pop()

                    anims.add_anim_clip("_".join(anim_name), start_frame, end)

                    command = cmd.execute_with(anims)
                    self.log.debug("Ogre Command: {}".format(command))

                    cmds.timeEditorClip(clipId=id_, e=True, removeClip=True)

                    instance.data["files"].append(anims.filename)


class ExtractOgreAnimComp(pyblish.api.InstancePlugin):

    label = "Ogre Animation Comp"
    optional = True

    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = ["animation.comp"]
    targets = ["animation", "ogre"]

    def process(self, instance):
        import os

        from maya import cmds, mel
        from pyblish_maya import maintained_selection

        from mamp.host.maya.export import ogre
        from mamp.host.maya.utils import temp_anim_comp

        dirname = os.path.join(instance.data["stage_dir"], "ogre")

        ensure_output_dir(dirname)

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        # Ogre Command
        cmd = ogre.OgreCommand(mel.eval)

        start_frame = 1.0

        with maintained_selection():
            cmds.select(instance.data["geo"])

            comp = instance.data["comp"]
            cmds.timeEditorComposition(comp, e=True, active=True)

            anims = ogre.OgreSkelOption(comp, dirname)

            start, end = instance.data["startFrame"], instance.data["endFrame"]

            # Although the skeleton file should retain the clip name we
            # want to remove some noise from our internal animation
            anim_name = " ".join(comp.split("_")[1:-1])
            anims.add_anim_clip(anim_name, start, end)

            self.log.debug("Extracting to: {}".format(anims.fullpath))

            command = cmd.execute_with(anims)

            self.log.debug("Ogre Command: {}".format(command))

            instance.data["files"].append(anims.filename)

