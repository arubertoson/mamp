"""
"""
import pyblish.api

from mamp.utils import temp_anim_comp


class ExtractOgreAnim(pyblish.api.InstancePlugin):

    label = "MAM Ogre Anim Export"
    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = [
        "mam.anim.clip"
    ]

    def process(self, instance):
        from maya import cmds, mel
        from pyblish_maya import maintained_selection

        from mamp.export import ogre

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], "ogre")
        try:
            os.makedirs(dirname)
        except OSError:
            pass

        # Ogre Command
        cmd = ogre.OgreCommand(mel.eval)
        anims = OgreSkelOption(instance.data["shot"], dirname)

        clip_ids = set()
        with temp_anim_comp("export", clip_ids) as comp:
            st, offset = 1.0, 1.0
            for clip in instance:
                clip_ids.add(cmds.timeEditorClip(
                    "{}_clip".format(clip),
                    animSource=clip,
                    startTime=st,
                    track="{comp}:0".format(comp),
                ))

                # Add the clip to the ogre skel export
                end = st + cmds.getAttr("{}.duration".format(clip))

                anims.add_anim_clip(clip, st, end)

                st += end + offset

            # Add the anim option to the ogre export command and perform the export
            cmd.add_option(anims)

            with maintained_selection():
                cmds.select(":geo")

                cmd.execute()

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        instance.data["files"].append(anims.filename)
