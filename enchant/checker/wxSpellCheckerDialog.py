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
#
# Portions of this code were automatically generated using wxGlade:
#
#         http://wxglade.sourceforge.net/
#
"""

    enchant.checker.wxSpellCheckerDialog: wxPython spellchecker interface
    
    This module provides the class wxSpellCheckerDialog, which provides
    a wxPython dialog that can be used as an interface to a spell checking
    session.  Currently it is intended as a proof-of-concept and demonstration
    class, but it should be suitable for general-purpose use in a program.
    
    The class must be given an enchant.checker.SpellChecker object with
    which to operate.  It can (in theory...) be used in modal and non-modal
    modes.  Use Show() when operating on an array of characters as it will
    modify the array in place, meaning other work can be done at the same
    time.  Use ShowModal() when operating on a static string.

"""

import wx

class wxSpellCheckerDialog(wx.Dialog):
    """Simple spellcheck dialog for wxPython
    
    This class implements a simple spellcheck interface for wxPython,
    in the form of a dialog.  It's intended mainly of an example of
    how to do this, although it should be useful for applications that
    just need a simple graphical spellchecker.
    
    The GUI code was created using wxGlade and the spellchecking related
    code lives in the following methods:
        
        * __do_init
        * The event callbacks _On<Something>
        * SetSpellChecker/GetSpellChecker
        * _Advance
    
    To use, a SpellChecker instance must be created and passed to the
    dialog before it is shown:
        
        >>> dlg = wxSpellCheckerDialog(None,-1,"")
        >>> chkr = SpellChecker("en_AU",text)
        >>> dlg.SetSpellChecker(chkr)
        >>> dlg.Show()
    
    This is most useful when the text to be checked is in the form of
    a character array, as it will be modified in place as the user
    interacts with the dialog.  For checking strings, the final result
    will need to be obtained from the SpellChecker object:
        
        >>> dlg = wxSpellCheckerDialog(None,-1,"")
        >>> chkr = SpellChecker("en_AU",text)
        >>> dlg.SetSpellChecker(chkr)
        >>> dlg.ShowModal()
        >>> text = dlg.GetSpellChecker().get_text()
    
    Currently the checker must deal with strings of the same type as
    returned by wxPython - unicode or normal string depending on the
    underlying syste.  This needs to be fixed, somehow...
    
    """
    
    def __init__(self, *args, **kwds):
        # begin wxGlade: wxSpellCheckerDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.error_label = wx.StaticText(self, -1, "Unrecognised Word:")
        self.error_text = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)
        self.replace_label = wx.StaticText(self, -1, "Replace with:")
        self.replace_text = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER)
        self.replace_list = wx.ListBox(self, -1, choices=["Option 1", "Option 2", "Option 3"], style=wx.LB_SINGLE)
        self.btn_ignore = wx.Button(self, -1, "Ignore")
        self.btn_ignoreall = wx.Button(self, -1, "Ignore All")
        self.btn_replace = wx.Button(self, -1, "Replace")
        self.btn_replaceall = wx.Button(self, -1, "Replace All")
        self.btn_add = wx.Button(self, -1, "Add")
        self.btn_close = wx.Button(self, -1, "Close")

        self.__set_properties()
        self.__do_layout()
        
        self.__do_init()
        self.__do_events()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: wxSpellCheckerDialog.__set_properties
        self.SetTitle("Checking Spelling...")
        self.replace_list.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: wxSpellCheckerDialog.__do_layout
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_7_copy_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7_copy_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2_copy = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.error_label, 0, wx.LEFT|wx.TOP, 5)
        sizer_1.Add(self.error_text, 1, wx.ALL|wx.EXPAND, 5)
        sizer_2_copy.Add(self.replace_label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2_copy.Add(self.replace_text, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(sizer_2_copy, 0, wx.EXPAND, 0)
        sizer_1.Add(self.replace_list, 2, wx.ALL|wx.EXPAND, 5)
        sizer_5.Add(sizer_1, 1, wx.EXPAND, 0)
        sizer_7.Add(self.btn_ignore, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_7_copy.Add(self.btn_ignoreall, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(sizer_7_copy, 1, wx.EXPAND, 0)
        sizer_7_copy_1.Add(self.btn_replace, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(sizer_7_copy_1, 1, wx.EXPAND, 0)
        sizer_7_copy_2.Add(self.btn_replaceall, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(sizer_7_copy_2, 1, wx.EXPAND, 0)
        sizer_7_copy_3.Add(self.btn_add, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(sizer_7_copy_3, 1, wx.EXPAND, 0)
        sizer_7_copy_4.Add(self.btn_close, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_6.Add(sizer_7_copy_4, 1, wx.EXPAND, 0)
        sizer_5.Add(sizer_6, 0, wx.ALL|wx.EXPAND, 5)
        self.SetAutoLayout(True)
        self.SetSizer(sizer_5)
        sizer_5.Fit(self)
        sizer_5.SetSizeHints(self)
        self.Layout()
        # end wxGlade
    
    def __do_init(self):
        """Initialise internal state for the dialog.
        Initially, no checker is available and buttons are disabled.
        """
        self._numContext = 40
        self._checker = None
        self._buttonsEnabled = True
        self._DisableButtons()
        # Remove placeholder options from replace_list
        self.replace_list.Clear()
        
    def __do_events(self):
        """Connect events for the dialog."""
        wx.EVT_BUTTON(self,self.btn_ignore.GetId(),self._OnIgnore)
        wx.EVT_BUTTON(self,self.btn_ignoreall.GetId(),self._OnIgnoreAll)
        wx.EVT_BUTTON(self,self.btn_replace.GetId(),self._OnReplace)
        wx.EVT_BUTTON(self,self.btn_replaceall.GetId(),self._OnReplaceAll)
        wx.EVT_BUTTON(self,self.btn_add.GetId(),self._OnAdd)
        wx.EVT_BUTTON(self,self.btn_close.GetId(),self._OnClose)
        wx.EVT_LISTBOX(self,self.replace_list.GetId(),self._OnReplSelect)
        wx.EVT_LISTBOX_DCLICK(self,self.replace_list.GetId(),self._OnReplace)
        
    def SetSpellChecker(self,chkr):
        """Set the spell checker, advancing to the first error."""
        self._checker = chkr
        self._Advance()
        
    def GetSpellChecker(self,chkr):
        """Get the currently in-use SpellChecker object."""
        return self._checker
    
    def _OnIgnore(self,evnt=None):
        """Callback for the "ignore" button.
        This simply advances to the next error.
        """
        self._Advance()
        
    def _OnIgnoreAll(self,evnt=None):
        """Callback for the "ignore all" button."""
        self._checker.ignore_always()
        self._Advance()
        
    def _OnReplace(self,evnt=None):
        """Callback for the "replace" button."""
        repl = self.replace_text.GetValue()
        self._checker.replace(repl)
        self._Advance()
        
    def _OnReplaceAll(self,evnt=None):
        """Callback for the "replace all" button."""
        repl = self.replace_text.GetValue()
        self._checker.replace_always(repl)
        self._Advance()
    
    def _OnClose(self,evnt=None):
        """Callback for the "close" button."""
        self.Close()
    
    def _OnAdd(self,evnt=None):
        """Callback for the "add" button."""
        self._checker.add_to_personal()
    
    def _OnReplSelect(self,evnt=None):
        """Callback when a new replacement option is selected."""
        sel = self.replace_list.GetSelection()
        if sel == -1:
            return
        opt = self.replace_list.GetString(sel)
        self.replace_text.SetValue(opt)

    def _Advance(self):
        """Advance to the next error.
        This method advances the SpellChecker to the next error, if
        any.  It then displays the error and some surrounding context,
        and well as listing the suggested replacements.
        """
        # Disable interaction if no checker
        if self._checker is None:
            self._DisableButtons()
            return
        # Advance to next error, disable if not available
        try:
            self._checker.next()
        except StopIteration:
            self._DisableButtons()
            self.error_text.SetValue("")
            self.replace_list.Clear()
            self.replace_text.SetValue("")
            return
        self._EnableButtons()
        # Display error context with erroneous word in red
        self.error_text.SetValue("")
        lContext = self._checker.leading_context(self._numContext)
        self.error_text.AppendText(lContext)
        self.error_text.SetDefaultStyle(wx.TextAttr(wx.RED))
        self.error_text.AppendText(self._checker.word)
        self.error_text.SetDefaultStyle(wx.TextAttr())
        tContext = self._checker.trailing_context(self._numContext)
        self.error_text.AppendText(tContext)
        # Display suggestions in the replacements list
        suggs = self._checker.suggest()
        self.replace_list.Clear()
        for s in suggs:
            self.replace_list.Append(s)
        if len(suggs) > 0:
            self.replace_text.SetValue(suggs[0])
        else:
            self.replace_text.SetValue("")
        
    def _EnableButtons(self):
        """Enable the checking-related buttons"""
        if self._buttonsEnabled:
            return
        self.btn_add.Enable(True)
        self.btn_ignore.Enable(True)
        self.btn_ignoreall.Enable(True)
        self.btn_replace.Enable(True)
        self.btn_replaceall.Enable(True)
        self._buttonsEnabled = True

    def _DisableButtons(self):
        """Disable the checking-related buttons"""    
        if not self._buttonsEnabled:
            return
        self.btn_add.Disable()
        self.btn_ignore.Disable()
        self.btn_ignoreall.Disable()
        self.btn_replace.Disable()
        self.btn_replaceall.Disable()
        self._buttonsEnabled = False
    
        
# end of class wxSpellCheckerDialog

def _test():
    class TestDialog(wxSpellCheckerDialog):
        def __init__(self,*args):
            wxSpellCheckerDialog.__init__(self,*args)
            wx.EVT_CLOSE(self,self.OnClose)
        def OnClose(self,evnt):
            if self._checker is not None:
                print "AFTER:", self._checker.get_text()
            self.Destroy()
    from enchant.checker import SpellChecker
    text = u"This is sme text with a fw speling errors in it. Here are a fw more to tst it ut."
    print "BEFORE:", text
    app = wx.PySimpleApp()
    dlg = TestDialog(None,-1,"")
    chkr = SpellChecker("en_US",text)
    dlg.SetSpellChecker(chkr)
    dlg.Show()
    app.MainLoop()
    
if __name__ == "__main__":
    _test()

