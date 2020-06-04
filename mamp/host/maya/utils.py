"""
"""
from contextlib import contextmanager

from maya import cmds


@contextmanager
def temp_anim_comp(comp):
    cmds.timeEditorComposition(comp, createTrack=True)
    try:
        yield comp
    finally:
        cmds.timeEditorComposition(comp, edit=True, delete=True)
