"""
"""
import pyblish.api

from mamp.utils import ensure_output_dir


class ExtractRig(pyblish.api.InstancePlugin):

    label = "Rig"
    order = pyblish.api.ExtractorOrder
    families = ["rig"]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], "mb")

        ensure_output_dir(dirname)

        filename = "{shot}.mb".format(**instance.context.data)

        path = os.path.join(dirname, filename)

        self.log.info("Performing Rig Extraction...")
        with maintained_selection():
            cmds.select(instance, noExpand=True)
            cmds.file(
                path,
                force=True,
                typ="mayaBinary",
                exportSelected=True,
                preserveReferences=False,
                channels=True,
                constraints=True,
                expressions=True,
                constructionHistory=True,
            )

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        instance.data["files"].append(filename)

        self.log.info("Extracted {instance} to {path}".format(**locals()))
