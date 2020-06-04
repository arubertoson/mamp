"""
"""
import pyblish.api


class CollectAnimComps(pyblish.api.ContextPlugin):
    """Collect Animation Clips


    """

    label = "Animation Comps"
    order = pyblish.api.CollectorOrder + 0.1
    hosts = ["maya"]
    targets = ["animation"]

    def process(self, context):
        import os
        from maya import cmds

        family = "animation"
        shot = context.data["shot"] 

        pattern = "{}_*_*_comp".format(shot)

        comps = cmds.ls(pattern, type="timeEditorTracks") 
        if not len(comps) > 0:
            return self.log.info("No objects with pattern: {}".format(pattern))

        stage = os.path.abspath(os.path.join(context.data["stage_dir"], family.replace(".", "/")))

        for comp in comps:
            shot, variant, blend, anim_type = comp.split("_") 

            clips = set([])

            start, end = None, None

            tracks = cmds.timeEditorTracks(comp, q=True, allTracksRecursive=True)
            for t in tracks:
                track_clips = cmds.timeEditorTracks(t, q=True, allClips=True)
                if track_clips is None:
                    continue

                clips.update(track_clips)
                for c in track_clips:
                    s = cmds.timeEditorClip(c, q=True, startTime=True)
                    e = cmds.timeEditorClip(c, q=True, endTime=True)
                    if start is None:
                        start, end = s, e
                        continue

                    start = min([start, s])
                    end = max([end, e])
            
            name = "{variant} {blend} [{start}-{end}]".format(**locals())

            instance = context.create_instance(name, family=family + "." + anim_type)
            instance.set_data("stage_dir", value=stage)
            instance.set_data("geo", value=cmds.ls("{shot}:geo".format(**locals())))

            # Export
            instance.data["comp"] = comp
            instance.data["tracks"] = len(tracks)
            instance.set_data("startFrame", value=start)
            instance.set_data("endFrame", value=end)

            instance[:] = list(clips)
