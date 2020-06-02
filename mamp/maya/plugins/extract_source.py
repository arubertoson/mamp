"""
"""
import pyblish.api


class ExtractSource(pyblish.api.InstancePlugin):

    label = "MAM Source"
    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = [
        "mam.model",
        "mam.rig",
        "mam.anim",
    ]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection

        datatype = "mb"

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], datatype)
        try:
            os.makedirs(dirname)
        except OSError:
            pass

        filename = "{shot}.{datatype}".format(instance.context.data["shot"], datatype)

        path = os.path.join(dirname, filename)

        with maintained_selection():
            cmds.select(instance, noExpand=True)
            cmds.file(path,
                force=True,
                type="mayaBinary",
                exportSelected=True,
                preserveReferences=True,
                constructionHistory=False,
            )

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        instance.data["files"].append(filename)
