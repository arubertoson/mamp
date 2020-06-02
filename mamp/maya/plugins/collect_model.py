"""
"""
import pyblish.api


GEO_NODE = "geo"


class CollectModel(pyblish.api.ContextPlugin):

    label = "MAM Collect Model"
    order = pyblish.api.CollectorOrder
    hosts = ["maya"]

    def process(self, context):
        import os
        from maya import cmds

        name, family = "roebuck", "mam.model"
        ws = os.path.join(context.data["workspace_dir"], family)

        instance = context.create_instance(name, family)
        instance.set_data["stagedir"] = os.path.join(ws, "stage")

        cmds.select(name + ":" + GEO_NODE)
        instance[:] = cmds.file(
            constructionHistory=True,
            exportSelected=True,
            preview=True,
            force=True,
        )
