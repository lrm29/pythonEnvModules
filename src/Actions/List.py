import os

from Utils.IO import *
from Utils.Path import *

class List:

    def __init__(self):

        modulesLoaded, modulePaths = getEnvModLoadedAndPaths()

        if not modulesLoaded:
            printErr("No modules have been loaded")
        else:
            centreTextInConsole(" Modules Loaded ")
            i = 0
            for modPath in modulePaths:
                loadedModulesToPrint = list()
                headPath, tailPath = os.path.split(modPath)
                for mod in modulesLoaded:
                    head, tail = os.path.split(mod)
                    if mod.startswith(modPath):
                        i += 1
                        loadedModulesToPrint.append(str(i) + ") " + mod.replace(headPath, "").strip(os.sep))
                if loadedModulesToPrint:
                    printErr("Path: " + modPath)
                    printDivider()
                    for module in loadedModulesToPrint:
                        printErr(module)
                    printErr("")

            printErr("A total of " + str(i)  + " modules are loaded")

