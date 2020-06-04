"""
"""
import os
import logging

import pyblish.api

from mamp.errors import SetupError
from mamp.utils import ensure_single_run


log = logging.getLogger(__name__)


@ensure_single_run
def setup(host):

    if not hasattr(host, "setup"):
        raise SetupError("host {} is missing the setup function".format(host.__name__))

    _register_gui()
    _register_global_plugins()
    _register_target()

    host.setup()


def _register_target():
    step = os.environ.get("MAM_CTX_STEP", "")

    if not step:
        log.warning("current context is missing step (MAM_CTX_STEP), please reestablish context")

    # XXX: move table is magic
    target = {"anim": "animation", "model": "model", "rig": "rig",}[step]

    pyblish.api.register_target(target)


def _register_global_plugins():
    from mamp import plugins

    path = os.path.dirname(plugins.__file__)
    pyblish.api.register_plugin_path(os.path.abspath(path))


def _register_gui():
    try:
        __import__("pyblish_qml")
    except ImportError:
        msg = "module \"pyblish_qml\" no in path, exiting..."
        log.info(msg)

        raise ImportError(msg)

    pyblish.api.register_gui("pyblish_qml")
