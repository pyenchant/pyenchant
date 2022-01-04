# GtkSpellCheckerDialog for pyenchant
#
# Copyright (C) 2004-2005, Fredrik Corneliusson
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

from typing import Any, Iterable, List, cast

import gi

from enchant.checker import SpellChecker

gi.require_version("Gdk", "3.0")
gi.require_version("Gtk", "3.0")
from gi.repository import Gdk, Gtk

#   columns
COLUMN_SUGGESTION = 0


def create_list_view(col_label: str) -> Gtk.TreeView:
    # create list widget
    list_ = Gtk.ListStore(str)
    list_view = Gtk.TreeView(model=list_)

    list_view.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
    # Add Columns
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(col_label, renderer, text=COLUMN_SUGGESTION)
    list_view.append_column(column)
    return list_view


class GtkSpellCheckerDialog(Gtk.Window):
    def __init__(self, checker: SpellChecker, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.set_title("Spell check")
        self.set_default_size(350, 200)

        self._checker = checker
        self._numContext = 40

        self.errors = None

        # create accel group
        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)

        # list of widgets to disable if there's no spell error left
        self._conditional_widgets = []  # type: List[Gtk.Widget]
        conditional = self._conditional_widgets.append

        # layout
        mainbox = Gtk.VBox(spacing=5)
        hbox = Gtk.HBox(spacing=5)
        self.add(mainbox)
        mainbox.pack_start(hbox, True, True, 5)

        box1 = Gtk.VBox(spacing=5)
        hbox.pack_start(box1, True, True, 5)
        conditional(box1)

        # unrecognized word
        text_view_lable = Gtk.Label(label="Unrecognized word")
        text_view_lable.set_justify(Gtk.Justification.LEFT)
        box1.pack_start(text_view_lable, False, False, 0)

        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        text_view.set_editable(False)
        text_view.set_cursor_visible(False)
        self.error_text = text_view.get_buffer()
        text_buffer = text_view.get_buffer()
        text_buffer.create_tag("fg_black", foreground="black")
        text_buffer.create_tag("fg_red", foreground="red")

        box1.pack_start(text_view, True, True, 0)

        # Change to
        change_to_box = Gtk.HBox()
        box1.pack_start(change_to_box, False, False, 0)

        change_to_label = Gtk.Label(label="Change to:")
        change_to_label.set_justify(Gtk.Justification.LEFT)
        self.replace_text = Gtk.Entry()
        change_to_box.pack_start(change_to_label, False, False, 0)
        change_to_box.pack_start(self.replace_text, True, True, 0)

        # scrolled window
        sw = Gtk.ScrolledWindow()
        sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        box1.pack_start(sw, True, True, 0)

        self.suggestion_list_view = create_list_view("Suggestions")
        self.suggestion_list_view.connect("button_press_event", self._onButtonPress)
        sw.add(self.suggestion_list_view)
        select = self.suggestion_list_view.get_selection()
        select.connect("changed", self._onSuggestionChanged)

        # ---Buttons---#000000#FFFFFF----------------------------------------------------
        button_box = Gtk.VButtonBox()
        hbox.pack_start(button_box, False, False, 5)

        # Ignore
        button = Gtk.Button.new_with_label("Ignore")
        button.connect("clicked", self._onIgnore)
        button_box.pack_start(button, True, True, 0)
        conditional(button)

        # Ignore all
        button = Gtk.Button.new_with_label("Ignore All")
        button.connect("clicked", self._onIgnoreAll)
        button_box.pack_start(button, True, True, 0)
        conditional(button)

        # Replace
        button = Gtk.Button.new_with_label("Replace")
        button.connect("clicked", self._onReplace)
        button_box.pack_start(button, True, True, 0)
        conditional(button)

        # Replace all
        button = Gtk.Button.new_with_label("Replace All")
        button.connect("clicked", self._onReplaceAll)
        button_box.pack_start(button, True, True, 0)
        conditional(button)

        # Recheck button
        button = Gtk.Button.new_with_mnemonic("_Add")
        button.connect("clicked", self._onAdd)

        button_box.pack_start(button, True, True, 0)
        conditional(button)

        # Close button
        button = Gtk.Button.new_from_icon_name("window-close", Gtk.IconSize.BUTTON)
        button.connect("clicked", Gtk.main_quit)
        button_box.pack_end(button, True, True, 0)

        # dictionary label
        self._dict_lable = Gtk.Label(label="Dictionary:%s" % (checker.dict.tag,))
        mainbox.pack_start(self._dict_lable, False, False, 5)

        # keyboard shortcuts
        accel = Gtk.AccelGroup()
        accel.connect(Gdk.KEY_Return, 0, 0, self._onIgnore)
        accel.connect(Gdk.KEY_Escape, 0, 0, Gtk.main_quit)
        self.add_accel_group(accel)

        mainbox.show_all()

    def _onIgnore(self, w: Gtk.Widget, *args: Any) -> None:
        print(["ignore"])
        self._advance()

    def _onIgnoreAll(self, w: Gtk.Widget, *args: Any) -> None:
        print(["ignore all"])
        self._checker.ignore_always()
        self._advance()

    def _onReplace(self, *args: Any) -> None:
        print(["Replace"])
        repl = self._getRepl()
        self._checker.replace(repl)
        self._advance()

    def _onReplaceAll(self, *args: Any) -> None:
        print(["Replace all"])
        repl = self._getRepl()
        self._checker.replace_always(repl)
        self._advance()

    def _onAdd(self, *args: Any) -> None:
        """Callback for the "add" button."""
        self._checker.add()
        self._advance()

    def _onButtonPress(self, widget: Gtk.Widget, event: Gdk.EventButton) -> None:
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            print(["Double click!"])
            self._onReplace()

    def _onSuggestionChanged(self, selection: Gtk.TreeSelection) -> None:
        model, iter = selection.get_selected()
        if iter:
            suggestion = model.get_value(iter, COLUMN_SUGGESTION)
            self.replace_text.set_text(suggestion)

    def _getRepl(self) -> str:
        """Get the chosen replacement string."""
        repl = self.replace_text.get_text()
        repl = self._checker.coerce_string(repl)
        return cast(str, repl)

    def _fillSuggestionList(self, suggestions: Iterable[str]) -> None:
        model = self.suggestion_list_view.get_model()
        model.clear()
        for suggestion in suggestions:
            value = "%s" % (suggestion,)
            model.append([value])

    def updateUI(self) -> None:
        self._advance()

    def _disableButtons(self) -> None:
        for w in self._conditional_widgets:
            w.set_sensitive(False)

    def _enableButtons(self) -> None:
        for w in self._conditional_widgets:
            w.set_sensitive(True)

    def _advance(self) -> None:
        """Advance to the next error.
        This method advances the SpellChecker to the next error, if
        any.  It then displays the error and some surrounding context,
        and well as listing the suggested replacements.
        """
        # Disable interaction if no checker
        if self._checker is None:
            self._disableButtons()
            self.emit("check-done")
            return

        # Advance to next error, disable if not available
        try:
            self._checker.next()
        except StopIteration:
            self._disableButtons()
            self.error_text.set_text("")
            self._fillSuggestionList([])
            self.replace_text.set_text("")
            return
        self._enableButtons()

        # Display error context with erroneous word in red
        self.error_text.set_text("")
        iter = self.error_text.get_iter_at_offset(0)
        append = self.error_text.insert_with_tags_by_name

        lContext = self._checker.leading_context(self._numContext)
        tContext = self._checker.trailing_context(self._numContext)
        append(iter, lContext, "fg_black")
        append(iter, self._checker.word, "fg_red")
        append(iter, tContext, "fg_black")

        # Display suggestions in the replacements list
        suggs = self._checker.suggest()
        self._fillSuggestionList(suggs)
        if suggs:
            self.replace_text.set_text(suggs[0])
        else:
            self.replace_text.set_text("")


def _test() -> None:
    text = "This is sme text with a fw speling errors in it. Here are a fw more to tst it ut."
    print(["BEFORE:", text])
    chkr = SpellChecker("en_US", text)

    chk_dlg = GtkSpellCheckerDialog(chkr)
    chk_dlg.show()
    chk_dlg.connect("delete_event", Gtk.main_quit)

    chk_dlg.updateUI()
    Gtk.main()


if __name__ == "__main__":
    _test()
