"""
"""
import pyblish.api

from mamp.utils import increment_version_at


class CollectAnimComps(pyblish.api.ContextPlugin):
    """Collect Animation Composition

    """

    label = "Animation Comps"
    order = pyblish.api.CollectorOrder + 0.1
    hosts = ["maya"]
    targets = ["animation"]

    def process(self, context):
        import os
        from maya import cmds

        family = "animation.comp"
        shot = context.data["shot"]

        pattern = "{}_*_*_clip".format(shot)

        comps = cmds.ls(pattern, type="timeEditorTracks")
        if not len(comps) > 0:
            return self.log.info("No objects with pattern: {}".format(pattern))

        stage = os.path.abspath(os.path.join(context.data["stage_dir"], "clip"))

        rig = "{}:all".format(shot)
        if not cmds.objExists(rig):
            raise RuntimeError("Rig does not exist, or wrong namespace")

        for comp in comps:
            shot, anim, variant, datatype = comp.split("_")

            clips = set([])

            start, end = None, None

            tracks = cmds.timeEditorTracks(comp, q=True, allTracks=True)
            for t in tracks:
                track_clips = cmds.timeEditorTracks(t, q=True, allClips=True)
                if track_clips is None:
                    continue

                clips.update(track_clips)
                for c in track_clips:
                    s = cmds.timeEditorClip(c, q=True, startTime=True)
                    e = max(
                        [
                            cmds.timeEditorClip(c, q=True, endTime=True),
                            cmds.timeEditorClip(c, q=True, loopEnd=True),
                        ]
                    )

                    if start is None:
                        start, end = s, e
                        continue

                    start = min([start, s])
                    end = max([end, e])

            name = "{anim} {variant} [{start}-{end}]".format(**locals())

            instance = context.create_instance(name, family=family)

            # Output dir
            dirname = increment_version_at(os.path.join(stage, anim, variant))
            instance.set_data("stage_dir", value=dirname)

            instance.set_data("geo", value=cmds.ls("{shot}:geo".format(**locals())))

            # Export
            instance.data["comp"] = comp
            instance.data["tracks"] = len(tracks)
            instance.set_data("startFrame", value=start)
            instance.set_data("endFrame", value=end)

            nodes = [cmds.timeEditorClip(i, q=True, animSource=True) for i in clips]
            instance.data["members"] = nodes + [comp] + [rig]

            instance[:] = [comp]
