# -*- coding: utf-8 -*-
#
# GPL License and Copyright Notice ============================================
#  This file is part of Wrye Bash.
#
#  Wrye Bash is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  Wrye Bash is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Wrye Bash; if not, write to the Free Software Foundation,
#  Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2019 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================

"""This module houses GUI classes that did not fit anywhere else. Once similar
classes accumulate in here, feel free to break them out into a module."""

__author__ = 'nycz, Infernio'

import wx as _wx

from ..exception import AbstractError

from .base_components import _AComponent
from .events import EventHandler

class ASplitStatusBar(_AComponent):
    """A status bar split into three sections. The first section supports
    reordering DraggableComponent instances placed in it via drag-n-drop, while
    the other two sections simply display text. The size of the first section
    is determined by the number of components in it and their icon size, the
    size of the third section is fixed, and the second section simply takes up
    all remaining space. Note that this is an abstract class - to use it, you
    will have to implement the abstract methods detailed below."""
    def __init__(self, parent):
        super(ASplitStatusBar, self).__init__()
        # Create native widget
        self._native_widget = _wx.StatusBar(self._resolve(parent))
        self._native_widget.SetFieldsCount(3)
        # Setup the internal state properly
        # The components added to the first section
        self._first_section_components = []
        # The index of the component that is currently being dragged, or
        # _wx.NOT_FOUND if no component is being dragged
        self._dragged_element = _wx.NOT_FOUND
        # The X position at which the current dragging process began
        self._drag_start = 0
        self.moved = False
        self.update_icon_sizes()
        # Events, internal use only
        self._on_resized = EventHandler(self._native_widget, _wx.EVT_SIZE)
        self._on_resized.subscribe(self._refresh_positions)

    # Abstract methods
    def update_icon_sizes(self):
        """Refreshes icons in this status bar to match the current icon_size.
        Must be implemented by any class wishing to extend this class."""
        raise AbstractError()

    def GetLink(self,uid=None,index=None,button=None): raise AbstractError

    @property
    def icon_size(self):
        """Should return the current size, in pixels, of the icons in the first
        section of this status bar. This is both the X and Y size, since the
        icons placed there must always be quadratic.

        :return: The size, in pixels, of the icons in the first section of this
            status bar."""
        raise AbstractError()

    def add_component(self, target_component): # type: (_DraggableComponent) -> None
        self._first_section_components.append(target_component)
        # DnD events (only on windows, CaptureMouse works badly in wxGTK)
        if _wx.Platform == '__WXMSW__':
            target_component.on_drag_started.subscribe(
                self._handle_drag_started)
            target_component.on_drag_stopped.subscribe(
                self._handle_drag_stopped)

    def _find_element_by_id(self, element_id, x_pos):
        for i, fs_element in enumerate(self._first_section_components):
            if fs_element._native_widget.GetId() == element_id:
                delta = x_pos / self.icon_size
                if abs(x_pos) % self.icon_size > self.icon_size:
                    delta += x_pos / abs(x_pos)
                i += delta
                if i < 0: i = 0
                elif i >= len(self._first_section_components):
                    i = len(self._first_section_components) - 1
                return i
        return _wx.NOT_FOUND

    def _handle_drag_started(self, element_id, element_position):
        x_pos = element_position[0]
        self._dragged_element = self._find_element_by_id(element_id, x_pos)
        if self._dragged_element != _wx.NOT_FOUND:
            self._drag_start = x_pos
            button = self._first_section_components[self._dragged_element]
            button._native_widget.CaptureMouse()

    def _handle_drag_stopped(self, element_id, element_position):
        if self._dragged_element != _wx.NOT_FOUND:
            button = self._first_section_components[self._dragged_element] # type: _DraggableComponent
            button.mouse_captured = False
            self._dragged_element = wx.NOT_FOUND
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
            if self.moved:
                self.moved = False
                return
        event.Skip()

    def OnDragEndForced(self, event):
        if self._dragged_element == wx.NOT_FOUND or not self.GetParent().IsActive():
            # The even for clicking the button sends a force capture loss
            # message.  Ignore lost capture messages if we're the active
            # window.  If we're not, that means something else forced the
            # loss of mouse capture.
            self._dragged_element = wx.NOT_FOUND
            self.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))
        event.Skip()

    def OnDrag(self, event):
        if self._dragged_element != wx.NOT_FOUND:
            if abs(event.GetPosition()[0] - self._drag_start) > 4:
                self.SetCursor(wx.StockCursor(wx.CURSOR_HAND))
            over = self._find_element_by_id(event)
            if over >= len(self._first_section_components): over -= 1
            if over not in (wx.NOT_FOUND, self._dragged_element):
                self.moved = True
                button = self._first_section_components[self._dragged_element]
                # update settings
                uid = self.GetLink(button=button).uid
                overUid = self.GetLink(index=over).uid
                _settings['bash.statusbar.order'].remove(uid)
                overIndex = _settings['bash.statusbar.order'].index(overUid)
                _settings['bash.statusbar.order'].insert(overIndex, uid)
                _settings.setChanged('bash.statusbar.order')
                # update self.buttons
                self._first_section_components.remove(button)
                self._first_section_components.insert(over, button)
                self._dragged_element = over
                # Refresh button positions
                self._refresh_positions()
        event.Skip()

    def _refresh_positions(self):
        """Internal callback used to move elements in the first section around
        when doing so is necessary - e.g. when the size of the status bar
        changes or when a dragged element is dropped."""
        rect = self._native_widget.GetFieldRect(0)
        x_pos, y_pos = rect.x + 4, rect.y + 2
        for fs_element in self._first_section_components:
            fs_element.position = (x_pos, y_pos)
            x_pos += self.icon_size

class CheckBox(_AComponent):
    """Represents a simple two-state checkbox.

    Events:
     - on_checked(checked: bool): Posted when this checkbox's state is changed
       by checking or unchecking it. The parameter is True if the checkbox is
       now checked and False if it is now unchecked."""
    def __init__(self, parent, label=u'', tooltip=None, checked=False):
        """Creates a new CheckBox with the specified properties.

        :param parent: The object that this checkbox belongs to. May be a wx
                       object or a component.
        :param label: The text shown on this checkbox.
        :param tooltip: A tooltip to show when the user hovers over this
                        checkbox.
        :param checked: The initial state of the checkbox."""
        super(CheckBox, self).__init__()
        # Create native widget
        self._native_widget = _wx.CheckBox(self._resolve(parent), _wx.ID_ANY,
                                           label=label, name=u'checkBox')
        if tooltip:
            self.tooltip = tooltip
        self.is_checked = checked
        # Events
        self.on_checked = EventHandler(self._native_widget, _wx.EVT_CHECKBOX,
                                       lambda event: [event.IsChecked()])

    @property
    def is_checked(self): # type: () -> bool
        """Returns True if this checkbox is checked.

        :return: True if this checkbox is checked."""
        return self._native_widget.GetValue()

    @is_checked.setter
    def is_checked(self, new_state): # type: (bool) -> None
        """Marks this checkbox as either checked or unchecked, depending on the
        value of new_state.

        :param new_state: True if this checkbox should be checked, False if it
                          should be unchecked."""
        self._native_widget.SetValue(new_state)
