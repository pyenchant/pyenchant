

import wx

from enchant.checker import SpellChecker
from enchant.checker.wxSpellCheckerDialog import wxSpellCheckerDialog

# Retrieve the text to be checked
text = "this is some smple text with a few erors in it"
print "[INITIAL TEXT:]", text

# Need to have an App before any windows will be shown
app = wx.PySimpleApp()

# Construct the dialog, and the SpellChecker it is to use
dlg = wxSpellCheckerDialog(None)
chkr = SpellChecker("en_US",text)
dlg.SetSpellChecker(chkr)

# Display the dialog, allowing user interaction
if dlg.ShowModal() == wx.ID_OK:
    # Checking completed successfully
    # Retrieve the modified text
    print "[FINAL TEXT:]", chkr.get_text()
else:
    # Checking was cancelled
    print "[CHECKING CANCELLED]"
    


