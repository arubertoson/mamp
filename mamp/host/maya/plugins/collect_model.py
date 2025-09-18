"""
"""
import pyblish.api


class CollectModel(pyblish.api.ContextPlugin):

    label = "MAM Collect Model"
    order = pyblish.api.CollectorOrder + 0.1
    hosts = ["maya"]
    targets = ["model"]

    def process(self, context):
        import os
        from maya import cmds

        shot = context.data["shot"]
        family = "model"

        models = cmds.listRelatives(cmds.ls("|all|geo"), children=True, fullPath=True) or []
        for m in models:
            instance = context.create_instance(m, family=family)

            # Models won't be collected from namespaces
            instance[:] = [m]
