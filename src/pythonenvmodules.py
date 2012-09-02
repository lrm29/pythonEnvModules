import os
import platform
import sys
import argparse

import Utils.IO
from Utils.Path import getPathVar
from Shell.Shell import getShell
import Parser
import Actions

def printHelp():
    pout = Utils.IO.printErr
    pout("(Python) Environment Modules")
    pout("Version 0.1")
    pout("http://github.com/lrm29/pythonEnvModules")

def main(args):
    try:
        parser = argparse.ArgumentParser(description="Load environment to terminal")
        parser.add_argument("--shell", dest="shellType", help="Specify the shell type")
        parser.add_argument("actionType", nargs=1, help="Action to perform")
        parser.add_argument("moduleFile", nargs='?', default='', help="Module file to read in")
        parser.add_argument("moduleFileSwap", nargs='?', default='', help="Module file to swap with")
        args = parser.parse_args()

        shell = getShell(args.shellType)
        action = args.actionType[0]

        # Print help message
        if action.startswith("h"):
            printHelp()
            return 0

        # Process actions
        if action.startswith("li"):
            actionList = Actions.List()

        elif action.startswith("av"):
            actionAvailable = Actions.Available()

        elif action.startswith("wh"):
            specificModuleFile = args.moduleFile
            actionAvailable = Actions.WhatIs(specificModuleFile)

        elif action.startswith("sh"):
            moduleFile = args.moduleFile
            variableData = Parser.VariableData()
            actionShow = Actions.Show(shell, variableData, moduleFile)

        elif action.startswith("use"):
            pathToUse = args.moduleFile
            actionUse = Actions.Use("ENV_MODULES_PATH", pathToUse, shell)

        elif action.startswith("unuse"):
            pathToUnUse = args.moduleFile
            actionUnuse = Actions.Unuse("ENV_MODULES_PATH", pathToUnUse, "ENV_MODULES_LOADED", shell)

        elif action.startswith("load"):
            moduleFile = args.moduleFile
            variableData = Parser.VariableData()
            actionLoad = Actions.Load(shell, variableData, moduleFile)

        elif action.startswith("unload"):
            moduleFile = args.moduleFile
            variableData = Parser.VariableData()
            actionUnload = Actions.Unload(shell, variableData, moduleFile)

        elif action.startswith("sw"):
            moduleFileToUnload = args.moduleFile
            variableData = Parser.VariableData()
            actionUnload = Actions.Unload(shell, variableData, moduleFileToUnload)

            moduleFileToLoad = args.moduleFileSwap
            variableData = Parser.VariableData()
            actionLoad = Actions.Load(shell, variableData, moduleFileToLoad)

        elif action.startswith("re"):
            moduleFileToUnload = args.moduleFile
            variableData = Parser.VariableData()
            actionUnload = Actions.Unload(shell, variableData, moduleFileToUnload)

            moduleFileToLoad = args.moduleFile
            variableData = Parser.VariableData()
            actionLoad = Actions.Load(shell, variableData, moduleFileToLoad)

        else:
            Utils.IO.printErr("Unknown action " + action)
            return 1

    except:
        return 1  # exit on error
    else:
        return 0  # exit errorlessly


if __name__ == '__main__':
    sys.exit(main(sys.argv))

