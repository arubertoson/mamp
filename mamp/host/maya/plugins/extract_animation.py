"""
"""
import pyblish.api

from mamp.utils import ensure_output_dir


class ExtractAnimClip(pyblish.api.InstancePlugin):

    label = "Animation Clip"
    optional = True

    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = ["animation.clip"]
    targets = ["animation"]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], "mb")

        ensure_output_dir(dirname)

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        with maintained_selection():
            for clip in instance:
                filename = "{clip}.mb".format(**locals())

                path = os.path.join(dirname, filename)

                cmds.select(clip, noExpand=True)
                cmds.file(
                    path,
                    force=True,
                    type="mayaBinary",
                    exportSelected=True,
                    preserveReferences=False,
                    constructionHistory=False,
                )

                self.log.debug("Extracted {}".format(path))
                instance.data["files"].append(filename)


# XXX: Should handle source file extract as well
class ExtractAnimComp(pyblish.api.InstancePlugin):

    label = "Animation Composition"
    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    optional = True

    families = ["animation.comp"]
    targets = ["animation"]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], "mb")

        ensure_output_dir(dirname)

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        with maintained_selection():
            comp = instance.data["comp"]
            cmds.timeEditorComposition(comp, e=True, active=True)

            tmpcomp = cmds.rename(comp, "_{}".format(comp))

            parent = cmds.timeEditor(clipId=instance, commonParentTrack=True)
            grpid = cmds.timeEditorClip(
                "export_group", clipId=instance, group=True, track=parent
            )

            # timeEditorClip -e -explode 4;
            clip = cmds.timeEditorBakeClips(
                clipId=grpid, sampleBy=1, keepOriginalClip=1, bakeToAnimSource=comp,
            )

            filename = "{clip}.mb".format(**locals())

            path = os.path.join(dirname, filename)

            cmds.select(clip, noExpand=True)
            cmds.file(
                path,
                force=True,
                type="mayaBinary",
                exportSelected=True,
                preserveReferences=True,
                constructionHistory=False,
            )

            cmds.delete(clip)
            cmds.rename(tmpcomp, comp)
            cmds.timeEditorClip(e=True, explode=grpid)

            self.log.debug("Extracted {}".format(path))
            instance.data["files"].append(filename)
