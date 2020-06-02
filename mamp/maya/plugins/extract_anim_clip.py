"""
"""
import pyblish.api


class ExtractAnimClip(pyblish.api.InstancePlugin):

    label = "MAM Anim Export"
    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = [
        "mam.anim.clip",
    ]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection

        family = instance.data["family"]
        datatype = family.rsplit(".", 1)[-1]

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], datatype)
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
        
                filename = "{clip}.mb".format(clip)

                path = os.path.join(dirname, filename)

                # cmds.select(clip, noExpand=True)
                # cmds.file(path,
                #     force=True,
                #     type="mayaBinary",
                #     exportSelected=True,
                #     preserveReferences=True,
                #     constructionHistory=False,
                # )

                self.log.debug("Extracted {}".format(path))
                instance.data["files"].append(filename)

        self.log.info("Finished extraction of animation clips")
