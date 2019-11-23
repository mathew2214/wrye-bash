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

from .cbash import ActorValue, FormID, MGEFCode, _CBash
from .oblivion import ObBaseRecord, ObCollection, ObModFile
from .utils import IUNICODE

CBASH_ENABLED = _CBash is not None
if CBASH_ENABLED:
    from .cbash import _CGetVersionMajor, _CGetVersionMinor, _CGetVersionRevision


def ValidateList(Elements, target):
    """Convenience function to ensure that a tuple/list of values is valid for the destination.
       Supports nested tuple/list values.
       Returns true if all of the FormIDs/ActorValues/MGEFCodes in the tuple/list are valid."""
    for element in Elements:
        if isinstance(element, FormID) and not element.ValidateFormID(target):
            return False
        elif isinstance(element, ActorValue) and not element.ValidateActorValue(target):
            return False
        elif isinstance(element, MGEFCode) and not element.ValidateMGEFCode(target):
            return False
        elif isinstance(element, (tuple, list)) and not ValidateList(element, target):
            return False
    return True

def ValidateDict(Elements, target):
    """Convenience function to ensure that a dict is valid for the destination.
       Supports nested dictionaries, and tuple/list values.
       Returns true if all of the FormIDs/ActorValues/MGEFCodes in the dict are valid."""
    for key, value in Elements.iteritems():
        if isinstance(key, FormID) and not key.ValidateFormID(target):
            return False
        elif isinstance(key, ActorValue) and not key.ValidateActorValue(target):
            return False
        elif isinstance(key, MGEFCode) and not key.ValidateMGEFCode(target):
            return False
        elif isinstance(value, FormID) and not value.ValidateFormID(target):
            return False
        elif isinstance(value, ActorValue) and not value.ValidateActorValue(target):
            return False
        elif isinstance(value, MGEFCode) and not value.ValidateMGEFCode(target):
            return False
        elif isinstance(key, tuple) and not ValidateList(key, target):
            return False
        elif isinstance(value, (tuple, list)) and not ValidateList(value, target):
            return False
        elif isinstance(value, dict) and not ValidateDict(value, target):
            return False
    return True

def getattr_deep(obj, attr):
    return reduce(getattr, attr.split("."), obj)

def setattr_deep(obj, attr, value):
    attrs = attr.split(".")
    setattr(reduce(getattr, attrs[:-1], obj), attrs[-1], value)

def ExtractExportList(Element):
    try:
        return [
            tuple(
                ExtractExportList(listElement)
                if hasattr(listElement, "exportattrs")
                else getattr(listElement, attr)
                for attr in listElement.exportattrs
            )
            for listElement in Element
        ]
    except TypeError:
        return [
            tuple(
                ExtractExportList(getattr(Element, attr))
                if hasattr(getattr(Element, attr), "exportattrs")
                else getattr(Element, attr)
                for attr in Element.exportattrs
            )
        ]

_dump_RecIndent = 2
_dump_LastIndent = _dump_RecIndent
_dump_ExpandLists = True

