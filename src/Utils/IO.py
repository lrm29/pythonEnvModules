import sys
import os
import string
import re

def printErr(args):
    print >> sys.stderr, args

def printOut(args):
    print >> sys.stdout, args

def printDivider():
    #rows, columns = os.popen('stty size', 'r').read().split()
    columns = 80
    printErr('-'*int(columns))

def centreTextInConsole(text):
    #, columns = os.popen('stty size', 'r').read().split()
    columns = 80
    return printErr(
        string.center(text, int(columns), '-')+ "\n"
    )

def find_between( s, first, last ):
    allFound = re.findall(first + '(.*?)' + last, s, re.DOTALL)
    return allFound

