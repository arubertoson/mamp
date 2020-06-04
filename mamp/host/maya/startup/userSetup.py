
try:
    __import__("pyblish_maya")
except ImportError as e:
    import traceback
    print(
        "mamp: Could not load integration: {}".format(traceback.format_exc())
    )

else:
    from mamp.host import maya
    from mamp.register import setup

    setup(maya)
