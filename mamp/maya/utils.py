"""
"""
from contextlibs import contextmanager

from maya import cmds


@contextmanager
def temp_anim_comp(comp, clip_ids):
    cmds.timeEditorComposition(comp, createTrack=True)
    try:
        yield comp
    finally:
        cmds.timeEditorComposition(comp, edit=True, delete=True)
        # Abusing pass by reference from clip cleanup
        for clip in clip_ids:
            cmds.timeEditorClip(clipId=clip, e=True, removeClipe=True)

