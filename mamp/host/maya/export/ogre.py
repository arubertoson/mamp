"""
"""
import os

class CmdOption:

    def __init__(self, name, path=""):
        self._cmd = [self._cmd_string]

        self._filename = name+"."+self._ext 
        self._dirname = path
        self._fullpath = os.path.join(path, self._filename)

    def __str__(self):
        return " ".join(self._cmd).format(**self.__dict__).replace("\\", "/")

    @property
    def dirname(self):
        return self._dirname

    @property
    def fullpath(self):
        return self._fullpath

    @property
    def filename(self):
        return self._filename

    @property
    def cmd(self):
        return self.__str__()


class OgreMeshOption(CmdOption):

    _cmd_string = '-version {_version} -mesh "{_fullpath}"'
    _ext = "mesh"

    # Defaults
    _version = "1.10"

    def with_ogre_mesh_version(self, version):
        self._version = version

    def with_vertex_bone_assignment(self):
        self._cmd.append("-v")
    
    def with_vertex_normals(self):
        self._cmd.append("-n")

    def with_texture_coordinates(self):
        self._cmd.append("-t")


class OgreSkelOption(CmdOption):

    _cmd_string = '-skel "{_fullpath}"'
    _ext = "skeleton"

    def with_skeleton_anims(self):
        if hasattr(self, "skel_anim") and self.skel_anim:
            return

        self.skel_anim = True
        self._cmd.append("-skeletonAnims -bindPose")

    def add_anim_clip(self, name, start, end):
        self.with_skeleton_anims()
        
        self._cmd.append(
            "-skeletonClip \"{name}\" startEnd {start} {end} frames sampleByFrames 1".format(**locals())
        )


class OgreMaterialOption(CmdOption):

    _cmd_string = '-mat "{_fullpath}"'
    _ext = "material"

    def with_prefix(self, prefix):
        self._cmd.append('-matPrefix "{prefix}"'.format(prefix))

    def with_light_off(self):
        self._cmd.append("-lightOff")
    

class OgreCommand(CmdOption):

    _cmd_string = " ".join([
        "ogreExport",
        "-{_export_selected}",
        "-{_coord_system}",
        "-lu {_unit_of_measure}",
        "-scale {_scale}",
    ])

    def __init__(self, executor):

        self._exec = executor
        self._cmd = [self._cmd_string]

        # Options Defaults
        self._export_selected = "sel"
        self._coord_system = "world"
        self._unit_of_measure = "pref"
        self._scale = 1.0

    def add_option(self, option):
        self._cmd.append(option.cmd)

    def execute(self):
        """
        """
        self._exec(str(self))

    def execute_with(self, *args):
        command = " ".join([str(self)] + [str(_) for _ in args])
        try:
            self._exec(command)
        except RuntimeError:
            pass

        return command


def testo(instr):
    print(instr)

if __name__ == "__main__":
    ocmd = OgreCommand(testo)

    omat = OgreMaterialOption("somemat", "/out/path")
    omat.with_light_off()

    oanim = OgreSkelOption("someskel", "/out/path")
    oanim.add_anim_clip("anim_clip", 1, 2)
    oanim.add_anim_clip("anim_clip", 3, 4)

    ocmd.add_option(omat)
    ocmd.add_option(oanim)

    ocmd.execute()
