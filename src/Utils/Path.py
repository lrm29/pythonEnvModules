import os
from Shell.Shell import *
from Utils.IO import *
import sys

def getPathVar(pathVarName):
    if pathVarName in os.environ:
        return os.environ[pathVarName].strip(os.pathsep).split(os.pathsep)
    else:
        return ""

def getEnvModLoadedAndPaths():
    # modulesLoaded contains the full path of all the modules currently
    # loaded into the environment
    modulesLoaded = getPathVar("ENV_MODULES_LOADED")
    # modulesPaths contains the paths that will be searched through to
    # find modules
    modulePaths = getPathVar("ENV_MODULES_PATH")

    if not modulePaths:
        printErr("ENV_MODULES_PATH is empty!")
        sys.exit(1)

    return modulesLoaded, modulePaths

def appendPath(pathVar, path, shell):
    if not pathVar in os.environ:
        os.environ[pathVar] = path
    else:
        if not path in os.environ[pathVar]:
            os.environ[pathVar] = os.environ[pathVar].strip(os.pathsep) + os.pathsep + path

def prependPath(pathVar, path, shell):
    if not pathVar in os.environ:
        os.environ[pathVar] = path.rstrip("/")
    else:
        alreadyUsed = False
        for pathI in os.environ[pathVar].split(os.pathsep):
            if path == pathI:
                alreadyUsed = True
        if not alreadyUsed:
            os.environ[pathVar] = path.rstrip("/") + os.pathsep + os.environ[pathVar].strip(os.pathsep)

def removePath(pathVar, pathName):
    path = getPathVar(pathVar)
    os.environ[pathVar] = ""
    for pathI in path:
        if pathI != pathName.rstrip("/"):
            os.environ[pathVar] = os.environ[pathVar].strip(os.pathsep) + os.pathsep + pathI
    os.environ[pathVar] = os.environ[pathVar].strip(os.pathsep)

def fileFoundInPath(moduleFile, modulesPath):
    # Check if the module given exists in a module path
    for mod in modulesPath:
        head, tail = os.path.split(mod.rstrip("/"))
        path = os.path.join(head, moduleFile)
        if os.path.isfile(path):
            return path

    # Check for a .version file in a path consisting of:
    # modulePath + moduleFile + "contents of .default"
    for mod in modulesPath:
        head, tail = os.path.split(mod.rstrip("/"))
        path = os.path.join(head, moduleFile)
        defaultFile = path + os.sep + ".default"
        #printErr(defaultFile)
        if os.path.isfile(defaultFile):
            contentsOfDefault = open(defaultFile).read().strip("\n")
            #printErr(path + os.sep + contentsOfDefault)
            return path + os.sep + contentsOfDefault

    printErr("Module " + moduleFile + " is not in " + path)

    return ""

