import re
import os
import shlex

from Utils.IO import *
from Utils.Path import *

import Actions

class Parser:

    def __init__(self, shell, variableData, moduleFile, loadOrUnload):
        self.shell = shell
        self.variableData = variableData

        self.fileName = os.path.split(moduleFile)[1]

        self.loadOrUnload = loadOrUnload

        self.fileNameRegex = re.compile('\$\(filename\)')
        self.localRegex = re.compile('\$\(([A-Za-z_]*)\)')
        self.envRegex = re.compile('\$env\(([A-Za-z_]*)\)')

    def replaceEnvVar(self, value):
        if self.fileNameRegex.search(value):
            for i in self.fileNameRegex.findall(value):
                replacement = self.fileName
                value = value.replace("$(filename)", replacement)

        if self.localRegex.search(value):
            for i in self.localRegex.findall(value):
                if i in self.variableData.setLocalVars:
                    replacement = self.variableData.setLocalVars[i]
                value = value.replace("$(" + i + ")", replacement)

        if self.envRegex.search(value):
            for i in self.envRegex.findall(value):
                if i in self.variableData.setEnvVars:
                    replacement = self.variableData.setEnvVars[i]
                elif i in os.environ:
                    replacement = os.environ[i]
                else:
                    replacement = ""
                value = value.replace("$env(" + i + ")", replacement)
        return value

    def getNameAndValue(self, tokens):
        name = tokens[1]
        value = self.replaceEnvVar(tokens[2])
        return name, value

    def parseLine(self, tokens):
        if not tokens:
            return
        if tokens[0] == "set":
            name, value = self.getNameAndValue(tokens)
            self.variableData.setLocalVars[name] = value
        if tokens[0] == "setenv":
            name, value = self.getNameAndValue(tokens)
            self.variableData.setEnvVars[name] = value
        if tokens[0] == "unsetenv":
            self.variableData.setEnvVars[tokens[1]] = ""
        elif tokens[0] == "set-alias":
            name, value = self.getNameAndValue(tokens)
            self.variableData.setAliasVars[name] = value
        elif tokens[0] == "prepend-path":
            name, value = self.getNameAndValue(tokens)
            prependPath(name, value, self.shell)
            self.variableData.setPathVars.add(name)
            self.variableData.setPathValues[value] = name
        elif tokens[0] == "append-path":
            name, value = self.getNameAndValue(tokens)
            appendPath(name, value, self.shell)
            self.variableData.setPathVars.add(name)
            self.variableData.setPathValues[value] = name
        elif tokens[0] == "module" and tokens[1] == "load":
            if "Unload" in self.loadOrUnload:
                actionLoad = Actions.Unload(self.shell, self.variableData, tokens[2])
            elif "Load" in self.loadOrUnload:
                actionLoad = Actions.Load(self.shell, self.variableData, tokens[2])
        else:
            return


    def parse(self, line):
        self.parseLine(shlex.split(line, True))


    def parseCodeFragments(self, codeFragment):
        cleanedSnippet = self.replaceEnvVar(codeFragment.strip("\n"))
        cleanedSnippet = cleanedSnippet.replace("parse", "self.parse")
        #printErr(cleanedSnippet)
        test = compile(cleanedSnippet, '<string>', 'exec')
        exec(test)
        #printErr("COMPILED")
