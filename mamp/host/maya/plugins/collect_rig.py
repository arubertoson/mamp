"""
"""
import pyblish.api

# XXX: create own ordering

from mamp.utils import increment_version_at


def _extract_variants(models):
    variants, static = [], []
    for m in models:
        if m.startswith("v_"):
            variants.append(m)
            continue

        static.append(m)

    return list(variants), list(static)


class CollectRig(pyblish.api.ContextPlugin):

    label = "Maya Rig"
    order = pyblish.api.CollectorOrder + 0.1
    hosts = ["maya"]
    targets = ["rig"]

    def process(self, context):
        import os

        from maya import cmds

        name = context.data["shot"]
        family = "rig"

        stage = context.data["stage_dir"]

        models = cmds.listRelatives(cmds.ls("|all|geo"), children=True) or []
        variants, static = _extract_variants(models)
        for v in variants:
            name = v.split("_", 1)[-1]
            instance = context.create_instance(name, family=family)

            dirname = increment_version_at(os.path.join(stage, name))
            instance.data["stage_dir"] = dirname

            # Variants and geo needs to be handled as two entities
            instance.data["variant"] = v
            instance.data["geo"] = [v] + static

            # Everything that is part of the rig will be selectable
            instance[:] = [v, "|all|rig"] + static
