"""
"""
import os
import pyblish.api

from mamp.utils import ensure_output_dir


class ExtractSource(pyblish.api.InstancePlugin):
    """Bla bla

    Some words
    """

    label = "Source File"
    order = pyblish.api.ExtractorOrder
    host = ["maya"]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection

        shot = instance.context.data["shot"]
        step = instance.context.data["step"]

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], "ma")

        ensure_output_dir(dirname)

        # XXX: Please reference the family name
        filename = "{shot}_{step}.ma".format(**locals())

        path = os.path.join(dirname, filename)

        with maintained_selection():
            self.log.debug("extracting to: {}".format(path))

            if instance.data["family"] == "animation.comp":
                cmds.timeEditorComposition(instance.data["comp"], e=True, active=True)

            cmds.select(instance.data["members"])

            cmds.file(
                path,
                force=True,
                typ="mayaAscii",
                exportSelected=True,
                preserveReferences=True,
                constructionHistory=True,
                shader=True,
                constraints=True,
                expressions=True,
            )

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        instance.data["files"].append(filename)