def dump_record(record, expand=False):
    def printRecord(record):
        def fflags(y):
            for x in range(32):
                z = 1 << x
                if y & z == z:
                    print hex(z)
        global _dump_RecIndent
        global _dump_LastIndent
        if hasattr(record, "copyattrs"):
            if _dump_ExpandLists == True:
                msize = max([len(attr) for attr in record.copyattrs if not attr.endswith('_list')])
            else:
                msize = max([len(attr) for attr in record.copyattrs])
            for attr in record.copyattrs:
                wasList = False
                if _dump_ExpandLists == True:
                    if attr.endswith("_list"):
                        attr = attr[:-5]
                        wasList = True
                rec = getattr(record, attr)
                if _dump_RecIndent:
                    print " " * (_dump_RecIndent - 1),
                if wasList:
                    print attr
                else:
                    print attr + " " * (msize - len(attr)), ":",
                if rec is None:
                    print rec
                elif "flag" in attr.lower() or "service" in attr.lower():
                    print hex(rec)
                    if _dump_ExpandLists == True:
                        for x in range(32):
                            z = pow(2, x)
                            if rec & z == z:
                                print " " * _dump_RecIndent, " Active" + " " * (
                                    msize - len("  Active")
                                ), "  :", hex(z)

                elif isinstance(rec, list):
                    if len(rec) > 0:
                        IsFidList = True
                        for obj in rec:
                            if not isinstance(obj, FormID):
                                IsFidList = False
                                break
                        if IsFidList:
                            print rec
                        elif not wasList:
                            print rec
                    elif not wasList:
                        print rec
                elif isinstance(rec, basestring):
                    print repr(rec)
                elif not wasList:
                    print rec
                _dump_RecIndent += 2
                printRecord(rec)
                _dump_RecIndent -= 2
        elif isinstance(record, list):
            if len(record) > 0:
                if hasattr(record[0], "copyattrs"):
                    _dump_LastIndent = _dump_RecIndent
                    for rec in record:
                        printRecord(rec)
                        if _dump_LastIndent == _dump_RecIndent:
                            print
    global _dump_ExpandLists
    _dump_ExpandLists = expand
    try:
        msize = max([len(attr) for attr in record.copyattrs])
        print "  fid" + " " * (msize - len("fid")), ":", record.fid
    except AttributeError:
        pass
    printRecord(record)

class CBashApi(object):
    Enabled = CBASH_ENABLED

    VersionMajor = _CGetVersionMajor() if Enabled else 0
    VersionMinor = _CGetVersionMinor() if Enabled else 0
    VersionRevision = _CGetVersionRevision() if Enabled else 0
    VersionInfo = (VersionMajor, VersionMinor, VersionRevision)

    VersionText = u"v%u.%u.%u" % VersionInfo if Enabled else ""

validTypes = {'GMST','GLOB','CLAS','FACT','HAIR','EYES','RACE',
              'SOUN','SKIL','MGEF','SCPT','LTEX','ENCH','SPEL',
              'BSGN','ACTI','APPA','ARMO','BOOK','CLOT','CONT',
              'DOOR','INGR','LIGH','MISC','STAT','GRAS','TREE',
              'FLOR','FURN','WEAP','AMMO','NPC_','CREA','LVLC',
              'SLGM','KEYM','ALCH','SBSP','SGST','LVLI','WTHR',
              'CLMT','REGN','WRLD','CELL','ACHR','ACRE','REFR',
              'PGRD','LAND','ROAD','DIAL','INFO','QUST','IDLE',
              'PACK','CSTY','LSCR','LVSP','ANIO','WATR','EFSH'}

aggregateTypes = {'GMST','GLOB','CLAS','FACT','HAIR','EYES','RACE',
                  'SOUN','SKIL','MGEF','SCPT','LTEX','ENCH','SPEL',
                  'BSGN','ACTI','APPA','ARMO','BOOK','CLOT','CONT',
                  'DOOR','INGR','LIGH','MISC','STAT','GRAS','TREE',
                  'FLOR','FURN','WEAP','AMMO','NPC_','CREA','LVLC',
                  'SLGM','KEYM','ALCH','SBSP','SGST','LVLI','WTHR',
                  'CLMT','REGN','WRLD','CELLS','ACHRS','ACRES','REFRS',
                  'PGRDS','LANDS','ROADS','DIAL','INFOS','QUST','IDLE',
                  'PACK','CSTY','LSCR','LVSP','ANIO','WATR','EFSH'}

pickupables = {'APPA','ARMO','BOOK','CLOT','INGR','LIGH','MISC',
               'WEAP','AMMO','SLGM','KEYM','ALCH','SGST'}

fnv_validTypes = set()

fnv_aggregateTypes = set()

fnv_pickupables = set()
