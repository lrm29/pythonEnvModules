from Utils.IO import *
from Shell.Shell import *
from Utils.Path import *

import Parser
from Actions import Conflict

import os
import shlex

class Unload:

    def __init__(self, shell, variableData, moduleFile):

        modulesLoaded, modulePaths = getEnvModLoadedAndPaths()

        fullModulePath = fileFoundInPath(moduleFile, modulePaths)

        parser = Parser.Parser(shell, variableData, fullModulePath, "Unload")

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
            outputString = shell.unsetEnvVar(env)
            printOut(outputString)

        for env in variableData.setAliasVars:
            outputString = shell.unsetAliasVar(env)
            printOut(outputString)

        for env in variableData.setPathValues:
            removePath(variableData.setPathValues[env], env)

        for env in variableData.setPathVars:
            printOut(shell.setPathVar(env, os.environ[env]))

        for mod in variableData.setModules:
            removePath("ENV_MODULES_LOADED", mod)
            printOut(shell.setEnvVar("ENV_MODULES_LOADED", os.environ["ENV_MODULES_LOADED"]))

