import os
from Utils.IO import *
from Utils.Path import *

class Available:

    def __init__(self):

        modulesLoaded, modulePaths = getEnvModLoadedAndPaths()

        centreTextInConsole(" Available Modules ")
        i = 0
        for mod in modulePaths:
            if not os.path.exists(mod):
                printErr("Search path " + mod + " does not exist!")
                continue
            printErr("Path: " + mod)
            printDivider()
            for root, dirs, files in os.walk(mod):
                headPath, tailPath = os.path.split(mod)
                rootMinusMod = root.replace(headPath, "").strip(os.sep)
                for name in files:
                    if not name.endswith(("~", "#")):
                        moduleFileName = os.path.join(root, name)
                        alreadyLoaded="         "
                        for modAlreadyLoaded in modulesLoaded:
                            if modAlreadyLoaded == moduleFileName:
                                alreadyLoaded = "(Loaded) "
                        startOfFile = file(moduleFileName).read(8)
                        if "#%Module" in startOfFile:
                            printErr(alreadyLoaded + (rootMinusMod + os.sep + name).lstrip(os.sep))
            printErr("")

