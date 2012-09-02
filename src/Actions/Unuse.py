import os

from Shell.Shell import *
from Utils.IO import *
from Utils.Path import *

class Unuse:

    def __init__(self, modulePathVar, moduleFilePath, modulesLoadedVar, shell):

        # Remove all modules in this path
        modulesLoaded = getPathVar(modulesLoadedVar)
        for mod in modulesLoaded:
            head, tail = os.path.split(mod)
            if head in moduleFilePath:
                removePath(modulesLoadedVar, mod)

        outputString = shell.setEnvVar(modulesLoadedVar, os.environ[modulesLoadedVar])
        print(outputString)

        # Remove the module path
        removePath(modulePathVar, moduleFilePath)
        outputString = shell.setEnvVar(modulePathVar, os.environ[modulePathVar])
        print(outputString)
