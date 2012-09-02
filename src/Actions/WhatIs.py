import os
from Utils.IO import *
from Utils.Path import *
import shlex

class WhatIs:

    def __init__(self, specificModuleFile):

        modulesLoaded, modulePaths = getEnvModLoadedAndPaths()

        centreTextInConsole(" Module Descriptions (module-whatis) ")

        if specificModuleFile:
            for modPath in modulePaths:
            # Recurse through the tree
                for root, dirs, files in os.walk(modPath):
                    rootMinusMod = root.replace(modPath,"").strip("/ ")
                    for name in files:
                        if name in specificModuleFile:
                            moduleFileName = os.path.join(root, name)
                            with open(moduleFileName) as f:
                                for line in f:
                                    tokens = shlex.split(line)
                                    if tokens:
                                        if tokens[0] == "module-whatis":
                                            printErr("Path: " + modPath)
                                            printDivider()
                                            printErr(name + ": " + tokens[1])

        else:
            for modPath in modulePaths:
                printErr("Path: " + modPath)
                printDivider()
                # Recurse through the tree
                for root, dirs, files in os.walk(modPath):
                    rootMinusMod = root.replace(modPath,"").strip("/ ")
                    for name in files:
                        if not name.endswith(("~", "#")):
                            moduleFileName = os.path.join(root, name)
                            with open(moduleFileName) as f:
                                for line in f:
                                    tokens = shlex.split(line)
                                    if tokens:
                                        if tokens[0] == "module-whatis":
                                            printErr(name + ": " + tokens[1])
                printErr("")

