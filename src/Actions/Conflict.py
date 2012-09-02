from Utils.IO import *
from Parser import *
import shlex, os

class Conflict:

    def __init__(self, moduleFile, modulePaths, modulesLoaded, parser):

        self.foundConflict = ""

        self.conflictList = set()

        for mod in modulesLoaded:
            if mod:
                with open(mod) as f:
                    for line in f:
                        tokens = shlex.split(line)
                        if tokens and "conflict" in tokens[0]:
                            self.conflictList.add(parser.replaceEnvVar(tokens[1]))

        for mod in modulesLoaded:

            if mod == moduleFile:
                printErr(mod + " already loaded")
                self.foundConflict = "true"
                return

            if self.conflictList and mod:
                with open(moduleFile) as f:
                    for line in f:
                        tokens = shlex.split(line)
                        if tokens and "conflict" in tokens[0]:
                            for conflictingModules in self.conflictList:
                                if conflictingModules == tokens[1]:
                                    printErr("Cannot load module " + moduleFile)
                                    printErr("Conflict with module " + conflictingModules)
                                    self.foundConflict = "true"
                                    return


