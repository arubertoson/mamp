"""
"""
import os
import sys

import pyblish.api

def register_plugins():
    from . import plugins
    path = os.path.dirname(plugins.__file__)

    pyblish.api.register_plugin_path(path)
    
