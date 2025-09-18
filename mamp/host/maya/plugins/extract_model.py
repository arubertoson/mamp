"""
"""
import os
import pyblish.api

from mamp.utils import ensure_output_dir


class ExtractModel(pyblish.api.InstancePlugin):
    """Extract Model
    """

    label = "Model"
    optional = True

    order = pyblish.api.ExtractorOrder
    host = ["maya"]

    def process(self, instance):
        from maya import cmds
        from pyblish_maya import maintained_selection

        shot = instance.context.data["shot"]
        step = instance.context.data["step"]

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], "mb")

        ensure_output_dir(dirname)

        # XXX: Please reference the family name
        filename = "{shot}_{step}.mb".format(**locals())

        path = os.path.join(dirname, filename)

        with maintained_selection():
            self.log.debug("extracting to: {}".format(path))

            cmds.select(instance)

            cmds.file(
                path,
                force=True,
                typ="mayaBinary",
                exportSelected=True,
                preserveReferences=False,
                constructionHistory=False,
            )

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        instance.data["files"].append(filename)

