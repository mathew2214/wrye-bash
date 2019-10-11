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

from ctypes import byref, cast, c_char, c_ulong, POINTER

from . import API_FIELDS, CBashRECORDARRAY, FormID, ObCollection
from . import _CCleanModMasters, _CCopyRecord, _CCreateRecord, \
    _CGetCollectionIDByModID, _CGetCollectionIDByRecordID, _CGetField,\
    _CGetFieldAttribute, _CGetFileNameByID, _CGetIdenticalToMasterRecords,\
    _CGetLongIDName, _CGetModIDByRecordID, _CGetModNameByID, \
    _CGetModNumEmptyGRUPs, _CGetModNumOrphans, _CGetModNumTypes, \
    _CGetModOrphansFormIDs, _CGetModTypes, _CGetNumIdenticalToMasterRecords, \
    _CGetRecordID, _CIsModEmpty, _CLoadMod, _CSaveMod, _CUnloadMod, \
    _CUpdateReferences
from . import _encode, _uni, deprint, GPath

class ObBaseRecord(object):
    __slots__ = ['_RecordID']
    _Type = 'BASE'
    def __init__(self, RecordID):
        self._RecordID = RecordID

    def __eq__(self, other):
        return self._RecordID == other._RecordID if type(other) is type(self) else False

    def __ne__(self, other):
        return not self.__eq__(other)

    def GetParentMod(self):
        return ObModFile(_CGetModIDByRecordID(self._RecordID))

    def GetParentCollection(self):
        return ObCollection(_CGetCollectionIDByRecordID(self._RecordID))

    def ResetRecord(self):
        _CResetRecord(self._RecordID)

    def UnloadRecord(self):
        _CUnloadRecord(self._RecordID)

    def DeleteRecord(self):
        _CDeleteRecord(self._RecordID)

    def GetRecordUpdatedReferences(self):
        return _CGetRecordUpdatedReferences(0, self._RecordID)

    def UpdateReferences(self, Old_NewFormIDs):
        Old_NewFormIDs = FormID.FilterValidDict(Old_NewFormIDs, self, True, True, AsShort=True)
        length = len(Old_NewFormIDs)
        if not length: return []
        OldFormIDs = (c_ulong * length)(*Old_NewFormIDs.keys())
        NewFormIDs = (c_ulong * length)(*Old_NewFormIDs.values())
        Changes = (c_ulong * length)()
        _CUpdateReferences(0, self._RecordID, OldFormIDs, NewFormIDs, byref(Changes), length)
        return [x for x in Changes]

    def History(self):
        cRecordIDs = (c_ulong * 257)() #just allocate enough for the max number + size
        numRecords = _CGetRecordHistory(self._RecordID, byref(cRecordIDs))
        return [self.__class__(cRecordIDs[x]) for x in range(numRecords)]

    def IsWinning(self, GetExtendedConflicts=False):
        """Returns true if the record is the last to load.
           If GetExtendedConflicts is True, scanned records will be considered.
           More efficient than running Conflicts() and checking the first value."""
        return _CIsRecordWinning(self._RecordID, c_ulong(GetExtendedConflicts)) > 0

    def HasInvalidFormIDs(self):
        return _CIsRecordFormIDsInvalid(self._RecordID) > 0

    def Conflicts(self, GetExtendedConflicts=False):
        numRecords = _CGetNumRecordConflicts(self._RecordID, c_ulong(GetExtendedConflicts)) #gives upper bound
        if(numRecords > 1):
            cRecordIDs = (c_ulong * numRecords)()
            numRecords = _CGetRecordConflicts(self._RecordID, byref(cRecordIDs), c_ulong(GetExtendedConflicts))
            return [self.__class__(cRecordIDs[x]) for x in range(numRecords)]
        return []

    def ConflictDetails(self, attrs=None):
        """New: attrs is an iterable, for each item, the following is checked:
           if the item is a string type: changes are reported
           if the item is another iterable (set,list,tuple), then if any of the subitems is
             different, then all sub items are reported.  This allows grouping of dependant
             items."""
        conflicting = {}
        if attrs is None: attrs = self.copyattrs
        if not attrs: return conflicting

        parentRecords = self.History()
        if parentRecords:
            for attr in attrs:
                if isinstance(attr,basestring):
                    # Single attr
                    conflicting.update([(attr,reduce(getattr, attr.split('.'), self)) for parentRecord in parentRecords if reduce(getattr, attr.split('.'), self) != reduce(getattr, attr.split('.'), parentRecord)])
                elif isinstance(attr,(list,tuple,set)):
                    # Group of attrs that need to stay together
                    for parentRecord in parentRecords:
                        subconflicting = {}
                        conflict = False
                        for subattr in attr:
                            self_value = reduce(getattr, subattr.split('.'), self)
                            if not conflict and self_value != reduce(getattr, subattr.split('.'), parentRecord):
                                conflict = True
                            subconflicting.update([(subattr,self_value)])
                        if conflict:
                            conflicting.update(subconflicting)
        else: #is the first instance of the record
            for attr in attrs:
                if isinstance(attr, basestring):
                    conflicting.update([(attr,reduce(getattr, attr.split('.'), self))])
                elif isinstance(attr,(list,tuple,set)):
                    conflicting.update([(subattr,reduce(getattr, subattr.split('.'), self)) for subattr in attr])

        skipped_conflicting = [(attr, value) for attr, value in conflicting.iteritems() if isinstance(value, FormID) and not value.ValidateFormID(self)]
        for attr, value in skipped_conflicting:
            try:
                deprint(_(u"%s attribute of %s record (maybe named: %s) importing from %s referenced an unloaded object (probably %s) - value skipped") % (attr, self.fid, self.full, self.GetParentMod().GName, value))
            except: #a record type that doesn't have a full chunk:
                deprint(_(u"%s attribute of %s record importing from %s referenced an unloaded object (probably %s) - value skipped") % (attr, self.fid, self.GetParentMod().GName, value))
            del conflicting[attr]

        return conflicting

    def mergeFilter(self, target):
        """This method is called by the bashed patch mod merger. The intention is
        to allow a record to be filtered according to the specified modSet. E.g.
        for a list record, items coming from mods not in the modSet could be
        removed from the list."""
        pass

    def CopyAsOverride(self, target, UseWinningParents=False):
        ##Record Creation Flags
        ##SetAsOverride       = 0x00000001
        ##CopyWinningParent   = 0x00000002
        DestParentID, DestModID = (0, target._ModID) if not hasattr(self, '_ParentID') else (self._ParentID, target._ModID) if isinstance(target, ObModFile) else (target._RecordID, target.GetParentMod()._ModID)
        RecordID = _CCopyRecord(self._RecordID, DestModID, DestParentID, 0, 0, c_ulong(0x00000003 if UseWinningParents else 0x00000001))
        return self.__class__(RecordID) if RecordID else None

    def CopyAsNew(self, target, UseWinningParents=False, RecordFormID=0):
        ##Record Creation Flags
        ##SetAsOverride       = 0x00000001
        ##CopyWinningParent   = 0x00000002
        DestParentID, DestModID = (0, target._ModID) if not hasattr(self, '_ParentID') else (self._ParentID, target._ModID) if isinstance(target, ObModFile) else (target._RecordID, target.GetParentMod()._ModID)
        RecordID = _CCopyRecord(self._RecordID, DestModID, DestParentID, RecordFormID.GetShortFormID(target) if RecordFormID else 0, 0, c_ulong(0x00000002 if UseWinningParents else 0))
        return self.__class__(RecordID) if RecordID else None

    @property
    def Parent(self):
        RecordID = getattr(self, '_ParentID', None)
        if RecordID:
            _CGetFieldAttribute.restype = (c_char * 4)
            retValue = _CGetFieldAttribute(RecordID, 0, 0, 0, 0, 0, 0, 0, 0)
            _CGetFieldAttribute.restype = c_ulong
            return type_record[retValue.value](RecordID)
        return None

    @property
    def recType(self):
        _CGetFieldAttribute.restype = (c_char * 4)
        retValue = _CGetFieldAttribute(self._RecordID, 0, 0, 0, 0, 0, 0, 0, 0).value
        _CGetFieldAttribute.restype = c_ulong
        return retValue

    flags1 = CBashGeneric(1, c_ulong)

    def get_fid(self):
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(self._RecordID, 2, 0, 0, 0, 0, 0, 0, 0)
        return FormID(self._RecordID, retValue.contents.value) if retValue else FormID(None,None)
    def set_fid(self, nValue):
        _CSetIDFields(self._RecordID, 0 if nValue is None else nValue.GetShortFormID(self), self.eid or 0)
    fid = property(get_fid, set_fid)

    flags2 = CBashGeneric(3, c_ulong)

    def get_eid(self):
        _CGetField.restype = c_char_p
        retValue = _CGetField(self._RecordID, 4, 0, 0, 0, 0, 0, 0, 0)
        return IUNICODE(_unicode(retValue)) if retValue else None
    def set_eid(self, nValue):
        nValue = 0 if nValue is None or not len(nValue) else _encode(nValue)
        _CGetField.restype = POINTER(c_ulong)
        _CSetIDFields(self._RecordID, _CGetField(self._RecordID, 2, 0, 0, 0, 0, 0, 0, 0).contents.value, nValue)
    eid = property(get_eid, set_eid)

    IsDeleted = CBashBasicFlag('flags1', 0x00000020)
    IsBorderRegion = CBashBasicFlag('flags1', 0x00000040)
    IsTurnOffFire = CBashBasicFlag('flags1', 0x00000080)
    IsCastsShadows = CBashBasicFlag('flags1', 0x00000200)
    IsPersistent = CBashBasicFlag('flags1', 0x00000400)
    IsQuest = CBashAlias('IsPersistent')
    IsQuestOrPersistent = CBashAlias('IsPersistent')
    IsInitiallyDisabled = CBashBasicFlag('flags1', 0x00000800)
    IsIgnored = CBashBasicFlag('flags1', 0x00001000)
    IsVisibleWhenDistant = CBashBasicFlag('flags1', 0x00008000)
    IsVWD = CBashAlias('IsVisibleWhenDistant')
    IsDangerousOrOffLimits = CBashBasicFlag('flags1', 0x00020000)
    IsCompressed = CBashBasicFlag('flags1', 0x00040000)
    IsCantWait = CBashBasicFlag('flags1', 0x00080000)
    baseattrs = ['flags1', 'flags2', 'eid']

