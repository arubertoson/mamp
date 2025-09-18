"""
"""
import pyblish.api

from mamp.utils import ensure_output_dir


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
        from mamp.host.maya.export import ogre

        # XXX: dynamically load ogre plugin

        dirname = os.path.join(instance.data["stage_dir"], "ogre")

        ensure_output_dir(dirname)

        name = instance.data["variant"].split("_", 1)[-1]

        # For integration
        if "files" not in instance.data:
            instance.data["files"] = []

        # Ogre Command
        cmd = ogre.OgreCommand(mel.eval)
        skel = ogre.OgreSkelOption(name, dirname)

        mat = ogre.OgreMaterialOption(name, dirname)

        mesh = ogre.OgreMeshOption(name, dirname)
        mesh.with_ogre_mesh_version(1.8)
        mesh.with_vertex_bone_assignment()
        mesh.with_vertex_normals()
        mesh.with_texture_coordinates()

        self.log.debug("Extracting to: {}".format(mat.fullpath))
        self.log.debug("Extracting to: {}".format(mesh.fullpath))

        # context menu
        cmds.select(instance.data["geo"])

        command = cmd.execute_with(mesh, mat, skel)

        self.log.debug("Ogre Command: {}".format(command))

        # XXX: keeping this here as an idea for a callout, it's a nasty side effect but meh.
        # result = subprocess.call(["ogrmm", mesh.fullpath, "--skeleton", skel.fullpath, "--output", mesh.fullpath])
        # if result > 0:
        #     self.log.warning("Failed to assign skeleton file: {} to mesh {}".format(skel.fullpath, mesh.fullpath))

        instance.data["files"].append(mat.filename)
        instance.data["files"].append(mesh.filename)
        instance.data["files"].append(skel.filename)
