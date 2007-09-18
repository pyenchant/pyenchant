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
    which to operate.
"""

import wx

class wxSpellCheckerDialog(wx.Dialog):
    sz = (300,70)
    def __init__(self, parent=None):
        wx.Dialog.__init__(self, parent, -1, "Checking Spelling...", style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self._numContext = 40
        self._checker = None
        self._buttonsEnabled = True
        self.error_text = wx.TextCtrl(self, -1, "", size=wxSpellCheckerDialog.sz, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)
        self.replace_text = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER)
        self.replace_list = wx.ListBox(self, -1, style=wx.LB_SINGLE)
        self.InitLayout()
        wx.EVT_LISTBOX(self,self.replace_list.GetId(),self.OnReplSelect)
        wx.EVT_LISTBOX_DCLICK(self,self.replace_list.GetId(),self.OnReplace)

    def InitLayout(self):
        """Lay out controls and add buttons."""
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        txtSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer = wx.BoxSizer(wx.VERTICAL)
        replaceSizer = wx.BoxSizer(wx.HORIZONTAL)
        txtSizer.Add(wx.StaticText(self, -1, "Unrecognised Word:"), 0, wx.LEFT|wx.TOP, 5)
        txtSizer.Add(self.error_text, 1, wx.ALL|wx.EXPAND, 5)
        replaceSizer.Add(wx.StaticText(self, -1, "Replace with:"), 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        replaceSizer.Add(self.replace_text, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        txtSizer.Add(replaceSizer, 0, wx.EXPAND, 0)
        txtSizer.Add(self.replace_list, 2, wx.ALL|wx.EXPAND, 5)
        sizer.Add(txtSizer, 1, wx.EXPAND, 0)
        self.buttons = []
        for label, action, tip in (\
            ("Ignore", self.OnIgnore, "Ignore this word and continue"),
            ("Ignore All", self.OnIgnoreAll, "Ignore all instances of this word and continue"),
            ("Replace", self.OnReplace, "Replace this word"),
            ("Replace All", self.OnReplaceAll, "Replace all instances of this word"),
            ("Add", self.OnAdd, "Add this word to the dictionary"),
            ("Done", self.OnDone, "Finish spell-checking and accept changes"),
            ):
            btn = wx.Button(self, -1, label)
            btn.SetToolTip(wx.ToolTip(tip))
            btnSizer.Add(btn, 0, wx.ALIGN_RIGHT|wx.ALL, 4)
            btn.Bind(wx.EVT_BUTTON, action)
            self.buttons.append(btn)
        sizer.Add(btnSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.SetAutoLayout(True)
        self.SetSizer(sizer)
        sizer.Fit(self)

    def Advance(self):
        """Advance to the next error.
        This method advances the SpellChecker to the next error, if
        any.  It then displays the error and some surrounding context,
        and well as listing the suggested replacements.
        """
        # Disable interaction if no checker
        if self._checker is None:
            self.EnableButtons(False)
            return False
        # Advance to next error, disable if not available
        try:
            self._checker.next()
        except StopIteration:
            self.EnableButtons(False)
            self.error_text.SetValue("")
            self.replace_list.Clear()
            self.replace_text.SetValue("")
            if self.IsModal(): # test needed for SetSpellChecker call
                # auto-exit when checking complete
                self.EndModal(wx.ID_OK)
            return False
        self.EnableButtons()
        # Display error context with erroneous word in red
        # Restoring default style was misbehaving under windows, so
        # I am forcing the rest of the text to be black
        self.error_text.SetValue("")
        self.error_text.SetDefaultStyle(wx.TextAttr(wx.BLACK))
        lContext = self._checker.leading_context(self._numContext)
        self.error_text.AppendText(lContext)
        self.error_text.SetDefaultStyle(wx.TextAttr(wx.RED))
        self.error_text.AppendText(self._checker.word)
        self.error_text.SetDefaultStyle(wx.TextAttr(wx.BLACK))
        tContext = self._checker.trailing_context(self._numContext)
        self.error_text.AppendText(tContext)
        # Display suggestions in the replacements list
        suggs = self._checker.suggest()
        self.replace_list.Set(suggs)
        self.replace_text.SetValue(suggs and suggs[0] or '')
        return True

    def EnableButtons(self, state=True):
        """Enable the checking-related buttons"""
        if state != self._buttonsEnabled:
            for btn in self.buttons[:-1]:
                btn.Enable(state)
            self._buttonsEnabled = state

    def GetRepl(self):
        """Get the chosen replacement string."""
        repl = self.replace_text.GetValue()
        # Coercion now done automatically in SpellChecker class
        #repl = self._checker.coerce_string(repl)
        return repl

    def OnAdd(self, evt):
        """Callback for the "add" button."""
        self._checker.add_to_pwl()

    def OnDone(self, evt):
        """Callback for the "close" button."""
        wxSpellCheckerDialog.sz = self.error_text.GetSizeTuple()
        self.EndModal(wx.ID_OK)

    def OnIgnore(self, evt):
        """Callback for the "ignore" button.
        This simply advances to the next error.
        """
        self.Advance()

    def OnIgnoreAll(self, evt):
        """Callback for the "ignore all" button."""
        self._checker.ignore_always()
        self.Advance()

    def OnReplace(self, evt):
        """Callback for the "replace" button."""
        repl = self.GetRepl()
        if repl:
            self._checker.replace(repl)
        self.Advance()

    def OnReplaceAll(self, evt):
        """Callback for the "replace all" button."""
        repl = self.GetRepl()
        self._checker.replace_always(repl)
        self.Advance()

    def OnReplSelect(self, evt):
        """Callback when a new replacement option is selected."""
        sel = self.replace_list.GetSelection()
        if sel == -1:
            return
        opt = self.replace_list.GetString(sel)
        self.replace_text.SetValue(opt)

    def SetSpellChecker(self,chkr):
        """Set the spell checker, advancing to the first error.
        Return True if error(s) to correct, else False."""
        self._checker = chkr
        return self.Advance()
