# pyenchant
#
# Copyright (C) 2004-2008, Ryan Kelly
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
#
# In addition, as a special exception, you are
# given permission to link the code of this program with
# non-LGPL Spelling Provider libraries (eg: a MSFT Office
# spell checker backend) and distribute linked combinations including
# the two.  You must obey the GNU Lesser General Public License in all
# respects for all of the code used other than said providers.  If you modify
# this file, you may extend this exception to your version of the
# file, but you are not obligated to do so.  If you do not wish to
# do so, delete this exception statement from your version.
#
"""

    enchant.checker.CmdLineChecker:  Command-Line spell checker

    This module provides the class CmdLineChecker, which interactively
    spellchecks a piece of text by interacting with the user on the
    command line.  It can also be run as a script to spellcheck a file.

"""

import sys

from enchant.checker import SpellChecker
from enchant.utils import printf

# Helpers

colors = {
    'normal'         : "\x1b[0m",
    'black'          : "\x1b[30m",
    'red'            : "\x1b[31m",
    'green'          : "\x1b[32m",
    'yellow'         : "\x1b[33m",
    'blue'           : "\x1b[34m",
    'purple'         : "\x1b[35m",
    'cyan'           : "\x1b[36m",
    'grey'           : "\x1b[90m",
    'gray'           : "\x1b[90m",
    'bold'           : "\x1b[1m"
}

def color(string, color='normal', prefix=''):
    """
    Change text color for the Linux terminal.

    Args:
        string (str): String to colorify
        color (str): Color to colorify the string in the following list:
            black, red, green, yellow, blue, purple, cyan, gr[ae]y
        prefix (str): Prefix to add to string (ex: Beginning of line graphics)
    """
    return colors[color] + prefix + string + colors['normal']

def success(string):
    return "[" + color("+", color='green') + "] " + string

def error(string):
    return "[" + color("!", color='red') + "] " + string

def warning(string):
    return "[" + color("*", color='yellow') + "] " + string

def info(string):
    return "[" + color(".", color='blue') + "] " + string

class CmdLineChecker:
    """A simple command-line spell checker.

    This class implements a simple command-line spell checker.  It must
    be given a SpellChecker instance to operate on, and interacts with
    the user by printing instructions on stdout and reading commands from
    stdin.
    """
    _DOC_ERRORS = ["stdout","stdin"]

    def __init__(self):
        self._stop = False
        self._checker = None

    def set_checker(self,chkr):
        self._checker = chkr

    def get_checker(self,chkr):
        return self._checker

    def run(self):
        """Run the spellchecking loop."""
        self._stop = False
        for err in self._checker:
            self.error = err
            printf(["ERROR:", err.word.encode('utf8')])
            printf(["HOW ABOUT:", err.suggest()])
            status = self.read_command()
            while not status and not self._stop:
                status = self.read_command()
            if self._stop:
                break
        printf(["DONE"])

    def print_help(self):
        printf([color("0", color='yellow') + ".." + color("N", color='yellow') + ":\t" + color("replace", color='bold') + " with the numbered suggestion"])
        printf([color("R", color='cyan') + color("0", color='yellow') + ".." + color("R", color='cyan') + color("N", color='yellow') + ":\t" + color("always replace", color='bold') + " with the numbered suggestion"])
        printf([color("i", color='cyan') + ":\t" + color("ignore", color='bold') + " this word"])
        printf([color("I", color='cyan') + ":\t" + color("always ignore", color='bold') + " this word"])
        printf([color("a", color='cyan') + ":\t" + color("add", color='bold') + " word to personal dictionary"])
        printf([color("e", color='cyan') + ":\t" + color("edit", color='bold') + " the word"])
        printf([color("q", color='cyan') + ":\t" + color("quit", color='bold') + " checking"])
        printf([color("h", color='cyan') + ":\tprint this " + color("help", color='bold') + " message"])
        printf(["----------------------------------------------------"])
        printf(["HOW ABOUT:", self.error.suggest()])

    def read_command(self):
        try:
            cmd = raw_input(">> ") # Python 2.x
        except NameError:
            cmd = input(">> ") # Python 3.x
        cmd = cmd.strip()

        if cmd.isdigit():
            repl = int(cmd)
            suggs = self.error.suggest()
            if repl >= len(suggs):
                printf(["No suggestion number", repl])
                return False
            printf(["Replacing '%s' with '%s'" % (self.error.word,suggs[repl])])
            self.error.replace(suggs[repl])
            return True

        if cmd[0] == "R":
            if not cmd[1:].isdigit():
                printf(["Badly formatted command (try 'help')"])
                return False
            repl = int(cmd[1:])
            suggs = self.error.suggest()
            if repl >= len(suggs):
                printf(["No suggestion number", repl])
                return False
            self.error.replace_always(suggs[repl])
            return True

        if cmd == "i":
            return True

        if cmd == "I":
            self.error.ignore_always()
            return True

        if cmd == "a":
            self.error.add()
            return True

        if cmd == "e":
            repl = raw_input("New Word: ")
            self.error.replace(repl.strip())
            return True

        if cmd == "q":
            self._stop = True
            return True

        if "help".startswith(cmd.lower()):
            self.print_help()
            return False

        printf(["Badly formatted command (try 'help')"])
        return False

    def run_on_file(self,infile,outfile=None,enc=None):
        """Run spellchecking on the named file.
        This method can be used to run the spellchecker over the named file.
        If <outfile> is not given, the corrected contents replace the contents
        of <infile>.  If <outfile> is given, the corrected contents will be
        written to that file.  Use "-" to have the contents written to stdout.
        If <enc> is given, it specifies the encoding used to read the
        file's contents into a unicode string.  The output will be written
        in the same encoding.
        """
        inStr = "".join(file(infile,"r").readlines())
        if enc is not None:
            inStr = inStr.decode(enc)
        self._checker.set_text(inStr)
        self.run()
        outStr = self._checker.get_text()
        if enc is not None:
            outStr = outStr.encode(enc)
        if outfile is None:
            outF = file(infile,"w")
        elif outfile == "-":
            outF = sys.stdout
        else:
            outF = file(outfile,"w")
        outF.write(outStr)
        outF.close()
    run_on_file._DOC_ERRORS = ["outfile","infile","outfile","stdout"]

def _run_as_script():
    """Run the command-line spellchecker as a script.
    This function allows the spellchecker to be invoked from the command-line
    to check spelling in a file.
    """
    # Check necessary command-line options
    from optparse import OptionParser
    op = OptionParser()
    op.add_option("-o","--output",dest="outfile",metavar="FILE",
                      help="write changes into FILE")
    op.add_option("-l","--lang",dest="lang",metavar="TAG",default="en_US",
                      help="use language idenfified by TAG")
    op.add_option("-e","--encoding",dest="enc",metavar="ENC",
                      help="file is unicode with encoding ENC")
    (opts,args) = op.parse_args()
    # Sanity check
    if len(args) < 1:
        raise ValueError("Must name a file to check")
    if len(args) > 1:
        raise ValueError("Can only check a single file")
    # Create and run the checker
    chkr = SpellChecker(opts.lang)
    cmdln = CmdLineChecker()
    cmdln.set_checker(chkr)
    cmdln.run_on_file(args[0],opts.outfile,opts.enc)



if __name__ == "__main__":
    _run_as_script()
