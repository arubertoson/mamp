"""
"""
import pyblish.api

from mamp.utils import increment_version_at

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

        stage = context.data["stage_dir"]

        models = cmds.listRelatives(cmds.ls("|all|geo"), children=True, fullPath=True) or []
        for m in models:
            instance = context.create_instance(m, family=family)

            name = m.split("|")[-1]

            dirname = increment_version_at(os.path.join(stage, name))
            instance.data["stage_dir"] = dirname

            geo = cmds.listRelatives(m, allDescendents=True)

            # Models won't be collected from namespaces
            instance[:] = instance.data["members"] = geo

            # instance[:] = [m]
