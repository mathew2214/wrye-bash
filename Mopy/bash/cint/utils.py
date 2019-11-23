# -*- coding: utf-8 -*-
#
######## BEGIN LICENSE BLOCK ######
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is CBash code.
#
# The Initial Developer of the Original Code is
# Waruddar.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#  Wrye Bash Team
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
####### END LICENSE BLOCK ######

from .. import bolt
from ..bolt import Path
from ..bolt import decode as _uni
from ..bolt import encode as _enc


def _encode(text,*args,**kwdargs):
    if len(args) > 1:
        args = list(args)
        args[1] = bolt.pluginEncoding
    else:
        kwdargs['firstEncoding'] = bolt.pluginEncoding
    if isinstance(text,Path): text = text.s
    return _enc(text,*args,**kwdargs)

def _unicode(text,*args,**kwdargs):
    if args:
        args = list(args)
        args[1] = bolt.pluginEncoding
    else:
        kwdargs['encoding'] = bolt.pluginEncoding
    return _uni(text,*args,**kwdargs)

class ICASEMixin:
    """Case insensitive string/unicode class mixin.  Performs like str/unicode,
       except comparisons are case insensitive."""
    def __eq__(self, other):
        try: return self.lower() == other.lower()
        except AttributeError: return False

    def __lt__(self, other):
        try: return self.lower() < other.lower()
        except AttributeError: return False

    def __le__(self, other):
        try: return self.lower() <= other.lower()
        except AttributeError: return False

    def __gt__(self, other):
        try: return self.lower() > other.lower()
        except AttributeError: return False

    def __ne__(self, other):
        try: return self.lower() != other.lower()
        except AttributeError: return False

    def __ge__(self, other):
        try: return self.lower() >= other.lower()
        except AttributeError: return False

    def __cmp__(self, other):
        try: return cmp(self.lower(), other.lower())
        except AttributeError: return False

    def __hash__(self):
        return hash(self.lower())

    def __contains__(self, other):
        try: return other.lower() in self.lower()
        except AttributeError: return False

    def count(self, other, *args):
        try:
            if isinstance(self,str): func = str.count
            else: func = unicode.count
            return func(self.lower(), other.lower(), *args)
        except AttributeError: return 0

    def endswith(self, other, *args):
        try:
            if isinstance(self,str): func = str.endswith
            else: func = unicode.endswith
            if isinstance(other, tuple):
                for value in other:
                    if func(self.lower(), value.lower(), *args):
                        return True
                return False
            return func(self.lower(), other.lower(), *args)
        except AttributeError: return False

    def find(self, other, *args):
        try:
            if isinstance(self,str): func = str.find
            else: func = unicode.find
            return func(self.lower(), other.lower(), *args)
        except AttributeError: return -1

    def index(self, other, *args):
        try:
            if isinstance(self,str): func = str.index
            else: func = unicode.index
            return func(self.lower(), other.lower(), *args)
        except AttributeError: return ValueError

    def rfind(self, other, *args):
        try:
            if isinstance(self,str): func = str.rfind
            else: func = unicode.rfind
            return func(self.lower(), other.lower(), *args)
        except AttributeError: return -1

    def rindex(self, other, *args):
        try:
            if isinstance(self,str): func = str.rindex
            else: func = unicode.rindex
            return func(self.lower(), other.lower(), *args)
        except AttributeError: return ValueError

    def startswith(self, other, *args):
        try:
            if isinstance(self,str): func = str.startswith
            else: func = unicode.startswith
            if isinstance(other, tuple):
                for value in other:
                    if func(self.lower(), value.lower(), *args):
                        return True
                return False
            return func(self.lower(), other.lower(), *args)
        except AttributeError: return False

class ISTRING(ICASEMixin,str):
    """Case insensitive strings class. Performs like str except comparisons are
    case insensitive."""
    pass

class IUNICODE(ICASEMixin,unicode):
    """Case insensitive unicode class.  Performs like unicode except
    comparisons are case insensitive."""
    pass

def ExtractCopyList(Elements):
    return [tuple(getattr(listElement, attr) for attr in listElement.copyattrs) for listElement in Elements]

def SetCopyList(oElements, nValues):
    for oElement, nValueTuple in zip(oElements, nValues):
        for nValue, attr in zip(nValueTuple, oElement.copyattrs):
            setattr(oElement, attr, nValue)
