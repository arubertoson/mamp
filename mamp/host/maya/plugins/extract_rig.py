"""
"""
import pyblish.api


class ExtractRig(pyblish.api.InstancePlugin):

    label = "MAM Rig"
    order = pyblish.api.ExtractorOrder
    families = ["rig"]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection
        
        # Make sure our stagedir exists
        dirname = instance.data["stage_dir"]
        try:
            os.makedirs(dirname)
        except OSError:
            pass

        context = instance.context

        filename = "{shot}.mb".format(**context.data)

        path = os.path.join(dirname, filename)

        self.log.info("Performing Rig Extraction...")
        with maintained_selection():
            cmds.select(instance, noExpand=True)
            cmds.file(path, 
                    force=True,
                    type="mayaBinary", 
                    exportSelected=True, 
                    preserveReferences=False,
                    constructionHistory=False, 
            )

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        instance.data["files"].append(filename)

        self.log.info("Extracted {instance} to {path}".format(**locals()))


# class ExtractOgreSkel(pyblish.api.InstancePlugin):
#
#     label = "Ogre Rig Extractor"
#     order = pyblish.api.ExtractorOrder
#     families = ["mam.rig"]
#     hosts = ["maya"]

