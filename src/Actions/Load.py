from Utils.IO import *
from Utils.Path import *
from Shell.Shell import *

import Parser

from Actions import Conflict

import os
import shlex

class Load:

    def __init__(self, shell, variableData, moduleFile):

        modulesLoaded, modulePaths = getEnvModLoadedAndPaths()

        fullModulePath = fileFoundInPath(moduleFile, modulePaths)

        parser = Parser.Parser(shell, variableData, fullModulePath, "Load")

        actionConflict = Conflict(fullModulePath, modulePaths, modulesLoaded, parser)
        if actionConflict.foundConflict:
            return

        if fullModulePath:
            with open(fullModulePath) as f:
                for line in f:
                    tokens = shlex.split(line, True)
                    if tokens and "$CODE" in tokens[0]:
                        codeString = ""
                        nextLine = f.next()
                        while True:
                            if "$CODE" in nextLine:
                                parser.parseCodeFragments(codeString)
                                break
                            else:
                                codeString += nextLine
                                nextLine = f.next()
                    else:
                        parser.parseLine(tokens)
        else:
            return 1


        variableData.setModules.add(fullModulePath)


        for env in variableData.setEnvVars:
            outputString = shell.setEnvVar(env, variableData.setEnvVars[env])
            printOut(outputString)

        for env in variableData.setAliasVars:
            outputString = shell.setAliasVar(env, variableData.setAliasVars[env])
            printOut(outputString)

        for env in variableData.setPathVars:
            outputString = shell.setPathVar(env, os.environ[env])
            printOut(outputString)

        for mod in variableData.setModules:
            prependPath("ENV_MODULES_LOADED", mod, shell);
            outputString = shell.setEnvVar("ENV_MODULES_LOADED", os.environ["ENV_MODULES_LOADED"])
            printOut(outputString)

