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
#  Wrye Bash copyright (C) 2005-2009 Wrye, 2010-2020 Wrye Bash Team
#  https://github.com/wrye-bash
#
# =============================================================================
"""This module houses abstractions over wx.html2.WebView, allowing us to
utilize fully interactive webpages inside a GUI. The main reason this was split
into its own file instead of remaining inside __init__ is the wx.html2 import,
which is quite ugly and should ideally remain as contained as possible."""

__author__ = u'Infernio'

# Try to import html2 webview, may not be available everywhere
try:
    import wx.html2 as _wx_html2
except ImportError:
    _wx_html2 = None
import wx as _wx

import urllib
import urlparse
import webbrowser

from .base_components import _AComponent
from .buttons import BackwardButton, ForwardButton, ReloadButton
from .text_components import TextArea
from .layouts import VLayout
from ..exception import StateError

def web_viewer_available():
    """Checks if WebViewer and its wx backing are available, meaning that we
    can render HTML.

    :return: True if we can render HTML."""
    return bool(_wx_html2)

class WebViewer(_AComponent):
    """Implements an HTML & CSS renderer with JavaScript support. May not be
    available on all platforms (see gui.webview.web_viewer_available()). Also
    creates three navigation buttons for going back and forwards in the
    browsing history and reloading the current page.

    Basic control from the Python side is offered through methods for
    navigating the history, clearing the history, navigating to a URL and
    reloading the current page."""
    _wx_widget_type = _wx_html2.WebView.New # type: _wx_html2.WebView

    def __init__(self, parent, buttons_parent=None):
        """Creates a new WebViewer with the specified parent.

        :param parent: The object that this web viewer belongs to. May be a wx
                       object or a component.
        :param buttons_parent: The object that the navigation buttons belong
                               to. If None, the same parent will be used."""
        if buttons_parent is None: buttons_parent = parent
        super(WebViewer, self).__init__(parent)
        self._back_button = BackwardButton(buttons_parent)
        self._back_button.on_clicked.subscribe(self.go_back)
        self._forward_button = ForwardButton(buttons_parent)
        self._forward_button.on_clicked.subscribe(self.go_forward)
        self._reload_button = ReloadButton(buttons_parent)
        self._reload_button.on_clicked.subscribe(self.reload)
        # Events - internal use only for now, expose if needed
        self._on_new_window = self._evt_handler(
            _wx_html2.EVT_WEBVIEW_NEWWINDOW, lambda event: [event.GetURL()])
        self._on_new_window.subscribe(self._handle_new_window_opened)
        self._on_page_loaded = self._evt_handler(_wx_html2.EVT_WEBVIEW_LOADED)
        self._on_page_loaded.subscribe(self._handle_page_loaded)

    def _handle_page_loaded(self):
        """Internal method used as a callback to update the navigation buttons
        in response to the user navigating inside the WebView."""
        # TODO(inf) On wx4, remove about:blank entries from history here
        # for history_entry in self._native_widget.GetBackwardHistory():
        #     if ...
        self.update_buttons()

    @staticmethod
    def _handle_new_window_opened(new_url): # type: (unicode) -> None
        """Internal method used as a callback when attempting to open a link
        in a new tab or window. We don't support that, so we just open it in
        the user's browser instead.

        :param new_url: The URL of the visited page."""
        webbrowser.open(new_url, new=2)

    def clear_history(self):
        """Clears the browsing history. Navigation buttons will be updated."""
        self._native_widget.ClearHistory()
        self.update_buttons()

    def get_navigation_buttons(self):
        """Returns a tuple containing references to the three navigation
        buttons for this WebViewer. The first is a 'back' button that will go
        to the last page in the browsing history when clicked, the second is a
        'forward' button that will go to the next page in the browsing history
        when clicked and the third is a 'reload' button which will reload the
        current page. They will be disabled when there are no pages for them to
        go to or when the entire WebViewer is disabled.

        :return: A tuple containing the navigation buttons for this
                 WebViewer."""
        return self._back_button, self._forward_button, self._reload_button

    def go_back(self):
        """Goes one step back in the browsing history, if that is possible.
        Navigation buttons will be updated accordingly."""
        if self._native_widget.CanGoBack():
            self._native_widget.GoBack()
        # do this just in case CanGoBack() is false and we're out of sync
        self.update_buttons()

    def go_forward(self):
        """Goes one step forward in the browsing history, if that is possible.
        Navigation buttons will be updated accordingly."""
        if self._native_widget.CanGoForward():
            self._native_widget.GoForward()
        # do this just in case CanGoForward() is false and we're out of sync
        self.update_buttons()

    def open_file(self, file_path): # type: (unicode) -> None
        """Opens the specified file by turning it into a 'file:' URL.

        :param file_path: The path to the file to open."""
        file_url = urlparse.urljoin(u'file:', urllib.pathname2url(file_path))
        self.open_url(file_url)

    def open_url(self, url): # type: (unicode) -> None
        """Opens the specified URL.

        :param url: The URL to open."""
        self._native_widget.LoadURL(url)

    def reload(self, bypass_cache=False):
        """Reloads the current website.

        :param bypass_cache: If set to True, disregard any entries in the
                             cache and reload them from the website instead."""
        if bypass_cache:
            reload_flags = _wx_html2.WEBVIEW_RELOAD_NO_CACHE
        else:
            reload_flags = _wx_html2.WEBVIEW_RELOAD_DEFAULT
        self._native_widget.Reload(reload_flags)

    def update_buttons(self):
        """Enables or disables the navigation buttons depending on the status
        of the browsing history (is there anything to go back / forward to?)
        and whether or not the WebViewer itself is enabled (if the WebViewer
        is disabled, the navigation buttons will be disabled as well)."""
        can_enable = self.enabled
        self._back_button.enabled = can_enable and \
                                    self._native_widget.CanGoBack()
        self._forward_button.enabled = can_enable and \
                                       self._native_widget.CanGoForward()
        self._reload_button.enabled = can_enable

