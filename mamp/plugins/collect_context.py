import pyblish.api


class CollectAssetContext(pyblish.api.ContextPlugin):
    """Inject Asset Context

    Will collect the active environment context.

    """

    label = "Asset Context"
    order = pyblish.api.CollectorOrder - 0.5
    hosts = ["*"]

    def process(self, context):
        import os

        project = os.environ["MAM_CTX_PROJECT"]
        sequence = os.environ["MAM_CTX_SEQUENCE"]
        shot = os.environ["MAM_CTX_SHOT"]
        step = os.environ["MAM_CTX_STEP"]


        context.data["app"] = "maya"

        context.set_data("project", value=project)
        context.set_data("sequence", value=sequence)
        context.set_data("shot", value=shot)
        context.set_data("step", value=step)

        context.set_data("label", value="{shot}".format(**locals()))
        
