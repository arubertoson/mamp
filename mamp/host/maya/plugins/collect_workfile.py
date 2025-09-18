import pyblish.api


class CollectMamMayaCurrentFile(pyblish.api.ContextPlugin):
    """Collect the current Maya file

    Collect the current maya file from the context, if the 
    file is in an unsaved state the context will be dirty 
    and update the label to reflect that.
    """

    order = pyblish.api.CollectorOrder + 0.01
    label = "Current Maya File"

    hosts = ['maya']
    version = (0, 1, 0)

    def process(self, context):
        import os
        from maya import cmds
        from pyblish_qml import settings

        prefix = ""

        modified = cmds.file(modified=True, query=True)
        if modified:
            prefix = "*"

        # Inject the current working file
        current_file = cmds.file(sceneName=True, query=True)
        
        # Maya returns forward-slashes by default
        scene = os.path.basename(current_file)
        normalised = os.path.normpath(current_file)
        
        context.set_data('currentFile', value=normalised)
        
        label = context.data.get("label", "")
        context.set_data('label', value="{label} ({prefix}{scene})".format(**locals()))
