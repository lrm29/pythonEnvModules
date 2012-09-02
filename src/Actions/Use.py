import os

from Shell.Shell import *
from Utils.Path import *
from Utils.IO import *

class Use:

    def __init__(self, modulePathVar, moduleFilePath, shell):

        removePath(modulePathVar, moduleFilePath)
        prependPath(modulePathVar, moduleFilePath, shell)
        outputString = shell.setEnvVar(modulePathVar, os.environ[modulePathVar])
        printOut(outputString)
