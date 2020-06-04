import pyblish.api


class CollectStageDir(pyblish.api.ContextPlugin):

    label = "Asset Stage"
    order = pyblish.api.CollectorOrder - 0.49
    hosts = ["maya"]

    def process(self, context):
        # XXX Should be handled by other service
        stage = "g:/project/{project}/assets/{sequence}/{shot}/stage/{step}/{app}".format(**context.data)

        context.set_data("stage_dir", value=stage)
