import pyblish.api


class CollectAssetContext(pyblish.api.ContextPlugin):
    """Inject current asset context into pyblish context."""

    order = pyblish.api.CollectorOrder - 1.0
    label = "Mam Asset Context"

    hosts = ["maya"]
    version = (0, 0, 1)

    def process(self, context):
        import os

        project = os.environ["MAM_CTX_PROJECT"]
        sequence = os.environ["MAM_CTX_SEQUENCE"]
        shot = os.environ["MAM_CTX_SHOT"]
        step = os.environ["MAM_CTX_STEP"]

        context.set_data("project", value=project)
        context.set_data("sequence", value=sequence)
        context.set_data("shot", value=shot)
        context.set_data("step", value=step)
