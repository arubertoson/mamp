"""
"""
import pyblish.api


class ExtractOgreRig(pyblish.api.InstancePlugin):

    label = "Ogre Rig"
    optional = True

    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = ["rig"]
    targets = ["ogre", "rig"]

    def process(self, instance):
        import os

        from maya import cmds, mel
        from mamp.maya.export import ogre

        self.log.info("Found ogre plugin")

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"])
        try:
            os.makedirs(dirname)
        except OSError:
            pass

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        cmd = ogre.OgreCommand(mel.eval)
        skel = ogre.OgreSkelOption(instance.context.data["shot"], dirname)

        # cmd.add_option(skel)
        instance.data["files"].append(skel.filename)

        for geo in instance:
            self.log.info("Extract ogre mesh: {}".format(geo))

            cmds.select(geo)

            name = geo.rsplit("|", 1)[-1]

            mat = ogre.OgreMaterialOption(name, dirname)
            mesh = ogre.OgreMeshOption(name, dirname)
            mesh.with_ogre_mesh_version(1.8)
            mesh.with_vertex_bone_assignment()
            mesh.with_vertex_normals()
            mesh.with_texture_coordinates()

            command = cmd.execute_with(mesh, mat, skel)
            self.log.info("Extract ogre format with: {}".format(command))

            instance.data["files"].append(mesh.filename)



class ExtractOgreAnimClip(pyblish.api.InstancePlugin):

    label = "Ogre Animation Clip"
    optional = True

    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = [
        "animation.clip"
    ]
    targets = ["animation", "ogre"]

    def process(self, instance):
        import os

        from maya import cmds, mel
        from pyblish_maya import maintained_selection

        from mamp.maya.export import ogre
        from mamp.maya.utils import temp_anim_comp

        self.log.info("Extracting clips: {}".format(len(instance)))

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], "ogre")
        try:
            os.makedirs(dirname)
        except OSError:
            pass

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        # Ogre Command
        cmd = ogre.OgreCommand(mel.eval)

        start_frame = 1.0

        with maintained_selection():
            cmds.select(instance.data["geo"])

            # XXX: Need to check if export exists
            with temp_anim_comp("export") as comp:
                for clip in instance:
                    self.log.info("extract {}, {}".format(clip, comp))
                    # source = cmds.timeEditorClip(12, q=True, animSource=True)

                    id_ = cmds.timeEditorClip(
                        "export_clip",
                        animSource=clip,
                        startTime=1.0,
                        track="{}:0".format(comp),
                    )

                    # Add the clip to the ogre skel export
                    end = start_frame + cmds.getAttr("{clip}.duration".format(**locals()))

                    anims = ogre.OgreSkelOption(clip, dirname)

                    # Although the skeleton file should retain the clip name we
                    # want to remove some noise from our internal animation
                    anim_name = " ".join(clip.split("_")[1:-1])
                    anims.add_anim_clip(anim_name, start_frame, end)

                    instance.data["files"].append(anims.filename)

                    cmd.execute_with(anims)

                    cmds.timeEditorClip(clipId=id_, e=True, removeClip=True)


class ExtractOgreAnimComp(pyblish.api.InstancePlugin):

    label = "Ogre Animation Comp"
    optional = True

    order = pyblish.api.ExtractorOrder
    host = ["maya"]
    families = [
        "animation.comp"
    ]
    targets = ["animation", "ogre"]

    def process(self, instance):
        import os

        from maya import cmds, mel
        from pyblish_maya import maintained_selection

        from mamp.maya.export import ogre
        from mamp.maya.utils import temp_anim_comp

        self.log.info("Extracting clips: {}".format(len(instance)))

        # Make sure our stagedir exists
        dirname = os.path.join(instance.data["stage_dir"], "ogre")
        try:
            os.makedirs(dirname)
        except OSError:
            pass

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        # Ogre Command
        cmd = ogre.OgreCommand(mel.eval)

        start_frame = 1.0

        with maintained_selection():
            cmds.select(instance.data["geo"])

            comp = instance.data["comp"]
            cmds.timeEditorComposition(comp, e=True, active=True)

            clip = comp.rsplit("_", 1)[0] + "_clip"

            anims = ogre.OgreSkelOption(clip, dirname)

            start, end = instance.data["startFrame"], instance.data["endFrame"]

            # Although the skeleton file should retain the clip name we
            # want to remove some noise from our internal animation
            anim_name = " ".join(clip.split("_")[1:-1])
            anims.add_anim_clip(anim_name, start, end)

            cmd.execute_with(anims)

            instance.data["files"].append(anims.filename)

