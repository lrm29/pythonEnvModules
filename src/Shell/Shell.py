import os
from Utils.IO import *

class Shell:
    def setKeyWord(self):
        return "NA"

    def setAliasWord(self):
        return "NA"

    def setKeyWordDelim(self):
        return "NA"

    def setEnvVar(self, var, value):
        return "NA"

    def setAliasVar(self, var, value):
        return "NA"

    def setPathVar(self, var, value):
        return "NA"


class BashShell(Shell):
    def setKeyWord(self):
        return "export"

    def unsetKeyWord(self):
        return "unset"

    def setAliasWord(self):
        return "alias"

    def unsetAliasWord(self):
        return "unalias"

    def setKeyWordDelim(self):
        return "="

    def pathDelim(self):
        return ":"

    def setEnvVar(self, var, value):
        return self.setKeyWord() + " " + var + self.setKeyWordDelim() + "\"" + value + "\"" + ";\n"

    def unsetEnvVar(self, var):
        return self.unsetKeyWord() + " " + var + ";\n"

    def setAliasVar(self, var, value):
        return self.setAliasWord() + " " + var + self.setKeyWordDelim() + "\"" + value + "\";\n"

    def unsetAliasVar(self, var):
        return self.unsetAliasWord() + " " + var + ";\n"

    def setPathVar(self, var, value):
        return self.setEnvVar(var, value)


class FishShell(Shell):
    def setKeyWord(self):
        return "set -gx"

    def unsetKeyWord(self):
        return "set -e"

    def setAliasWord(self):
        return "function"

    def unsetAliasWord(self):
        return "functions -e"

    def setKeyWordDelim(self):
        return " "

    def pathDelim(self):
        return " "

    def setEnvVar(self, var, value):
        return self.setKeyWord() + " " + var + self.setKeyWordDelim() + "\"" + value + "\"" + ";\n"

    def unsetEnvVar(self, var):
        return self.unsetKeyWord() + " " + var + ";\n"

    def setAliasVar(self, var, value):
        return self.setAliasWord() + " " + var + ";" + value + "; end" + ";\n"

    def unsetAliasVar(self, var):
        return self.unsetAliasWord() + " " + var + ";\n"

    def setPathVar(self, var, value):
        newValues = ""
        values = value.split(os.pathsep)
        for i in values:
            if os.path.exists(i):
                newValues += i + " "

        return self.setKeyWord() + " " + var + " " + newValues + ";\n"


class CShell(Shell):
    def setKeyWord(self):
        return "setenv"

    def setKeyWordDelim(self):
        return " "

    def setEnvVar(self, var, value):
        return self.setKeyWord() + " " + var + self.setKeyWordDelim() + value + "\n"


shellTypes = {
    'bash'  : BashShell,
    'sh'    : BashShell,
    'csh'   : CShell,
    'fish'  : FishShell
}


def getShell(shellName):
    # Get the shell type
    try:
        shell = shellTypes[shellName]()
    except:
        printErr(
            "Error : " + shellName
          + " is not supported as a shell by this program"
        )

    return shell