class ObTES4Record(object):
    __slots__ = ['_RecordID']
    _Type = 'TES4'
    def __init__(self, RecordID):
        self._RecordID = RecordID

    def GetParentMod(self):
        return ObModFile(_CGetModIDByRecordID(self._RecordID))

    def GetParentCollection(self):
        return ObCollection(_CGetCollectionIDByRecordID(self._RecordID))

    def ResetRecord(self):
        pass

    def UnloadRecord(self):
        pass

    @property
    def recType(self):
        return self._Type

    flags1 = CBashGeneric(1, c_ulong)
    flags2 = CBashGeneric(3, c_ulong)
    version = CBashFLOAT32(5)
    numRecords = CBashGeneric(6, c_ulong)
    nextObject = CBashGeneric(7, c_ulong)
    ofst_p = CBashUINT8ARRAY(8)
    dele_p = CBashUINT8ARRAY(9)
    author = CBashUNICODE(10)
    description = CBashUNICODE(11)
    masters = CBashIUNICODEARRAY(12)
    DATA = CBashJunk(13)
    IsESM = CBashBasicFlag('flags1', 0x00000001)
    exportattrs = copyattrs = ['flags1', 'flags2', 'version', 'numRecords', 'nextObject',
                               'author', 'description', 'masters']

class ObGMSTRecord(ObBaseRecord):
    __slots__ = []
    _Type = 'GMST'
    def get_value(self):
        fieldtype = _CGetFieldAttribute(self._RecordID, 5, 0, 0, 0, 0, 0, 0, 2)
        if fieldtype == API_FIELDS.UNKNOWN: return None
        _CGetField.restype = POINTER(c_long) if fieldtype == API_FIELDS.SINT32 else POINTER(c_float) if fieldtype == API_FIELDS.FLOAT32 else c_char_p
        retValue = _CGetField(self._RecordID, 5, 0, 0, 0, 0, 0, 0, 0)
        return (_unicode(retValue) if fieldtype == API_FIELDS.STRING else round(retValue.contents.value,6) if fieldtype == API_FIELDS.FLOAT32 else retValue.contents.value) if retValue else None
    def set_value(self, nValue):
        if nValue is None: _CDeleteField(self._RecordID, 5, 0, 0, 0, 0, 0, 0)
        else:
            fieldtype = _CGetFieldAttribute(self._RecordID, 5, 0, 0, 0, 0, 0, 0, 2)
            try: _CSetField(self._RecordID, 5, 0, 0, 0, 0, 0, 0, byref(c_long(int(nValue))) if fieldtype == API_FIELDS.SINT32 else byref(c_float(round(nValue,6))) if fieldtype == API_FIELDS.FLOAT32 else _encode(nValue), 0)
            except TypeError: return
            except ValueError: return
    value = property(get_value, set_value)
    exportattrs = copyattrs = ObBaseRecord.baseattrs + ['value']

