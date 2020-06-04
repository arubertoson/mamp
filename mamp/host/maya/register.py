"""
"""
import os
import sys
import logging

import pyblish.api

import mamp


log = logging.getLogger(__name__)


def setup():
    """Setup integration

    Registers Maya plug-ins and appends appends an item to the mam-menu
    
    """

    _register_host()
    _register_plugins()

    _install_menu()
    _configure_qml()


def _configure_qml():
    try:
        __import__("pyblish_qml")
    except ImportError:
        log.warning("Maya integration failed, \"pyblish_qml\" no in path.")
        
    from PySide2 import QtWidgets
    from pyblish_qml import settings

    app = QtWidgets.QApplication.instance()
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()

    # QML Settings
    settings.WindowSize = (width / 3, height / 3)
    settings.WindowPosition = (width / 6, height / 6)
    settings.HiddenSections = ["Collect", "Extract", "Other"]


def _register_plugins():
    from mamp.host.maya import plugins

    path = os.path.dirname(plugins.__file__)

    pyblish.api.register_plugin_path(os.path.abspath(path))


def _register_host():
    pyblish.api.register_host("maya")


def _install_menu():
    # XXX: Better system for menus
    from maya import cmds

    MAIN_MENU_NAME = "MAM_MAIN_MENU"
    MENU_LABEL = "MAM Tools"

    if not cmds.menu(MAIN_MENU_NAME, exists=True):
        cmds.menu(
            MAIN_MENU_NAME, label=MENU_LABEL, parent="MayaWindow",
        )

    pyblish_button = "MAM_PYBLISH"
    pyblish_subdiv = "MAM_PYBLISH_SUBDIV"

    # This must be duplicated here, due to this function
    # not being available through the above `evalDeferred`
    for item in (pyblish_button, pyblish_subdiv):
        if cmds.menuItem(item, exists=True):
            cmds.deleteUI(item, menuItem=True)

    icon = os.path.dirname(pyblish.__file__)
    icon = os.path.join(icon, "icons", "logo-32x32.svg")

    # Menu
    cmds.menuItem(
        pyblish_button,
        insertAfter="",
        label="Publish...",
        image=icon,
        command="import pyblish_maya; pyblish_maya.show()",
        parent=MAIN_MENU_NAME,
    )
    cmds.menuItem(
        pyblish_subdiv,
        insertAfter=pyblish_button,
        divider=True,
        parent=MAIN_MENU_NAME,
    )