class HtmlDisplay(_AComponent):
    """A wrapper around WebViewer that implements a fallback raw text display
    of the HTML code, as well as permanently disabled fallback versions of
    WebViewer's navigation buttons."""
    _wx_widget_type = _wx.Window

    def __init__(self, parent):
        """Creates a new HtmlDisplay with the specified parent.

        :param parent: The object that this HTML display belongs to. May be a
                       wx object or a component."""
        super(HtmlDisplay, self).__init__(parent)
        # init the fallback/plaintext widget
        self._text_ctrl = TextArea(self, editable=False, auto_tooltip=False)
        items = [self._text_ctrl]
        if web_viewer_available():
            # We can render HTML, create the WebViewer and use its buttons
            self._html_ctrl = WebViewer(self, buttons_parent=parent)
            self._prev_button, self._next_button, self._reload_button = \
                self._html_ctrl.get_navigation_buttons()
            items.append(self._html_ctrl)
            self._text_ctrl.enabled = False
        else:
            # Emulate the buttons WebViewer would normally provide
            self._prev_button = BackwardButton(parent)
            self._next_button = ForwardButton(parent)
            self._reload_button = ReloadButton(parent)
        VLayout(item_weight=4, item_expand=True, items=items).apply_to(self)
        self.switch_to_text() # default to text

    def _update_views(self, enable_html):
        """Internal method to switch between HTML and text display, as well as
        update the state of the WebViewer buttons.

        :param enable_html: If set to True, use the HTML display if
                            available."""
        if web_viewer_available():
            self._html_ctrl.enabled = enable_html
            self._html_ctrl.visible = enable_html
            self._html_ctrl.update_buttons()
        self._text_ctrl.enabled = not enable_html
        self._text_ctrl.visible = not enable_html

    @property
    def fallback_text(self):
        """Returns the fallback text displayed by the text display."""
        return self._text_ctrl.text_content

    @fallback_text.setter
    def fallback_text(self, new_fallback):
        """Changes the fallback text that will be displayed by the text
        display, but does not switch to text mode - see switch_to_text()."""
        self._text_ctrl.text_content = new_fallback

    def load_text(self, target_text):
        """Switches to text mode (see switch_to_text()) and sets the
        specified text as the unmodified contents of the text display."""
        if not isinstance(target_text, unicode): # needs to be unicode by now
            raise StateError(u'HtmlDisplay can only load unicode text.')
        self._text_ctrl.text_content = target_text
        self._text_ctrl.modified = False
        self.switch_to_text()

    def is_text_modified(self):
        """Returns True if the text display has been marked as modified,
        either by the user editing it or by calling set_text_modified(True)."""
        return self._text_ctrl.modified

    def set_text_modified(self, text_modified):
        """Changes whether the text display is marked as modified or not."""
        self._text_ctrl.modified = text_modified

    def set_text_editable(self, text_editable):
        # type: (bool) -> None
        """Changes whether or not the text display is editable."""
        self._text_ctrl.editable = text_editable

    def switch_to_html(self):
        """Disables the text viewer and switches to HTML mode, if WebViewer is
        available."""
        if not web_viewer_available(): return
        self._update_views(enable_html=True)
        self._native_widget.Layout()

    def switch_to_text(self):
        """Disables the HTML viewer and switches to raw text mode."""
        self._update_views(enable_html=False)
        self._native_widget.Layout()

    def get_buttons(self):
        """Returns the three navigation buttons as a tuple."""
        return self._prev_button, self._next_button, self._reload_button

    def try_load_html(self, file_path, file_text=u''):
        """Load a HTML file if WebViewer is available, or load the text.

        :param file_path: A bolt.Path instance or a unicode string.
        :Param file_text: If the HTML viewer is unavailable, use this as the
                          fallback text."""
        if web_viewer_available():
            self._html_ctrl.clear_history()
            self._html_ctrl.open_file(u'%s' % file_path)
            self.switch_to_html()
        else:
            self.load_text(file_text)
