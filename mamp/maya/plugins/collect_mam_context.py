import pyblish.api


class CollectMamContext(pyblish.api.ContextPlugin):
    """Inject current asset context into pyblish context."""

    label = "Mam Asset Context"
    order = pyblish.api.CollectorOrder - 0.5
    hosts = ["*"]

    def process(self, context):
        import os

        project = os.environ["MAM_CTX_PROJECT"]
        sequence = os.environ["MAM_CTX_SEQUENCE"]
        shot = os.environ["MAM_CTX_SHOT"]
        step = os.environ["MAM_CTX_STEP"]

        self.log.info("Trying to set context data... {shot}".format(shot))
        context.set_data("project", value=project)
        context.set_data("sequence", value=sequence)
        context.set_data("shot", value=shot)
        context.set_data("step", value=step)
