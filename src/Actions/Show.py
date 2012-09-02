import os
import shlex
from Utils.IO import *
from Utils.Path import *
import Parser

class Show:

    def __init__(self, shell, variableData, moduleFile):

        modulePaths = getPathVar("ENV_MODULES_PATH")

        fullModulePath = fileFoundInPath(moduleFile, modulePaths)

        parser = Parser.Parser(shell, variableData, fullModulePath, "no")

        foundFile = False
        for modPath in modulePaths:
            head, tail = os.path.split(modPath)
            moduleFilePath = os.path.join(head, moduleFile)
            if os.path.isfile(moduleFilePath) and tail in moduleFile:
                foundFile = True
                with open(moduleFilePath) as f:
                    for line in f:
                        if line.strip():
                            tokens = shlex.split(line, True)
                            parser.parseLine(tokens)
                            printErr(parser.replaceEnvVar(line.strip()))

        if not foundFile:
            printErr("Not showing " + moduleFile + ": Could not find file")
