# pyenchant
#
# Copyright (C) 2004-2005, Ryan Kelly
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

    TODO: document the CmdLineChecker module

"""

import sys
from enchant.checker import SpellChecker

class CmdLineChecker:
    """A simple command-line spell checker.
    This class uses the SpellChecker class to implement
    a simple command-line spell checker.  Use its run()
    method to start things off.  This class is *not*
    meant to be used for any serious work, but as an example
    and stress-test for the SpellChecker class.
    """
    def __init__(self):
        self._stop = False
        
    def run(self,args=None):
        """Run the spellchecking loop, with given arguments.
        Currently the only argument is the name of a file to
        check.  For example, the check the contents of the
        file 'test.txt' use:
            
            chkr.run(('test.txt',))
            
        The language is assumed to be US English (for now)    
        """
        if args is None:
            args = sys.argv
        f = file(args[0],"r")
        chkr = SpellChecker("en_US","".join(f.readlines()))
        f.close()
        for err in chkr:
            self.error = err
            print "ERROR:", err.word
            print "HOW ABOUT:", err.suggest()
            status = self.readcommand()
            while not status:
                if status is None:
                    sys.exit(1)
                status = self.readcommand()
        sys.stdout.write(chkr.get_text())
    
    def printhelp(self):
        print "0..N:    replace with the numbered suggestion"
        print "R0..rN:  always replace with the numbered suggestion"
        print "i:       ignore this word"
        print "I:       always ignore this word"
        print "a:       add word to personal dictionary"
        print "e:       edit the word"
        print "s:       stop checking and write out changes"
        print "q:       quit, discarding all changes"
        print "h:       print this help message"
        print "----------------------------------------------------"
        print "HOW ABOUT:", self.error.suggest()
    
    def readcommand(self):
        cmd = raw_input(">>")
        cmd = cmd.strip()
        
        if cmd.isdigit():
            repl = int(cmd)
            suggs = self.error.suggest()
            if repl >= len(suggs):
                print "No suggestion number", repl
                return False
            print "Replacing '%s' with '%s'" % (self.error.word,suggs[repl])
            self.error.replace(suggs[repl])
            return True
        
        if cmd[0] == "R":
            if not cmd[1:].isdigit():
                print "Badly formatted command"
                return False
            repl = int(cmd[1:])
            suggs = self.error.suggest()
            if repl >= len(suggs):
                print "No suggestion number", repl
                return False
            self.error.replace_always(suggs[repl])
            return True
        
        if cmd == "i":
            return True
        
        if cmd == "I":
            self.error.ignore_always()
            return True
            
        if cmd == "a":
            self.error.add_to_personal()
            return True
        
        if cmd == "e":
            repl = raw_input("New Word: ")
            self.error.replace(repl.strip())
            return True
        
        if cmd == "s":
            self._stop = True
            return None
            
        if cmd == "q":
            return None
        
        if "help".startswith(cmd.lower()):
            self.printhelp()
            return False
        
        print "Badly formatted command"
        return False