class ObModFile(object):
    __slots__ = ['_ModID']
    def __init__(self, ModID):
        self._ModID = ModID

    def __eq__(self, other):
        return self._ModID == other._ModID if type(other) is type(self) else False

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def FileName(self):
        return _uni(_CGetFileNameByID(self._ModID)) or u'Missing'

    @property
    def ModName(self):
        return _uni(_CGetModNameByID(self._ModID)) or u'Missing'

    @property
    def GName(self):
        return GPath(self.ModName)

    def GetParentCollection(self):
        return ObCollection(_CGetCollectionIDByModID(self._ModID))

    def HasRecord(self, RecordIdentifier):
        if not RecordIdentifier: return False
        formID, editorID = (0, _encode(RecordIdentifier)) if isinstance(RecordIdentifier, basestring) else (RecordIdentifier.GetShortFormID(self),0)
        if not (formID or editorID): return False
        return bool(_CGetRecordID(self._ModID, formID, editorID))

    def LookupRecord(self, RecordIdentifier):
        if not RecordIdentifier: return None
        formID, editorID = (0, _encode(RecordIdentifier)) if isinstance(RecordIdentifier, basestring) else (RecordIdentifier.GetShortFormID(self),0)
        if not (formID or editorID): return None
        RecordID = _CGetRecordID(self._ModID, formID, editorID)
        if RecordID:
            _CGetFieldAttribute.restype = (c_char * 4)
            RecordType = type_record[_CGetFieldAttribute(RecordID, 0, 0, 0, 0, 0, 0, 0, 0).value]
            _CGetFieldAttribute.restype = c_ulong
            return RecordType(RecordID)
        return None

    def IsEmpty(self):
        return _CIsModEmpty(self._ModID) > 0

    def GetNewRecordTypes(self):
        numRecords = _CGetModNumTypes(self._ModID)
        if(numRecords > 0):
            cRecords = ((c_char * 4) * numRecords)()
            _CGetModTypes(self._ModID, byref(cRecords))
            return [cRecord.value for cRecord in cRecords if cRecord]
        return []

    def GetNumEmptyGRUPs(self):
        return _CGetModNumEmptyGRUPs(self._ModID)

    def GetOrphanedFormIDs(self):
        numFormIDs = _CGetModNumOrphans(self._ModID)
        if(numFormIDs > 0):
            cFormIDs = (c_ulong * numFormIDs)()
            _CGetModOrphansFormIDs(self._ModID, byref(cFormIDs))
            RecordID = _CGetRecordID(self._ModID, 0, 0)
            return [FormID(_CGetLongIDName(RecordID, cFormID, 0), cFormID) for cFormID in cFormIDs if cFormID]
        return []

    def UpdateReferences(self, Old_NewFormIDs):
        Old_NewFormIDs = FormID.FilterValidDict(Old_NewFormIDs, self, True, True, AsShort=True)
        length = len(Old_NewFormIDs)
        if not length: return []
        OldFormIDs = (c_ulong * length)(*Old_NewFormIDs.keys())
        NewFormIDs = (c_ulong * length)(*Old_NewFormIDs.values())
        Changes = (c_ulong * length)()
        _CUpdateReferences(self._ModID, 0, OldFormIDs, NewFormIDs, byref(Changes), length)
        return [x for x in Changes]

    def CleanMasters(self):
        return _CCleanModMasters(self._ModID)

    def GetRecordsIdenticalToMaster(self):
        numRecords = _CGetNumIdenticalToMasterRecords(self._ModID)
        if(numRecords > 0):
            cRecords = (c_ulong * numRecords)()
            _CGetIdenticalToMasterRecords(self._ModID, byref(cRecords))
            _CGetFieldAttribute.restype = (c_char * 4)
            values = [type_record[_CGetFieldAttribute(x, 0, 0, 0, 0, 0, 0, 0, 0).value](x) for x in cRecords]
            _CGetFieldAttribute.restype = c_ulong
            return values
        return []

    def Load(self):
        _CLoadMod(self._ModID)

    def Unload(self):
        _CUnloadMod(self._ModID)

    def save(self, CloseCollection=True, CleanMasters=True, DestinationName=None):
        return _CSaveMod(self._ModID, c_ulong(0 | (0x00000001 if CleanMasters else 0) | (0x00000002 if CloseCollection else 0)), _encode(DestinationName) if DestinationName else DestinationName)

    @property
    def TES4(self):
        return ObTES4Record(_CGetRecordID(self._ModID, 0, 0))

    def create_GMST(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("GMST", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObGMSTRecord(RecordID) if RecordID else None
    GMST = CBashRECORDARRAY(ObGMSTRecord, 'GMST')

    def create_GLOB(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("GLOB", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObGLOBRecord(RecordID) if RecordID else None
    GLOB = CBashRECORDARRAY(ObGLOBRecord, 'GLOB')

    def create_CLAS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CLAS", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObCLASRecord(RecordID) if RecordID else None
    CLAS = CBashRECORDARRAY(ObCLASRecord, 'CLAS')

    def create_FACT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("FACT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObFACTRecord(RecordID) if RecordID else None
    FACT = CBashRECORDARRAY(ObFACTRecord, 'FACT')

    def create_HAIR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("HAIR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObHAIRRecord(RecordID) if RecordID else None
    HAIR = CBashRECORDARRAY(ObHAIRRecord, 'HAIR')

    def create_EYES(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("EYES", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObEYESRecord(RecordID) if RecordID else None
    EYES = CBashRECORDARRAY(ObEYESRecord, 'EYES')

    def create_RACE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("RACE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObRACERecord(RecordID) if RecordID else None
    RACE = CBashRECORDARRAY(ObRACERecord, 'RACE')

    def create_SOUN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SOUN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObSOUNRecord(RecordID) if RecordID else None
    SOUN = CBashRECORDARRAY(ObSOUNRecord, 'SOUN')

    def create_SKIL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SKIL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObSKILRecord(RecordID) if RecordID else None
    SKIL = CBashRECORDARRAY(ObSKILRecord, 'SKIL')

    def create_MGEF(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("MGEF", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObMGEFRecord(RecordID) if RecordID else None
    MGEF = CBashRECORDARRAY(ObMGEFRecord, 'MGEF')

    def create_SCPT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SCPT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObSCPTRecord(RecordID) if RecordID else None
    SCPT = CBashRECORDARRAY(ObSCPTRecord, 'SCPT')

    def create_LTEX(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LTEX", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObLTEXRecord(RecordID) if RecordID else None
    LTEX = CBashRECORDARRAY(ObLTEXRecord, 'LTEX')

    def create_ENCH(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ENCH", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObENCHRecord(RecordID) if RecordID else None
    ENCH = CBashRECORDARRAY(ObENCHRecord, 'ENCH')

    def create_SPEL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SPEL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObSPELRecord(RecordID) if RecordID else None
    SPEL = CBashRECORDARRAY(ObSPELRecord, 'SPEL')

    def create_BSGN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("BSGN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObBSGNRecord(RecordID) if RecordID else None
    BSGN = CBashRECORDARRAY(ObBSGNRecord, 'BSGN')

    def create_ACTI(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ACTI", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObACTIRecord(RecordID) if RecordID else None
    ACTI = CBashRECORDARRAY(ObACTIRecord, 'ACTI')

    def create_APPA(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("APPA", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObAPPARecord(RecordID) if RecordID else None
    APPA = CBashRECORDARRAY(ObAPPARecord, 'APPA')

    def create_ARMO(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ARMO", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObARMORecord(RecordID) if RecordID else None
    ARMO = CBashRECORDARRAY(ObARMORecord, 'ARMO')

    def create_BOOK(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("BOOK", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObBOOKRecord(RecordID) if RecordID else None
    BOOK = CBashRECORDARRAY(ObBOOKRecord, 'BOOK')

    def create_CLOT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CLOT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObCLOTRecord(RecordID) if RecordID else None
    CLOT = CBashRECORDARRAY(ObCLOTRecord, 'CLOT')

    def create_CONT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CONT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObCONTRecord(RecordID) if RecordID else None
    CONT = CBashRECORDARRAY(ObCONTRecord, 'CONT')

    def create_DOOR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("DOOR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObDOORRecord(RecordID) if RecordID else None
    DOOR = CBashRECORDARRAY(ObDOORRecord, 'DOOR')

    def create_INGR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("INGR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObINGRRecord(RecordID) if RecordID else None
    INGR = CBashRECORDARRAY(ObINGRRecord, 'INGR')

    def create_LIGH(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LIGH", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObLIGHRecord(RecordID) if RecordID else None
    LIGH = CBashRECORDARRAY(ObLIGHRecord, 'LIGH')

    def create_MISC(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("MISC", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObMISCRecord(RecordID) if RecordID else None
    MISC = CBashRECORDARRAY(ObMISCRecord, 'MISC')

    def create_STAT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("STAT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObSTATRecord(RecordID) if RecordID else None
    STAT = CBashRECORDARRAY(ObSTATRecord, 'STAT')

    def create_GRAS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("GRAS", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObGRASRecord(RecordID) if RecordID else None
    GRAS = CBashRECORDARRAY(ObGRASRecord, 'GRAS')

    def create_TREE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("TREE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObTREERecord(RecordID) if RecordID else None
    TREE = CBashRECORDARRAY(ObTREERecord, 'TREE')

    def create_FLOR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("FLOR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObFLORRecord(RecordID) if RecordID else None
    FLOR = CBashRECORDARRAY(ObFLORRecord, 'FLOR')

    def create_FURN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("FURN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObFURNRecord(RecordID) if RecordID else None
    FURN = CBashRECORDARRAY(ObFURNRecord, 'FURN')

    def create_WEAP(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("WEAP", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObWEAPRecord(RecordID) if RecordID else None
    WEAP = CBashRECORDARRAY(ObWEAPRecord, 'WEAP')

    def create_AMMO(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("AMMO", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObAMMORecord(RecordID) if RecordID else None
    AMMO = CBashRECORDARRAY(ObAMMORecord, 'AMMO')

    def create_NPC_(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("NPC_", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObNPC_Record(RecordID) if RecordID else None
    NPC_ = CBashRECORDARRAY(ObNPC_Record, 'NPC_')

    def create_CREA(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CREA", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObCREARecord(RecordID) if RecordID else None
    CREA = CBashRECORDARRAY(ObCREARecord, 'CREA')

    def create_LVLC(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LVLC", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObLVLCRecord(RecordID) if RecordID else None
    LVLC = CBashRECORDARRAY(ObLVLCRecord, 'LVLC')

    def create_SLGM(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SLGM", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObSLGMRecord(RecordID) if RecordID else None
    SLGM = CBashRECORDARRAY(ObSLGMRecord, 'SLGM')

    def create_KEYM(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("KEYM", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObKEYMRecord(RecordID) if RecordID else None
    KEYM = CBashRECORDARRAY(ObKEYMRecord, 'KEYM')

    def create_ALCH(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ALCH", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObALCHRecord(RecordID) if RecordID else None
    ALCH = CBashRECORDARRAY(ObALCHRecord, 'ALCH')

    def create_SBSP(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SBSP", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObSBSPRecord(RecordID) if RecordID else None
    SBSP = CBashRECORDARRAY(ObSBSPRecord, 'SBSP')

    def create_SGST(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SGST", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObSGSTRecord(RecordID) if RecordID else None
    SGST = CBashRECORDARRAY(ObSGSTRecord, 'SGST')

    def create_LVLI(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LVLI", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObLVLIRecord(RecordID) if RecordID else None
    LVLI = CBashRECORDARRAY(ObLVLIRecord, 'LVLI')

    def create_WTHR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("WTHR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObWTHRRecord(RecordID) if RecordID else None
    WTHR = CBashRECORDARRAY(ObWTHRRecord, 'WTHR')

    def create_CLMT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CLMT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObCLMTRecord(RecordID) if RecordID else None
    CLMT = CBashRECORDARRAY(ObCLMTRecord, 'CLMT')

    def create_REGN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("REGN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObREGNRecord(RecordID) if RecordID else None
    REGN = CBashRECORDARRAY(ObREGNRecord, 'REGN')

    def create_WRLD(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("WRLD", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObWRLDRecord(RecordID) if RecordID else None
    WRLD = CBashRECORDARRAY(ObWRLDRecord, 'WRLD')

    def create_CELL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CELL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObCELLRecord(RecordID) if RecordID else None
    CELL = CBashRECORDARRAY(ObCELLRecord, 'CELL')

    def create_DIAL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("DIAL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObDIALRecord(RecordID) if RecordID else None
    DIAL = CBashRECORDARRAY(ObDIALRecord, 'DIAL')

    def create_QUST(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("QUST", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObQUSTRecord(RecordID) if RecordID else None
    QUST = CBashRECORDARRAY(ObQUSTRecord, 'QUST')

    def create_IDLE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("IDLE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObIDLERecord(RecordID) if RecordID else None
    IDLE = CBashRECORDARRAY(ObIDLERecord, 'IDLE')

    def create_PACK(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("PACK", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObPACKRecord(RecordID) if RecordID else None
    PACK = CBashRECORDARRAY(ObPACKRecord, 'PACK')

    def create_CSTY(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CSTY", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObCSTYRecord(RecordID) if RecordID else None
    CSTY = CBashRECORDARRAY(ObCSTYRecord, 'CSTY')

    def create_LSCR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LSCR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObLSCRRecord(RecordID) if RecordID else None
    LSCR = CBashRECORDARRAY(ObLSCRRecord, 'LSCR')

    def create_LVSP(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LVSP", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObLVSPRecord(RecordID) if RecordID else None
    LVSP = CBashRECORDARRAY(ObLVSPRecord, 'LVSP')

    def create_ANIO(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ANIO", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObANIORecord(RecordID) if RecordID else None
    ANIO = CBashRECORDARRAY(ObANIORecord, 'ANIO')

    def create_WATR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("WATR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObWATRRecord(RecordID) if RecordID else None
    WATR = CBashRECORDARRAY(ObWATRRecord, 'WATR')

    def create_EFSH(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("EFSH", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return ObEFSHRecord(RecordID) if RecordID else None
    EFSH = CBashRECORDARRAY(ObEFSHRecord, 'EFSH')

    ##Aggregate properties. Useful for iterating through all records without going through the parent records.
    WorldCELLS = CBashRECORDARRAY(ObCELLRecord, 'WCEL') ##"WCEL" is an artificial type CBash uses to distinguish World Cells
    CELLS = CBashRECORDARRAY(ObCELLRecord, 'CLLS') ##"CLLS" is an artificial type CBash uses to distinguish all cells (includes WCEL)
    INFOS = CBashRECORDARRAY(ObINFORecord, 'INFO')
    ACHRS = CBashRECORDARRAY(ObACHRRecord, 'ACHR')
    ACRES = CBashRECORDARRAY(ObACRERecord, 'ACRE')
    REFRS = CBashRECORDARRAY(ObREFRRecord, 'REFR')
    PGRDS = CBashRECORDARRAY(ObPGRDRecord, 'PGRD')
    LANDS = CBashRECORDARRAY(ObLANDRecord, 'LAND')
    ROADS = CBashRECORDARRAY(ObROADRecord, 'ROAD')

    @property
    def tops(self):
        return dict((("GMST", self.GMST),("GLOB", self.GLOB),("CLAS", self.CLAS),("FACT", self.FACT),
                     ("HAIR", self.HAIR),("EYES", self.EYES),("RACE", self.RACE),("SOUN", self.SOUN),
                     ("SKIL", self.SKIL),("MGEF", self.MGEF),("SCPT", self.SCPT),("LTEX", self.LTEX),
                     ("ENCH", self.ENCH),("SPEL", self.SPEL),("BSGN", self.BSGN),("ACTI", self.ACTI),
                     ("APPA", self.APPA),("ARMO", self.ARMO),("BOOK", self.BOOK),("CLOT", self.CLOT),
                     ("CONT", self.CONT),("DOOR", self.DOOR),("INGR", self.INGR),("LIGH", self.LIGH),
                     ("MISC", self.MISC),("STAT", self.STAT),("GRAS", self.GRAS),("TREE", self.TREE),
                     ("FLOR", self.FLOR),("FURN", self.FURN),("WEAP", self.WEAP),("AMMO", self.AMMO),
                     ("NPC_", self.NPC_),("CREA", self.CREA),("LVLC", self.LVLC),("SLGM", self.SLGM),
                     ("KEYM", self.KEYM),("ALCH", self.ALCH),("SBSP", self.SBSP),("SGST", self.SGST),
                     ("LVLI", self.LVLI),("WTHR", self.WTHR),("CLMT", self.CLMT),("REGN", self.REGN),
                     ("CELL", self.CELL),("WRLD", self.WRLD),("DIAL", self.DIAL),("QUST", self.QUST),
                     ("IDLE", self.IDLE),("PACK", self.PACK),("CSTY", self.CSTY),("LSCR", self.LSCR),
                     ("LVSP", self.LVSP),("ANIO", self.ANIO),("WATR", self.WATR),("EFSH", self.EFSH)))

    @property
    def aggregates(self):
        return dict((("GMST", self.GMST),("GLOB", self.GLOB),("CLAS", self.CLAS),("FACT", self.FACT),
                     ("HAIR", self.HAIR),("EYES", self.EYES),("RACE", self.RACE),("SOUN", self.SOUN),
                     ("SKIL", self.SKIL),("MGEF", self.MGEF),("SCPT", self.SCPT),("LTEX", self.LTEX),
                     ("ENCH", self.ENCH),("SPEL", self.SPEL),("BSGN", self.BSGN),("ACTI", self.ACTI),
                     ("APPA", self.APPA),("ARMO", self.ARMO),("BOOK", self.BOOK),("CLOT", self.CLOT),
                     ("CONT", self.CONT),("DOOR", self.DOOR),("INGR", self.INGR),("LIGH", self.LIGH),
                     ("MISC", self.MISC),("STAT", self.STAT),("GRAS", self.GRAS),("TREE", self.TREE),
                     ("FLOR", self.FLOR),("FURN", self.FURN),("WEAP", self.WEAP),("AMMO", self.AMMO),
                     ("NPC_", self.NPC_),("CREA", self.CREA),("LVLC", self.LVLC),("SLGM", self.SLGM),
                     ("KEYM", self.KEYM),("ALCH", self.ALCH),("SBSP", self.SBSP),("SGST", self.SGST),
                     ("LVLI", self.LVLI),("WTHR", self.WTHR),("CLMT", self.CLMT),("REGN", self.REGN),
                     ("WRLD", self.WRLD),("CELL", self.CELLS),("ACHR", self.ACHRS),("ACRE", self.ACRES),
                     ("REFR", self.REFRS),("PGRD", self.PGRDS),("LAND", self.LANDS),("ROAD", self.ROADS),
                     ("DIAL", self.DIAL),("INFO", self.INFOS),("QUST", self.QUST),("IDLE", self.IDLE),
                     ("PACK", self.PACK),("CSTY", self.CSTY),("LSCR", self.LSCR),("LVSP", self.LVSP),
                     ("ANIO", self.ANIO),("WATR", self.WATR),("EFSH", self.EFSH)))

type_record = dict([('BASE',ObBaseRecord),(None,None),('',None),
                    ('GMST',ObGMSTRecord),('GLOB',ObGLOBRecord),('CLAS',ObCLASRecord),
                    ('FACT',ObFACTRecord),('HAIR',ObHAIRRecord),('EYES',ObEYESRecord),
                    ('RACE',ObRACERecord),('SOUN',ObSOUNRecord),('SKIL',ObSKILRecord),
                    ('MGEF',ObMGEFRecord),('SCPT',ObSCPTRecord),('LTEX',ObLTEXRecord),
                    ('ENCH',ObENCHRecord),('SPEL',ObSPELRecord),('BSGN',ObBSGNRecord),
                    ('ACTI',ObACTIRecord),('APPA',ObAPPARecord),('ARMO',ObARMORecord),
                    ('BOOK',ObBOOKRecord),('CLOT',ObCLOTRecord),('CONT',ObCONTRecord),
                    ('DOOR',ObDOORRecord),('INGR',ObINGRRecord),('LIGH',ObLIGHRecord),
                    ('MISC',ObMISCRecord),('STAT',ObSTATRecord),('GRAS',ObGRASRecord),
                    ('TREE',ObTREERecord),('FLOR',ObFLORRecord),('FURN',ObFURNRecord),
                    ('WEAP',ObWEAPRecord),('AMMO',ObAMMORecord),('NPC_',ObNPC_Record),
                    ('CREA',ObCREARecord),('LVLC',ObLVLCRecord),('SLGM',ObSLGMRecord),
                    ('KEYM',ObKEYMRecord),('ALCH',ObALCHRecord),('SBSP',ObSBSPRecord),
                    ('SGST',ObSGSTRecord),('LVLI',ObLVLIRecord),('WTHR',ObWTHRRecord),
                    ('CLMT',ObCLMTRecord),('REGN',ObREGNRecord),('WRLD',ObWRLDRecord),
                    ('CELL',ObCELLRecord),('ACHR',ObACHRRecord),('ACRE',ObACRERecord),
                    ('REFR',ObREFRRecord),('PGRD',ObPGRDRecord),('LAND',ObLANDRecord),
                    ('ROAD',ObROADRecord),('DIAL',ObDIALRecord),('INFO',ObINFORecord),
                    ('QUST',ObQUSTRecord),('IDLE',ObIDLERecord),('PACK',ObPACKRecord),
                    ('CSTY',ObCSTYRecord),('LSCR',ObLSCRRecord),('LVSP',ObLVSPRecord),
                    ('ANIO',ObANIORecord),('WATR',ObWATRRecord),('EFSH',ObEFSHRecord)])
