"""
"""
import os
import pyblish.api

def ensure_dir_exists(dirname):
    """
    """
    try:
        os.makedirs(dirname)
    except OSError:
        pass

class ExtractSource(pyblish.api.InstancePlugin):
    """Bla bla

    Some words
    """

    label = "Source File"
    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    optional = True
    active = False
    target = ["anim.comp"]

    def process(self, instance):
        import os

        from maya import cmds
        from pyblish_maya import maintained_selection

        shot = instance.context.data["shot"]
        family, subfam = instance.data["family"].split(".", 1)[0], instance.data["family"]

        if not subfam:
            subfam = family

        # Make sure our stagedir exists
        dirname = instance.data["stage_dir"]
        ensure_dir_exists(dirname)

        # XXX: Please reference the family name
        filename = "{shot}_{subfam}.ma".format(**locals())

        path = os.path.join(dirname, filename)

        with maintained_selection():
            cmds.select(instance, noExpand=True)
            cmds.file(path,
                force=True,
                type="mayaAscii",
                exportSelected=True,
                preserveReferences=True,
                constructionHistory=False,
            )

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        instance.data["files"].append(filename)
