"""
"""
import pyblish.api


class ExtractAnimClip(pyblish.api.InstancePlugin):

    label = "Anim Clips"
    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = ["animation.clip"]
    targets = ["animation"]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection

        family = instance.data["family"]

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"])
        try:
            os.makedirs(dirname)         
        except OSError:
            pass

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        self.log.info("Performing Rig Extraction")
        with maintained_selection():
            for clip in instance:
                filename = "{clip}.mb".format(**locals())

                path = os.path.join(dirname, filename)

                self.log.info("extracting {clip}".format(**locals()))

                cmds.select(clip, noExpand=True)
                cmds.file(path,
                    force=True,
                    type="mayaBinary",
                    exportSelected=True,
                    preserveReferences=True,
                    constructionHistory=False,
                )

                self.log.debug("Extracted {}".format(path))
                instance.data["files"].append(filename)

        self.log.info("Finished extraction of animation clips")



class ExtractAnimComp(pyblish.api.InstancePlugin):

    label = "Animation Composition"
    order = pyblish.api.ExtractorOrder
    host = ["maya"]

    families = ["animation.comp"]
    targets = ["animation"]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection

        family = instance.data["family"]

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"])
        try:
            os.makedirs(dirname)         
        except OSError:
            pass

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        self.log.info("Performing Rig Extraction")
        with maintained_selection():
            comp = instance.data["comp"]
            cmds.timeEditorComposition(comp, e=True, active=True)

            newname = comp.rsplit("_", 1)[0] + "_clip"
            clip = cmds.timeEditorBakeClips(
                clipId=instance, 
                sampleBy=1, 
                keepOriginalClip=1, 
                bakeToAnimSource=newname,
            )

            filename = "{clip}.mb".format(**locals())

            path = os.path.join(dirname, filename)

            cmds.select(clip, noExpand=True)
            cmds.file(path,
                force=True,
                type="mayaBinary",
                exportSelected=True,
                preserveReferences=True,
                constructionHistory=False,
            )

            cmds.delete(clip)

            self.log.debug("Extracted {}".format(path))
            instance.data["files"].append(filename)
