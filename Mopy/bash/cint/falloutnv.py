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

import math
from ctypes import POINTER, byref, c_bool, c_byte, c_char, c_char_p, c_float, c_long, \
    c_short, c_ubyte, c_ulong, c_ushort, cast

from ..bolt import GPath
from ..bolt import decode as _uni
from ..bolt import deprint
from .cbash import API_FIELDS, IUNICODE, CBashAlias, CBashBasicFlag, CBashBasicType, \
    CBashDEGREES, CBashDEGREES_LISTX2, CBashFLOAT32, CBashFLOAT32_GROUP, \
    CBashFLOAT32_LIST, CBashFLOAT32_LISTX2, CBashFORMID, CBashFORMID_GROUP, \
    CBashFORMID_LIST, CBashFORMID_LISTX2, CBashFORMID_OR_FLOAT32_LISTX2, \
    CBashFORMID_OR_FLOAT32_LISTX3, CBashFORMID_OR_STRING, CBashFORMID_OR_UINT32, \
    CBashFORMID_OR_UINT32_ARRAY, CBashFORMID_OR_UINT32_ARRAY_GROUP, \
    CBashFORMID_OR_UINT32_ARRAY_LIST, CBashFORMID_OR_UINT32_ARRAY_LISTX2, \
    CBashFORMIDARRAY, CBashFORMIDARRAY_LIST, CBashGeneric, CBashGeneric_GROUP, \
    CBashGeneric_LIST, CBashGeneric_LISTX2, CBashGeneric_LISTX3, CBashGrouped, \
    CBashInvertedFlag, CBashISTRING, CBashISTRING_GROUP, CBashISTRING_LIST, \
    CBashISTRING_LISTX2, CBashISTRINGARRAY, CBashIUNICODEARRAY, CBashJunk, CBashLIST, \
    CBashLIST_GROUP, CBashLIST_LIST, CBashLIST_LISTX2, CBashMaskedType, \
    CBashRECORDARRAY, CBashSINT16ARRAY, CBashSTRING, CBashSTRING_LIST, \
    CBashSTRING_LISTX2, CBashSUBRECORD, CBashSUBRECORDARRAY, CBashUINT8ARRAY, \
    CBashUINT8ARRAY_GROUP, CBashUINT8ARRAY_LIST, CBashUINT8ARRAY_LISTX2, \
    CBashUINT8ARRAY_LISTX3, CBashUINT32ARRAY, CBashUNICODE, \
    CBashUNKNOWN_OR_FORMID_OR_UINT32_LIST, CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX2, \
    CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX3, CBashUNKNOWN_OR_GENERIC, FormID, _CBash
from .oblivion import BaseComponent, Faction, ListComponent, ListX2Component, \
    ListX3Component, ObCollection, Var, VarX2, VarX3
from .utils import ExtractCopyList, SetCopyList, _encode, _unicode

if _CBash is not None:
    from .cbash import _CCleanModMasters, _CCopyRecord, _CCreateRecord, _CDeleteField, \
        _CDeleteRecord, _CGetCollectionIDByModID, _CGetCollectionIDByRecordID, _CGetField, \
        _CGetFieldAttribute, _CGetFileNameByID, _CGetIdenticalToMasterRecords, \
        _CGetLongIDName, _CGetModIDByRecordID, _CGetModNameByID, _CGetModNumEmptyGRUPs, \
        _CGetModNumOrphans, _CGetModNumTypes, _CGetModOrphansFormIDs, _CGetModTypes, \
        _CGetNumIdenticalToMasterRecords, _CGetNumRecordConflicts, _CGetRecordConflicts, \
        _CGetRecordHistory, _CGetRecordID, _CGetRecordUpdatedReferences, _CIsModEmpty, \
        _CIsRecordFormIDsInvalid, _CIsRecordWinning, _CLoadMod, _CResetRecord, _CSaveMod, \
        _CSetField, _CSetIDFields, _CUnloadMod, _CUnloadRecord, _CUpdateReferences


class FNVItem(ListComponent):
    __slots__ = []
    item = CBashFORMID_LIST(1)
    count = CBashGeneric_LIST(2, c_long)
    owner = CBashFORMID_LIST(3)
    globalOrRank = CBashUNKNOWN_OR_FORMID_OR_UINT32_LIST(4)
    condition = CBashFLOAT32_LIST(5)
    exportattrs = copyattrs = ['item', 'count', 'owner',
                               'globalOrRank', 'condition']

class FNVCondition(ListComponent):
    __slots__ = []
    operType = CBashGeneric_LIST(1, c_ubyte)
    unused1 = CBashUINT8ARRAY_LIST(2, 3)
    compValue = CBashFLOAT32_LIST(3)
    ifunc = CBashGeneric_LIST(4, c_ulong)
    param1 = CBashUNKNOWN_OR_FORMID_OR_UINT32_LIST(5)
    param2 = CBashUNKNOWN_OR_FORMID_OR_UINT32_LIST(6)
    runOn = CBashGeneric_LIST(7, c_ulong)
    reference = CBashUNKNOWN_OR_FORMID_OR_UINT32_LIST(8)
    IsEqual = CBashMaskedType('operType', 0xF0, 0x00, 'IsNotEqual')
    IsNotEqual = CBashMaskedType('operType', 0xF0, 0x20, 'IsEqual')
    IsGreater = CBashMaskedType('operType', 0xF0, 0x40, 'IsEqual')
    IsGreaterOrEqual = CBashMaskedType('operType', 0xF0, 0x60, 'IsEqual')
    IsLess = CBashMaskedType('operType', 0xF0, 0x80, 'IsEqual')
    IsLessOrEqual = CBashMaskedType('operType', 0xF0, 0xA0, 'IsEqual')
    IsOr = CBashBasicFlag('operType', 0x01)
    IsRunOnTarget = CBashBasicFlag('operType', 0x02)
    IsUseGlobal = CBashBasicFlag('operType', 0x04)
    IsResultOnSubject = CBashBasicType('runOn', 0, 'IsResultOnTarget')
    IsResultOnTarget = CBashBasicType('runOn', 1, 'IsResultOnSubject')
    IsResultOnReference = CBashBasicType('runOn', 2, 'IsResultOnSubject')
    IsResultOnCombatTarget = CBashBasicType('runOn', 3, 'IsResultOnSubject')
    IsResultOnLinkedReference = CBashBasicType('runOn', 4, 'IsResultOnSubject')
    exportattrs = copyattrs = ['operType', 'compValue', 'ifunc', 'param1',
                               'param2', 'runOn', 'reference']

class FNVConditionX2(ListX2Component):
    __slots__ = []
    operType = CBashGeneric_LISTX2(1, c_ubyte)
    unused1 = CBashUINT8ARRAY_LISTX2(2, 3)
    compValue = CBashFORMID_OR_FLOAT32_LISTX2(3)
    ifunc = CBashGeneric_LISTX2(4, c_ulong)
    param1 = CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX2(5)
    param2 = CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX2(6)
    runOn = CBashGeneric_LISTX2(7, c_ulong)
    reference = CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX2(8)
    IsEqual = CBashMaskedType('operType', 0xF0, 0x00, 'IsNotEqual')
    IsNotEqual = CBashMaskedType('operType', 0xF0, 0x20, 'IsEqual')
    IsGreater = CBashMaskedType('operType', 0xF0, 0x40, 'IsEqual')
    IsGreaterOrEqual = CBashMaskedType('operType', 0xF0, 0x60, 'IsEqual')
    IsLess = CBashMaskedType('operType', 0xF0, 0x80, 'IsEqual')
    IsLessOrEqual = CBashMaskedType('operType', 0xF0, 0xA0, 'IsEqual')
    IsOr = CBashBasicFlag('operType', 0x01)
    IsRunOnTarget = CBashBasicFlag('operType', 0x02)
    IsUseGlobal = CBashBasicFlag('operType', 0x04)
    IsResultOnSubject = CBashBasicType('runOn', 0, 'IsResultOnTarget')
    IsResultOnTarget = CBashBasicType('runOn', 1, 'IsResultOnSubject')
    IsResultOnReference = CBashBasicType('runOn', 2, 'IsResultOnSubject')
    IsResultOnCombatTarget = CBashBasicType('runOn', 3, 'IsResultOnSubject')
    IsResultOnLinkedReference = CBashBasicType('runOn', 4, 'IsResultOnSubject')
    exportattrs = copyattrs = ['operType', 'compValue', 'ifunc', 'param1',
                               'param2', 'runOn', 'reference']

class FNVConditionX3(ListX3Component):
    __slots__ = []
    operType = CBashGeneric_LISTX3(1, c_ubyte)
    unused1 = CBashUINT8ARRAY_LISTX3(2, 3)
    compValue = CBashFORMID_OR_FLOAT32_LISTX3(3)
    ifunc = CBashGeneric_LISTX3(4, c_ulong)
    param1 = CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX3(5)
    param2 = CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX3(6)
    runOn = CBashGeneric_LISTX3(7, c_ulong)
    reference = CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX3(8)
    IsEqual = CBashMaskedType('operType', 0xF0, 0x00, 'IsNotEqual')
    IsNotEqual = CBashMaskedType('operType', 0xF0, 0x20, 'IsEqual')
    IsGreater = CBashMaskedType('operType', 0xF0, 0x40, 'IsEqual')
    IsGreaterOrEqual = CBashMaskedType('operType', 0xF0, 0x60, 'IsEqual')
    IsLess = CBashMaskedType('operType', 0xF0, 0x80, 'IsEqual')
    IsLessOrEqual = CBashMaskedType('operType', 0xF0, 0xA0, 'IsEqual')
    IsOr = CBashBasicFlag('operType', 0x01)
    IsRunOnTarget = CBashBasicFlag('operType', 0x02)
    IsUseGlobal = CBashBasicFlag('operType', 0x04)
    IsResultOnSubject = CBashBasicType('runOn', 0, 'IsResultOnTarget')
    IsResultOnTarget = CBashBasicType('runOn', 1, 'IsResultOnSubject')
    IsResultOnReference = CBashBasicType('runOn', 2, 'IsResultOnSubject')
    IsResultOnCombatTarget = CBashBasicType('runOn', 3, 'IsResultOnSubject')
    IsResultOnLinkedReference = CBashBasicType('runOn', 4, 'IsResultOnSubject')
    exportattrs = copyattrs = ['operType', 'compValue', 'ifunc', 'param1',
                               'param2', 'runOn', 'reference']

class FNVEffect(ListComponent):
    __slots__ = []
    effect = CBashFORMID_LIST(1)
    magnitude = CBashGeneric_LIST(2, c_ulong)
    area = CBashGeneric_LIST(3, c_ulong)
    duration = CBashGeneric_LIST(4, c_ulong)
    rangeType = CBashGeneric_LIST(5, c_ulong)
    actorValue = CBashGeneric_LIST(6, c_long)

    def create_condition(self):
        length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 7, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, self._FieldID, self._ListIndex, 7, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVConditionX2(self._RecordID, self._FieldID, self._ListIndex, 7, length)
    conditions = CBashLIST_LIST(7, FNVConditionX2)
    conditions_list = CBashLIST_LIST(7, FNVConditionX2, True)

    IsSelf = CBashBasicType('rangeType', 0, 'IsTouch')
    IsTouch = CBashBasicType('rangeType', 1, 'IsSelf')
    IsTarget = CBashBasicType('rangeType', 2, 'IsSelf')
    exportattrs = copyattrs = ['effect', 'magnitude', 'area', 'duration',
                               'rangeType', 'actorValue', 'conditions_list']

class FNVRelation(ListComponent):
    __slots__ = []
    faction = CBashFORMID_LIST(1)
    mod = CBashGeneric_LIST(2, c_long)
    groupReactionType = CBashGeneric_LIST(3, c_ulong)

    IsNeutral = CBashBasicType('groupReactionType', 0, 'IsEnemy')
    IsEnemy = CBashBasicType('groupReactionType', 1, 'IsNeutral')
    IsAlly = CBashBasicType('groupReactionType', 2, 'IsNeutral')
    IsFriend = CBashBasicType('groupReactionType', 3, 'IsNeutral')
    exportattrs = copyattrs = ['faction', 'mod', 'groupReactionType']

class FNVAltTexture(ListComponent):
    __slots__ = []
    name = CBashSTRING_LIST(1)
    texture = CBashFORMID_LIST(2)
    index = CBashGeneric_LIST(3, c_long)
    exportattrs = copyattrs = ['name', 'texture', 'index']

class FNVDestructable(BaseComponent):
    __slots__ = []
    class Stage(ListComponent):
        __slots__ = []
        health = CBashGeneric_LIST(1, c_ubyte)
        index = CBashGeneric_LIST(2, c_ubyte)
        stage = CBashGeneric_LIST(3, c_ubyte)
        flags = CBashGeneric_LIST(4, c_ubyte)
        dps = CBashGeneric_LIST(5, c_long)
        explosion = CBashFORMID_LIST(6)
        debris = CBashFORMID_LIST(7)
        debrisCount = CBashGeneric_LIST(8, c_long)
        modPath = CBashISTRING_LIST(9)
        modt_p = CBashUINT8ARRAY_LIST(10)

        IsCapDamage = CBashBasicFlag('flags', 0x01)
        IsDisable = CBashBasicFlag('flags', 0x02)
        IsDestroy = CBashBasicFlag('flags', 0x04)
        copyattrs = ['health', 'index', 'stage',
                     'flags', 'dps', 'explosion',
                     'debris', 'debrisCount',
                     'modPath', 'modt_p']
        exportattrs = copyattrs[:]
        exportattrs.remove('modt_p')

    health = CBashGeneric_GROUP(0, c_long)
    count = CBashGeneric_GROUP(1, c_ubyte)
    flags = CBashGeneric_GROUP(2, c_ubyte)
    unused1 = CBashUINT8ARRAY_GROUP(3, 2)

    def create_stage(self):
        FieldID = self._FieldID + 4
        length = _CGetFieldAttribute(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Stage(self._RecordID, FieldID, length)
    stages = CBashLIST_GROUP(4, Stage)
    stages_list = CBashLIST_GROUP(4, Stage, True)
    IsVATSTargetable = CBashBasicFlag('flags', 0x01)
    exportattrs = copyattrs = ['health', 'count', 'flags', 'stages_list']

class WorldModel(BaseComponent):
    __slots__ = []
    modPath = CBashISTRING_GROUP(0)
    modt_p = CBashUINT8ARRAY_GROUP(1)

    def create_altTexture(self):
        FieldID = self._FieldID + 2
        length = _CGetFieldAttribute(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, FieldID, length)
    altTextures = CBashLIST_GROUP(2, FNVAltTexture)
    altTextures_list = CBashLIST_GROUP(2, FNVAltTexture, True)
    copyattrs = ['modPath', 'modt_p', 'altTextures_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

#--Fallout New Vegas
class FnvBaseRecord(object):
    __slots__ = ['_RecordID']
    _Type = 'BASE'
    def __init__(self, RecordID):
        self._RecordID = RecordID

    def __eq__(self, other):
        return self._RecordID == other._RecordID if type(other) is type(self) else False

    def __ne__(self, other):
        return not self.__eq__(other)

    def GetParentMod(self):
        return FnvModFile(_CGetModIDByRecordID(self._RecordID))

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
                        if conflict: conflicting.update(subconflicting)
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
        DestParentID, DestModID = (0, target._ModID) if not hasattr(self, '_ParentID') else (self._ParentID, target._ModID) if isinstance(target, FnvModFile) else (target._RecordID, target.GetParentMod()._ModID)
        RecordID = _CCopyRecord(self._RecordID, DestModID, DestParentID, 0, 0, c_ulong(0x00000003 if UseWinningParents else 0x00000001))
        return self.__class__(RecordID) if RecordID else None

    def CopyAsNew(self, target, UseWinningParents=False, RecordFormID=0):
        ##Record Creation Flags
        ##SetAsOverride       = 0x00000001
        ##CopyWinningParent   = 0x00000002
        DestParentID, DestModID = (0, target._ModID) if not hasattr(self, '_ParentID') else (self._ParentID, target._ModID) if isinstance(target, FnvModFile) else (target._RecordID, target.GetParentMod()._ModID)
        RecordID = _CCopyRecord(self._RecordID, DestModID, DestParentID, RecordFormID.GetShortFormID(target) if RecordFormID else 0, 0, c_ulong(0x00000002 if UseWinningParents else 0))
        return self.__class__(RecordID) if RecordID else None

    @property
    def Parent(self):
        RecordID = getattr(self, '_ParentID', None)
        if RecordID:
            _CGetFieldAttribute.restype = (c_char * 4)
            retValue = _CGetFieldAttribute(RecordID, 0, 0, 0, 0, 0, 0, 0, 0)
            _CGetFieldAttribute.restype = c_ulong
            return fnv_type_record[retValue.value](RecordID)
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

    versionControl1 = CBashUINT8ARRAY(3, 4)
    formVersion = CBashGeneric(5, c_ushort)
    versionControl2 = CBashUINT8ARRAY(6, 2)

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
    IsHasTreeLOD = CBashBasicFlag('flags1', 0x00000040)
    IsConstant = CBashAlias('IsHasTreeLOD')
    IsHiddenFromLocalMap = CBashAlias('IsHasTreeLOD')
    IsTurnOffFire = CBashBasicFlag('flags1', 0x00000080)
    IsInaccessible = CBashBasicFlag('flags1', 0x00000100)
    IsOnLocalMap = CBashBasicFlag('flags1', 0x00000200)
    IsMotionBlur = CBashAlias('IsOnLocalMap')
    IsPersistent = CBashBasicFlag('flags1', 0x00000400)
    IsQuest = CBashAlias('IsPersistent')
    IsQuestOrPersistent = CBashAlias('IsPersistent')
    IsInitiallyDisabled = CBashBasicFlag('flags1', 0x00000800)
    IsIgnored = CBashBasicFlag('flags1', 0x00001000)
    IsNoVoiceFilter = CBashBasicFlag('flags1', 0x00002000)
    IsVoiceFilter = CBashInvertedFlag('IsNoVoiceFilter')
    IsVisibleWhenDistant = CBashBasicFlag('flags1', 0x00008000)
    IsVWD = CBashAlias('IsVisibleWhenDistant')
    IsRandomAnimStartOrHighPriorityLOD = CBashBasicFlag('flags1', 0x00010000)
    IsRandomAnimStart = CBashAlias('IsRandomAnimStartOrHighPriorityLOD')
    IsHighPriorityLOD = CBashAlias('IsRandomAnimStartOrHighPriorityLOD')
    IsTalkingActivator = CBashBasicFlag('flags1', 0x00020000)
    IsCompressed = CBashBasicFlag('flags1', 0x00040000)
    IsPlatformSpecificTexture = CBashBasicFlag('flags1', 0x00080000)
    IsObstacleOrNoAIAcquire = CBashBasicFlag('flags1', 0x02000000)
    IsObstacle = CBashAlias('IsObstacleOrNoAIAcquire')
    IsNoAIAcquire = CBashAlias('IsObstacleOrNoAIAcquire')
    IsNavMeshFilter = CBashBasicFlag('flags1', 0x04000000)
    IsNavMeshBoundBox = CBashBasicFlag('flags1', 0x08000000)
    IsNonPipboyOrAutoReflected = CBashBasicFlag('flags1', 0x10000000)
    IsNonPipboy = CBashAlias('IsNonPipboyOrAutoReflected')
    IsAutoReflected = CBashAlias('IsNonPipboyOrAutoReflected')
    IsPipboy = CBashInvertedFlag('IsNonPipboyOrAutoReflected')
    IsChildUsableOrAutoRefracted = CBashBasicFlag('flags1', 0x20000000)
    IsChildUsable = CBashAlias('IsChildUsableOrAutoRefracted')
    IsAutoRefracted = CBashAlias('IsChildUsableOrAutoRefracted')
    IsNavMeshGround = CBashBasicFlag('flags1', 0x40000000)
    baseattrs = ['flags1', 'versionControl1', 'formVersion', 'versionControl2', 'eid']

class FnvTES4Record(object):
    __slots__ = ['_RecordID']
    _Type = 'TES4'
    def __init__(self, RecordID):
        self._RecordID = RecordID

    def GetParentMod(self):
        return FnvModFile(_CGetModIDByRecordID(self._RecordID))

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
    versionControl1 = CBashUINT8ARRAY(3, 4)
    formVersion = CBashGeneric(14, c_ushort)
    versionControl2 = CBashUINT8ARRAY(15, 2)
    version = CBashFLOAT32(5)
    numRecords = CBashGeneric(6, c_ulong)
    nextObject = CBashGeneric(7, c_ulong)
    ofst_p = CBashUINT8ARRAY(8)
    dele_p = CBashUINT8ARRAY(9)
    author = CBashUNICODE(10)
    description = CBashUNICODE(11)
    masters = CBashIUNICODEARRAY(12)
    DATA = CBashJunk(13)
    overrides = CBashFORMIDARRAY(16)
    screenshot_p = CBashUINT8ARRAY(17)

    IsESM = CBashBasicFlag('flags1', 0x00000001)
    exportattrs = copyattrs = ['flags1', 'versionControl1', 'formVersion', 'versionControl2', 'version', 'numRecords', 'nextObject',
                               'author', 'description', 'masters', 'overrides', 'screenshot_p']

class FnvACHRRecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 55, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'ACHR'
    class Decal(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        unknown1 = CBashUINT8ARRAY_LIST(2, 24)
        copyattrs = ['reference', 'unknown1']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')

    class ParentRef(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        delay = CBashFLOAT32_LIST(2)
        exportattrs = copyattrs = ['reference', 'delay']

    base = CBashFORMID(7)
    encounterZone = CBashFORMID(8)
    xrgd_p = CBashUINT8ARRAY(9)
    xrgb_p = CBashUINT8ARRAY(10)
    idleTime = CBashFLOAT32(11)
    idle = CBashFORMID(12)
    unused1 = CBashUINT8ARRAY(13, 4)
    numRefs = CBashGeneric(14, c_ulong)
    compiledSize = CBashGeneric(15, c_ulong)
    lastIndex = CBashGeneric(16, c_ulong)
    scriptType = CBashGeneric(17, c_ushort)
    scriptFlags = CBashGeneric(18, c_ushort)
    compiled_p = CBashUINT8ARRAY(19)
    scriptText = CBashISTRING(20)

    def create_var(self):
        length = _CGetFieldAttribute(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Var(self._RecordID, 21, length)
    vars = CBashLIST(21, Var)
    vars_list = CBashLIST(21, Var, True)

    references = CBashFORMID_OR_UINT32_ARRAY(22)
    topic = CBashFORMID(23)
    levelMod = CBashGeneric(24, c_long)
    merchantContainer = CBashFORMID(25)
    count = CBashGeneric(26, c_long)
    radius = CBashFLOAT32(27)
    health = CBashFLOAT32(28)

    def create_decal(self):
        length = _CGetFieldAttribute(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Decal(self._RecordID, 29, length)
    decals = CBashLIST(29, Decal)
    decals_list = CBashLIST(29, Decal, True)

    linkedReference = CBashFORMID(30)
    startRed = CBashGeneric(31, c_ubyte)
    startGreen = CBashGeneric(32, c_ubyte)
    startBlue = CBashGeneric(33, c_ubyte)
    unused2 = CBashUINT8ARRAY(34, 1)
    endRed = CBashGeneric(35, c_ubyte)
    endGreen = CBashGeneric(36, c_ubyte)
    endBlue = CBashGeneric(37, c_ubyte)
    unused3 = CBashUINT8ARRAY(38, 1)
    activateParentFlags = CBashGeneric(39, c_ubyte)

    def create_activateParentRef(self):
        length = _CGetFieldAttribute(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ParentRef(self._RecordID, 40, length)
    activateParentRefs = CBashLIST(40, ParentRef)
    activateParentRefs_list = CBashLIST(40, ParentRef, True)

    prompt = CBashSTRING(41)
    parent = CBashFORMID(42)
    parentFlags = CBashGeneric(43, c_ubyte)
    unused4 = CBashUINT8ARRAY(44, 3)
    emittance = CBashFORMID(45)
    boundRef = CBashFORMID(46)
    ignoredBySandbox = CBashGeneric(47, c_bool)
    scale = CBashFLOAT32(48)
    posX = CBashFLOAT32(49)
    posY = CBashFLOAT32(50)
    posZ = CBashFLOAT32(51)
    rotX = CBashFLOAT32(52)
    rotX_degrees = CBashDEGREES(52)
    rotY = CBashFLOAT32(53)
    rotY_degrees = CBashDEGREES(53)
    rotZ = CBashFLOAT32(54)
    rotZ_degrees = CBashDEGREES(54)

    IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

    IsOppositeParent = CBashBasicFlag('parentFlags', 0x00000001)
    IsPopIn = CBashBasicFlag('parentFlags', 0x00000002)

    IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
    IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
    IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')

    copyattrs = FnvBaseRecord.baseattrs + ['base', 'encounterZone', 'xrgd_p', 'xrgb_p',
                                           'idleTime', 'idle', 'numRefs', 'compiledSize',
                                           'lastIndex', 'scriptType', 'scriptFlags',
                                           'compiled_p', 'scriptText', 'vars_list',
                                           'references', 'topic', 'levelMod',
                                           'merchantContainer', 'count',
                                           'radius', 'health', 'decals_list',
                                           'linkedReference',
                                           'startRed', 'startGreen', 'startBlue',
                                           'endRed', 'endGreen', 'endBlue',
                                           'activateParentFlags',
                                           'activateParentRefs_list', 'prompt',
                                           'parent', 'parentFlags', 'emittance',
                                           'boundRef', 'ignoredBySandbox', 'scale',
                                           'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ']
    exportattrs = copyattrs[:]
    exportattrs.remove('xrgd_p')
    exportattrs.remove('xrgb_p')
    exportattrs.remove('compiled_p')

class FnvACRERecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 57, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'ACRE'
    class Decal(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        unknown1 = CBashUINT8ARRAY_LIST(2, 24)
        copyattrs = ['reference', 'unknown1']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')

    class ParentRef(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        delay = CBashFLOAT32_LIST(2)
        exportattrs = copyattrs = ['reference', 'delay']

    base = CBashFORMID(7)
    encounterZone = CBashFORMID(8)
    xrgd_p = CBashUINT8ARRAY(9)
    xrgb_p = CBashUINT8ARRAY(10)
    idleTime = CBashFLOAT32(11)
    idle = CBashFORMID(12)
    unused1 = CBashUINT8ARRAY(13, 4)
    numRefs = CBashGeneric(14, c_ulong)
    compiledSize = CBashGeneric(15, c_ulong)
    lastIndex = CBashGeneric(16, c_ulong)
    scriptType = CBashGeneric(17, c_ushort)
    scriptFlags = CBashGeneric(18, c_ushort)
    compiled_p = CBashUINT8ARRAY(19)
    scriptText = CBashISTRING(20)

    def create_var(self):
        length = _CGetFieldAttribute(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Var(self._RecordID, 21, length)
    vars = CBashLIST(21, Var)
    vars_list = CBashLIST(21, Var, True)

    references = CBashFORMID_OR_UINT32_ARRAY(22)
    topic = CBashFORMID(23)
    levelMod = CBashGeneric(24, c_long)
    owner = CBashFORMID(25)
    rank = CBashGeneric(26, c_long)
    merchantContainer = CBashFORMID(27)
    count = CBashGeneric(28, c_long)
    radius = CBashFLOAT32(29)
    health = CBashFLOAT32(30)

    def create_decal(self):
        length = _CGetFieldAttribute(self._RecordID, 31, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 31, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Decal(self._RecordID, 31, length)
    decals = CBashLIST(31, Decal)
    decals_list = CBashLIST(31, Decal, True)

    linkedReference = CBashFORMID(32)
    startRed = CBashGeneric(33, c_ubyte)
    startGreen = CBashGeneric(34, c_ubyte)
    startBlue = CBashGeneric(35, c_ubyte)
    unused2 = CBashUINT8ARRAY(36, 1)
    endRed = CBashGeneric(37, c_ubyte)
    endGreen = CBashGeneric(38, c_ubyte)
    endBlue = CBashGeneric(39, c_ubyte)
    unused3 = CBashUINT8ARRAY(40, 1)
    activateParentFlags = CBashGeneric(41, c_ubyte)

    def create_activateParentRef(self):
        length = _CGetFieldAttribute(self._RecordID, 42, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 42, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ParentRef(self._RecordID, 42, length)
    activateParentRefs = CBashLIST(42, ParentRef)
    activateParentRefs_list = CBashLIST(42, ParentRef, True)

    prompt = CBashSTRING(43)
    parent = CBashFORMID(44)
    parentFlags = CBashGeneric(45, c_ubyte)
    unused4 = CBashUINT8ARRAY(46, 3)
    emittance = CBashFORMID(47)
    boundRef = CBashFORMID(48)
    ignoredBySandbox = CBashGeneric(49, c_bool)
    scale = CBashFLOAT32(50)
    posX = CBashFLOAT32(51)
    posY = CBashFLOAT32(52)
    posZ = CBashFLOAT32(53)
    rotX = CBashFLOAT32(54)
    rotX_degrees = CBashDEGREES(54)
    rotY = CBashFLOAT32(55)
    rotY_degrees = CBashDEGREES(55)
    rotZ = CBashFLOAT32(56)
    rotZ_degrees = CBashDEGREES(56)

    IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

    IsOppositeParent = CBashBasicFlag('parentFlags', 0x00000001)
    IsPopIn = CBashBasicFlag('parentFlags', 0x00000002)

    IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
    IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
    IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')

    copyattrs = FnvBaseRecord.baseattrs + ['base', 'encounterZone', 'xrgd_p', 'xrgb_p',
                                           'idleTime', 'idle', 'numRefs', 'compiledSize',
                                           'lastIndex', 'scriptType', 'scriptFlags',
                                           'compiled_p', 'scriptText', 'vars_list',
                                           'references', 'topic', 'levelMod', 'owner',
                                           'rank', 'merchantContainer', 'count',
                                           'radius', 'health', 'decals_list',
                                           'linkedReference',
                                           'startRed', 'startGreen', 'startBlue',
                                           'endRed', 'endGreen', 'endBlue',
                                           'activateParentFlags',
                                           'activateParentRefs_list', 'prompt',
                                           'parent', 'parentFlags', 'emittance',
                                           'boundRef', 'ignoredBySandbox', 'scale',
                                           'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ']
    exportattrs = copyattrs[:]
    exportattrs.remove('xrgd_p')
    exportattrs.remove('xrgb_p')
    exportattrs.remove('compiled_p')

class FnvREFRRecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 141, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'REFR'
    class Decal(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        unknown1 = CBashUINT8ARRAY_LIST(2, 24)
        copyattrs = ['reference', 'unknown1']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')

    class ParentRef(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        delay = CBashFLOAT32_LIST(2)
        exportattrs = copyattrs = ['reference', 'delay']

    class ReflRefr(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        type = CBashGeneric_LIST(2, c_ulong)

        IsReflection = CBashBasicType('type', 0, 'IsRefraction')
        IsRefraction = CBashBasicType('type', 1, 'IsReflection')
        exportattrs = copyattrs = ['reference', 'type']

    base = CBashFORMID(7)
    encounterZone = CBashFORMID(8)
    xrgd_p = CBashUINT8ARRAY(9)
    xrgb_p = CBashUINT8ARRAY(10)
    idleTime = CBashFLOAT32(11)
    idle = CBashFORMID(12)
    unused1 = CBashUINT8ARRAY(13, 4)
    numRefs = CBashGeneric(14, c_ulong)
    compiledSize = CBashGeneric(15, c_ulong)
    lastIndex = CBashGeneric(16, c_ulong)
    scriptType = CBashGeneric(17, c_ushort)
    scriptFlags = CBashGeneric(18, c_ushort)
    compiled_p = CBashUINT8ARRAY(19)
    scriptText = CBashISTRING(20)

    def create_var(self):
        length = _CGetFieldAttribute(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Var(self._RecordID, 21, length)
    vars = CBashLIST(21, Var)
    vars_list = CBashLIST(21, Var, True)

    references = CBashFORMID_OR_UINT32_ARRAY(22)
    topic = CBashFORMID(23)
    levelMod = CBashGeneric(24, c_long)
    owner = CBashFORMID(25)
    rank = CBashGeneric(26, c_long)
    count = CBashGeneric(27, c_long)
    radius = CBashFLOAT32(28)
    health = CBashFLOAT32(29)
    radiation = CBashFLOAT32(30)
    charge = CBashFLOAT32(31)

    def create_decal(self):
        length = _CGetFieldAttribute(self._RecordID, 32, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 32, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Decal(self._RecordID, 32, length)
    decals = CBashLIST(32, Decal)
    decals_list = CBashLIST(32, Decal, True)

    linkedReference = CBashFORMID(33)
    startRed = CBashGeneric(34, c_ubyte)
    startRed = CBashGeneric(35, c_ubyte)
    startBlue = CBashGeneric(36, c_ubyte)
    unused2 = CBashUINT8ARRAY(37, 1)
    endRed = CBashGeneric(38, c_ubyte)
    endGreen = CBashGeneric(39, c_ubyte)
    endBlue = CBashGeneric(40, c_ubyte)
    unused3 = CBashUINT8ARRAY(41, 1)
    rclr_p = CBashUINT8ARRAY(42)
    activateParentFlags = CBashGeneric(43, c_ubyte)

    def create_activateParentRef(self):
        length = _CGetFieldAttribute(self._RecordID, 44, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 44, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ParentRef(self._RecordID, 44, length)
    activateParentRefs = CBashLIST(44, ParentRef)
    activateParentRefs_list = CBashLIST(44, ParentRef, True)

    prompt = CBashSTRING(45)
    parent = CBashFORMID(46)
    parentFlags = CBashGeneric(47, c_ubyte)
    unused4 = CBashUINT8ARRAY(48, 3)
    emittance = CBashFORMID(49)
    boundRef = CBashFORMID(50)
    primitiveX = CBashFLOAT32(51)
    primitiveY = CBashFLOAT32(52)
    primitiveZ = CBashFLOAT32(53)
    primitiveRed = CBashFLOAT32(54)
    primitiveGreen = CBashFLOAT32(55)
    primitiveBlue = CBashFLOAT32(56)
    primitiveUnknown = CBashFLOAT32(57)
    primitiveType = CBashGeneric(58, c_ulong)
    collisionType = CBashGeneric(59, c_ulong)
    extentX = CBashFLOAT32(60)
    extentY = CBashFLOAT32(61)
    extentZ = CBashFLOAT32(62)
    destinationFid = CBashFORMID(63)
    destinationPosX = CBashFLOAT32(64)
    destinationPosY = CBashFLOAT32(65)
    destinationPosZ = CBashFLOAT32(66)
    destinationRotX = CBashFLOAT32(67)
    destinationRotX_degrees = CBashDEGREES(67)
    destinationRotY = CBashFLOAT32(68)
    destinationRotY_degrees = CBashDEGREES(68)
    destinationRotZ = CBashFLOAT32(69)
    destinationRotZ_degrees = CBashDEGREES(69)
    destinationFlags = CBashGeneric(70, c_ulong)
    markerFlags = CBashGeneric(71, c_ubyte)
    markerFull = CBashSTRING(72)
    markerType = CBashGeneric(73, c_ubyte)
    unused5 = CBashUINT8ARRAY(74, 1)
    markerReputation = CBashFORMID(75)
    audioFull_p = CBashUINT8ARRAY(76)
    audioLocation = CBashFORMID(77)
    audioBnam_p = CBashUINT8ARRAY(78)
    audioUnknown1 = CBashFLOAT32(79)
    audioUnknown2 = CBashFLOAT32(80)
    xsrf_p = CBashUINT8ARRAY(81)
    xsrd_p = CBashUINT8ARRAY(82)
    target = CBashFORMID(83)
    rangeRadius = CBashFLOAT32(84)
    rangeType = CBashGeneric(85, c_ulong)
    staticPercentage = CBashFLOAT32(86)
    positionReference = CBashFORMID(87)
    lockLevel = CBashGeneric(88, c_ubyte)
    unused6 = CBashUINT8ARRAY(89, 3)
    lockKey = CBashFORMID(90)
    lockFlags = CBashGeneric(91, c_ubyte)
    unused7 = CBashUINT8ARRAY(92, 3)
    lockUnknown1 = CBashUINT8ARRAY(93)
    ammo = CBashFORMID(94)
    ammoCount = CBashGeneric(95, c_long)

    def create_reflrefr(self):
        length = _CGetFieldAttribute(self._RecordID, 96, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 96, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ReflRefr(self._RecordID, 96, length)
    reflrefrs = CBashLIST(96, ReflRefr)
    reflrefrs_list = CBashLIST(96, ReflRefr, True)

    litWaters = CBashFORMIDARRAY(97)
    actionFlags = CBashGeneric(98, c_ulong)
    navMesh = CBashFORMID(99)
    navUnknown1 = CBashGeneric(100, c_ushort)
    unused8 = CBashUINT8ARRAY(101, 2)
    portalLinkedRoom1 = CBashFORMID(102)
    portalLinkedRoom2 = CBashFORMID(103)
    portalWidth = CBashFLOAT32(104)
    portalHeight = CBashFLOAT32(105)
    portalPosX = CBashFLOAT32(106)
    portalPosY = CBashFLOAT32(107)
    portalPosZ = CBashFLOAT32(108)
    portalQ1 = CBashFLOAT32(109)
    portalQ2 = CBashFLOAT32(110)
    portalQ3 = CBashFLOAT32(111)
    portalQ4 = CBashFLOAT32(112)
    seed = CBashGeneric(113, c_ubyte)
    roomCount = CBashGeneric(114, c_ushort)
    roomUnknown1 = CBashUINT8ARRAY(115)
    rooms = CBashFORMIDARRAY(116)
    occPlaneWidth = CBashFLOAT32(117)
    occPlaneHeight = CBashFLOAT32(118)
    occPlanePosX = CBashFLOAT32(119)
    occPlanePosY = CBashFLOAT32(120)
    occPlanePosZ = CBashFLOAT32(121)
    occPlaneQ1 = CBashFLOAT32(122)
    occPlaneQ2 = CBashFLOAT32(123)
    occPlaneQ3 = CBashFLOAT32(124)
    occPlaneQ4 = CBashFLOAT32(125)
    occPlaneRight = CBashFORMID(126)
    occPlaneLeft = CBashFORMID(127)
    occPlaneBottom = CBashFORMID(128)
    occPlaneTop = CBashFORMID(129)
    lod1 = CBashFLOAT32(130)
    lod2 = CBashFLOAT32(131)
    lod3 = CBashFLOAT32(132)
    ignoredBySandbox = CBashGeneric(133, c_bool)
    scale = CBashFLOAT32(134)
    posX = CBashFLOAT32(135)
    posY = CBashFLOAT32(136)
    posZ = CBashFLOAT32(137)
    rotX = CBashFLOAT32(138)
    rotX_degrees = CBashDEGREES(138)
    rotY = CBashFLOAT32(139)
    rotY_degrees = CBashDEGREES(139)
    rotZ = CBashFLOAT32(140)
    rotZ_degrees = CBashDEGREES(140)

    IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

    IsNoAlarm = CBashBasicFlag('destinationFlags', 0x00000001)

    IsVisible = CBashBasicFlag('markerFlags', 0x00000001)
    IsCanTravelTo = CBashBasicFlag('markerFlags', 0x00000002)

    IsUseDefault = CBashBasicFlag('actionFlags', 0x00000001)
    IsActivate = CBashBasicFlag('actionFlags', 0x00000002)
    IsOpen = CBashBasicFlag('actionFlags', 0x00000004)
    IsOpenByDefault = CBashBasicFlag('actionFlags', 0x00000008)

    IsOppositeParent = CBashBasicFlag('parentFlags', 0x00000001)
    IsPopIn = CBashBasicFlag('parentFlags', 0x00000002)

    IsLeveledLock = CBashBasicFlag('lockFlags', 0x00000004)

    IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
    IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
    IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')

    IsNone = CBashBasicType('primitiveType', 0, 'IsBox')
    IsBox = CBashBasicType('primitiveType', 1, 'IsNone')
    IsSphere = CBashBasicType('primitiveType', 2, 'IsNone')
    IsPortalBox = CBashBasicType('primitiveType', 3, 'IsNone')

    IsUnidentified = CBashBasicType('collisionType', 0, 'IsStatic')
    IsStatic = CBashBasicType('collisionType', 1, 'IsUnidentified')
    IsAnimStatic = CBashBasicType('collisionType', 2, 'IsUnidentified')
    IsTransparent = CBashBasicType('collisionType', 3, 'IsUnidentified')
    IsClutter = CBashBasicType('collisionType', 4, 'IsUnidentified')
    IsWeapon = CBashBasicType('collisionType', 5, 'IsUnidentified')
    IsProjectile = CBashBasicType('collisionType', 6, 'IsUnidentified')
    IsSpell = CBashBasicType('collisionType', 7, 'IsUnidentified')
    IsBiped = CBashBasicType('collisionType', 8, 'IsUnidentified')
    IsTrees = CBashBasicType('collisionType', 9, 'IsUnidentified')
    IsProps = CBashBasicType('collisionType', 10, 'IsUnidentified')
    IsWater = CBashBasicType('collisionType', 11, 'IsUnidentified')
    IsTrigger = CBashBasicType('collisionType', 12, 'IsUnidentified')
    IsTerrain = CBashBasicType('collisionType', 13, 'IsUnidentified')
    IsTrap = CBashBasicType('collisionType', 14, 'IsUnidentified')
    IsNonCollidable = CBashBasicType('collisionType', 15, 'IsUnidentified')
    IsCloudTrap = CBashBasicType('collisionType', 16, 'IsUnidentified')
    IsGround = CBashBasicType('collisionType', 17, 'IsUnidentified')
    IsPortal = CBashBasicType('collisionType', 18, 'IsUnidentified')
    IsDebrisSmall = CBashBasicType('collisionType', 19, 'IsUnidentified')
    IsDebrisLarge = CBashBasicType('collisionType', 20, 'IsUnidentified')
    IsAcousticSpace = CBashBasicType('collisionType', 21, 'IsUnidentified')
    IsActorZone = CBashBasicType('collisionType', 22, 'IsUnidentified')
    IsProjectileZone = CBashBasicType('collisionType', 23, 'IsUnidentified')
    IsGasTrap = CBashBasicType('collisionType', 24, 'IsUnidentified')
    IsShellCasing = CBashBasicType('collisionType', 25, 'IsUnidentified')
    IsTransparentSmall = CBashBasicType('collisionType', 26, 'IsUnidentified')
    IsInvisibleWall = CBashBasicType('collisionType', 27, 'IsUnidentified')
    IsTransparentSmallAnim = CBashBasicType('collisionType', 28, 'IsUnidentified')
    IsDeadBip = CBashBasicType('collisionType', 29, 'IsUnidentified')
    IsCharController = CBashBasicType('collisionType', 30, 'IsUnidentified')
    IsAvoidBox = CBashBasicType('collisionType', 31, 'IsUnidentified')
    IsCollisionBox = CBashBasicType('collisionType', 32, 'IsUnidentified')
    IsCameraSphere = CBashBasicType('collisionType', 33, 'IsUnidentified')
    IsDoorDetection = CBashBasicType('collisionType', 34, 'IsUnidentified')
    IsCameraPick = CBashBasicType('collisionType', 35, 'IsUnidentified')
    IsItemPick = CBashBasicType('collisionType', 36, 'IsUnidentified')
    IsLineOfSight = CBashBasicType('collisionType', 37, 'IsUnidentified')
    IsPathPick = CBashBasicType('collisionType', 38, 'IsUnidentified')
    IsCustomPick1 = CBashBasicType('collisionType', 39, 'IsUnidentified')
    IsCustomPick2 = CBashBasicType('collisionType', 40, 'IsUnidentified')
    IsSpellExplosion = CBashBasicType('collisionType', 41, 'IsUnidentified')
    IsDroppingPick = CBashBasicType('collisionType', 42, 'IsUnidentified')

    IsMarkerNone = CBashBasicType('markerType', 0, 'IsMarkerNone')
    IsCity = CBashBasicType('markerType', 1, 'IsMarkerNone')
    IsSettlement = CBashBasicType('markerType', 2, 'IsMarkerNone')
    IsEncampment = CBashBasicType('markerType', 3, 'IsMarkerNone')
    IsNaturalLandmark = CBashBasicType('markerType', 4, 'IsMarkerNone')
    IsCave = CBashBasicType('markerType', 5, 'IsMarkerNone')
    IsFactory = CBashBasicType('markerType', 6, 'IsMarkerNone')
    IsMonument = CBashBasicType('markerType', 7, 'IsMarkerNone')
    IsMilitary = CBashBasicType('markerType', 8, 'IsMarkerNone')
    IsOffice = CBashBasicType('markerType', 9, 'IsMarkerNone')
    IsTownRuins = CBashBasicType('markerType', 10, 'IsMarkerNone')
    IsUrbanRuins = CBashBasicType('markerType', 11, 'IsMarkerNone')
    IsSewerRuins = CBashBasicType('markerType', 12, 'IsMarkerNone')
    IsMetro = CBashBasicType('markerType', 13, 'IsMarkerNone')
    IsVault = CBashBasicType('markerType', 14, 'IsMarkerNone')

    IsRadius = CBashBasicType('rangeType', 0, 'IsEverywhere')
    IsEverywhere = CBashBasicType('rangeType', 1, 'IsRadius')
    IsWorldAndLinkedInteriors = CBashBasicType('rangeType', 2, 'IsRadius')
    IsLinkedInteriors = CBashBasicType('rangeType', 3, 'IsRadius')
    IsCurrentCellOnly = CBashBasicType('rangeType', 4, 'IsRadius')
    copyattrs = FnvBaseRecord.baseattrs + ['base', 'encounterZone', 'xrgd_p', 'xrgb_p',
                                           'idleTime', 'idle', 'numRefs',
                                           'compiledSize', 'lastIndex', 'scriptType',
                                           'scriptFlags', 'compiled_p', 'scriptText',
                                           'vars_list', 'references', 'topic', 'levelMod',
                                           'owner', 'rank', 'count', 'radius', 'health',
                                           'radiation', 'charge', 'decals_list',
                                           'linkedReference',
                                           'startRed', 'startRed', 'startBlue',
                                           'endRed', 'endGreen', 'endBlue',
                                           'rclr_p', 'activateParentFlags',
                                           'activateParentRefs_list', 'prompt', 'parent',
                                           'parentFlags', 'emittance', 'boundRef',
                                           'primitiveX', 'primitiveY', 'primitiveZ',
                                           'primitiveRed', 'primitiveGreen', 'primitiveBlue',
                                           'primitiveUnknown', 'primitiveType',
                                           'collisionType', 'extentX', 'extentY', 'extentZ',
                                           'destinationFid', 'destinationPosX',
                                           'destinationPosY', 'destinationPosZ',
                                           'destinationRotX', 'destinationRotY',
                                           'destinationRotZ', 'destinationFlags',
                                           'markerFlags', 'markerFull', 'markerType',
                                           'markerReputation', 'audioFull_p', 'audioLocation',
                                           'audioBnam_p', 'audioUnknown1', 'audioUnknown2',
                                           'xsrf_p', 'xsrd_p', 'target', 'rangeRadius',
                                           'rangeType', 'staticPercentage', 'positionReference',
                                           'lockLevel', 'lockKey', 'lockFlags', 'lockUnknown1',
                                           'ammo', 'ammoCount', 'reflrefrs_list', 'litWaters',
                                           'actionFlags', 'navMesh', 'navUnknown1',
                                           'portalLinkedRoom1', 'portalLinkedRoom2',
                                           'portalWidth', 'portalHeight', 'portalPosX',
                                           'portalPosY', 'portalPosZ', 'portalQ1', 'portalQ2',
                                           'portalQ3', 'portalQ4', 'seed', 'roomCount',
                                           'roomUnknown1', 'rooms', 'occPlaneWidth',
                                           'occPlaneHeight', 'occPlanePosX', 'occPlanePosY',
                                           'occPlanePosZ', 'occPlaneQ1', 'occPlaneQ2',
                                           'occPlaneQ3', 'occPlaneQ4', 'occPlaneRight',
                                           'occPlaneLeft', 'occPlaneBottom', 'occPlaneTop',
                                           'lod1', 'lod2', 'lod3', 'ignoredBySandbox',
                                           'scale', 'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ']
    exportattrs = copyattrs[:]
    exportattrs.remove('xsrf_p')
    exportattrs.remove('xsrd_p')
    exportattrs.remove('audioBnam_p')
    exportattrs.remove('audioFull_p')
    exportattrs.remove('rclr_p')
    exportattrs.remove('xrgd_p')
    exportattrs.remove('xrgb_p')
    exportattrs.remove('compiled_p')

class FnvPGRERecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 56, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'PGRE'
    class Decal(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        unknown1 = CBashUINT8ARRAY_LIST(2, 24)
        copyattrs = ['reference', 'unknown1']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')

    class ParentRef(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        delay = CBashFLOAT32_LIST(2)
        exportattrs = copyattrs = ['reference', 'delay']

    class ReflRefr(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        type = CBashGeneric_LIST(2, c_ulong)

        IsReflection = CBashBasicType('type', 0, 'IsRefraction')
        IsRefraction = CBashBasicType('type', 1, 'IsReflection')
        exportattrs = copyattrs = ['reference', 'type']

    base = CBashFORMID(7)
    encounterZone = CBashFORMID(8)
    xrgd_p = CBashUINT8ARRAY(9)
    xrgb_p = CBashUINT8ARRAY(10)
    idleTime = CBashFLOAT32(11)
    idle = CBashFORMID(12)
    unused1 = CBashUINT8ARRAY(13, 4)
    numRefs = CBashGeneric(14, c_ulong)
    compiledSize = CBashGeneric(15, c_ulong)
    lastIndex = CBashGeneric(16, c_ulong)
    scriptType = CBashGeneric(17, c_ushort)
    scriptFlags = CBashGeneric(18, c_ushort)
    compiled_p = CBashUINT8ARRAY(19)
    scriptText = CBashISTRING(20)

    def create_var(self):
        length = _CGetFieldAttribute(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Var(self._RecordID, 21, length)
    vars = CBashLIST(21, Var)
    vars_list = CBashLIST(21, Var, True)

    references = CBashFORMID_OR_UINT32_ARRAY(22)
    topic = CBashFORMID(23)
    owner = CBashFORMID(24)
    rank = CBashGeneric(25, c_long)
    count = CBashGeneric(26, c_long)
    radius = CBashFLOAT32(27)
    health = CBashFLOAT32(28)

    def create_decal(self):
        length = _CGetFieldAttribute(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Decal(self._RecordID, 29, length)
    decals = CBashLIST(29, Decal)
    decals_list = CBashLIST(29, Decal, True)

    linkedReference = CBashFORMID(30)
    startRed = CBashGeneric(31, c_ubyte)
    startGreen = CBashGeneric(32, c_ubyte)
    startBlue = CBashGeneric(33, c_ubyte)
    unused2 = CBashUINT8ARRAY(34, 1)
    endRed = CBashGeneric(35, c_ubyte)
    endGreen = CBashGeneric(36, c_ubyte)
    endBlue = CBashGeneric(37, c_ubyte)
    unused3 = CBashUINT8ARRAY(38, 1)
    activateParentFlags = CBashGeneric(39, c_ubyte)

    def create_activateParentRef(self):
        length = _CGetFieldAttribute(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ParentRef(self._RecordID, 40, length)
    activateParentRefs = CBashLIST(40, ParentRef)
    activateParentRefs_list = CBashLIST(40, ParentRef, True)

    prompt = CBashSTRING(41)
    parent = CBashFORMID(42)
    parentFlags = CBashGeneric(43, c_ubyte)
    unused4 = CBashUINT8ARRAY(44, 3)
    emittance = CBashFORMID(45)
    boundRef = CBashFORMID(46)

    def create_reflrefr(self):
        length = _CGetFieldAttribute(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ReflRefr(self._RecordID, 47, length)
    reflrefrs = CBashLIST(47, ReflRefr)
    reflrefrs_list = CBashLIST(47, ReflRefr, True)

    ignoredBySandbox = CBashGeneric(48, c_bool)
    scale = CBashFLOAT32(49)
    posX = CBashFLOAT32(50)
    posY = CBashFLOAT32(51)
    posZ = CBashFLOAT32(52)
    rotX = CBashFLOAT32(53)
    rotX_degrees = CBashDEGREES(53)
    rotY = CBashFLOAT32(54)
    rotY_degrees = CBashDEGREES(54)
    rotZ = CBashFLOAT32(55)
    rotZ_degrees = CBashDEGREES(55)

    IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

    IsOppositeParent = CBashBasicFlag('parentFlags', 0x00000001)
    IsPopIn = CBashBasicFlag('parentFlags', 0x00000002)

    IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
    IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
    IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')

    copyattrs = FnvBaseRecord.baseattrs + ['base', 'encounterZone', 'xrgd_p', 'xrgb_p',
                                           'idleTime', 'idle', 'numRefs', 'compiledSize',
                                           'lastIndex', 'scriptType', 'scriptFlags',
                                           'compiled_p', 'scriptText', 'vars_list',
                                           'references', 'topic', 'owner',
                                           'rank', 'count',
                                           'radius', 'health', 'decals_list',
                                           'linkedReference',
                                           'startRed', 'startGreen', 'startBlue',
                                           'endRed', 'endGreen', 'endBlue',
                                           'activateParentFlags',
                                           'activateParentRefs_list', 'prompt',
                                           'parent', 'parentFlags', 'emittance',
                                           'boundRef', 'reflrefrs_list',
                                           'ignoredBySandbox', 'scale',
                                           'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ']
    exportattrs = copyattrs[:]
    exportattrs.remove('xrgd_p')
    exportattrs.remove('xrgb_p')
    exportattrs.remove('compiled_p')

class FnvPMISRecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 56, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'PMIS'
    class Decal(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        unknown1 = CBashUINT8ARRAY_LIST(2, 24)
        copyattrs = ['reference', 'unknown1']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')

    class ParentRef(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        delay = CBashFLOAT32_LIST(2)
        exportattrs = copyattrs = ['reference', 'delay']

    class ReflRefr(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        type = CBashGeneric_LIST(2, c_ulong)

        IsReflection = CBashBasicType('type', 0, 'IsRefraction')
        IsRefraction = CBashBasicType('type', 1, 'IsReflection')
        exportattrs = copyattrs = ['reference', 'type']

    base = CBashFORMID(7)
    encounterZone = CBashFORMID(8)
    xrgd_p = CBashUINT8ARRAY(9)
    xrgb_p = CBashUINT8ARRAY(10)
    idleTime = CBashFLOAT32(11)
    idle = CBashFORMID(12)
    unused1 = CBashUINT8ARRAY(13, 4)
    numRefs = CBashGeneric(14, c_ulong)
    compiledSize = CBashGeneric(15, c_ulong)
    lastIndex = CBashGeneric(16, c_ulong)
    scriptType = CBashGeneric(17, c_ushort)
    scriptFlags = CBashGeneric(18, c_ushort)
    compiled_p = CBashUINT8ARRAY(19)
    scriptText = CBashISTRING(20)

    def create_var(self):
        length = _CGetFieldAttribute(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Var(self._RecordID, 21, length)
    vars = CBashLIST(21, Var)
    vars_list = CBashLIST(21, Var, True)

    references = CBashFORMID_OR_UINT32_ARRAY(22)
    topic = CBashFORMID(23)
    owner = CBashFORMID(24)
    rank = CBashGeneric(25, c_long)
    count = CBashGeneric(26, c_long)
    radius = CBashFLOAT32(27)
    health = CBashFLOAT32(28)

    def create_decal(self):
        length = _CGetFieldAttribute(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Decal(self._RecordID, 29, length)
    decals = CBashLIST(29, Decal)
    decals_list = CBashLIST(29, Decal, True)

    linkedReference = CBashFORMID(30)
    startRed = CBashGeneric(31, c_ubyte)
    startGreen = CBashGeneric(32, c_ubyte)
    startBlue = CBashGeneric(33, c_ubyte)
    unused2 = CBashUINT8ARRAY(34, 1)
    endRed = CBashGeneric(35, c_ubyte)
    endGreen = CBashGeneric(36, c_ubyte)
    endBlue = CBashGeneric(37, c_ubyte)
    unused3 = CBashUINT8ARRAY(38, 1)
    activateParentFlags = CBashGeneric(39, c_ubyte)

    def create_activateParentRef(self):
        length = _CGetFieldAttribute(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ParentRef(self._RecordID, 40, length)
    activateParentRefs = CBashLIST(40, ParentRef)
    activateParentRefs_list = CBashLIST(40, ParentRef, True)

    prompt = CBashSTRING(41)
    parent = CBashFORMID(42)
    parentFlags = CBashGeneric(43, c_ubyte)
    unused4 = CBashUINT8ARRAY(44, 3)
    emittance = CBashFORMID(45)
    boundRef = CBashFORMID(46)

    def create_reflrefr(self):
        length = _CGetFieldAttribute(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ReflRefr(self._RecordID, 47, length)
    reflrefrs = CBashLIST(47, ReflRefr)
    reflrefrs_list = CBashLIST(47, ReflRefr, True)

    ignoredBySandbox = CBashGeneric(48, c_bool)
    scale = CBashFLOAT32(49)
    posX = CBashFLOAT32(50)
    posY = CBashFLOAT32(51)
    posZ = CBashFLOAT32(52)
    rotX = CBashFLOAT32(53)
    rotX_degrees = CBashDEGREES(53)
    rotY = CBashFLOAT32(54)
    rotY_degrees = CBashDEGREES(54)
    rotZ = CBashFLOAT32(55)
    rotZ_degrees = CBashDEGREES(55)

    IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

    IsOppositeParent = CBashBasicFlag('parentFlags', 0x00000001)
    IsPopIn = CBashBasicFlag('parentFlags', 0x00000002)

    IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
    IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
    IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')

    copyattrs = FnvBaseRecord.baseattrs + ['base', 'encounterZone', 'xrgd_p', 'xrgb_p',
                                           'idleTime', 'idle', 'numRefs', 'compiledSize',
                                           'lastIndex', 'scriptType', 'scriptFlags',
                                           'compiled_p', 'scriptText', 'vars_list',
                                           'references', 'topic', 'owner',
                                           'rank', 'count',
                                           'radius', 'health', 'decals_list',
                                           'linkedReference',
                                           'startRed', 'startGreen', 'startBlue',
                                           'endRed', 'endGreen', 'endBlue',
                                           'activateParentFlags',
                                           'activateParentRefs_list', 'prompt',
                                           'parent', 'parentFlags', 'emittance',
                                           'boundRef', 'reflrefrs_list',
                                           'ignoredBySandbox', 'scale',
                                           'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ']
    exportattrs = copyattrs[:]
    exportattrs.remove('xrgd_p')
    exportattrs.remove('xrgb_p')
    exportattrs.remove('compiled_p')

class FnvPBEARecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 56, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'PBEA'
    class Decal(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        unknown1 = CBashUINT8ARRAY_LIST(2, 24)
        copyattrs = ['reference', 'unknown1']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')

    class ParentRef(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        delay = CBashFLOAT32_LIST(2)
        exportattrs = copyattrs = ['reference', 'delay']

    class ReflRefr(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        type = CBashGeneric_LIST(2, c_ulong)

        IsReflection = CBashBasicType('type', 0, 'IsRefraction')
        IsRefraction = CBashBasicType('type', 1, 'IsReflection')
        exportattrs = copyattrs = ['reference', 'type']

    base = CBashFORMID(7)
    encounterZone = CBashFORMID(8)
    xrgd_p = CBashUINT8ARRAY(9)
    xrgb_p = CBashUINT8ARRAY(10)
    idleTime = CBashFLOAT32(11)
    idle = CBashFORMID(12)
    unused1 = CBashUINT8ARRAY(13, 4)
    numRefs = CBashGeneric(14, c_ulong)
    compiledSize = CBashGeneric(15, c_ulong)
    lastIndex = CBashGeneric(16, c_ulong)
    scriptType = CBashGeneric(17, c_ushort)
    scriptFlags = CBashGeneric(18, c_ushort)
    compiled_p = CBashUINT8ARRAY(19)
    scriptText = CBashISTRING(20)

    def create_var(self):
        length = _CGetFieldAttribute(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Var(self._RecordID, 21, length)
    vars = CBashLIST(21, Var)
    vars_list = CBashLIST(21, Var, True)

    references = CBashFORMID_OR_UINT32_ARRAY(22)
    topic = CBashFORMID(23)
    owner = CBashFORMID(24)
    rank = CBashGeneric(25, c_long)
    count = CBashGeneric(26, c_long)
    radius = CBashFLOAT32(27)
    health = CBashFLOAT32(28)

    def create_decal(self):
        length = _CGetFieldAttribute(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Decal(self._RecordID, 29, length)
    decals = CBashLIST(29, Decal)
    decals_list = CBashLIST(29, Decal, True)

    linkedReference = CBashFORMID(30)
    startRed = CBashGeneric(31, c_ubyte)
    startGreen = CBashGeneric(32, c_ubyte)
    startBlue = CBashGeneric(33, c_ubyte)
    unused2 = CBashUINT8ARRAY(34, 1)
    endRed = CBashGeneric(35, c_ubyte)
    endGreen = CBashGeneric(36, c_ubyte)
    endBlue = CBashGeneric(37, c_ubyte)
    unused3 = CBashUINT8ARRAY(38, 1)
    activateParentFlags = CBashGeneric(39, c_ubyte)

    def create_activateParentRef(self):
        length = _CGetFieldAttribute(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ParentRef(self._RecordID, 40, length)
    activateParentRefs = CBashLIST(40, ParentRef)
    activateParentRefs_list = CBashLIST(40, ParentRef, True)

    prompt = CBashSTRING(41)
    parent = CBashFORMID(42)
    parentFlags = CBashGeneric(43, c_ubyte)
    unused4 = CBashUINT8ARRAY(44, 3)
    emittance = CBashFORMID(45)
    boundRef = CBashFORMID(46)

    def create_reflrefr(self):
        length = _CGetFieldAttribute(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ReflRefr(self._RecordID, 47, length)
    reflrefrs = CBashLIST(47, ReflRefr)
    reflrefrs_list = CBashLIST(47, ReflRefr, True)

    ignoredBySandbox = CBashGeneric(48, c_bool)
    scale = CBashFLOAT32(49)
    posX = CBashFLOAT32(50)
    posY = CBashFLOAT32(51)
    posZ = CBashFLOAT32(52)
    rotX = CBashFLOAT32(53)
    rotX_degrees = CBashDEGREES(53)
    rotY = CBashFLOAT32(54)
    rotY_degrees = CBashDEGREES(54)
    rotZ = CBashFLOAT32(55)
    rotZ_degrees = CBashDEGREES(55)

    IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

    IsOppositeParent = CBashBasicFlag('parentFlags', 0x00000001)
    IsPopIn = CBashBasicFlag('parentFlags', 0x00000002)

    IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
    IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
    IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')

    copyattrs = FnvBaseRecord.baseattrs + ['base', 'encounterZone', 'xrgd_p', 'xrgb_p',
                                           'idleTime', 'idle', 'numRefs', 'compiledSize',
                                           'lastIndex', 'scriptType', 'scriptFlags',
                                           'compiled_p', 'scriptText', 'vars_list',
                                           'references', 'topic', 'owner',
                                           'rank', 'count',
                                           'radius', 'health', 'decals_list',
                                           'linkedReference',
                                           'startRed', 'startGreen', 'startBlue',
                                           'endRed', 'endGreen', 'endBlue',
                                           'activateParentFlags',
                                           'activateParentRefs_list', 'prompt',
                                           'parent', 'parentFlags', 'emittance',
                                           'boundRef', 'reflrefrs_list',
                                           'ignoredBySandbox', 'scale',
                                           'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ']
    exportattrs = copyattrs[:]
    exportattrs.remove('xrgd_p')
    exportattrs.remove('xrgb_p')
    exportattrs.remove('compiled_p')

class FnvPFLARecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 56, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'PFLA'
    class Decal(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        unknown1 = CBashUINT8ARRAY_LIST(2, 24)
        copyattrs = ['reference', 'unknown1']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')

    class ParentRef(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        delay = CBashFLOAT32_LIST(2)
        exportattrs = copyattrs = ['reference', 'delay']

    class ReflRefr(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        type = CBashGeneric_LIST(2, c_ulong)

        IsReflection = CBashBasicType('type', 0, 'IsRefraction')
        IsRefraction = CBashBasicType('type', 1, 'IsReflection')
        exportattrs = copyattrs = ['reference', 'type']

    base = CBashFORMID(7)
    encounterZone = CBashFORMID(8)
    xrgd_p = CBashUINT8ARRAY(9)
    xrgb_p = CBashUINT8ARRAY(10)
    idleTime = CBashFLOAT32(11)
    idle = CBashFORMID(12)
    unused1 = CBashUINT8ARRAY(13, 4)
    numRefs = CBashGeneric(14, c_ulong)
    compiledSize = CBashGeneric(15, c_ulong)
    lastIndex = CBashGeneric(16, c_ulong)
    scriptType = CBashGeneric(17, c_ushort)
    scriptFlags = CBashGeneric(18, c_ushort)
    compiled_p = CBashUINT8ARRAY(19)
    scriptText = CBashISTRING(20)

    def create_var(self):
        length = _CGetFieldAttribute(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Var(self._RecordID, 21, length)
    vars = CBashLIST(21, Var)
    vars_list = CBashLIST(21, Var, True)

    references = CBashFORMID_OR_UINT32_ARRAY(22)
    topic = CBashFORMID(23)
    owner = CBashFORMID(24)
    rank = CBashGeneric(25, c_long)
    count = CBashGeneric(26, c_long)
    radius = CBashFLOAT32(27)
    health = CBashFLOAT32(28)

    def create_decal(self):
        length = _CGetFieldAttribute(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Decal(self._RecordID, 29, length)
    decals = CBashLIST(29, Decal)
    decals_list = CBashLIST(29, Decal, True)

    linkedReference = CBashFORMID(30)
    startRed = CBashGeneric(31, c_ubyte)
    startGreen = CBashGeneric(32, c_ubyte)
    startBlue = CBashGeneric(33, c_ubyte)
    unused2 = CBashUINT8ARRAY(34, 1)
    endRed = CBashGeneric(35, c_ubyte)
    endGreen = CBashGeneric(36, c_ubyte)
    endBlue = CBashGeneric(37, c_ubyte)
    unused3 = CBashUINT8ARRAY(38, 1)
    activateParentFlags = CBashGeneric(39, c_ubyte)

    def create_activateParentRef(self):
        length = _CGetFieldAttribute(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ParentRef(self._RecordID, 40, length)
    activateParentRefs = CBashLIST(40, ParentRef)
    activateParentRefs_list = CBashLIST(40, ParentRef, True)

    prompt = CBashSTRING(41)
    parent = CBashFORMID(42)
    parentFlags = CBashGeneric(43, c_ubyte)
    unused4 = CBashUINT8ARRAY(44, 3)
    emittance = CBashFORMID(45)
    boundRef = CBashFORMID(46)

    def create_reflrefr(self):
        length = _CGetFieldAttribute(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ReflRefr(self._RecordID, 47, length)
    reflrefrs = CBashLIST(47, ReflRefr)
    reflrefrs_list = CBashLIST(47, ReflRefr, True)

    ignoredBySandbox = CBashGeneric(48, c_bool)
    scale = CBashFLOAT32(49)
    posX = CBashFLOAT32(50)
    posY = CBashFLOAT32(51)
    posZ = CBashFLOAT32(52)
    rotX = CBashFLOAT32(53)
    rotX_degrees = CBashDEGREES(53)
    rotY = CBashFLOAT32(54)
    rotY_degrees = CBashDEGREES(54)
    rotZ = CBashFLOAT32(55)
    rotZ_degrees = CBashDEGREES(55)

    IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

    IsOppositeParent = CBashBasicFlag('parentFlags', 0x00000001)
    IsPopIn = CBashBasicFlag('parentFlags', 0x00000002)

    IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
    IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
    IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')

    copyattrs = FnvBaseRecord.baseattrs + ['base', 'encounterZone', 'xrgd_p', 'xrgb_p',
                                           'idleTime', 'idle', 'numRefs', 'compiledSize',
                                           'lastIndex', 'scriptType', 'scriptFlags',
                                           'compiled_p', 'scriptText', 'vars_list',
                                           'references', 'topic', 'owner',
                                           'rank', 'count',
                                           'radius', 'health', 'decals_list',
                                           'linkedReference',
                                           'startRed', 'startGreen', 'startBlue',
                                           'endRed', 'endGreen', 'endBlue',
                                           'activateParentFlags',
                                           'activateParentRefs_list', 'prompt',
                                           'parent', 'parentFlags', 'emittance',
                                           'boundRef', 'reflrefrs_list',
                                           'ignoredBySandbox', 'scale',
                                           'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ']
    exportattrs = copyattrs[:]
    exportattrs.remove('xrgd_p')
    exportattrs.remove('xrgb_p')
    exportattrs.remove('compiled_p')

class FnvPCBERecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 56, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'PCBE'
    class Decal(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        unknown1 = CBashUINT8ARRAY_LIST(2, 24)
        copyattrs = ['reference', 'unknown1']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')

    class ParentRef(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        delay = CBashFLOAT32_LIST(2)
        exportattrs = copyattrs = ['reference', 'delay']

    class ReflRefr(ListComponent):
        __slots__ = []
        reference = CBashFORMID_LIST(1)
        type = CBashGeneric_LIST(2, c_ulong)

        IsReflection = CBashBasicType('type', 0, 'IsRefraction')
        IsRefraction = CBashBasicType('type', 1, 'IsReflection')
        exportattrs = copyattrs = ['reference', 'type']

    base = CBashFORMID(7)
    encounterZone = CBashFORMID(8)
    xrgd_p = CBashUINT8ARRAY(9)
    xrgb_p = CBashUINT8ARRAY(10)
    idleTime = CBashFLOAT32(11)
    idle = CBashFORMID(12)
    unused1 = CBashUINT8ARRAY(13, 4)
    numRefs = CBashGeneric(14, c_ulong)
    compiledSize = CBashGeneric(15, c_ulong)
    lastIndex = CBashGeneric(16, c_ulong)
    scriptType = CBashGeneric(17, c_ushort)
    scriptFlags = CBashGeneric(18, c_ushort)
    compiled_p = CBashUINT8ARRAY(19)
    scriptText = CBashISTRING(20)

    def create_var(self):
        length = _CGetFieldAttribute(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 21, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Var(self._RecordID, 21, length)
    vars = CBashLIST(21, Var)
    vars_list = CBashLIST(21, Var, True)

    references = CBashFORMID_OR_UINT32_ARRAY(22)
    topic = CBashFORMID(23)
    owner = CBashFORMID(24)
    rank = CBashGeneric(25, c_long)
    count = CBashGeneric(26, c_long)
    radius = CBashFLOAT32(27)
    health = CBashFLOAT32(28)

    def create_decal(self):
        length = _CGetFieldAttribute(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Decal(self._RecordID, 29, length)
    decals = CBashLIST(29, Decal)
    decals_list = CBashLIST(29, Decal, True)

    linkedReference = CBashFORMID(30)
    startRed = CBashGeneric(31, c_ubyte)
    startGreen = CBashGeneric(32, c_ubyte)
    startBlue = CBashGeneric(33, c_ubyte)
    unused2 = CBashUINT8ARRAY(34, 1)
    endRed = CBashGeneric(35, c_ubyte)
    endGreen = CBashGeneric(36, c_ubyte)
    endBlue = CBashGeneric(37, c_ubyte)
    unused3 = CBashUINT8ARRAY(38, 1)
    activateParentFlags = CBashGeneric(39, c_ubyte)

    def create_activateParentRef(self):
        length = _CGetFieldAttribute(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 40, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ParentRef(self._RecordID, 40, length)
    activateParentRefs = CBashLIST(40, ParentRef)
    activateParentRefs_list = CBashLIST(40, ParentRef, True)

    prompt = CBashSTRING(41)
    parent = CBashFORMID(42)
    parentFlags = CBashGeneric(43, c_ubyte)
    unused4 = CBashUINT8ARRAY(44, 3)
    emittance = CBashFORMID(45)
    boundRef = CBashFORMID(46)

    def create_reflrefr(self):
        length = _CGetFieldAttribute(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 47, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.ReflRefr(self._RecordID, 47, length)
    reflrefrs = CBashLIST(47, ReflRefr)
    reflrefrs_list = CBashLIST(47, ReflRefr, True)

    ignoredBySandbox = CBashGeneric(48, c_bool)
    scale = CBashFLOAT32(49)
    posX = CBashFLOAT32(50)
    posY = CBashFLOAT32(51)
    posZ = CBashFLOAT32(52)
    rotX = CBashFLOAT32(53)
    rotX_degrees = CBashDEGREES(53)
    rotY = CBashFLOAT32(54)
    rotY_degrees = CBashDEGREES(54)
    rotZ = CBashFLOAT32(55)
    rotZ_degrees = CBashDEGREES(55)

    IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

    IsOppositeParent = CBashBasicFlag('parentFlags', 0x00000001)
    IsPopIn = CBashBasicFlag('parentFlags', 0x00000002)

    IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
    IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
    IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')

    copyattrs = FnvBaseRecord.baseattrs + ['base', 'encounterZone', 'xrgd_p', 'xrgb_p',
                                           'idleTime', 'idle', 'numRefs', 'compiledSize',
                                           'lastIndex', 'scriptType', 'scriptFlags',
                                           'compiled_p', 'scriptText', 'vars_list',
                                           'references', 'topic', 'owner',
                                           'rank', 'count',
                                           'radius', 'health', 'decals_list',
                                           'linkedReference',
                                           'startRed', 'startGreen', 'startBlue',
                                           'endRed', 'endGreen', 'endBlue',
                                           'activateParentFlags',
                                           'activateParentRefs_list', 'prompt',
                                           'parent', 'parentFlags', 'emittance',
                                           'boundRef', 'reflrefrs_list',
                                           'ignoredBySandbox', 'scale',
                                           'posX', 'posY', 'posZ', 'rotX', 'rotY', 'rotZ']
    exportattrs = copyattrs[:]
    exportattrs.remove('xrgd_p')
    exportattrs.remove('xrgb_p')
    exportattrs.remove('compiled_p')

class FnvNAVMRecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 20, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'NAVM'
    class Vertex(ListComponent):
        __slots__ = []
        x = CBashFLOAT32_LIST(1)
        y = CBashFLOAT32_LIST(2)
        z = CBashFLOAT32_LIST(3)

        exportattrs = copyattrs = ['x', 'y', 'z']

    class Triangle(ListComponent):
        __slots__ = []
        vertex1 = CBashGeneric_LIST(1, c_short)
        vertex2 = CBashGeneric_LIST(2, c_short)
        vertex3 = CBashGeneric_LIST(3, c_short)
        edge1 = CBashGeneric_LIST(4, c_short)
        edge2 = CBashGeneric_LIST(5, c_short)
        edge3 = CBashGeneric_LIST(6, c_short)
        flags = CBashGeneric_LIST(7, c_ulong)

        IsTriangle0External = CBashBasicFlag('flags', 0x00000001)
        IsTriangle1External = CBashBasicFlag('flags', 0x00000002)
        IsTriangle2External = CBashBasicFlag('flags', 0x00000004)
        IsUnknown4 = CBashBasicFlag('flags', 0x00000008)
        IsUnknown5 = CBashBasicFlag('flags', 0x00000010)
        IsUnknown6 = CBashBasicFlag('flags', 0x00000020)
        IsUnknown7 = CBashBasicFlag('flags', 0x00000040)
        IsUnknown8 = CBashBasicFlag('flags', 0x00000080)
        IsUnknown9 = CBashBasicFlag('flags', 0x00000100)
        IsUnknown10 = CBashBasicFlag('flags', 0x00000200)
        IsUnknown11 = CBashBasicFlag('flags', 0x00000400)
        IsUnknown12 = CBashBasicFlag('flags', 0x00000800)
        IsUnknown13 = CBashBasicFlag('flags', 0x00001000)
        IsUnknown14 = CBashBasicFlag('flags', 0x00002000)
        IsUnknown15 = CBashBasicFlag('flags', 0x00004000)
        IsUnknown16 = CBashBasicFlag('flags', 0x00008000)
        IsUnknown17 = CBashBasicFlag('flags', 0x00010000)
        IsUnknown18 = CBashBasicFlag('flags', 0x00020000)
        IsUnknown19 = CBashBasicFlag('flags', 0x00040000)
        IsUnknown20 = CBashBasicFlag('flags', 0x00080000)
        IsUnknown21 = CBashBasicFlag('flags', 0x00100000)
        IsUnknown22 = CBashBasicFlag('flags', 0x00200000)
        IsUnknown23 = CBashBasicFlag('flags', 0x00400000)
        IsUnknown24 = CBashBasicFlag('flags', 0x00800000)
        IsUnknown25 = CBashBasicFlag('flags', 0x01000000)
        IsUnknown26 = CBashBasicFlag('flags', 0x02000000)
        IsUnknown27 = CBashBasicFlag('flags', 0x04000000)
        IsUnknown28 = CBashBasicFlag('flags', 0x08000000)
        IsUnknown29 = CBashBasicFlag('flags', 0x10000000)
        IsUnknown30 = CBashBasicFlag('flags', 0x20000000)
        IsUnknown31 = CBashBasicFlag('flags', 0x40000000)
        IsUnknown32 = CBashBasicFlag('flags', 0x80000000)
        exportattrs = copyattrs = ['vertex1', 'vertex2', 'vertex3', 'edge1', 'edge2', 'edge3', 'flags']

    class Door(ListComponent):
        __slots__ = []
        door = CBashFORMID_LIST(1)
        unknown1 = CBashGeneric_LIST(2, c_ushort)
        unused1 = CBashUINT8ARRAY_LIST(3, 2)

        exportattrs = copyattrs = ['door', 'unknown1']

    class Connection(ListComponent):
        __slots__ = []
        unknown1 = CBashUINT8ARRAY_LIST(1)
        mesh = CBashFORMID_LIST(2)
        triangle = CBashGeneric_LIST(3, c_ushort)

        exportattrs = copyattrs = ['unknown1', 'mesh', 'triangle']

    version = CBashGeneric(7, c_ulong)
    cell = CBashFORMID(8)
    numVertices = CBashGeneric(9, c_ulong)
    numTriangles = CBashGeneric(10, c_ulong)
    numConnections = CBashGeneric(11, c_ulong)
    numUnknown = CBashGeneric(12, c_ulong)
    numDoors = CBashGeneric(13, c_ulong)

    def create_vertic(self):
        length = _CGetFieldAttribute(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Vertex(self._RecordID, 14, length)
    vertices = CBashLIST(14, Vertex)
    vertices_list = CBashLIST(14, Vertex, True)

    def create_triangle(self):
        length = _CGetFieldAttribute(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Triangle(self._RecordID, 15, length)
    triangles = CBashLIST(15, Triangle)
    triangles_list = CBashLIST(15, Triangle, True)

    unknown1 = CBashSINT16ARRAY(16)

    def create_door(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Door(self._RecordID, 17, length)
    doors = CBashLIST(17, Door)
    doors_list = CBashLIST(17, Door, True)

    nvgd_p = CBashUINT8ARRAY(18)

    def create_connection(self):
        length = _CGetFieldAttribute(self._RecordID, 19, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 19, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Connection(self._RecordID, 19, length)
    connections = CBashLIST(19, Connection)
    connections_list = CBashLIST(19, Connection, True)

    copyattrs = FnvBaseRecord.baseattrs + ['version', 'cell', 'numVertices',
                                           'numTriangles', 'numConnections',
                                           'numUnknown', 'numDoors',
                                           'vertices_list', 'triangles_list',
                                           'unknown1', 'doors_list', 'nvgd_p',
                                           'connections_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('nvgd_p')

class FnvLANDRecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'LAND'
    class Normal(ListX2Component):
        __slots__ = []
        x = CBashGeneric_LISTX2(1, c_ubyte)
        y = CBashGeneric_LISTX2(2, c_ubyte)
        z = CBashGeneric_LISTX2(3, c_ubyte)
        exportattrs = copyattrs = ['x', 'y', 'z']

    class Height(ListX2Component):
        __slots__ = []
        height = CBashGeneric_LISTX2(1, c_byte)
        exportattrs = copyattrs = ['height']

    class Color(ListX2Component):
        __slots__ = []
        red = CBashGeneric_LISTX2(1, c_ubyte)
        green = CBashGeneric_LISTX2(2, c_ubyte)
        blue = CBashGeneric_LISTX2(3, c_ubyte)
        exportattrs = copyattrs = ['red', 'green', 'blue']

    class BaseTexture(ListComponent):
        __slots__ = []
        texture = CBashFORMID_LIST(1)
        quadrant = CBashGeneric_LIST(2, c_byte)
        unused1 = CBashUINT8ARRAY_LIST(3, 1)
        layer = CBashGeneric_LIST(4, c_short)
        exportattrs = copyattrs = ['texture', 'quadrant', 'layer']

    class AlphaLayer(ListComponent):
        __slots__ = []
        class Opacity(ListX2Component):
            __slots__ = []
            position = CBashGeneric_LISTX2(1, c_ushort)
            unused1 = CBashUINT8ARRAY_LISTX2(2, 2)
            opacity = CBashFLOAT32_LISTX2(3)
            exportattrs = copyattrs = ['position', 'opacity']
        texture = CBashFORMID_LIST(1)
        quadrant = CBashGeneric_LIST(2, c_byte)
        unused1 = CBashUINT8ARRAY_LIST(3, 1)
        layer = CBashGeneric_LIST(4, c_short)

        def create_opacity(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 5, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 5, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Opacity(self._RecordID, self._FieldID, self._ListIndex, 5, length)
        opacities = CBashLIST_LIST(5, Opacity)
        opacities_list = CBashLIST_LIST(5, Opacity, True)

        exportattrs = copyattrs = ['texture', 'quadrant', 'layer', 'opacities_list']

    class VertexTexture(ListComponent):
        __slots__ = []
        texture = CBashFORMID_LIST(1)
        exportattrs = copyattrs = ['texture']

    class Position(ListX2Component):
        __slots__ = []
        height = CBashFLOAT32_LISTX2(1)
        normalX = CBashGeneric_LISTX2(2, c_ubyte)
        normalY = CBashGeneric_LISTX2(3, c_ubyte)
        normalZ = CBashGeneric_LISTX2(4, c_ubyte)
        red = CBashGeneric_LISTX2(5, c_ubyte)
        green = CBashGeneric_LISTX2(6, c_ubyte)
        blue = CBashGeneric_LISTX2(7, c_ubyte)
        baseTexture = CBashFORMID_LISTX2(8)
        alphaLayer1Texture = CBashFORMID_LISTX2(9)
        alphaLayer1Opacity = CBashFLOAT32_LISTX2(10)
        alphaLayer2Texture = CBashFORMID_LISTX2(11)
        alphaLayer2Opacity = CBashFLOAT32_LISTX2(12)
        alphaLayer3Texture = CBashFORMID_LISTX2(13)
        alphaLayer3Opacity = CBashFLOAT32_LISTX2(14)
        alphaLayer4Texture = CBashFORMID_LISTX2(15)
        alphaLayer4Opacity = CBashFLOAT32_LISTX2(16)
        alphaLayer5Texture = CBashFORMID_LISTX2(17)
        alphaLayer5Opacity = CBashFLOAT32_LISTX2(18)
        alphaLayer6Texture = CBashFORMID_LISTX2(19)
        alphaLayer6Opacity = CBashFLOAT32_LISTX2(20)
        alphaLayer7Texture = CBashFORMID_LISTX2(21)
        alphaLayer7Opacity = CBashFLOAT32_LISTX2(22)
        alphaLayer8Texture = CBashFORMID_LISTX2(23)
        alphaLayer8Opacity = CBashFLOAT32_LISTX2(24)
        exportattrs = copyattrs = ['height', 'normalX', 'normalY', 'normalZ',
                                   'red', 'green', 'blue', 'baseTexture',
                                   'alphaLayer1Texture', 'alphaLayer1Opacity',
                                   'alphaLayer2Texture', 'alphaLayer2Opacity',
                                   'alphaLayer3Texture', 'alphaLayer3Opacity',
                                   'alphaLayer4Texture', 'alphaLayer4Opacity',
                                   'alphaLayer5Texture', 'alphaLayer5Opacity',
                                   'alphaLayer6Texture', 'alphaLayer6Opacity',
                                   'alphaLayer7Texture', 'alphaLayer7Opacity',
                                   'alphaLayer8Texture', 'alphaLayer8Opacity']

    data_p = CBashUINT8ARRAY(7)

    def get_normals(self):
        return [[self.Normal(self._RecordID, 8, x, 0, y) for y in range(0,33)] for x in range(0,33)]
    def set_normals(self, nElements):
        if nElements is None or len(nElements) != 33: return
        for oElement, nElement in zip(self.normals, nElements if isinstance(nElements[0], tuple) else [ExtractCopyList(nElements[x]) for x in range(0,33)]):
            SetCopyList(oElement, nElement)
    normals = property(get_normals, set_normals)
    def get_normals_list(self):
        return [ExtractCopyList([self.Normal(self._RecordID, 8, x, 0, y) for y in range(0,33)]) for x in range(0,33)]

    normals_list = property(get_normals_list, set_normals)

    heightOffset = CBashFLOAT32(9)

    def get_heights(self):
        return [[self.Height(self._RecordID, 10, x, 0, y) for y in range(0,33)] for x in range(0,33)]
    def set_heights(self, nElements):
        if nElements is None or len(nElements) != 33: return
        for oElement, nElement in zip(self.heights, nElements if isinstance(nElements[0], tuple) else [ExtractCopyList(nElements[x]) for x in range(0,33)]):
            SetCopyList(oElement, nElement)

    heights = property(get_heights, set_heights)
    def get_heights_list(self):
        return [ExtractCopyList([self.Height(self._RecordID, 10, x, 0, y) for y in range(0,33)]) for x in range(0,33)]
    heights_list = property(get_heights_list, set_heights)

    unused1 = CBashUINT8ARRAY(11, 3)

    def get_colors(self):
        return [[self.Color(self._RecordID, 12, x, 0, y) for y in range(0,33)] for x in range(0,33)]
    def set_colors(self, nElements):
        if nElements is None or len(nElements) != 33: return
        for oElement, nElement in zip(self.colors, nElements if isinstance(nElements[0], tuple) else [ExtractCopyList(nElements[x]) for x in range(0,33)]):
            SetCopyList(oElement, nElement)

    colors = property(get_colors, set_colors)
    def get_colors_list(self):
        return [ExtractCopyList([self.Color(self._RecordID, 12, x, 0, y) for y in range(0,33)]) for x in range(0,33)]
    colors_list = property(get_colors_list, set_colors)

    def create_baseTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 13, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 13, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.BaseTexture(self._RecordID, 13, length)
    baseTextures = CBashLIST(13, BaseTexture)
    baseTextures_list = CBashLIST(13, BaseTexture, True)

    def create_alphaLayer(self):
        length = _CGetFieldAttribute(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.AlphaLayer(self._RecordID, 14, length)
    alphaLayers = CBashLIST(14, AlphaLayer)
    alphaLayers_list = CBashLIST(14, AlphaLayer, True)

    def create_vertexTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.VertexTexture(self._RecordID, 15, length)
    vertexTextures = CBashLIST(15, VertexTexture)
    vertexTextures_list = CBashLIST(15, VertexTexture, True)

    ##The Positions accessor is unique in that it duplicates the above accessors. It just presents the data in a more friendly format.
    def get_Positions(self):
        return [[self.Position(self._RecordID, 16, row, 0, column) for column in range(0,33)] for row in range(0,33)]
    def set_Positions(self, nElements):
        if nElements is None or len(nElements) != 33: return
        for oElement, nElement in zip(self.Positions, nElements if isinstance(nElements[0], tuple) else [ExtractCopyList(nElements[x]) for x in range(0,33)]):
            SetCopyList(oElement, nElement)
    Positions = property(get_Positions, set_Positions)
    def get_Positions_list(self):
        return [ExtractCopyList([self.Position(self._RecordID, 16, x, 0, y) for y in range(0,33)]) for x in range(0,33)]
    Positions_list = property(get_Positions_list, set_Positions)
    copyattrs = FnvBaseRecord.baseattrs + ['data_p', 'normals_list', 'heights_list', 'heightOffset',
                                           'colors_list', 'baseTextures_list', 'alphaLayers_list',
                                           'vertexTextures_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('data_p')

class FnvINFORecord(FnvBaseRecord):
    __slots__ = []
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 44, 0, 0, 0, 0, 0, 0, 0)

    _Type = 'INFO'
    class Response(ListComponent):
        __slots__ = []
        emotionType = CBashGeneric_LIST(1, c_ulong)
        emotionValue = CBashGeneric_LIST(2, c_long)
        unused1 = CBashUINT8ARRAY_LIST(3, 4)
        responseNum = CBashGeneric_LIST(4, c_ubyte)
        unused2 = CBashUINT8ARRAY_LIST(5, 3)
        sound = CBashFORMID_LIST(6)
        flags = CBashGeneric_LIST(7, c_ubyte)
        unused3 = CBashUINT8ARRAY_LIST(8, 3)
        responseText = CBashSTRING_LIST(9)
        actorNotes = CBashISTRING_LIST(10)
        editNotes = CBashISTRING_LIST(11)
        speakerAnim = CBashFORMID_LIST(12)
        listenerAnim = CBashFORMID_LIST(13)

        IsUseEmotionAnim = CBashBasicFlag('flags', 0x01)

        IsNeutral = CBashBasicType('emotionType', 0, 'IsAnger')
        IsAnger = CBashBasicType('emotionType', 1, 'IsNeutral')
        IsDisgust = CBashBasicType('emotionType', 2, 'IsNeutral')
        IsFear = CBashBasicType('emotionType', 3, 'IsNeutral')
        IsSad = CBashBasicType('emotionType', 4, 'IsNeutral')
        IsHappy = CBashBasicType('emotionType', 5, 'IsNeutral')
        IsSurprise = CBashBasicType('emotionType', 6, 'IsNeutral')
        IsPained = CBashBasicType('emotionType', 7, 'IsNeutral')
        exportattrs = copyattrs = ['emotionType', 'emotionValue', 'responseNum',
                                   'sound', 'flags', 'responseText', 'actorNotes',
                                   'editNotes', 'speakerAnim', 'listenerAnim']

    class InfoScript(BaseComponent):
        __slots__ = []
        unused1 = CBashUINT8ARRAY_GROUP(0, 4)
        numRefs = CBashGeneric_GROUP(1, c_ulong)
        compiledSize = CBashGeneric_GROUP(2, c_ulong)
        lastIndex = CBashGeneric_GROUP(3, c_ulong)
        scriptType = CBashGeneric_GROUP(4, c_ushort)
        scriptFlags = CBashGeneric_GROUP(5, c_ushort)
        compiled_p = CBashUINT8ARRAY_GROUP(6)
        scriptText = CBashISTRING_GROUP(7)
        def create_var(self):
            FieldID = self._FieldID + 8
            length = _CGetFieldAttribute(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return Var(self._RecordID, FieldID, length)
        vars = CBashLIST_GROUP(8, Var)
        vars_list = CBashLIST_GROUP(8, Var, True)
        references = CBashFORMID_OR_UINT32_ARRAY_GROUP(9)

        IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

        IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
        IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
        IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')
        copyattrs = ['numRefs', 'compiledSize', 'lastIndex',
                     'scriptType', 'scriptFlags', 'compiled_p',
                     'scriptText', 'vars_list', 'references']
        exportattrs = copyattrs[:]
        exportattrs.remove('compiled_p')

    dialType = CBashGeneric(7, c_ubyte)
    nextSpeaker = CBashGeneric(8, c_ubyte)
    flags = CBashGeneric(9, c_ushort)
    quest = CBashFORMID(10)
    topic = CBashFORMID(11)
    prevInfo = CBashFORMID(12)
    addTopics = CBashFORMIDARRAY(13)

    def create_response(self):
        length = _CGetFieldAttribute(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Response(self._RecordID, 14, length)
    responses = CBashLIST(14, Response)
    responses_list = CBashLIST(14, Response, True)

    def create_condition(self):
        length = _CGetFieldAttribute(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVCondition(self._RecordID, 15, length)
    conditions = CBashLIST(15, FNVCondition)
    conditions_list = CBashLIST(15, FNVCondition, True)

    choices = CBashFORMIDARRAY(16)
    linksFrom = CBashFORMIDARRAY(17)
    unknown = CBashFORMIDARRAY(18)
    begin = CBashGrouped(19, InfoScript)
    begin_list = CBashGrouped(19, InfoScript, True)

    end = CBashGrouped(29, InfoScript)
    end_list = CBashGrouped(29, InfoScript, True)

    unusedSound = CBashFORMID(39)
    prompt = CBashSTRING(40)
    speaker = CBashFORMID(41)
    actorValueOrPerk = CBashFORMID(42)
    challengeType = CBashGeneric(43, c_ulong)

    IsGoodbye = CBashBasicFlag('flags', 0x0001)
    IsRandom = CBashBasicFlag('flags', 0x0002)
    IsSayOnce = CBashBasicFlag('flags', 0x0004)
    IsRunImmediately = CBashBasicFlag('flags', 0x0008)
    IsInfoRefusal = CBashBasicFlag('flags', 0x0010)
    IsRandomEnd = CBashBasicFlag('flags', 0x0020)
    IsRunForRumors = CBashBasicFlag('flags', 0x0040)
    IsSpeechChallenge = CBashBasicFlag('flags', 0x0080)
    IsSayOnceADay = CBashBasicFlag('flags', 0x0100)
    IsAlwaysDarken = CBashBasicFlag('flags', 0x0200)

    IsTopic = CBashBasicType('dialType', 0, 'IsConversation')
    IsConversation = CBashBasicType('dialType', 1, 'IsTopic')
    IsCombat = CBashBasicType('dialType', 2, 'IsTopic')
    IsPersuasion = CBashBasicType('dialType', 3, 'IsTopic')
    IsDetection = CBashBasicType('dialType', 4, 'IsTopic')
    IsService = CBashBasicType('dialType', 5, 'IsTopic')
    IsMisc = CBashBasicType('dialType', 6, 'IsTopic')
    IsRadio = CBashBasicType('dialType', 7, 'IsTopic')

    IsTarget = CBashBasicType('nextSpeaker', 0, 'IsSelf')
    IsSelf = CBashBasicType('nextSpeaker', 1, 'IsTarget')
    IsEither = CBashBasicType('nextSpeaker', 2, 'IsTarget')

    IsNone = CBashBasicType('challengeType', 0, 'IsVeryEasy')
    IsVeryEasy = CBashBasicType('challengeType', 1, 'IsNone')
    IsEasy = CBashBasicType('challengeType', 2, 'IsNone')
    IsAverage = CBashBasicType('challengeType', 3, 'IsNone')
    IsHard = CBashBasicType('challengeType', 4, 'IsNone')
    IsVeryHard = CBashBasicType('challengeType', 5, 'IsNone')
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['dialType', 'nextSpeaker', 'flags',
                                                         'quest', 'topic', 'prevInfo',
                                                         'addTopics', 'responses_list',
                                                         'conditions_list', 'choices',
                                                         'linksFrom', 'unknown', 'begin_list',
                                                         'end_list', 'prompt', 'speaker',
                                                         'actorValueOrPerk', 'challengeType']

class FnvGMSTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'GMST'
    def get_value(self):
        fieldtype = _CGetFieldAttribute(self._RecordID, 7, 0, 0, 0, 0, 0, 0, 2)
        if fieldtype == API_FIELDS.UNKNOWN: return None
        _CGetField.restype = POINTER(c_long) if fieldtype == API_FIELDS.SINT32 else POINTER(c_float) if fieldtype == API_FIELDS.FLOAT32 else c_char_p
        retValue = _CGetField(self._RecordID, 7, 0, 0, 0, 0, 0, 0, 0)
        return (_unicode(retValue) if fieldtype == API_FIELDS.STRING else round(retValue.contents.value,6) if fieldtype == API_FIELDS.FLOAT32 else retValue.contents.value) if retValue else None
    def set_value(self, nValue):
        if nValue is None: _CDeleteField(self._RecordID, 7, 0, 0, 0, 0, 0, 0)
        else:
            fieldtype = _CGetFieldAttribute(self._RecordID, 7, 0, 0, 0, 0, 0, 0, 2)
            _CSetField(self._RecordID, 7, 0, 0, 0, 0, 0, 0, byref(c_long(nValue)) if fieldtype == API_FIELDS.SINT32 else byref(c_float(round(nValue,6))) if fieldtype == API_FIELDS.FLOAT32 else _encode(nValue), 0)
    value = property(get_value, set_value)
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['value']

class FnvTXSTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'TXST'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    baseImageOrTransparencyPath = CBashISTRING(13)
    normalMapOrSpecularPath = CBashISTRING(14)
    envMapMaskOrUnkPath = CBashISTRING(15)
    glowMapOrUnusedPath = CBashISTRING(16)
    parallaxMapOrUnusedPath = CBashISTRING(17)
    envMapOrUnusedPath = CBashISTRING(18)
    decalMinWidth = CBashFLOAT32(19)
    decalMaxWidth = CBashFLOAT32(20)
    decalMinHeight = CBashFLOAT32(21)
    decalMaxHeight = CBashFLOAT32(22)
    decalDepth = CBashFLOAT32(23)
    decalShininess = CBashFLOAT32(24)
    decalScale = CBashFLOAT32(25)
    decalPasses = CBashGeneric(26, c_ubyte)
    decalFlags = CBashGeneric(27, c_ubyte)
    decalUnused1 = CBashUINT8ARRAY(28, 2)
    decalRed = CBashGeneric(29, c_ubyte)
    decalGreen = CBashGeneric(30, c_ubyte)
    decalBlue = CBashGeneric(31, c_ubyte)
    decalUnused2 = CBashUINT8ARRAY(32, 1)
    flags = CBashGeneric(33, c_ushort)

    IsNoSpecularMap = CBashBasicFlag('flags', 0x00000001)
    IsSpecularMap = CBashInvertedFlag('IsNoSpecularMap')

    IsObjectParallax = CBashBasicFlag('decalFlags', 0x00000001)
    IsObjectAlphaBlending = CBashBasicFlag('decalFlags', 0x00000002)
    IsObjectAlphaTesting = CBashBasicFlag('decalFlags', 0x00000004)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2', 'baseImageOrTransparencyPath',
                                           'normalMapOrSpecularPath', 'envMapMaskOrUnkPath', 'glowMapOrUnusedPath',
                                           'parallaxMapOrUnusedPath', 'envMapOrUnusedPath', 'decalMinWidth',
                                           'decalMaxWidth', 'decalMinHeight', 'decalMaxHeight',
                                           'decalDepth', 'decalShininess', 'decalScale',
                                           'decalPasses', 'decalFlags', 'decalUnused1',
                                           'decalRed', 'decalGreen', 'decalBlue',
                                           'decalUnused2', 'flags']
    exportattrs = copyattrs[:]
    exportattrs.remove('decalUnused1')
    exportattrs.remove('decalUnused2')

class FnvMICNRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'MICN'
    iconPath = CBashISTRING(7)
    smallIconPath = CBashISTRING(8)

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['iconPath', 'smallIconPath']

class FnvGLOBRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'GLOB'
    format = CBashGeneric(7, c_char)
    value = CBashFLOAT32(8)

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['format', 'value']

class FnvCLASRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CLAS'
    full = CBashSTRING(7)
    description = CBashSTRING(8)
    iconPath = CBashISTRING(9)
    smallIconPath = CBashISTRING(10)
    tagSkills1 = CBashGeneric(11, c_long)
    tagSkills2 = CBashGeneric(12, c_long)
    tagSkills3 = CBashGeneric(13, c_long)
    tagSkills4 = CBashGeneric(14, c_long)
    flags = CBashGeneric(15, c_ulong)
    services = CBashGeneric(16, c_ulong)
    trainSkill = CBashGeneric(17, c_byte)
    trainLevel = CBashGeneric(18, c_ubyte)
    unused1 = CBashUINT8ARRAY(19, 2)
    strength = CBashGeneric(20, c_ubyte)
    perception = CBashGeneric(21, c_ubyte)
    endurance = CBashGeneric(22, c_ubyte)
    charisma = CBashGeneric(23, c_ubyte)
    intelligence = CBashGeneric(24, c_ubyte)
    agility = CBashGeneric(25, c_ubyte)
    luck = CBashGeneric(26, c_ubyte)

    IsPlayable = CBashBasicFlag('flags', 0x00000001)
    IsGuard = CBashBasicFlag('flags', 0x00000002)

    IsServicesWeapons = CBashBasicFlag('services', 0x00000001)
    IsServicesArmor = CBashBasicFlag('services', 0x00000002)
    IsServicesClothing = CBashBasicFlag('services', 0x00000004)
    IsServicesBooks = CBashBasicFlag('services', 0x00000008)
    IsServicesFood = CBashBasicFlag('services', 0x00000010)
    IsServicesChems = CBashBasicFlag('services', 0x00000020)
    IsServicesStimpacks = CBashBasicFlag('services', 0x00000040)
    IsServicesLights = CBashBasicFlag('services', 0x00000080)
    IsServicesMiscItems = CBashBasicFlag('services', 0x00000400)
    IsServicesPotions = CBashBasicFlag('services', 0x00002000)
    IsServicesTraining = CBashBasicFlag('services', 0x00004000)
    IsServicesRecharge = CBashBasicFlag('services', 0x00010000)
    IsServicesRepair = CBashBasicFlag('services', 0x00020000)
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['full', 'description', 'iconPath', 'smallIconPath',
                                                         'tagSkills1', 'tagSkills2', 'tagSkills3',
                                                         'tagSkills4', 'flags', 'services',
                                                         'trainSkill', 'trainLevel', 'strength',
                                                         'perception', 'endurance', 'charisma',
                                                         'intelligence', 'agility', 'luck']

class FnvFACTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'FACT'
    class Rank(ListComponent):
        __slots__ = []
        rank = CBashGeneric_LIST(1, c_long)
        male = CBashSTRING_LIST(2)
        female = CBashSTRING_LIST(3)
        insigniaPath = CBashISTRING_LIST(4)
        exportattrs = copyattrs = ['rank', 'male', 'female', 'insigniaPath']

    full = CBashSTRING(7)

    def create_relation(self):
        length = _CGetFieldAttribute(self._RecordID, 8, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 8, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVRelation(self._RecordID, 8, length)
    relations = CBashLIST(8, FNVRelation)
    relations_list = CBashLIST(8, FNVRelation, True)

    flags = CBashGeneric(9, c_ushort)
    unused1 = CBashUINT8ARRAY(10, 2)
    crimeGoldMultiplier = CBashFLOAT32(11)

    def create_rank(self):
        length = _CGetFieldAttribute(self._RecordID, 12, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 12, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Rank(self._RecordID, 12, length)
    ranks = CBashLIST(12, Rank)
    ranks_list = CBashLIST(12, Rank, True)

    reputation = CBashFORMID(13)

    IsHiddenFromPC = CBashBasicFlag('flags', 0x0001)
    IsEvil = CBashBasicFlag('flags', 0x0002)
    IsSpecialCombat = CBashBasicFlag('flags', 0x0004)
    IsTrackCrime = CBashBasicFlag('flags', 0x0100)
    IsAllowSell = CBashBasicFlag('flags', 0x0200)
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['full', 'relations_list', 'flags',
                                                         'crimeGoldMultiplier', 'ranks_list', 'reputation']

class FnvHDPTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'HDPT'
    full = CBashSTRING(7)
    modPath = CBashISTRING(8)
    modb = CBashFLOAT32(9)
    modt_p = CBashUINT8ARRAY(10)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 11, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 11, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 11, length)
    altTextures = CBashLIST(11, FNVAltTexture)
    altTextures_list = CBashLIST(11, FNVAltTexture, True)

    modelFlags = CBashGeneric(12, c_ubyte)
    flags = CBashGeneric(13, c_ubyte)
    parts = CBashFORMIDARRAY(14)

    IsPlayable = CBashBasicFlag('flags', 0x01)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['full', 'modPath', 'modb',
                                           'modt_p', 'altTextures_list',
                                           'modelFlags', 'flags', 'parts']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvHAIRRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'HAIR'
    full = CBashSTRING(7)
    modPath = CBashISTRING(8)
    modb = CBashFLOAT32(9)
    modt_p = CBashUINT8ARRAY(10)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 11, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 11, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 11, length)
    altTextures = CBashLIST(11, FNVAltTexture)
    altTextures_list = CBashLIST(11, FNVAltTexture, True)

    modelFlags = CBashGeneric(12, c_ubyte)
    iconPath = CBashISTRING(13)
    flags = CBashGeneric(14, c_ubyte)

    IsPlayable = CBashBasicFlag('flags', 0x01)
    IsNotMale = CBashBasicFlag('flags', 0x02)
    IsMale = CBashInvertedFlag('IsNotMale')
    IsNotFemale = CBashBasicFlag('flags', 0x04)
    IsFemale = CBashInvertedFlag('IsNotFemale')
    IsFixedColor = CBashBasicFlag('flags', 0x08)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['full', 'modPath', 'modb',
                                           'modt_p', 'altTextures_list',
                                           'modelFlags', 'iconPath', 'flags']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvEYESRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'EYES'
    full = CBashSTRING(7)
    iconPath = CBashISTRING(8)
    flags = CBashGeneric(9, c_ubyte)

    IsPlayable = CBashBasicFlag('flags', 0x01)
    IsNotMale = CBashBasicFlag('flags', 0x02)
    IsMale = CBashInvertedFlag('IsNotMale')
    IsNotFemale = CBashBasicFlag('flags', 0x04)
    IsFemale = CBashInvertedFlag('IsNotFemale')
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['full', 'iconPath', 'flags']

class FnvRACERecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'RACE'
    class RaceModel(BaseComponent):
        __slots__ = []
        modPath = CBashISTRING_GROUP(0)
        modb = CBashFLOAT32_GROUP(1)
        modt_p = CBashUINT8ARRAY_GROUP(2)

        def create_altTexture(self):
            FieldID = self._FieldID + 3
            length = _CGetFieldAttribute(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return FNVAltTexture(self._RecordID, FieldID, length)
        altTextures = CBashLIST_GROUP(3, FNVAltTexture)
        altTextures_list = CBashLIST_GROUP(3, FNVAltTexture, True)
        flags = CBashGeneric_GROUP(4, c_ubyte)
        iconPath = CBashISTRING_GROUP(5)
        smallIconPath = CBashISTRING_GROUP(6)

        IsHead = CBashBasicFlag('flags', 0x01)
        IsTorso = CBashBasicFlag('flags', 0x02)
        IsRightHand = CBashBasicFlag('flags', 0x04)
        IsLeftHand = CBashBasicFlag('flags', 0x08)
        copyattrs = ['modPath', 'modb', 'modt_p', 'altTextures_list',
                     'flags', 'iconPath', 'smallIconPath']
        exportattrs = copyattrs[:]
        exportattrs.remove('modt_p')

    full = CBashSTRING(7)
    description = CBashSTRING(8)

    def create_relation(self):
        length = _CGetFieldAttribute(self._RecordID, 9, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 9, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVRelation(self._RecordID, 9, length)
    relations = CBashLIST(9, FNVRelation)
    relations_list = CBashLIST(9, FNVRelation, True)

    skill1 = CBashGeneric(10, c_byte)
    skill1Boost = CBashGeneric(11, c_byte)
    skill2 = CBashGeneric(12, c_byte)
    skill2Boost = CBashGeneric(13, c_byte)
    skill3 = CBashGeneric(14, c_byte)
    skill3Boost = CBashGeneric(15, c_byte)
    skill4 = CBashGeneric(16, c_byte)
    skill4Boost = CBashGeneric(17, c_byte)
    skill5 = CBashGeneric(18, c_byte)
    skill5Boost = CBashGeneric(19, c_byte)
    skill6 = CBashGeneric(20, c_byte)
    skill6Boost = CBashGeneric(21, c_byte)
    skill7 = CBashGeneric(22, c_byte)
    skill7Boost = CBashGeneric(23, c_byte)
    unused1 = CBashUINT8ARRAY(24, 2)
    maleHeight = CBashFLOAT32(25)
    femaleHeight = CBashFLOAT32(26)
    maleWeight = CBashFLOAT32(27)
    femaleWeight = CBashFLOAT32(28)
    flags = CBashGeneric(29, c_ulong)
    older = CBashFORMID(30)
    younger = CBashFORMID(31)
    maleVoice = CBashFORMID(32)
    femaleVoice = CBashFORMID(33)
    defaultHairMale = CBashFORMID(34)
    defaultHairFemale = CBashFORMID(35)
    defaultHairMaleColor = CBashGeneric(36, c_ubyte)
    defaultHairFemaleColor = CBashGeneric(37, c_ubyte)
    mainClamp = CBashFLOAT32(38)
    faceClamp = CBashFLOAT32(39)
    attr_p = CBashUINT8ARRAY(40)
    maleHead = CBashGrouped(41, RaceModel)
    maleHead_list = CBashGrouped(41, RaceModel, True)

    maleEars = CBashGrouped(48, RaceModel)
    maleEars_list = CBashGrouped(48, RaceModel, True)

    maleMouth = CBashGrouped(55, RaceModel)
    maleMouth_list = CBashGrouped(55, RaceModel, True)

    maleTeethLower = CBashGrouped(62, RaceModel)
    maleTeethLower_list = CBashGrouped(62, RaceModel, True)

    maleTeethUpper = CBashGrouped(69, RaceModel)
    maleTeethUpper_list = CBashGrouped(69, RaceModel, True)

    maleTongue = CBashGrouped(76, RaceModel)
    maleTongue_list = CBashGrouped(76, RaceModel, True)

    maleLeftEye = CBashGrouped(83, RaceModel)
    maleLeftEye_list = CBashGrouped(83, RaceModel, True)

    maleRightEye = CBashGrouped(90, RaceModel)
    maleRightEye_list = CBashGrouped(90, RaceModel, True)

    femaleHead = CBashGrouped(97, RaceModel)
    femaleHead_list = CBashGrouped(97, RaceModel, True)

    femaleEars = CBashGrouped(104, RaceModel)
    femaleEars_list = CBashGrouped(104, RaceModel, True)

    femaleMouth = CBashGrouped(111, RaceModel)
    femaleMouth_list = CBashGrouped(111, RaceModel, True)

    femaleTeethLower = CBashGrouped(118, RaceModel)
    femaleTeethLower_list = CBashGrouped(118, RaceModel, True)

    femaleTeethUpper = CBashGrouped(125, RaceModel)
    femaleTeethUpper_list = CBashGrouped(125, RaceModel, True)

    femaleTongue = CBashGrouped(132, RaceModel)
    femaleTongue_list = CBashGrouped(132, RaceModel, True)

    femaleLeftEye = CBashGrouped(139, RaceModel)
    femaleLeftEye_list = CBashGrouped(139, RaceModel, True)

    femaleRightEye = CBashGrouped(146, RaceModel)
    femaleRightEye_list = CBashGrouped(146, RaceModel, True)

    maleUpperBody = CBashGrouped(153, RaceModel)
    maleUpperBody_list = CBashGrouped(153, RaceModel, True)

    maleLeftHand = CBashGrouped(160, RaceModel)
    maleLeftHand_list = CBashGrouped(160, RaceModel, True)

    maleRightHand = CBashGrouped(167, RaceModel)
    maleRightHand_list = CBashGrouped(167, RaceModel, True)

    maleUpperBodyTexture = CBashGrouped(174, RaceModel)
    maleUpperBodyTexture_list = CBashGrouped(174, RaceModel, True)

    femaleUpperBody = CBashGrouped(181, RaceModel)
    femaleUpperBody_list = CBashGrouped(181, RaceModel, True)

    femaleLeftHand = CBashGrouped(188, RaceModel)
    femaleLeftHand_list = CBashGrouped(188, RaceModel, True)

    femaleRightHand = CBashGrouped(195, RaceModel)
    femaleRightHand_list = CBashGrouped(195, RaceModel, True)

    femaleUpperBodyTexture = CBashGrouped(202, RaceModel)
    femaleUpperBodyTexture_list = CBashGrouped(202, RaceModel, True)

    hairs = CBashFORMIDARRAY(209)
    eyes = CBashFORMIDARRAY(210)
    maleFggs_p = CBashUINT8ARRAY(211, 200)
    maleFgga_p = CBashUINT8ARRAY(212, 120)
    maleFgts_p = CBashUINT8ARRAY(213, 200)
    maleSnam_p = CBashUINT8ARRAY(214, 2)
    femaleFggs_p = CBashUINT8ARRAY(215, 200)
    femaleFgga_p = CBashUINT8ARRAY(216, 120)
    femaleFgts_p = CBashUINT8ARRAY(217, 200)
    femaleSnam_p = CBashUINT8ARRAY(218, 2)

    IsPlayable = CBashBasicFlag('flags', 0x00000001)
    IsChild = CBashBasicFlag('flags', 0x00000004)
    copyattrs = FnvBaseRecord.baseattrs + ['full', 'description',
                                           'relations_list', 'skill1', 'skill1Boost',
                                           'skill2', 'skill2Boost', 'skill3',
                                           'skill3Boost', 'skill4', 'skill4Boost',
                                           'skill5', 'skill5Boost', 'skill6',
                                           'skill6Boost', 'skill7', 'skill7Boost',
                                           'maleHeight', 'femaleHeight',
                                           'maleWeight', 'femaleWeight', 'flags',
                                           'older', 'younger',
                                           'maleVoice', 'femaleVoice',
                                           'defaultHairMale', 'defaultHairFemale',
                                           'defaultHairMaleColor', 'defaultHairFemaleColor',
                                           'mainClamp', 'faceClamp', 'attr_p',
                                           'maleHead_list', 'maleEars_list',
                                           'maleMouth_list', 'maleTeethLower_list',
                                           'maleTeethUpper_list', 'maleTongue_list',
                                           'maleLeftEye_list', 'maleRightEye_list',
                                           'femaleHead_list', 'femaleEars_list',
                                           'femaleMouth_list', 'femaleTeethLower_list',
                                           'femaleTeethUpper_list', 'femaleTongue_list',
                                           'femaleLeftEye_list', 'femaleRightEye_list',
                                           'maleUpperBody_list', 'maleLeftHand_list',
                                           'maleRightHand_list', 'maleUpperBodyTexture_list',
                                           'femaleUpperBody_list', 'femaleLeftHand_list',
                                           'femaleRightHand_list',
                                           'femaleUpperBodyTexture_list',
                                           'hairs', 'eyes',
                                           'maleFggs_p', 'maleFgga_p', 'maleFgts_p',
                                           'maleSnam_p',
                                           'femaleFggs_p', 'femaleFgga_p', 'femaleFgts_p',
                                           'femaleSnam_p']
    exportattrs = copyattrs[:]
    exportattrs.remove('attr_p')
    exportattrs.remove('maleFggs_p')
    exportattrs.remove('maleFgga_p')
    exportattrs.remove('maleFgts_p')
    exportattrs.remove('maleSnam_p')
    exportattrs.remove('femaleFggs_p')
    exportattrs.remove('femaleFgga_p')
    exportattrs.remove('femaleFgts_p')
    exportattrs.remove('femaleSnam_p')

class FnvSOUNRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'SOUN'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    soundPath = CBashISTRING(13)
    chance = CBashGeneric(14, c_ubyte)
    minDistance = CBashGeneric(15, c_ubyte)
    maxDistance = CBashGeneric(16, c_ubyte)
    freqAdjustment = CBashGeneric(17, c_byte)
    unused1 = CBashUINT8ARRAY(18, 1)
    flags = CBashGeneric(19, c_ulong)
    staticAtten = CBashGeneric(20, c_short)
    stopTime = CBashGeneric(21, c_ubyte)
    startTime = CBashGeneric(22, c_ubyte)
    attenCurve = CBashSINT16ARRAY(23, 5)
    reverb = CBashGeneric(24, c_short)
    priority = CBashGeneric(25, c_long)
    x = CBashGeneric(26, c_long)
    y = CBashGeneric(27, c_long)

    IsRandomFrequencyShift = CBashBasicFlag('flags', 0x00000001)
    IsPlayAtRandom = CBashBasicFlag('flags', 0x00000002)
    IsEnvironmentIgnored = CBashBasicFlag('flags', 0x00000004)
    IsRandomLocation = CBashBasicFlag('flags', 0x00000008)
    IsLoop = CBashBasicFlag('flags', 0x00000010)
    IsMenuSound = CBashBasicFlag('flags', 0x00000020)
    Is2D = CBashBasicFlag('flags', 0x00000040)
    Is360LFE = CBashBasicFlag('flags', 0x00000080)
    IsDialogueSound = CBashBasicFlag('flags', 0x00000100)
    IsEnvelopeFast = CBashBasicFlag('flags', 0x00000200)
    IsEnvelopeSlow = CBashBasicFlag('flags', 0x00000400)
    Is2DRadius = CBashBasicFlag('flags', 0x00000800)
    IsMuteWhenSubmerged = CBashBasicFlag('flags', 0x00001000)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2', 'soundPath',
                                           'chance', 'minDistance', 'maxDistance',
                                           'freqAdjustment', 'unused1', 'flags',
                                           'staticAtten', 'stopTime', 'startTime',
                                           'attenCurve', 'reverb', 'priority',
                                           'x', 'y']
    exportattrs = copyattrs[:]
    exportattrs.remove('unused1')

class FnvASPCRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ASPC'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    dawnOrDefaultLoop = CBashFORMID(13)
    afternoon = CBashFORMID(14)
    dusk = CBashFORMID(15)
    night = CBashFORMID(16)
    walla = CBashFORMID(17)
    wallaTriggerCount = CBashGeneric(18, c_ulong)
    regionSound = CBashFORMID(19)
    environmentType = CBashGeneric(20, c_ulong)
    spaceType = CBashGeneric(21, c_ulong)

    IsEnvironmentNone = CBashBasicType('environmentType', 0, 'IsEnvironmentDefault')
    IsEnvironmentDefault = CBashBasicType('environmentType', 1, 'IsEnvironmentNone')
    IsEnvironmentGeneric = CBashBasicType('environmentType', 2, 'IsEnvironmentNone')
    IsEnvironmentPaddedCell = CBashBasicType('environmentType', 3, 'IsEnvironmentNone')
    IsEnvironmentRoom = CBashBasicType('environmentType', 4, 'IsEnvironmentNone')
    IsEnvironmentBathroom = CBashBasicType('environmentType', 5, 'IsEnvironmentNone')
    IsEnvironmentLivingroom = CBashBasicType('environmentType', 6, 'IsEnvironmentNone')
    IsEnvironmentStoneRoom = CBashBasicType('environmentType', 7, 'IsEnvironmentNone')
    IsEnvironmentAuditorium = CBashBasicType('environmentType', 8, 'IsEnvironmentNone')
    IsEnvironmentConcerthall = CBashBasicType('environmentType', 9, 'IsEnvironmentNone')
    IsEnvironmentCave = CBashBasicType('environmentType', 10, 'IsEnvironmentNone')
    IsEnvironmentArena = CBashBasicType('environmentType', 11, 'IsEnvironmentNone')
    IsEnvironmentHangar = CBashBasicType('environmentType', 12, 'IsEnvironmentNone')
    IsEnvironmentCarpetedHallway = CBashBasicType('environmentType', 13, 'IsEnvironmentNone')
    IsEnvironmentHallway = CBashBasicType('environmentType', 14, 'IsEnvironmentNone')
    IsEnvironmentStoneCorridor = CBashBasicType('environmentType', 15, 'IsEnvironmentNone')
    IsEnvironmentAlley = CBashBasicType('environmentType', 16, 'IsEnvironmentNone')
    IsEnvironmentForest = CBashBasicType('environmentType', 17, 'IsEnvironmentNone')
    IsEnvironmentCity = CBashBasicType('environmentType', 18, 'IsEnvironmentNone')
    IsEnvironmentMountains = CBashBasicType('environmentType', 19, 'IsEnvironmentNone')
    IsEnvironmentQuarry = CBashBasicType('environmentType', 20, 'IsEnvironmentNone')
    IsEnvironmentPlain = CBashBasicType('environmentType', 21, 'IsEnvironmentNone')
    IsEnvironmentParkinglot = CBashBasicType('environmentType', 22, 'IsEnvironmentNone')
    IsEnvironmentSewerpipe = CBashBasicType('environmentType', 23, 'IsEnvironmentNone')
    IsEnvironmentUnderwater = CBashBasicType('environmentType', 24, 'IsEnvironmentNone')
    IsEnvironmentSmallRoom = CBashBasicType('environmentType', 25, 'IsEnvironmentNone')
    IsEnvironmentMediumRoom = CBashBasicType('environmentType', 26, 'IsEnvironmentNone')
    IsEnvironmentLargeRoom = CBashBasicType('environmentType', 27, 'IsEnvironmentNone')
    IsEnvironmentMediumHall = CBashBasicType('environmentType', 28, 'IsEnvironmentNone')
    IsEnvironmentLargeHall = CBashBasicType('environmentType', 29, 'IsEnvironmentNone')
    IsEnvironmentPlate = CBashBasicType('environmentType', 30, 'IsEnvironmentNone')

    IsSpaceExterior = CBashBasicType('spaceType', 0, 'IsSpaceInterior')
    IsSpaceInterior = CBashBasicType('spaceType', 1, 'IsSpaceExterior')
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                                         'boundX2', 'boundY2', 'boundZ2',
                                                         'dawnOrDefaultLoop', 'afternoon',
                                                         'dusk', 'night', 'walla',
                                                         'wallaTriggerCount', 'regionSound',
                                                         'environmentType', 'spaceType']

class FnvMGEFRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'MGEF'
    full = CBashSTRING(7)
    description = CBashSTRING(8)
    iconPath = CBashISTRING(9)
    smallIconPath = CBashISTRING(10)
    modPath = CBashISTRING(11)
    modb = CBashFLOAT32(12)
    modt_p = CBashUINT8ARRAY(13)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 14, length)
    altTextures = CBashLIST(14, FNVAltTexture)
    altTextures_list = CBashLIST(14, FNVAltTexture, True)

    modelFlags = CBashGeneric(15, c_ubyte)
    flags = CBashGeneric(16, c_ulong)
    baseCostUnused = CBashFLOAT32(17)
    associated = CBashFORMID(18)
    schoolUnused = CBashGeneric(19, c_long)
    resistType = CBashGeneric(20, c_long)
    numCounters = CBashGeneric(21, c_ushort)
    unused1 = CBashUINT8ARRAY(22, 2)
    light = CBashFORMID(23)
    projectileSpeed = CBashFLOAT32(24)
    effectShader = CBashFORMID(25)
    displayShader = CBashFORMID(26)
    effectSound = CBashFORMID(27)
    boltSound = CBashFORMID(28)
    hitSound = CBashFORMID(29)
    areaSound = CBashFORMID(30)
    cefEnchantmentUnused = CBashFLOAT32(31)
    cefBarterUnused = CBashFLOAT32(32)
    archType = CBashGeneric(33, c_ulong)
    actorValue = CBashGeneric(34, c_long)

    IsHostile = CBashBasicFlag('flags', 0x00000001)
    IsRecover = CBashBasicFlag('flags', 0x00000002)
    IsDetrimental = CBashBasicFlag('flags', 0x00000004)
    IsSelf = CBashBasicFlag('flags', 0x00000010)
    IsTouch = CBashBasicFlag('flags', 0x00000020)
    IsTarget = CBashBasicFlag('flags', 0x00000040)
    IsNoDuration = CBashBasicFlag('flags', 0x00000080)
    IsNoMagnitude = CBashBasicFlag('flags', 0x00000100)
    IsNoArea = CBashBasicFlag('flags', 0x00000200)
    IsFXPersist = CBashBasicFlag('flags', 0x00000400)
    IsGoryVisuals = CBashBasicFlag('flags', 0x00001000)
    IsDisplayNameOnly = CBashBasicFlag('flags', 0x00002000)
    IsRadioBroadcast = CBashBasicFlag('flags', 0x00008000)
    IsUseSkill = CBashBasicFlag('flags', 0x00080000)
    IsUseAttr = CBashBasicFlag('flags', 0x00100000)
    IsPainless = CBashBasicFlag('flags', 0x01000000)
    IsSprayType = CBashBasicFlag('flags', 0x02000000)
    IsBoltType = CBashBasicFlag('flags', 0x04000000)
    IsFogType = CBashBasicFlag('flags', 0x06000000)
    IsNoHitEffect = CBashBasicFlag('flags', 0x08000000)
    IsPersistOnDeath = CBashBasicFlag('flags', 0x10000000)
    IsUnknown1 = CBashBasicFlag('flags', 0x20000000)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsValueModifier = CBashBasicType('archType', 0, 'IsScript')
    IsScript = CBashBasicType('archType', 1, 'IsValueModifier')
    IsDispel = CBashBasicType('archType', 2, 'IsValueModifier')
    IsCureDisease = CBashBasicType('archType', 3, 'IsValueModifier')
    IsInvisibility = CBashBasicType('archType', 11, 'IsValueModifier')
    IsChameleon = CBashBasicType('archType', 12, 'IsValueModifier')
    IsLight = CBashBasicType('archType', 13, 'IsValueModifier')
    IsLock = CBashBasicType('archType', 16, 'IsValueModifier')
    IsOpen = CBashBasicType('archType', 17, 'IsValueModifier')
    IsBoundItem = CBashBasicType('archType', 18, 'IsValueModifier')
    IsSummonCreature = CBashBasicType('archType', 19, 'IsValueModifier')
    IsParalysis = CBashBasicType('archType', 24, 'IsValueModifier')
    IsCureParalysis = CBashBasicType('archType', 30, 'IsValueModifier')
    IsCureAddiction = CBashBasicType('archType', 31, 'IsValueModifier')
    IsCurePoison = CBashBasicType('archType', 32, 'IsValueModifier')
    IsConcussion = CBashBasicType('archType', 33, 'IsValueModifier')
    IsValueAndParts = CBashBasicType('archType', 34, 'IsValueModifier')
    IsLimbCondition = CBashBasicType('archType', 35, 'IsValueModifier')
    IsTurbo = CBashBasicType('archType', 36, 'IsValueModifier')
    copyattrs = FnvBaseRecord.baseattrs + ['full', 'description', 'iconPath', 'smallIconPath',
                                           'modPath', 'modb', 'modt_p', 'altTextures_list',
                                           'modelFlags', 'flags', 'baseCostUnused', 'associated',
                                           'schoolUnused', 'resistType', 'numCounters', 'unused1',
                                           'light', 'projectileSpeed', 'effectShader', 'displayShader',
                                           'effectSound', 'boltSound', 'hitSound', 'areaSound',
                                           'cefEnchantmentUnused', 'cefBarterUnused', 'archType', 'actorValue']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')
    exportattrs.remove('baseCostUnused')
    exportattrs.remove('schoolUnused')
    exportattrs.remove('unused1')
    exportattrs.remove('cefEnchantmentUnused')
    exportattrs.remove('cefBarterUnused')

class FnvSCPTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'SCPT'
    unused1 = CBashUINT8ARRAY(7, 4)
    numRefs = CBashGeneric(8, c_ulong)
    compiledSize = CBashGeneric(9, c_ulong)
    lastIndex = CBashGeneric(10, c_ulong)
    scriptType = CBashGeneric(11, c_ushort)
    scriptFlags = CBashGeneric(12, c_ushort)
    compiled_p = CBashUINT8ARRAY(13)
    scriptText = CBashISTRING(14)

    def create_var(self):
        length = _CGetFieldAttribute(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Var(self._RecordID, 15, length)
    vars = CBashLIST(15, Var)
    vars_list = CBashLIST(15, Var, True)

    references = CBashFORMID_OR_UINT32_ARRAY(16)

    IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

    IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
    IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
    IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')
    copyattrs = FnvBaseRecord.baseattrs + ['unused1', 'numRefs', 'compiledSize',
                                           'lastIndex', 'scriptType', 'scriptFlags',
                                           'compiled_p', 'scriptText',
                                           'vars_list', 'references']
    exportattrs = copyattrs[:]
    exportattrs.remove('unused1')
    exportattrs.remove('compiled_p')

class FnvLTEXRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'LTEX'
    iconPath = CBashISTRING(7)
    smallIconPath = CBashISTRING(8)
    texture = CBashFORMID(9)
    types = CBashGeneric(10, c_ubyte)
    friction = CBashGeneric(11, c_ubyte)
    restitution = CBashGeneric(12, c_ubyte)
    specularExponent = CBashGeneric(13, c_ubyte)
    grasses = CBashFORMIDARRAY(14)

    IsStone = CBashBasicType('types', 0, 'IsCloth')
    IsCloth = CBashBasicType('types', 1, 'IsStone')
    IsDirt = CBashBasicType('types', 2, 'IsStone')
    IsGlass = CBashBasicType('types', 3, 'IsStone')
    IsGrass = CBashBasicType('types', 4, 'IsStone')
    IsMetal = CBashBasicType('types', 5, 'IsStone')
    IsOrganic = CBashBasicType('types', 6, 'IsStone')
    IsSkin = CBashBasicType('types', 7, 'IsStone')
    IsWater = CBashBasicType('types', 8, 'IsStone')
    IsWood = CBashBasicType('types', 9, 'IsStone')
    IsHeavyStone = CBashBasicType('types', 10, 'IsStone')
    IsHeavyMetal = CBashBasicType('types', 11, 'IsStone')
    IsHeavyWood = CBashBasicType('types', 12, 'IsStone')
    IsChain = CBashBasicType('types', 13, 'IsStone')
    IsSnow = CBashBasicType('types', 14, 'IsStone')
    IsElevator = CBashBasicType('types', 15, 'IsStone')
    IsHollowMetal = CBashBasicType('types', 16, 'IsStone')
    IsSheetMetal = CBashBasicType('types', 17, 'IsStone')
    IsSand = CBashBasicType('types', 18, 'IsStone')
    IsBrokenConcrete = CBashBasicType('types', 19, 'IsStone')
    IsVehicleBody = CBashBasicType('types', 20, 'IsStone')
    IsVehiclePartSolid = CBashBasicType('types', 21, 'IsStone')
    IsVehiclePartHollow = CBashBasicType('types', 22, 'IsStone')
    IsBarrel = CBashBasicType('types', 23, 'IsStone')
    IsBottle = CBashBasicType('types', 24, 'IsStone')
    IsSodaCan = CBashBasicType('types', 25, 'IsStone')
    IsPistol = CBashBasicType('types', 26, 'IsStone')
    IsRifle = CBashBasicType('types', 27, 'IsStone')
    IsShoppingCart = CBashBasicType('types', 28, 'IsStone')
    IsLunchBox = CBashBasicType('types', 29, 'IsStone')
    IsBabyRattle = CBashBasicType('types', 30, 'IsStone')
    IsRubberBall = CBashBasicType('types', 31, 'IsStone')
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['iconPath', 'smallIconPath', 'texture',
                                                         'types', 'friction', 'restitution',
                                                         'specularExponent', 'grasses']

class FnvENCHRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ENCH'
    full = CBashSTRING(7)
    itemType = CBashGeneric(8, c_ulong)
    chargeAmountUnused = CBashGeneric(9, c_ulong)
    enchantCostUnused = CBashGeneric(10, c_ulong)
    flags = CBashGeneric(11, c_ubyte)
    unused1 = CBashUINT8ARRAY(12, 3)

    def create_effect(self):
        length = _CGetFieldAttribute(self._RecordID, 13, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 13, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVEffect(self._RecordID, 13, length)
    effects = CBashLIST(13, FNVEffect)
    effects_list = CBashLIST(13, FNVEffect, True)

    IsNoAutoCalc = CBashBasicFlag('flags', 0x01)
    IsAutoCalc = CBashInvertedFlag('IsNoAutoCalc')
    IsHideEffect = CBashBasicFlag('flags', 0x04)
    IsWeapon = CBashBasicType('itemType', 2, 'IsApparel')
    IsApparel = CBashBasicType('itemType', 3, 'IsWeapon')
    copyattrs = FnvBaseRecord.baseattrs + ['full', 'itemType', 'chargeAmountUnused',
                                           'enchantCostUnused', 'flags', 'effects_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('chargeAmountUnused')
    exportattrs.remove('enchantCostUnused')

class FnvSPELRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'SPEL'
    full = CBashSTRING(7)
    spellType = CBashGeneric(8, c_ulong)
    costUnused = CBashGeneric(9, c_ulong)
    levelTypeUnused = CBashGeneric(10, c_ulong)
    flags = CBashGeneric(11, c_ubyte)
    unused1 = CBashUINT8ARRAY(12, 3)

    def create_effect(self):
        length = _CGetFieldAttribute(self._RecordID, 13, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 13, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVEffect(self._RecordID, 13, length)
    effects = CBashLIST(13, FNVEffect)
    effects_list = CBashLIST(13, FNVEffect, True)

    IsManualCost = CBashBasicFlag('flags', 0x01)
    IsStartSpell = CBashBasicFlag('flags', 0x04)
    IsSilenceImmune = CBashBasicFlag('flags', 0x0A)
    IsAreaEffectIgnoresLOS = CBashBasicFlag('flags', 0x10)
    IsAEIgnoresLOS = CBashAlias('IsAreaEffectIgnoresLOS')
    IsScriptAlwaysApplies = CBashBasicFlag('flags', 0x20)
    IsDisallowAbsorbReflect = CBashBasicFlag('flags', 0x40)
    IsDisallowAbsorb = CBashAlias('IsDisallowAbsorbReflect')
    IsDisallowReflect = CBashAlias('IsDisallowAbsorbReflect')
    IsTouchExplodesWOTarget = CBashBasicFlag('flags', 0x80)
    IsTouchExplodes = CBashAlias('IsTouchExplodesWOTarget')

    IsActorEffect = CBashBasicType('spellType', 0, 'IsDisease')
    IsDisease = CBashBasicType('spellType', 1, 'IsActorEffect')
    IsPower = CBashBasicType('spellType', 2, 'IsActorEffect')
    IsLesserPower = CBashBasicType('spellType', 3, 'IsActorEffect')
    IsAbility = CBashBasicType('spellType', 4, 'IsActorEffect')
    IsPoison = CBashBasicType('spellType', 5, 'IsActorEffect')
    IsAddiction = CBashBasicType('spellType', 10, 'IsActorEffect')
    copyattrs = FnvBaseRecord.baseattrs + ['full', 'spellType', 'costUnused',
                                           'levelTypeUnused', 'flags', 'effects_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('costUnused')
    exportattrs.remove('levelTypeUnused')

class FnvACTIRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ACTI'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    script = CBashFORMID(19)
    destructable = CBashGrouped(20, FNVDestructable)
    destructable_list = CBashGrouped(20, FNVDestructable, True)

    loopSound = CBashFORMID(25)
    actSound = CBashFORMID(26)
    radioTemplate = CBashFORMID(27)
    radioStation = CBashFORMID(28)
    water = CBashFORMID(29)
    prompt = CBashSTRING(30)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'script', 'destructable_list',
                                           'loopSound', 'actSound',
                                           'radioTemplate', 'radioStation',
                                           'water', 'prompt']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvTACTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'TACT'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    script = CBashFORMID(19)
    destructable = CBashGrouped(20, FNVDestructable)
    destructable_list = CBashGrouped(20, FNVDestructable, True)

    loopSound = CBashFORMID(25)
    voice = CBashFORMID(26)
    radioTemplate = CBashFORMID(27)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'script', 'destructable_list',
                                           'loopSound', 'voice', 'radioTemplate']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvTERMRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'TERM'
    class Menu(ListComponent):
        __slots__ = []
        text = CBashSTRING_LIST(1)
        resultText = CBashSTRING_LIST(2)
        flags = CBashGeneric_LIST(3, c_ubyte)
        displayNote = CBashFORMID_LIST(4)
        subMenu = CBashFORMID_LIST(5)
        unused1 = CBashUINT8ARRAY_LIST(6, 4)
        numRefs = CBashGeneric_LIST(7, c_ulong)
        compiledSize = CBashGeneric_LIST(8, c_ulong)
        lastIndex = CBashGeneric_LIST(9, c_ulong)
        scriptType = CBashGeneric_LIST(10, c_ushort)
        scriptFlags = CBashGeneric_LIST(11, c_ushort)
        compiled_p = CBashUINT8ARRAY_LIST(12)
        scriptText = CBashISTRING_LIST(13)

        def create_var(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 14, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 14, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return VarX2(self._RecordID, self._FieldID, self._ListIndex, 14, length)
        vars = CBashLIST_LIST(14, VarX2)
        vars_list = CBashLIST_LIST(14, VarX2, True)

        references = CBashFORMID_OR_UINT32_ARRAY_LIST(15)
        def create_condition(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 16, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 16, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return FNVConditionX2(self._RecordID, self._FieldID, self._ListIndex, 16, length)
        conditions = CBashLIST_LIST(16, FNVConditionX2)
        conditions_list = CBashLIST_LIST(16, FNVConditionX2, True)

        IsAddNote = CBashBasicFlag('flags', 0x01)
        IsForceRedraw = CBashBasicFlag('flags', 0x02)

        IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

        IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
        IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
        IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')
        copyattrs = ['text', 'resultText', 'flags',
                     'displayNote', 'subMenu', 'numRefs',
                     'compiledSize', 'lastIndex',
                     'scriptType', 'scriptFlags', 'compiled_p',
                     'scriptText', 'vars_list',
                     'references', 'conditions_list',]
        exportattrs = copyattrs[:]
        exportattrs.remove('compiled_p')

    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    script = CBashFORMID(19)
    destructable = CBashGrouped(20, FNVDestructable)
    destructable_list = CBashGrouped(20, FNVDestructable, True)

    description = CBashSTRING(25)
    loopSound = CBashFORMID(26)
    passNote = CBashFORMID(27)
    difficultyType = CBashGeneric(28, c_ubyte)
    flags = CBashGeneric(29, c_ubyte)
    serverType = CBashGeneric(30, c_ubyte)
    unused1 = CBashUINT8ARRAY(31, 1)

    def create_menu(self):
        length = _CGetFieldAttribute(self._RecordID, 32, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 32, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Menu(self._RecordID, 32, length)
    menus = CBashLIST(32, Menu)
    menus_list = CBashLIST(32, Menu, True)

    IsVeryEasy = CBashBasicType('difficultyType', 0, 'IsEasy')
    IsEasy = CBashBasicType('difficultyType', 1, 'IsVeryEasy')
    IsAverage = CBashBasicType('difficultyType', 2, 'IsVeryEasy')
    IsHard = CBashBasicType('difficultyType', 3, 'IsVeryEasy')
    IsVeryHard = CBashBasicType('difficultyType', 4, 'IsVeryEasy')
    IsRequiresKey = CBashBasicType('difficultyType', 5, 'IsVeryEasy')

    IsLeveled = CBashBasicFlag('flags', 0x01)
    IsUnlocked = CBashBasicFlag('flags', 0x02)
    IsAlternateColors = CBashBasicFlag('flags', 0x04)
    IsHideWelcomeTextWhenDisplayingImage = CBashBasicFlag('flags', 0x08)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsServer1 = CBashBasicType('serverType', 0, 'IsServer2')
    IsServer2 = CBashBasicType('serverType', 1, 'IsServer1')
    IsServer3 = CBashBasicType('serverType', 2, 'IsServer1')
    IsServer4 = CBashBasicType('serverType', 3, 'IsServer1')
    IsServer5 = CBashBasicType('serverType', 4, 'IsServer1')
    IsServer6 = CBashBasicType('serverType', 5, 'IsServer1')
    IsServer7 = CBashBasicType('serverType', 6, 'IsServer1')
    IsServer8 = CBashBasicType('serverType', 7, 'IsServer1')
    IsServer9 = CBashBasicType('serverType', 8, 'IsServer1')
    IsServer10 = CBashBasicType('serverType', 9, 'IsServer1')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'script', 'destructable_list',
                                           'description', 'loopSound',
                                           'passNote', 'difficultyType',
                                           'flags', 'serverType', 'menus_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvARMORecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ARMO'
    class BipedModel(BaseComponent):
        __slots__ = []
        modPath = CBashISTRING_GROUP(0)
        modt_p = CBashUINT8ARRAY_GROUP(1)

        def create_altTexture(self):
            FieldID = self._FieldID + 2
            length = _CGetFieldAttribute(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return FNVAltTexture(self._RecordID, FieldID, length)
        altTextures = CBashLIST_GROUP(2, FNVAltTexture)
        altTextures_list = CBashLIST_GROUP(2, FNVAltTexture, True)
        flags = CBashGeneric_GROUP(3, c_ubyte)

        IsHead = CBashBasicFlag('flags', 0x01)
        IsTorso = CBashBasicFlag('flags', 0x02)
        IsRightHand = CBashBasicFlag('flags', 0x04)
        IsLeftHand = CBashBasicFlag('flags', 0x08)
        copyattrs = ['modPath', 'modt_p', 'altTextures_list',
                     'flags']
        exportattrs = copyattrs[:]
        exportattrs.remove('modt_p')

    class Sound(ListComponent):
        __slots__ = []
        sound = CBashFORMID_LIST(1)
        chance = CBashGeneric_LIST(2, c_ubyte)
        unused1 = CBashUINT8ARRAY_LIST(3, 3)
        type = CBashGeneric_LIST(4, c_ulong)
        IsWalk = CBashBasicType('type', 17, 'IsSneak')
        IsSneak = CBashBasicType('type', 18, 'IsWalk')
        IsRun = CBashBasicType('type', 19, 'IsWalk')
        IsSneakArmor = CBashBasicType('type', 20, 'IsWalk')
        IsRunArmor = CBashBasicType('type', 21, 'IsWalk')
        IsWalkArmor = CBashBasicType('type', 22, 'IsWalk')
        exportattrs = copyattrs = ['sound', 'chance', 'type']

    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    script = CBashFORMID(14)
    effect = CBashFORMID(15)
    flags = CBashGeneric(16, c_ulong)
    extraFlags = CBashGeneric(17, c_ubyte)
    unused1 = CBashUINT8ARRAY(18, 3)
    male = CBashGrouped(19, BipedModel)
    male_list = CBashGrouped(19, BipedModel, True)

    maleWorld = CBashGrouped(23, WorldModel)
    maleWorld_list = CBashGrouped(23, WorldModel, True)

    maleIconPath = CBashISTRING(26)
    maleSmallIconPath = CBashISTRING(27)
    female = CBashGrouped(28, BipedModel)
    female_list = CBashGrouped(28, BipedModel, True)

    femaleWorld = CBashGrouped(32, WorldModel)
    femaleWorld_list = CBashGrouped(32, WorldModel, True)

    femaleIconPath = CBashISTRING(35)
    femaleSmallIconPath = CBashISTRING(36)
    ragdollTemplatePath = CBashISTRING(37)
    repairList = CBashFORMID(38)
    modelList = CBashFORMID(39)
    equipmentType = CBashGeneric(40, c_long)
    pickupSound = CBashFORMID(41)
    dropSound = CBashFORMID(42)
    value = CBashGeneric(43, c_long)
    health = CBashGeneric(44, c_long)
    weight = CBashFLOAT32(45)
    AR = CBashGeneric(46, c_short)
    voiceFlags = CBashGeneric(47, c_ushort)
    DT = CBashFLOAT32(48)
    unknown1 = CBashUINT8ARRAY(49, 4)
    overrideSounds = CBashGeneric(50, c_ulong)
    def create_sound(self):
        length = _CGetFieldAttribute(self._RecordID, 51, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 51, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Sound(self._RecordID, 51, length)
    sounds = CBashLIST(51, Sound)
    sounds_list = CBashLIST(51, Sound, True)

    soundsTemplate = CBashFORMID(52)

    IsHead = CBashBasicFlag('flags', 0x00000001)
    IsHair = CBashBasicFlag('flags', 0x00000002)
    IsUpperBody = CBashBasicFlag('flags', 0x00000004)
    IsLeftHand = CBashBasicFlag('flags', 0x00000008)
    IsRightHand = CBashBasicFlag('flags', 0x00000010)
    IsWeapon = CBashBasicFlag('flags', 0x00000020)
    IsPipBoy = CBashBasicFlag('flags', 0x00000040)
    IsBackpack = CBashBasicFlag('flags', 0x00000080)
    IsNecklace = CBashBasicFlag('flags', 0x00000100)
    IsHeadband = CBashBasicFlag('flags', 0x00000200)
    IsHat = CBashBasicFlag('flags', 0x00000400)
    IsEyeGlasses = CBashBasicFlag('flags', 0x00000800)
    IsNoseRing = CBashBasicFlag('flags', 0x00001000)
    IsEarrings = CBashBasicFlag('flags', 0x00002000)
    IsMask = CBashBasicFlag('flags', 0x00004000)
    IsChoker = CBashBasicFlag('flags', 0x00008000)
    IsMouthObject = CBashBasicFlag('flags', 0x00010000)
    IsBodyAddon1 = CBashBasicFlag('flags', 0x00020000)
    IsBodyAddon2 = CBashBasicFlag('flags', 0x00040000)
    IsBodyAddon3 = CBashBasicFlag('flags', 0x00080000)

    IsUnknown1 = CBashBasicFlag('extraFlags', 0x0001)
    IsUnknown2 = CBashBasicFlag('extraFlags', 0x0002)
    IsHasBackpack = CBashBasicFlag('extraFlags', 0x0004)
    IsMedium = CBashBasicFlag('extraFlags', 0x0008)
    IsUnknown3 = CBashBasicFlag('extraFlags', 0x0010)
    IsPowerArmor = CBashBasicFlag('extraFlags', 0x0020)
    IsNonPlayable = CBashBasicFlag('extraFlags', 0x0040)
    IsHeavy = CBashBasicFlag('extraFlags', 0x0080)

    IsNone = CBashBasicType('equipmentType', -1, 'IsBigGuns')
    IsBigGuns = CBashBasicType('equipmentType', 0, 'IsNone')
    IsEnergyWeapons = CBashBasicType('equipmentType', 1, 'IsNone')
    IsSmallGuns = CBashBasicType('equipmentType', 2, 'IsNone')
    IsMeleeWeapons = CBashBasicType('equipmentType', 3, 'IsNone')
    IsUnarmedWeapon = CBashBasicType('equipmentType', 4, 'IsNone')
    IsThrownWeapons = CBashBasicType('equipmentType', 5, 'IsNone')
    IsMine = CBashBasicType('equipmentType', 6, 'IsNone')
    IsBodyWear = CBashBasicType('equipmentType', 7, 'IsNone')
    IsHeadWear = CBashBasicType('equipmentType', 8, 'IsNone')
    IsHandWear = CBashBasicType('equipmentType', 9, 'IsNone')
    IsChems = CBashBasicType('equipmentType', 10, 'IsNone')
    IsStimpack = CBashBasicType('equipmentType', 11, 'IsNone')
    IsEdible = CBashBasicType('equipmentType', 12, 'IsNone')
    IsAlcohol = CBashBasicType('equipmentType', 13, 'IsNone')

    IsNotOverridingSounds = CBashBasicType('overrideSounds', 0, 'IsOverridingSounds')
    IsOverridingSounds = CBashBasicType('overrideSounds', 1, 'IsNotOverridingSounds')

    IsModulatesVoice = CBashBasicFlag('voiceFlags', 0x0001)
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                                         'boundX2', 'boundY2', 'boundZ2',
                                                         'full', 'script', 'effect',
                                                         'flags', 'extraFlags',
                                                         'male_list', 'maleWorld_list',
                                                         'maleIconPath', 'maleSmallIconPath',
                                                         'female_list', 'femaleWorld_list',
                                                         'femaleIconPath', 'femaleSmallIconPath',
                                                         'ragdollTemplatePath', 'repairList',
                                                         'modelList', 'equipmentType',
                                                         'pickupSound', 'dropSound', 'value',
                                                         'health', 'weight', 'AR', 'voiceFlags',
                                                         'DT', 'unknown1', 'overrideSounds',
                                                         'sounds_list', 'soundsTemplate']

class FnvBOOKRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'BOOK'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    script = CBashFORMID(21)
    description = CBashSTRING(22)
    destructable = CBashGrouped(23, FNVDestructable)
    destructable_list = CBashGrouped(23, FNVDestructable, True)

    flags = CBashGeneric(28, c_ubyte)
    teaches = CBashGeneric(29, c_byte)
    value = CBashGeneric(30, c_long)
    weight = CBashFLOAT32(31)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsFixed = CBashBasicFlag('flags', 0x00000002)
    IsCantBeTaken = CBashAlias('IsFixed')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath',
                                           'script', 'description',
                                           'destructable_list', 'flags',
                                           'teaches', 'value', 'weight']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvCONTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CONT'
    def mergeFilter(self, target):
        """Filter out items that don't come from specified modSet.
        Filters items."""
        self.items = [x for x in self.items if x.item.ValidateFormID(target)]

    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    script = CBashFORMID(19)

    def create_item(self):
        length = _CGetFieldAttribute(self._RecordID, 20, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 20, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVItem(self._RecordID, 20, length)
    items = CBashLIST(20, FNVItem)
    items_list = CBashLIST(20, FNVItem, True)

    destructable = CBashGrouped(21, FNVDestructable)
    destructable_list = CBashGrouped(21, FNVDestructable, True)

    flags = CBashGeneric(26, c_ubyte)
    weight = CBashFLOAT32(27)
    openSound = CBashFORMID(28)
    closeSound = CBashFORMID(29)
    loopSound = CBashFORMID(30)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsRespawn = CBashBasicFlag('flags', 0x00000001)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'script', 'items_list',
                                           'destructable_list', 'flags',
                                           'weight', 'openSound',
                                           'closeSound', 'loopSound',]
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvDOORRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'DOOR'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    script = CBashFORMID(19)
    destructable = CBashGrouped(20, FNVDestructable)
    destructable_list = CBashGrouped(20, FNVDestructable, True)

    openSound = CBashFORMID(25)
    closeSound = CBashFORMID(26)
    loopSound = CBashFORMID(27)
    flags = CBashGeneric(28, c_ubyte)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsAutomatic = CBashBasicFlag('flags', 0x02)
    IsHidden = CBashBasicFlag('flags', 0x04)
    IsMinimalUse = CBashBasicFlag('flags', 0x08)
    IsSlidingDoor = CBashBasicFlag('flags', 0x10)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'script', 'destructable_list',
                                           'openSound', 'closeSound',
                                           'loopSound', 'flags']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvINGRRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'INGR'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    script = CBashFORMID(21)
    equipmentType = CBashGeneric(22, c_long)
    weight = CBashFLOAT32(23)
    value = CBashGeneric(24, c_long)
    flags = CBashGeneric(25, c_ubyte)
    unused1 = CBashUINT8ARRAY(26, 3)

    def create_effect(self):
        length = _CGetFieldAttribute(self._RecordID, 27, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 27, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVEffect(self._RecordID, 27, length)
    effects = CBashLIST(27, FNVEffect)
    effects_list = CBashLIST(27, FNVEffect, True)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath',
                                           'script', 'equipmentType',
                                           'weight', 'value', 'flags',
                                           'effects_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvLIGHRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'LIGH'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    script = CBashFORMID(21)
    duration = CBashGeneric(22, c_long)
    radius = CBashGeneric(23, c_ulong)
    red = CBashGeneric(24, c_ubyte)
    green = CBashGeneric(25, c_ubyte)
    blue = CBashGeneric(26, c_ubyte)
    unused1 = CBashUINT8ARRAY(27, 1)
    flags = CBashGeneric(28, c_ulong)
    falloff = CBashFLOAT32(29)
    fov = CBashFLOAT32(30)
    value = CBashGeneric(31, c_ulong)
    weight = CBashFLOAT32(32)
    fade = CBashFLOAT32(33)
    sound = CBashFORMID(34)

    IsDynamic = CBashBasicFlag('flags', 0x00000001)
    IsCanTake = CBashBasicFlag('flags', 0x00000002)
    IsNegative = CBashBasicFlag('flags', 0x00000004)
    IsFlickers = CBashBasicFlag('flags', 0x00000008)
    IsOffByDefault = CBashBasicFlag('flags', 0x00000020)
    IsFlickerSlow = CBashBasicFlag('flags', 0x00000040)
    IsPulse = CBashBasicFlag('flags', 0x00000080)
    IsPulseSlow = CBashBasicFlag('flags', 0x00000100)
    IsSpotLight = CBashBasicFlag('flags', 0x00000200)
    IsSpotShadow = CBashBasicFlag('flags', 0x00000400)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath',
                                           'script', 'duration', 'radius',
                                           'red', 'green', 'blue',
                                           'flags', 'falloff', 'fov',
                                           'value', 'weight', 'fade', 'sound']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvMISCRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'MISC'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    script = CBashFORMID(21)
    destructable = CBashGrouped(22, FNVDestructable)
    destructable_list = CBashGrouped(22, FNVDestructable, True)

    pickupSound = CBashFORMID(27)
    dropSound = CBashFORMID(28)
    value = CBashGeneric(29, c_long)
    weight = CBashFLOAT32(30)
    loopSound = CBashFORMID(31)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath',
                                           'script', 'destructable_list',
                                           'pickupSound', 'dropSound',
                                           'value', 'weight', 'loopSound']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvSTATRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'STAT'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    modPath = CBashISTRING(13)
    modb = CBashFLOAT32(14)
    modt_p = CBashUINT8ARRAY(15)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 16, length)
    altTextures = CBashLIST(16, FNVAltTexture)
    altTextures_list = CBashLIST(16, FNVAltTexture, True)

    modelFlags = CBashGeneric(17, c_ubyte)
    passSound = CBashGeneric(18, c_byte)
    loopSound = CBashFORMID(19)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsNone = CBashBasicType('passSound', -1, 'IsBushA')
    IsBushA = CBashBasicType('passSound', 0, 'IsNone')
    IsBushB = CBashBasicType('passSound', 1, 'IsNone')
    IsBushC = CBashBasicType('passSound', 2, 'IsNone')
    IsBushD = CBashBasicType('passSound', 3, 'IsNone')
    IsBushE = CBashBasicType('passSound', 4, 'IsNone')
    IsBushF = CBashBasicType('passSound', 5, 'IsNone')
    IsBushG = CBashBasicType('passSound', 6, 'IsNone')
    IsBushH = CBashBasicType('passSound', 7, 'IsNone')
    IsBushI = CBashBasicType('passSound', 8, 'IsNone')
    IsBushJ = CBashBasicType('passSound', 9, 'IsNone')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'passSound', 'loopSound',]
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvSCOLRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'SCOL'
    class Static(ListComponent):
        __slots__ = []
        class Placement(ListX2Component):
            __slots__ = []
            posX = CBashFLOAT32_LISTX2(1)
            posY = CBashFLOAT32_LISTX2(2)
            posZ = CBashFLOAT32_LISTX2(3)
            rotX = CBashFLOAT32_LISTX2(4)
            rotX_degrees = CBashDEGREES_LISTX2(4)
            rotY = CBashFLOAT32_LISTX2(5)
            rotY_degrees = CBashDEGREES_LISTX2(5)
            rotZ = CBashFLOAT32_LISTX2(6)
            rotZ_degrees = CBashDEGREES_LISTX2(6)
            scale = CBashFLOAT32_LISTX2(7)
            exportattrs = copyattrs = ['posX', 'posY', 'posZ',
                                       'rotX', 'rotY', 'rotZ',
                                       'scale']

        static = CBashFORMID_LIST(1)

        def create_placement(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Placement(self._RecordID, self._FieldID, self._ListIndex, 2, length)
        placements = CBashLIST_LIST(2, Placement)
        placements_list = CBashLIST_LIST(2, Placement, True)

        exportattrs = copyattrs = ['static', 'placements_list']

    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    modPath = CBashISTRING(13)
    modb = CBashFLOAT32(14)
    modt_p = CBashUINT8ARRAY(15)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 16, length)
    altTextures = CBashLIST(16, FNVAltTexture)
    altTextures_list = CBashLIST(16, FNVAltTexture, True)

    modelFlags = CBashGeneric(17, c_ubyte)

    def create_static(self):
        length = _CGetFieldAttribute(self._RecordID, 18, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 18, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Static(self._RecordID, 18, length)
    statics = CBashLIST(18, Static)
    statics_list = CBashLIST(18, Static, True)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'statics_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvMSTTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'MSTT'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    destructable = CBashGrouped(19, FNVDestructable)
    destructable_list = CBashGrouped(19, FNVDestructable, True)

    data_p = CBashUINT8ARRAY(24)
    sound = CBashFORMID(25)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'destructable_list', 'data_p',
                                           'sound']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')
    exportattrs.remove('data_p')

class FnvPWATRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'PWAT'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    modPath = CBashISTRING(13)
    modb = CBashFLOAT32(14)
    modt_p = CBashUINT8ARRAY(15)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 16, length)
    altTextures = CBashLIST(16, FNVAltTexture)
    altTextures_list = CBashLIST(16, FNVAltTexture, True)

    modelFlags = CBashGeneric(17, c_ubyte)
    flags = CBashGeneric(18, c_ulong)
    water = CBashFORMID(19)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsReflects = CBashBasicFlag('flags', 0x00000001)
    IsReflectsActors = CBashBasicFlag('flags', 0x00000002)
    IsReflectsLand = CBashBasicFlag('flags', 0x00000004)
    IsReflectsLODLand = CBashBasicFlag('flags', 0x00000008)
    IsReflectsLODBuildings = CBashBasicFlag('flags', 0x00000010)
    IsReflectsTrees = CBashBasicFlag('flags', 0x00000020)
    IsReflectsSky = CBashBasicFlag('flags', 0x00000040)
    IsReflectsDynamicObjects = CBashBasicFlag('flags', 0x00000080)
    IsReflectsDeadBodies = CBashBasicFlag('flags', 0x00000100)
    IsRefracts = CBashBasicFlag('flags', 0x00000200)
    IsRefractsActors = CBashBasicFlag('flags', 0x00000400)
    IsRefractsLand = CBashBasicFlag('flags', 0x00000800)
    IsRefractsDynamicObjects = CBashBasicFlag('flags', 0x00010000)
    IsRefractsDeadBodies = CBashBasicFlag('flags', 0x00020000)
    IsSilhouetteReflections = CBashBasicFlag('flags', 0x00040000)
    IsDepth = CBashBasicFlag('flags', 0x10000000)
    IsObjectTextureCoordinates = CBashBasicFlag('flags', 0x20000000)
    IsNoUnderwaterFog = CBashBasicFlag('flags', 0x80000000)
    IsUnderwaterFog = CBashInvertedFlag('IsNoUnderwaterFog')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'modPath', 'modb', 'modt_p',
                                           'altTextures_list',
                                           'modelFlags', 'flags', 'water']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvGRASRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'GRAS'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    modPath = CBashISTRING(13)
    modb = CBashFLOAT32(14)
    modt_p = CBashUINT8ARRAY(15)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 16, length)
    altTextures = CBashLIST(16, FNVAltTexture)
    altTextures_list = CBashLIST(16, FNVAltTexture, True)

    modelFlags = CBashGeneric(17, c_ubyte)
    density = CBashGeneric(18, c_ubyte)
    minSlope = CBashGeneric(19, c_ubyte)
    maxSlope = CBashGeneric(20, c_ubyte)
    unused1 = CBashUINT8ARRAY(21, 1)
    waterDistance = CBashGeneric(22, c_ushort)
    unused2 = CBashUINT8ARRAY(23, 2)
    waterOp = CBashGeneric(24, c_ulong)
    posRange = CBashFLOAT32(25)
    heightRange = CBashFLOAT32(26)
    colorRange = CBashFLOAT32(27)
    wavePeriod = CBashFLOAT32(28)
    flags = CBashGeneric(29, c_ubyte)
    unused3 = CBashUINT8ARRAY(30, 3)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsVLighting = CBashBasicFlag('flags', 0x00000001)
    IsVertexLighting = CBashAlias('IsVLighting')
    IsUScaling = CBashBasicFlag('flags', 0x00000002)
    IsUniformScaling = CBashAlias('IsUScaling')
    IsFitSlope = CBashBasicFlag('flags', 0x00000004)
    IsFitToSlope = CBashAlias('IsFitSlope')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'density', 'minSlope', 'maxSlope',
                                           'waterDistance', 'waterOp',
                                           'posRange', 'heightRange',
                                           'colorRange', 'wavePeriod',
                                           'flags']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvTREERecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'TREE'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    modPath = CBashISTRING(13)
    modb = CBashFLOAT32(14)
    modt_p = CBashUINT8ARRAY(15)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 16, length)
    altTextures = CBashLIST(16, FNVAltTexture)
    altTextures_list = CBashLIST(16, FNVAltTexture, True)

    modelFlags = CBashGeneric(17, c_ubyte)
    iconPath = CBashISTRING(18)
    smallIconPath = CBashISTRING(19)
    speedTree = CBashUINT32ARRAY(20)
    curvature = CBashFLOAT32(21)
    minAngle = CBashFLOAT32(22)
    maxAngle = CBashFLOAT32(23)
    branchDim = CBashFLOAT32(24)
    leafDim = CBashFLOAT32(25)
    shadowRadius = CBashGeneric(26, c_long)
    rockSpeed = CBashFLOAT32(27)
    rustleSpeed = CBashFLOAT32(28)
    widthBill = CBashFLOAT32(29)
    heightBill = CBashFLOAT32(30)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath',
                                           'speedTree', 'curvature',
                                           'minAngle', 'maxAngle',
                                           'branchDim', 'leafDim',
                                           'shadowRadius', 'rockSpeed',
                                           'rustleSpeed', 'widthBill',
                                           'heightBill']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvFURNRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'FURN'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    script = CBashFORMID(19)
    destructable = CBashGrouped(20, FNVDestructable)
    destructable_list = CBashGrouped(20, FNVDestructable, True)

    flags = CBashGeneric(25, c_ulong)

    IsAnim01 = CBashBasicFlag('flags', 0x00000001)
    IsAnim02 = CBashBasicFlag('flags', 0x00000002)
    IsAnim03 = CBashBasicFlag('flags', 0x00000004)
    IsAnim04 = CBashBasicFlag('flags', 0x00000008)
    IsAnim05 = CBashBasicFlag('flags', 0x00000010)
    IsAnim06 = CBashBasicFlag('flags', 0x00000020)
    IsAnim07 = CBashBasicFlag('flags', 0x00000040)
    IsAnim08 = CBashBasicFlag('flags', 0x00000080)
    IsAnim09 = CBashBasicFlag('flags', 0x00000100)
    IsAnim10 = CBashBasicFlag('flags', 0x00000200)
    IsAnim11 = CBashBasicFlag('flags', 0x00000400)
    IsAnim12 = CBashBasicFlag('flags', 0x00000800)
    IsAnim13 = CBashBasicFlag('flags', 0x00001000)
    IsAnim14 = CBashBasicFlag('flags', 0x00002000)
    IsAnim15 = CBashBasicFlag('flags', 0x00004000)
    IsAnim16 = CBashBasicFlag('flags', 0x00008000)
    IsAnim17 = CBashBasicFlag('flags', 0x00010000)
    IsAnim18 = CBashBasicFlag('flags', 0x00020000)
    IsAnim19 = CBashBasicFlag('flags', 0x00040000)
    IsAnim20 = CBashBasicFlag('flags', 0x00080000)
    IsAnim21 = CBashBasicFlag('flags', 0x00100000)
    IsAnim22 = CBashBasicFlag('flags', 0x00200000)
    IsAnim23 = CBashBasicFlag('flags', 0x00400000)
    IsAnim24 = CBashBasicFlag('flags', 0x00800000)
    IsAnim25 = CBashBasicFlag('flags', 0x01000000)
    IsAnim26 = CBashBasicFlag('flags', 0x02000000)
    IsAnim27 = CBashBasicFlag('flags', 0x04000000)
    IsAnim28 = CBashBasicFlag('flags', 0x08000000)
    IsAnim29 = CBashBasicFlag('flags', 0x10000000)
    IsAnim30 = CBashBasicFlag('flags', 0x20000000)
    IsSitAnim = CBashMaskedType('flags', 0xC0000000, 0x40000000, 'IsSleepAnim')
    IsSleepAnim = CBashMaskedType('flags', 0xC0000000, 0x80000000, 'IsSitAnim')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'script', 'destructable_list',
                                           'flags']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvWEAPRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'WEAP'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    script = CBashFORMID(21)
    effect = CBashFORMID(22)
    chargeAmount = CBashGeneric(23, c_short)
    ammo = CBashFORMID(24)
    destructable = CBashGrouped(25, FNVDestructable)
    destructable_list = CBashGrouped(25, FNVDestructable, True)

    repairList = CBashFORMID(30)
    equipmentType = CBashGeneric(31, c_long)
    modelList = CBashFORMID(32)
    pickupSound = CBashFORMID(33)
    dropSound = CBashFORMID(34)
    shell = CBashGrouped(35, WorldModel)
    shell_list = CBashGrouped(35, WorldModel, True)

    scope = CBashGrouped(38, WorldModel)
    scope_list = CBashGrouped(38, WorldModel, True)

    scopeEffect = CBashFORMID(41)
    world = CBashGrouped(42, WorldModel)
    world_list = CBashGrouped(42, WorldModel, True)

    vatsName = CBashSTRING(45)
    weaponNode = CBashSTRING(46)
    model1Path = CBashISTRING(47)
    model2Path = CBashISTRING(48)
    model12Path = CBashISTRING(49)
    model3Path = CBashISTRING(50)
    model13Path = CBashISTRING(51)
    model23Path = CBashISTRING(52)
    model123Path = CBashISTRING(53)
    impact = CBashFORMID(54)
    model = CBashFORMID(55)
    model1 = CBashFORMID(56)
    model2 = CBashFORMID(57)
    model12 = CBashFORMID(58)
    model3 = CBashFORMID(59)
    model13 = CBashFORMID(60)
    model23 = CBashFORMID(61)
    model123 = CBashFORMID(62)
    mod1 = CBashFORMID(63)
    mod2 = CBashFORMID(64)
    mod3 = CBashFORMID(65)
    sound3D = CBashFORMID(66)
    soundDist = CBashFORMID(67)
    sound2D = CBashFORMID(68)
    sound3DLoop = CBashFORMID(69)
    soundMelee = CBashFORMID(70)
    soundBlock = CBashFORMID(71)
    soundIdle = CBashFORMID(72)
    soundEquip = CBashFORMID(73)
    soundUnequip = CBashFORMID(74)
    soundMod3D = CBashFORMID(75)
    soundModDist = CBashFORMID(76)
    soundMod2D = CBashFORMID(77)
    value = CBashGeneric(78, c_long)
    health = CBashGeneric(79, c_long)
    weight = CBashFLOAT32(80)
    damage = CBashGeneric(81, c_short)
    clipSize = CBashGeneric(82, c_ubyte)
    animType = CBashGeneric(83, c_ulong)
    animMult = CBashFLOAT32(84)
    reach = CBashFLOAT32(85)
    flags = CBashGeneric(86, c_ubyte)
    gripAnim = CBashGeneric(87, c_ubyte)
    ammoUse = CBashGeneric(88, c_ubyte)
    reloadAnim = CBashGeneric(89, c_ubyte)
    minSpread = CBashFLOAT32(90)
    spread = CBashFLOAT32(91)
    unknown1 = CBashFLOAT32(92)
    sightFOV = CBashFLOAT32(93)
    unknown2 = CBashFLOAT32(94)
    projectile = CBashFORMID(95)
    VATSHitChance = CBashGeneric(96, c_ubyte)
    attackAnim = CBashGeneric(97, c_ubyte)
    projectileCount = CBashGeneric(98, c_ubyte)
    weaponAV = CBashGeneric(99, c_ubyte)
    minRange = CBashFLOAT32(100)
    maxRange = CBashFLOAT32(101)
    onHit = CBashGeneric(102, c_ulong)
    extraFlags = CBashGeneric(103, c_ulong)
    animAttackMult = CBashFLOAT32(104)
    fireRate = CBashFLOAT32(105)
    overrideAP = CBashFLOAT32(106)
    leftRumble = CBashFLOAT32(107)
    timeRumble = CBashFLOAT32(108)
    overrideDamageToWeapon = CBashFLOAT32(109)
    reloadTime = CBashFLOAT32(110)
    jamTime = CBashFLOAT32(111)
    aimArc = CBashFLOAT32(112)
    skill = CBashGeneric(113, c_long)
    rumbleType = CBashGeneric(114, c_ulong)
    rumbleWavelength = CBashFLOAT32(115)
    limbDamageMult = CBashFLOAT32(116)
    resistType = CBashGeneric(117, c_long)
    sightUsage = CBashFLOAT32(118)
    semiFireDelayMin = CBashFLOAT32(119)
    semiFireDelayMax = CBashFLOAT32(120)
    unknown3 = CBashFLOAT32(121)
    effectMod1 = CBashGeneric(122, c_ulong)
    effectMod2 = CBashGeneric(123, c_ulong)
    effectMod3 = CBashGeneric(124, c_ulong)
    valueAMod1 = CBashFLOAT32(125)
    valueAMod2 = CBashFLOAT32(126)
    valueAMod3 = CBashFLOAT32(127)
    overridePwrAtkAnim = CBashGeneric(128, c_ulong)
    strengthReq = CBashGeneric(129, c_ulong)
    unknown4 = CBashGeneric(130, c_ubyte)
    reloadAnimMod = CBashGeneric(131, c_ubyte)
    unknown5 = CBashUINT8ARRAY(132, 2)
    regenRate = CBashFLOAT32(133)
    killImpulse = CBashFLOAT32(134)
    valueBMod1 = CBashFLOAT32(135)
    valueBMod2 = CBashFLOAT32(136)
    valueBMod3 = CBashFLOAT32(137)
    skillReq = CBashGeneric(138, c_ulong)
    critDamage = CBashGeneric(139, c_ushort)
    unused1 = CBashUINT8ARRAY(140, 2)
    critMult = CBashFLOAT32(141)
    critFlags = CBashGeneric(142, c_ubyte)
    unused2 = CBashUINT8ARRAY(143, 3)
    critEffect = CBashFORMID(144)
    vatsEffect = CBashFORMID(145)
    vatsSkill = CBashFLOAT32(146)
    vatsDamageMult = CBashFLOAT32(147)
    AP = CBashFLOAT32(148)
    silenceType = CBashGeneric(149, c_ubyte)
    modRequiredType = CBashGeneric(150, c_ubyte)
    unused3 = CBashUINT8ARRAY(151, 2)
    soundLevelType = CBashGeneric(152, c_ulong)

    IsNotNormalWeapon = CBashBasicFlag('flags', 0x01)
    IsNormalWeapon = CBashInvertedFlag('IsNotNormalWeapon')
    IsAutomatic = CBashBasicFlag('flags', 0x02)
    IsHasScope = CBashBasicFlag('flags', 0x04)
    IsCantDrop = CBashBasicFlag('flags', 0x08)
    IsCanDrop = CBashInvertedFlag('IsCantDrop')
    IsHideBackpack = CBashBasicFlag('flags', 0x10)
    IsEmbeddedWeapon = CBashBasicFlag('flags', 0x20)
    IsDontUse1stPersonISAnimations = CBashBasicFlag('flags', 0x40)
    IsUse1stPersonISAnimations = CBashInvertedFlag('IsDontUse1stPersonISAnimations')
    IsNonPlayable = CBashBasicFlag('flags', 0x80)
    IsPlayable = CBashInvertedFlag('IsNonPlayable')

    IsPlayerOnly = CBashBasicFlag('extraFlags', 0x00000001)
    IsNPCsUseAmmo = CBashBasicFlag('extraFlags', 0x00000002)
    IsNoJamAfterReload = CBashBasicFlag('extraFlags', 0x00000004)
    IsJamAfterReload = CBashInvertedFlag('IsNoJamAfterReload')
    IsOverrideActionPoints = CBashBasicFlag('extraFlags', 0x00000008)
    IsMinorCrime = CBashBasicFlag('extraFlags', 0x00000010)
    IsRangeFixed = CBashBasicFlag('extraFlags', 0x00000020)
    IsNotUsedInNormalCombat = CBashBasicFlag('extraFlags', 0x00000040)
    IsUsedInNormalCombat = CBashInvertedFlag('IsNotUsedInNormalCombat')
    IsOverrideDamageToWeaponMult = CBashBasicFlag('extraFlags', 0x00000080)
    IsDontUse3rdPersonISAnimations = CBashBasicFlag('extraFlags', 0x00000100)
    IsUse3rdPersonISAnimations = CBashInvertedFlag('IsDontUse3rdPersonISAnimations')
    IsShortBurst = CBashBasicFlag('extraFlags', 0x00000200)
    IsRumbleAlternate = CBashBasicFlag('extraFlags', 0x00000400)
    IsLongBurst = CBashBasicFlag('extraFlags', 0x00000800)
    IsScopeHasNightVision = CBashBasicFlag('extraFlags', 0x00001000)
    IsScopeFromMod = CBashBasicFlag('extraFlags', 0x00002000)

    IsCritOnDeath = CBashBasicFlag('critFlags', 0x01)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsNone = CBashBasicType('equipmentType', -1, 'IsBigGuns')
    IsBigGuns = CBashBasicType('equipmentType', 0, 'IsNone')
    IsEnergyWeapons = CBashBasicType('equipmentType', 1, 'IsNone')
    IsSmallGuns = CBashBasicType('equipmentType', 2, 'IsNone')
    IsMeleeWeapons = CBashBasicType('equipmentType', 3, 'IsNone')
    IsUnarmedWeapon = CBashBasicType('equipmentType', 4, 'IsNone')
    IsThrownWeapons = CBashBasicType('equipmentType', 5, 'IsNone')
    IsMine = CBashBasicType('equipmentType', 6, 'IsNone')
    IsBodyWear = CBashBasicType('equipmentType', 7, 'IsNone')
    IsHeadWear = CBashBasicType('equipmentType', 8, 'IsNone')
    IsHandWear = CBashBasicType('equipmentType', 9, 'IsNone')
    IsChems = CBashBasicType('equipmentType', 10, 'IsNone')
    IsStimpack = CBashBasicType('equipmentType', 11, 'IsNone')
    IsEdible = CBashBasicType('equipmentType', 12, 'IsNone')
    IsAlcohol = CBashBasicType('equipmentType', 13, 'IsNone')

    IsHand2Hand = CBashBasicType('animType', 0, 'IsMelee1Hand')
    IsMelee1Hand = CBashBasicType('animType', 1, 'IsHand2Hand')
    IsMelee2Hand = CBashBasicType('animType', 2, 'IsHand2Hand')
    IsPistolBallistic1Hand = CBashBasicType('animType', 3, 'IsHand2Hand')
    IsPistolEnergy1Hand = CBashBasicType('animType', 4, 'IsHand2Hand')
    IsRifleBallistic2Hand = CBashBasicType('animType', 5, 'IsHand2Hand')
    IsRifleAutomatic2Hand = CBashBasicType('animType', 6, 'IsHand2Hand')
    IsRifleEnergy2Hand = CBashBasicType('animType', 7, 'IsHand2Hand')
    IsHandle2Hand = CBashBasicType('animType', 8, 'IsHand2Hand')
    IsLauncher2Hand = CBashBasicType('animType', 9, 'IsHand2Hand')
    IsGrenadeThrow1Hand = CBashBasicType('animType', 10, 'IsHand2Hand')
    IsLandMine1Hand = CBashBasicType('animType', 11, 'IsHand2Hand')
    IsMineDrop1Hand = CBashBasicType('animType', 12, 'IsHand2Hand')
    IsThrown1Hand = CBashBasicType('animType', 13, 'IsHand2Hand')

    IsHandGrip1 = CBashBasicType('gripAnim', 230, 'IsHandGrip2')
    IsHandGrip2 = CBashBasicType('gripAnim', 231, 'IsHandGrip1')
    IsHandGrip3 = CBashBasicType('gripAnim', 232, 'IsHandGrip1')
    IsHandGrip4 = CBashBasicType('gripAnim', 233, 'IsHandGrip1')
    IsHandGrip5 = CBashBasicType('gripAnim', 234, 'IsHandGrip1')
    IsHandGrip6 = CBashBasicType('gripAnim', 235, 'IsHandGrip1')
    IsHandGripDefault = CBashBasicType('gripAnim', 236, 'IsHandGrip1')

    IsReloadA = CBashBasicType('reloadAnim', 0, 'IsReloadB')
    IsReloadB = CBashBasicType('reloadAnim', 1, 'IsReloadA')
    IsReloadC = CBashBasicType('reloadAnim', 2, 'IsReloadA')
    IsReloadD = CBashBasicType('reloadAnim', 3, 'IsReloadA')
    IsReloadE = CBashBasicType('reloadAnim', 4, 'IsReloadA')
    IsReloadF = CBashBasicType('reloadAnim', 5, 'IsReloadA')
    IsReloadG = CBashBasicType('reloadAnim', 6, 'IsReloadA')
    IsReloadH = CBashBasicType('reloadAnim', 7, 'IsReloadA')
    IsReloadI = CBashBasicType('reloadAnim', 8, 'IsReloadA')
    IsReloadJ = CBashBasicType('reloadAnim', 9, 'IsReloadA')
    IsReloadK = CBashBasicType('reloadAnim', 10, 'IsReloadA')
    IsReloadL = CBashBasicType('reloadAnim', 11, 'IsReloadA')
    IsReloadM = CBashBasicType('reloadAnim', 12, 'IsReloadA')
    IsReloadN = CBashBasicType('reloadAnim', 13, 'IsReloadA')
    IsReloadO = CBashBasicType('reloadAnim', 14, 'IsReloadA')
    IsReloadP = CBashBasicType('reloadAnim', 15, 'IsReloadA')
    IsReloadQ = CBashBasicType('reloadAnim', 16, 'IsReloadA')
    IsReloadR = CBashBasicType('reloadAnim', 17, 'IsReloadA')
    IsReloadS = CBashBasicType('reloadAnim', 18, 'IsReloadA')
    IsReloadW = CBashBasicType('reloadAnim', 19, 'IsReloadA')
    IsReloadX = CBashBasicType('reloadAnim', 20, 'IsReloadA')
    IsReloadY = CBashBasicType('reloadAnim', 21, 'IsReloadA')
    IsReloadZ = CBashBasicType('reloadAnim', 22, 'IsReloadA')

    IsAttackLeft = CBashBasicType('attackAnim', 26, 'IsAttackRight')
    IsAttackRight = CBashBasicType('attackAnim', 32, 'IsAttackLeft')
    IsAttack3 = CBashBasicType('attackAnim', 38, 'IsAttackLeft')
    IsAttack4 = CBashBasicType('attackAnim', 44, 'IsAttackLeft')
    IsAttack5 = CBashBasicType('attackAnim', 50, 'IsAttackLeft')
    IsAttack6 = CBashBasicType('attackAnim', 56, 'IsAttackLeft')
    IsAttack7 = CBashBasicType('attackAnim', 62, 'IsAttackLeft')
    IsAttack8 = CBashBasicType('attackAnim', 68, 'IsAttackLeft')
    IsAttack9 = CBashBasicType('attackAnim', 144, 'IsAttackLeft')
    IsAttackLoop = CBashBasicType('attackAnim', 74, 'IsAttackLeft')
    IsAttackSpin = CBashBasicType('attackAnim', 80, 'IsAttackLeft')
    IsAttackSpin2 = CBashBasicType('attackAnim', 86, 'IsAttackLeft')
    IsAttackThrow = CBashBasicType('attackAnim', 114, 'IsAttackLeft')
    IsAttackThrow2 = CBashBasicType('attackAnim', 120, 'IsAttackLeft')
    IsAttackThrow3 = CBashBasicType('attackAnim', 126, 'IsAttackLeft')
    IsAttackThrow4 = CBashBasicType('attackAnim', 132, 'IsAttackLeft')
    IsAttackThrow5 = CBashBasicType('attackAnim', 138, 'IsAttackLeft')
    IsAttackThrow6 = CBashBasicType('attackAnim', 150, 'IsAttackLeft')
    IsAttackThrow7 = CBashBasicType('attackAnim', 156, 'IsAttackLeft')
    IsAttackThrow8 = CBashBasicType('attackAnim', 162, 'IsAttackLeft')
    IsPlaceMine = CBashBasicType('attackAnim', 102, 'IsAttackLeft')
    IsPlaceMine2 = CBashBasicType('attackAnim', 108, 'IsAttackLeft')
    IsAttackDefault = CBashBasicType('attackAnim', 255, 'IsAttackLeft')

    IsNormalFormulaBehavior = CBashBasicType('weaponAV', 0, 'IsDismemberOnly')
    IsDismemberOnly = CBashBasicType('weaponAV', 1, 'IsNormalFormulaBehavior')
    IsExplodeOnly = CBashBasicType('weaponAV', 2, 'IsNormalFormulaBehavior')
    IsNoDismemberExplode = CBashBasicType('weaponAV', 3, 'IsNormalFormulaBehavior')
    IsDismemberExplode = CBashInvertedFlag('IsNoDismemberExplode')

    IsOnHitPerception = CBashBasicType('onHit', 0, 'IsEndurance')
    IsOnHitEndurance = CBashBasicType('onHit', 1, 'IsPerception')
    IsOnHitLeftAttack = CBashBasicType('onHit', 2, 'IsPerception')
    IsOnHitRightAttack = CBashBasicType('onHit', 3, 'IsPerception')
    IsOnHitLeftMobility = CBashBasicType('onHit', 4, 'IsPerception')
    IsOnHitRightMobilty = CBashBasicType('onHit', 5, 'IsPerception')
    IsOnHitBrain = CBashBasicType('onHit', 6, 'IsPerception')

    IsRumbleConstant = CBashBasicType('rumbleType', 0, 'IsSquare')
    IsRumbleSquare = CBashBasicType('rumbleType', 1, 'IsConstant')
    IsRumbleTriangle = CBashBasicType('rumbleType', 2, 'IsConstant')
    IsRumbleSawtooth = CBashBasicType('rumbleType', 3, 'IsConstant')

    IsUnknown0 = CBashBasicType('overridePwrAtkAnim', 0, 'IsAttackCustom1Power')
    IsAttackCustom1Power = CBashBasicType('overridePwrAtkAnim', 97, 'IsAttackCustom2Power')
    IsAttackCustom2Power = CBashBasicType('overridePwrAtkAnim', 98, 'IsAttackCustom1Power')
    IsAttackCustom3Power = CBashBasicType('overridePwrAtkAnim', 99, 'IsAttackCustom1Power')
    IsAttackCustom4Power = CBashBasicType('overridePwrAtkAnim', 100, 'IsAttackCustom1Power')
    IsAttackCustom5Power = CBashBasicType('overridePwrAtkAnim', 101, 'IsAttackCustom1Power')
    IsAttackCustomDefault = CBashBasicType('overridePwrAtkAnim', 255, 'IsAttackCustom1Power')

    IsModReloadA = CBashBasicType('reloadAnimMod', 0, 'IsModReloadB')
    IsModReloadB = CBashBasicType('reloadAnimMod', 1, 'IsModReloadA')
    IsModReloadC = CBashBasicType('reloadAnimMod', 2, 'IsModReloadA')
    IsModReloadD = CBashBasicType('reloadAnimMod', 3, 'IsModReloadA')
    IsModReloadE = CBashBasicType('reloadAnimMod', 4, 'IsModReloadA')
    IsModReloadF = CBashBasicType('reloadAnimMod', 5, 'IsModReloadA')
    IsModReloadG = CBashBasicType('reloadAnimMod', 6, 'IsModReloadA')
    IsModReloadH = CBashBasicType('reloadAnimMod', 7, 'IsModReloadA')
    IsModReloadI = CBashBasicType('reloadAnimMod', 8, 'IsModReloadA')
    IsModReloadJ = CBashBasicType('reloadAnimMod', 9, 'IsModReloadA')
    IsModReloadK = CBashBasicType('reloadAnimMod', 10, 'IsModReloadA')
    IsModReloadL = CBashBasicType('reloadAnimMod', 11, 'IsModReloadA')
    IsModReloadM = CBashBasicType('reloadAnimMod', 12, 'IsModReloadA')
    IsModReloadN = CBashBasicType('reloadAnimMod', 13, 'IsModReloadA')
    IsModReloadO = CBashBasicType('reloadAnimMod', 14, 'IsModReloadA')
    IsModReloadP = CBashBasicType('reloadAnimMod', 15, 'IsModReloadA')
    IsModReloadQ = CBashBasicType('reloadAnimMod', 16, 'IsModReloadA')
    IsModReloadR = CBashBasicType('reloadAnimMod', 17, 'IsModReloadA')
    IsModReloadS = CBashBasicType('reloadAnimMod', 18, 'IsModReloadA')
    IsModReloadW = CBashBasicType('reloadAnimMod', 19, 'IsModReloadA')
    IsModReloadX = CBashBasicType('reloadAnimMod', 20, 'IsModReloadA')
    IsModReloadY = CBashBasicType('reloadAnimMod', 21, 'IsModReloadA')
    IsModReloadZ = CBashBasicType('reloadAnimMod', 22, 'IsModReloadA')

    IsVATSNotSilent = CBashBasicType('silenceType', 0, 'IsVATSSilent')
    IsVATSSilent = CBashBasicType('silenceType', 1, 'IsVATSNotSilent')

    IsVATSNotModRequired = CBashBasicType('modRequiredType', 0, 'IsVATSNotModRequired')
    IsVATSModRequired = CBashBasicType('modRequiredType', 1, 'IsVATSModRequired')

    IsLoud = CBashBasicType('soundLevelType', 0, 'IsNormal')
    IsNormal = CBashBasicType('soundLevelType', 1, 'IsLoud')
    IsSilent = CBashBasicType('soundLevelType', 2, 'IsLoud')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath', 'script',
                                           'effect', 'chargeAmount', 'ammo',
                                           'destructable_list', 'repairList',
                                           'equipmentType', 'modelList',
                                           'pickupSound', 'dropSound', 'shell_list',
                                           'scope_list', 'scopeEffect', 'world_list',
                                           'vatsName', 'weaponNode', 'model1Path',
                                           'model2Path', 'model12Path', 'model3Path',
                                           'model13Path', 'model23Path',
                                           'model123Path', 'impact', 'model',
                                           'model1', 'model2', 'model12', 'model3',
                                           'model13', 'model23', 'model123', 'mod1',
                                           'mod2', 'mod3', 'sound3D', 'soundDist',
                                           'sound2D', 'sound3DLoop', 'soundMelee',
                                           'soundBlock', 'soundIdle', 'soundEquip',
                                           'soundUnequip', 'soundMod3D',
                                           'soundModDist', 'soundMod2D', 'value',
                                           'health', 'weight', 'damage', 'clipSize',
                                           'animType', 'animMult', 'reach', 'flags',
                                           'gripAnim', 'ammoUse', 'reloadAnim',
                                           'minSpread', 'spread', 'unknown1',
                                           'sightFOV', 'unknown2', 'projectile',
                                           'VATSHitChance', 'attackAnim',
                                           'projectileCount', 'weaponAV',
                                           'minRange', 'maxRange', 'onHit',
                                           'extraFlags', 'animAttackMult',
                                           'fireRate', 'overrideAP', 'leftRumble',
                                           'timeRumble', 'overrideDamageToWeapon',
                                           'reloadTime', 'jamTime', 'aimArc',
                                           'skill', 'rumbleType',
                                           'rumbleWavelength', 'limbDamageMult',
                                           'resistType', 'sightUsage',
                                           'semiFireDelayMin', 'semiFireDelayMax',
                                           'unknown3', 'effectMod1', 'effectMod2',
                                           'effectMod3', 'valueAMod1', 'valueAMod2',
                                           'valueAMod3', 'overridePwrAtkAnim',
                                           'strengthReq', 'unknown4',
                                           'reloadAnimMod', 'unknown5', 'regenRate',
                                           'killImpulse', 'valueBMod1', 'valueBMod2',
                                           'valueBMod3', 'skillReq', 'critDamage',
                                           'critMult', 'critFlags', 'critEffect',
                                           'vatsEffect', 'vatsSkill', 'vatsDamageMult', 'AP',
                                           'silenceType', 'modRequiredType',
                                           'soundLevelType']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')
    exportattrs.remove('unknown1')
    exportattrs.remove('unknown2')
    exportattrs.remove('unknown3')
    exportattrs.remove('unknown4')
    exportattrs.remove('unknown5')

class FnvAMMORecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'AMMO'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    script = CBashFORMID(21)
    destructable = CBashGrouped(22, FNVDestructable)
    destructable_list = CBashGrouped(22, FNVDestructable, True)

    pickupSound = CBashFORMID(27)
    dropSound = CBashFORMID(28)
    speed = CBashFLOAT32(29)
    flags = CBashGeneric(30, c_ubyte)
    unused1 = CBashUINT8ARRAY(31, 3)
    value = CBashGeneric(32, c_long)
    clipRounds = CBashGeneric(33, c_ubyte)
    projectilesPerShot = CBashGeneric(34, c_ulong)
    projectile = CBashFORMID(35)
    weight = CBashFLOAT32(36)
    consumedAmmo = CBashFORMID(37)
    consumedPercentage = CBashFLOAT32(38)
    shortName = CBashSTRING(39)
    abbreviation = CBashSTRING(40)
    effects = CBashFORMIDARRAY(41)

    IsNotNormalWeapon = CBashBasicFlag('flags', 0x01)
    IsNormalWeapon = CBashInvertedFlag('IsNotNormalWeapon')
    IsNonPlayable = CBashBasicFlag('flags', 0x02)
    IsPlayable = CBashInvertedFlag('IsNonPlayable')

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath', 'script',
                                           'destructable_list', 'pickupSound',
                                           'dropSound', 'speed', 'flags',
                                           'value', 'clipRounds',
                                           'projectilesPerShot', 'projectile',
                                           'weight', 'consumedAmmo',
                                           'consumedPercentage', 'shortName',
                                           'abbreviation', 'effects']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvNPC_Record(FnvBaseRecord):
    __slots__ = []
    _Type = 'NPC_'
    def mergeFilter(self, target):
        """Filter out items that don't come from specified modSet.
        Filters items."""
        self.items = [x for x in self.items if x.item.ValidateFormID(target)]

    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    flags = CBashGeneric(19, c_ulong)
    fatigue = CBashGeneric(20, c_ushort)
    barterGold = CBashGeneric(21, c_ushort)
    level = CBashGeneric(22, c_short)
    calcMin = CBashGeneric(23, c_ushort)
    calcMax = CBashGeneric(24, c_ushort)
    speedMult = CBashGeneric(25, c_ushort)
    karma = CBashFLOAT32(26)
    dispBase = CBashGeneric(27, c_short)
    templateFlags = CBashGeneric(28, c_ushort)

    def create_faction(self):
        length = _CGetFieldAttribute(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 29, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Faction(self._RecordID, 29, length)
    factions = CBashLIST(29, Faction)
    factions_list = CBashLIST(29, Faction, True)

    deathItem = CBashFORMID(30)
    voice = CBashFORMID(31)
    template = CBashFORMID(32)
    race = CBashFORMID(33)
    actorEffects = CBashFORMIDARRAY(34)
    unarmedEffect = CBashFORMID(35)
    unarmedAnim = CBashGeneric(36, c_ushort)
    destructable = CBashGrouped(37, FNVDestructable)
    destructable_list = CBashGrouped(37, FNVDestructable, True)

    script = CBashFORMID(42)

    def create_item(self):
        length = _CGetFieldAttribute(self._RecordID, 43, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 43, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVItem(self._RecordID, 43, length)
    items = CBashLIST(43, FNVItem)
    items_list = CBashLIST(43, FNVItem, True)

    aggression = CBashGeneric(44, c_ubyte)
    confidence = CBashGeneric(45, c_ubyte)
    energyLevel = CBashGeneric(46, c_ubyte)
    responsibility = CBashGeneric(47, c_ubyte)
    mood = CBashGeneric(48, c_ubyte)
    unused1 = CBashUINT8ARRAY(49, 3)
    services = CBashGeneric(50, c_ulong)
    trainSkill = CBashGeneric(51, c_byte)
    trainLevel = CBashGeneric(52, c_ubyte)
    assistance = CBashGeneric(53, c_ubyte)
    aggroFlags = CBashGeneric(54, c_ubyte)
    aggroRadius = CBashGeneric(55, c_long)
    aiPackages = CBashFORMIDARRAY(56)
    iclass = CBashFORMID(57)
    baseHealth = CBashGeneric(58, c_long)
    strength = CBashGeneric(59, c_ubyte)
    perception = CBashGeneric(60, c_ubyte)
    endurance = CBashGeneric(61, c_ubyte)
    charisma = CBashGeneric(62, c_ubyte)
    intelligence = CBashGeneric(63, c_ubyte)
    agility = CBashGeneric(64, c_ubyte)
    luck = CBashGeneric(65, c_ubyte)
    barter = CBashGeneric(66, c_ubyte)
    bigGuns = CBashGeneric(67, c_ubyte)
    energy = CBashGeneric(68, c_ubyte)
    explosives = CBashGeneric(69, c_ubyte)
    lockpick = CBashGeneric(70, c_ubyte)
    medicine = CBashGeneric(71, c_ubyte)
    melee = CBashGeneric(72, c_ubyte)
    repair = CBashGeneric(73, c_ubyte)
    science = CBashGeneric(74, c_ubyte)
    guns = CBashGeneric(75, c_ubyte)
    sneak = CBashGeneric(76, c_ubyte)
    speech = CBashGeneric(77, c_ubyte)
    survival = CBashGeneric(78, c_ubyte)
    unarmed = CBashGeneric(79, c_ubyte)
    barterBoost = CBashGeneric(80, c_ubyte)
    bigGunsBoost = CBashGeneric(81, c_ubyte)
    energyBoost = CBashGeneric(82, c_ubyte)
    explosivesBoost = CBashGeneric(83, c_ubyte)
    lockpickBoost = CBashGeneric(84, c_ubyte)
    medicineBoost = CBashGeneric(85, c_ubyte)
    meleeBoost = CBashGeneric(86, c_ubyte)
    repairBoost = CBashGeneric(87, c_ubyte)
    scienceBoost = CBashGeneric(88, c_ubyte)
    gunsBoost = CBashGeneric(89, c_ubyte)
    sneakBoost = CBashGeneric(90, c_ubyte)
    speechBoost = CBashGeneric(91, c_ubyte)
    survivalBoost = CBashGeneric(92, c_ubyte)
    unarmedBoost = CBashGeneric(93, c_ubyte)
    headParts = CBashFORMIDARRAY(94)
    hair = CBashFORMID(95)
    hairLength = CBashFLOAT32(96)
    eyes = CBashFORMID(97)
    hairRed = CBashGeneric(98, c_ubyte)
    hairGreen = CBashGeneric(99, c_ubyte)
    hairBlue = CBashGeneric(100, c_ubyte)
    unused2 = CBashUINT8ARRAY(101, 1)
    combatStyle = CBashFORMID(102)
    impactType = CBashGeneric(103, c_ulong)
    fggs_p = CBashUINT8ARRAY(104, 200)
    fgga_p = CBashUINT8ARRAY(105, 120)
    fgts_p = CBashUINT8ARRAY(106, 200)
    unknown = CBashGeneric(107, c_ushort)
    height = CBashFLOAT32(108)
    weight = CBashFLOAT32(109)

    IsFemale = CBashBasicFlag('flags', 0x00000001)
    IsEssential = CBashBasicFlag('flags', 0x00000002)
    IsCharGenFacePreset = CBashBasicFlag('flags', 0x00000004)
    IsRespawn = CBashBasicFlag('flags', 0x00000008)
    IsAutoCalcStats = CBashBasicFlag('flags', 0x00000010)
    IsPCLevelOffset = CBashBasicFlag('flags', 0x00000080)
    IsUseTemplate = CBashBasicFlag('flags', 0x00000100)
    IsNoLowLevel = CBashBasicFlag('flags', 0x00000200)
    IsNoBloodSpray = CBashBasicFlag('flags', 0x00000800)
    IsNoBloodDecal = CBashBasicFlag('flags', 0x00001000)
    IsNoVATSMelee = CBashBasicFlag('flags', 0x00100000)
    IsCanBeAllRaces = CBashBasicFlag('flags', 0x00400000)
    IsAutoCalcService = CBashBasicFlag('flags', 0x00800000)
    IsNoKnockdowns = CBashBasicFlag('flags', 0x03000000)
    IsNotPushable = CBashBasicFlag('flags', 0x08000000)
    IsNoHeadTracking = CBashBasicFlag('flags', 0x40000000)

    IsUseTraits = CBashBasicFlag('templateFlags', 0x00000001)
    IsUseStats = CBashBasicFlag('templateFlags', 0x00000002)
    IsUseFactions = CBashBasicFlag('templateFlags', 0x00000004)
    IsUseAEList = CBashBasicFlag('templateFlags', 0x00000008)
    IsUseAIData = CBashBasicFlag('templateFlags', 0x00000010)
    IsUseAIPackages = CBashBasicFlag('templateFlags', 0x00000020)
    IsUseModelAnim = CBashBasicFlag('templateFlags', 0x00000040)
    IsUseBaseData = CBashBasicFlag('templateFlags', 0x00000080)
    IsUseInventory = CBashBasicFlag('templateFlags', 0x00000100)
    IsUseScript = CBashBasicFlag('templateFlags', 0x00000200)

    IsAggroRadiusBehavior = CBashBasicFlag('aggroFlags', 0x01)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsUnaggressive = CBashBasicType('aggression', 0, 'IsAggressive')
    IsAggressive = CBashBasicType('aggression', 1, 'IsUnaggressive')
    IsVeryAggressive = CBashBasicType('aggression', 2, 'IsUnaggressive')
    IsFrenzied = CBashBasicType('aggression', 3, 'IsUnaggressive')

    IsCowardly = CBashBasicType('confidence', 0, 'IsCautious')
    IsCautious = CBashBasicType('confidence', 1, 'IsCowardly')
    IsAverage = CBashBasicType('confidence', 2, 'IsCowardly')
    IsBrave = CBashBasicType('confidence', 3, 'IsCowardly')
    IsFoolhardy = CBashBasicType('confidence', 4, 'IsCowardly')

    IsNeutral = CBashBasicType('mood', 0, 'IsAfraid')
    IsAfraid = CBashBasicType('mood', 1, 'IsNeutral')
    IsAnnoyed = CBashBasicType('mood', 2, 'IsNeutral')
    IsCocky = CBashBasicType('mood', 3, 'IsNeutral')
    IsDrugged = CBashBasicType('mood', 4, 'IsNeutral')
    IsPleasant = CBashBasicType('mood', 5, 'IsNeutral')
    IsAngry = CBashBasicType('mood', 6, 'IsNeutral')
    IsSad = CBashBasicType('mood', 7, 'IsNeutral')

    IsHelpsNobody = CBashBasicType('assistance', 0, 'IsHelpsAllies')
    IsHelpsAllies = CBashBasicType('assistance', 1, 'IsHelpsNobody')
    IsHelpsFriendsAndAllies = CBashBasicType('assistance', 2, 'IsHelpsNobody')

    IsStone = CBashBasicType('impactType', 0, 'IsDirt')
    IsDirt = CBashBasicType('impactType', 1, 'IsStone')
    IsGrass = CBashBasicType('impactType', 2, 'IsStone')
    IsGlass = CBashBasicType('impactType', 3, 'IsStone')
    IsMetal = CBashBasicType('impactType', 4, 'IsStone')
    IsWood = CBashBasicType('impactType', 5, 'IsStone')
    IsOrganic = CBashBasicType('impactType', 6, 'IsStone')
    IsCloth = CBashBasicType('impactType', 7, 'IsStone')
    IsWater = CBashBasicType('impactType', 8, 'IsStone')
    IsHollowMetal = CBashBasicType('impactType', 9, 'IsStone')
    IsOrganicBug = CBashBasicType('impactType', 10, 'IsStone')
    IsOrganicGlow = CBashBasicType('impactType', 11, 'IsStone')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'flags', 'fatigue', 'barterGold',
                                           'level', 'calcMin', 'calcMax',
                                           'speedMult', 'karma', 'dispBase',
                                           'templateFlags', 'factions_list',
                                           'deathItem', 'voice', 'template',
                                           'race', 'actorEffects', 'unarmedEffect',
                                           'unarmedAnim', 'destructable_list',
                                           'script', 'items_list', 'aggression',
                                           'confidence', 'energyLevel',
                                           'responsibility', 'mood',
                                           'services', 'trainSkill', 'trainLevel',
                                           'assistance', 'aggroFlags',
                                           'aggroRadius', 'aiPackages', 'iclass',
                                           'baseHealth', 'strength', 'perception',
                                           'endurance', 'charisma', 'intelligence',
                                           'agility', 'luck', 'barter', 'bigGuns',
                                           'energy', 'explosives', 'lockpick',
                                           'medicine', 'melee', 'repair',
                                           'science', 'guns', 'sneak', 'speech',
                                           'survival', 'unarmed', 'barterBoost',
                                           'bigGunsBoost', 'energyBoost',
                                           'explosivesBoost', 'lockpickBoost',
                                           'medicineBoost', 'meleeBoost',
                                           'repairBoost', 'scienceBoost',
                                           'gunsBoost', 'sneakBoost', 'speechBoost',
                                           'survivalBoost', 'unarmedBoost',
                                           'headParts', 'hair', 'hairLength', 'eyes',
                                           'hairRed', 'hairGreen', 'hairBlue',
                                           'combatStyle', 'impactType', 'fggs_p',
                                           'fgga_p', 'fgts_p', 'unknown',
                                           'height', 'weight']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')
    exportattrs.remove('fggs_p')
    exportattrs.remove('fgga_p')
    exportattrs.remove('fgts_p')
    exportattrs.remove('unknown')

class FnvCREARecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CREA'
    def mergeFilter(self, target):
        """Filter out items that don't come from specified modSet.
        Filters items."""
        self.items = [x for x in self.items if x.item.ValidateFormID(target)]

    class SoundType(ListComponent):
        __slots__ = []
        class Sound(ListX2Component):
            __slots__ = []
            sound = CBashFORMID_LISTX2(1)
            chance = CBashGeneric_LISTX2(2, c_ubyte)
            exportattrs = copyattrs = ['sound', 'chance']

        soundType = CBashGeneric_LIST(1, c_ulong)
        def create_sound(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Sound(self._RecordID, self._FieldID, self._ListIndex, 2, length)
        sounds = CBashLIST_LIST(2, Sound)
        sounds_list = CBashLIST_LIST(2, Sound, True)

        IsLeftFoot = CBashBasicType('soundType', 0, 'IsRightFoot')
        IsRightFoot = CBashBasicType('soundType', 1, 'IsLeftFoot')
        IsLeftBackFoot = CBashBasicType('soundType', 2, 'IsLeftFoot')
        IsRightBackFoot = CBashBasicType('soundType', 3, 'IsLeftFoot')
        IsIdle = CBashBasicType('soundType', 4, 'IsLeftFoot')
        IsAware = CBashBasicType('soundType', 5, 'IsLeftFoot')
        IsAttack = CBashBasicType('soundType', 6, 'IsLeftFoot')
        IsHit = CBashBasicType('soundType', 7, 'IsLeftFoot')
        IsDeath = CBashBasicType('soundType', 8, 'IsLeftFoot')
        IsWeapon = CBashBasicType('soundType', 9, 'IsLeftFoot')
        IsMovementLoop = CBashBasicType('soundType', 10, 'IsLeftFoot')
        IsConsciousLoop = CBashBasicType('soundType', 11, 'IsLeftFoot')
        IsAuxiliary1 = CBashBasicType('soundType', 12, 'IsLeftFoot')
        IsAuxiliary2 = CBashBasicType('soundType', 13, 'IsLeftFoot')
        IsAuxiliary3 = CBashBasicType('soundType', 14, 'IsLeftFoot')
        IsAuxiliary4 = CBashBasicType('soundType', 15, 'IsLeftFoot')
        IsAuxiliary5 = CBashBasicType('soundType', 16, 'IsLeftFoot')
        IsAuxiliary6 = CBashBasicType('soundType', 17, 'IsLeftFoot')
        IsAuxiliary7 = CBashBasicType('soundType', 18, 'IsLeftFoot')
        IsAuxiliary8 = CBashBasicType('soundType', 19, 'IsLeftFoot')
        IsJump = CBashBasicType('soundType', 20, 'IsLeftFoot')
        IsPlayRandomLoop = CBashBasicType('soundType', 21, 'IsLeftFoot')
        exportattrs = copyattrs = ['soundType', 'sounds_list']

    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    actorEffects = CBashFORMIDARRAY(19)
    unarmedEffect = CBashFORMID(20)
    unarmedAnim = CBashGeneric(21, c_ushort)
    bodyParts = CBashISTRINGARRAY(22)
    nift_p = CBashUINT8ARRAY(23)
    flags = CBashGeneric(24, c_ulong)
    fatigue = CBashGeneric(25, c_ushort)
    barterGold = CBashGeneric(26, c_ushort)
    level = CBashGeneric(27, c_short)
    calcMin = CBashGeneric(28, c_ushort)
    calcMax = CBashGeneric(29, c_ushort)
    speedMult = CBashGeneric(30, c_ushort)
    karma = CBashFLOAT32(31)
    dispBase = CBashGeneric(32, c_short)
    templateFlags = CBashGeneric(33, c_ushort)
    def create_faction(self):
        length = _CGetFieldAttribute(self._RecordID, 34, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 34, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return Faction(self._RecordID, 34, length)
    factions = CBashLIST(34, Faction)
    factions_list = CBashLIST(34, Faction, True)

    deathItem = CBashFORMID(35)
    voice = CBashFORMID(36)
    template = CBashFORMID(37)
    destructable = CBashGrouped(38, FNVDestructable)
    destructable_list = CBashGrouped(38, FNVDestructable, True)

    script = CBashFORMID(43)

    def create_item(self):
        length = _CGetFieldAttribute(self._RecordID, 44, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 44, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVItem(self._RecordID, 44, length)
    items = CBashLIST(44, FNVItem)
    items_list = CBashLIST(44, FNVItem, True)

    aggression = CBashGeneric(45, c_ubyte)
    confidence = CBashGeneric(46, c_ubyte)
    energyLevel = CBashGeneric(47, c_ubyte)
    responsibility = CBashGeneric(48, c_ubyte)
    mood = CBashGeneric(49, c_ubyte)
    unused1 = CBashUINT8ARRAY(50, 3)
    services = CBashGeneric(51, c_ulong)
    trainSkill = CBashGeneric(52, c_byte)
    trainLevel = CBashGeneric(53, c_ubyte)
    assistance = CBashGeneric(54, c_ubyte)
    aggroFlags = CBashGeneric(55, c_ubyte)
    aggroRadius = CBashGeneric(56, c_long)
    aiPackages = CBashFORMIDARRAY(57)
    animations = CBashISTRINGARRAY(58)
    creatureType = CBashGeneric(59, c_ubyte)
    combat = CBashGeneric(60, c_ubyte)
    magic = CBashGeneric(61, c_ubyte)
    stealth = CBashGeneric(62, c_ubyte)
    health = CBashGeneric(63, c_ushort)
    unused2 = CBashUINT8ARRAY(64, 2)
    attackDamage = CBashGeneric(65, c_short)
    strength = CBashGeneric(66, c_ubyte)
    perception = CBashGeneric(67, c_ubyte)
    endurance = CBashGeneric(68, c_ubyte)
    charisma = CBashGeneric(69, c_ubyte)
    intelligence = CBashGeneric(70, c_ubyte)
    agility = CBashGeneric(71, c_ubyte)
    luck = CBashGeneric(72, c_ubyte)
    attackReach = CBashGeneric(73, c_ubyte)
    combatStyle = CBashFORMID(74)
    partData = CBashFORMID(75)
    turningSpeed = CBashFLOAT32(76)
    baseScale = CBashFLOAT32(77)
    footWeight = CBashFLOAT32(78)
    impactType = CBashGeneric(79, c_ulong)
    soundLevel = CBashGeneric(80, c_ulong)
    inheritsSoundsFrom = CBashFORMID(81)

    def create_soundTyp(self):
        length = _CGetFieldAttribute(self._RecordID, 82, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 82, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.SoundType(self._RecordID, 82, length)
    soundTypes = CBashLIST(82, SoundType)
    soundTypes_list = CBashLIST(82, SoundType, True)

    impactData = CBashFORMID(83)
    meleeList = CBashFORMID(84)

    IsBiped = CBashBasicFlag('flags', 0x00000001)
    IsEssential = CBashBasicFlag('flags', 0x00000002)
    IsWeaponAndShield = CBashBasicFlag('flags', 0x00000004)
    IsRespawn = CBashBasicFlag('flags', 0x00000008)
    IsSwims = CBashBasicFlag('flags', 0x00000010)
    IsFlies = CBashBasicFlag('flags', 0x00000020)
    IsWalks = CBashBasicFlag('flags', 0x00000040)
    IsPCLevelOffset = CBashBasicFlag('flags', 0x00000080)
    IsUnknown1 = CBashBasicFlag('flags', 0x00000100)
    IsNoLowLevel = CBashBasicFlag('flags', 0x00000200)
    IsLowLevel = CBashInvertedFlag('IsNoLowLevel')
    IsNoBloodSpray = CBashBasicFlag('flags', 0x00000800)
    IsBloodSpray = CBashInvertedFlag('IsNoBloodSpray')
    IsNoBloodDecal = CBashBasicFlag('flags', 0x00001000)
    IsBloodDecal = CBashInvertedFlag('IsNoBloodDecal')
    IsNoHead = CBashBasicFlag('flags', 0x00008000)
    IsHead = CBashInvertedFlag('IsNoHead')
    IsNoRightArm = CBashBasicFlag('flags', 0x00010000)
    IsRightArm = CBashInvertedFlag('IsNoRightArm')
    IsNoLeftArm = CBashBasicFlag('flags', 0x00020000)
    IsLeftArm = CBashInvertedFlag('IsNoLeftArm')
    IsNoCombatInWater = CBashBasicFlag('flags', 0x00040000)
    IsCombatInWater = CBashInvertedFlag('IsNoCombatInWater')
    IsNoShadow = CBashBasicFlag('flags', 0x00080000)
    IsShadow = CBashInvertedFlag('IsNoShadow')
    IsNoVATSMelee = CBashBasicFlag('flags', 0x00100000)
    IsVATSMelee = CBashInvertedFlag('IsNoVATSMelee')
    IsAllowPCDialogue = CBashBasicFlag('flags', 0x00200000)
    IsCantOpenDoors = CBashBasicFlag('flags', 0x00400000)
    IsCanOpenDoors = CBashInvertedFlag('IsCantOpenDoors')
    IsImmobile = CBashBasicFlag('flags', 0x00800000)
    IsTiltFrontBack = CBashBasicFlag('flags', 0x01000000)
    IsTiltLeftRight = CBashBasicFlag('flags', 0x02000000)
    IsNoKnockdowns = CBashBasicFlag('flags', 0x03000000)
    IsKnockdowns = CBashInvertedFlag('IsNoKnockdowns')
    IsNotPushable = CBashBasicFlag('flags', 0x08000000)
    IsPushable = CBashInvertedFlag('IsNotPushable')
    IsAllowPickpocket = CBashBasicFlag('flags', 0x10000000)
    IsGhost = CBashBasicFlag('flags', 0x20000000)
    IsNoHeadTracking = CBashBasicFlag('flags', 0x40000000)
    IsHeadTracking = CBashInvertedFlag('IsNoHeadTracking')
    IsInvulnerable = CBashBasicFlag('flags', 0x80000000)

    IsUseTraits = CBashBasicFlag('templateFlags', 0x00000001)
    IsUseStats = CBashBasicFlag('templateFlags', 0x00000002)
    IsUseFactions = CBashBasicFlag('templateFlags', 0x00000004)
    IsUseAEList = CBashBasicFlag('templateFlags', 0x00000008)
    IsUseAIData = CBashBasicFlag('templateFlags', 0x00000010)
    IsUseAIPackages = CBashBasicFlag('templateFlags', 0x00000020)
    IsUseModelAnim = CBashBasicFlag('templateFlags', 0x00000040)
    IsUseBaseData = CBashBasicFlag('templateFlags', 0x00000080)
    IsUseInventory = CBashBasicFlag('templateFlags', 0x00000100)
    IsUseScript = CBashBasicFlag('templateFlags', 0x00000200)

    IsAggroRadiusBehavior = CBashBasicFlag('aggroFlags', 0x01)

    IsServicesWeapons = CBashBasicFlag('services', 0x00000001)
    IsServicesArmor = CBashBasicFlag('services', 0x00000002)
    IsServicesClothing = CBashBasicFlag('services', 0x00000004)
    IsServicesBooks = CBashBasicFlag('services', 0x00000008)
    IsServicesIngredients = CBashBasicFlag('services', 0x00000010)
    IsServicesLights = CBashBasicFlag('services', 0x00000080)
    IsServicesApparatus = CBashBasicFlag('services', 0x00000100)
    IsServicesMiscItems = CBashBasicFlag('services', 0x00000400)
    IsServicesSpells = CBashBasicFlag('services', 0x00000800)
    IsServicesMagicItems = CBashBasicFlag('services', 0x00001000)
    IsServicesPotions = CBashBasicFlag('services', 0x00002000)
    IsServicesTraining = CBashBasicFlag('services', 0x00004000)
    IsServicesRecharge = CBashBasicFlag('services', 0x00010000)
    IsServicesRepair = CBashBasicFlag('services', 0x00020000)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsAnimal = CBashBasicType('creatureType', 0, 'IsMutatedAnimal')
    IsMutatedAnimal = CBashBasicType('creatureType', 1, 'IsAnimal')
    IsMutatedInsect = CBashBasicType('creatureType', 2, 'IsAnimal')
    IsAbomination = CBashBasicType('creatureType', 3, 'IsAnimal')
    IsSuperMutant = CBashBasicType('creatureType', 4, 'IsAnimal')
    IsFeralGhoul = CBashBasicType('creatureType', 5, 'IsAnimal')
    IsRobot = CBashBasicType('creatureType', 6, 'IsAnimal')
    IsGiant = CBashBasicType('creatureType', 7, 'IsAnimal')

    IsLoud = CBashBasicType('soundLevel', 0, 'IsNormal')
    IsNormal = CBashBasicType('soundLevel', 1, 'IsLoud')
    IsSilent = CBashBasicType('soundLevel', 2, 'IsLoud')

    IsUnaggressive = CBashBasicType('aggression', 0, 'IsAggressive')
    IsAggressive = CBashBasicType('aggression', 1, 'IsUnaggressive')
    IsVeryAggressive = CBashBasicType('aggression', 2, 'IsUnaggressive')
    IsFrenzied = CBashBasicType('aggression', 3, 'IsUnaggressive')

    IsCowardly = CBashBasicType('confidence', 0, 'IsCautious')
    IsCautious = CBashBasicType('confidence', 1, 'IsCowardly')
    IsAverage = CBashBasicType('confidence', 2, 'IsCowardly')
    IsBrave = CBashBasicType('confidence', 3, 'IsCowardly')
    IsFoolhardy = CBashBasicType('confidence', 4, 'IsCowardly')

    IsNeutral = CBashBasicType('mood', 0, 'IsAfraid')
    IsAfraid = CBashBasicType('mood', 1, 'IsNeutral')
    IsAnnoyed = CBashBasicType('mood', 2, 'IsNeutral')
    IsCocky = CBashBasicType('mood', 3, 'IsNeutral')
    IsDrugged = CBashBasicType('mood', 4, 'IsNeutral')
    IsPleasant = CBashBasicType('mood', 5, 'IsNeutral')
    IsAngry = CBashBasicType('mood', 6, 'IsNeutral')
    IsSad = CBashBasicType('mood', 7, 'IsNeutral')

    IsHelpsNobody = CBashBasicType('assistance', 0, 'IsHelpsAllies')
    IsHelpsAllies = CBashBasicType('assistance', 1, 'IsHelpsNobody')
    IsHelpsFriendsAndAllies = CBashBasicType('assistance', 2, 'IsHelpsNobody')

    IsStone = CBashBasicType('impactType', 0, 'IsDirt')
    IsDirt = CBashBasicType('impactType', 1, 'IsStone')
    IsGrass = CBashBasicType('impactType', 2, 'IsStone')
    IsGlass = CBashBasicType('impactType', 3, 'IsStone')
    IsMetal = CBashBasicType('impactType', 4, 'IsStone')
    IsWood = CBashBasicType('impactType', 5, 'IsStone')
    IsOrganic = CBashBasicType('impactType', 6, 'IsStone')
    IsCloth = CBashBasicType('impactType', 7, 'IsStone')
    IsWater = CBashBasicType('impactType', 8, 'IsStone')
    IsHollowMetal = CBashBasicType('impactType', 9, 'IsStone')
    IsOrganicBug = CBashBasicType('impactType', 10, 'IsStone')
    IsOrganicGlow = CBashBasicType('impactType', 11, 'IsStone')

    IsAttackLeft = CBashBasicType('unarmedAnim', 26, 'IsAttackLeftUp')
    IsAttackLeftUp = CBashBasicType('unarmedAnim', 27, 'IsAttackLeft')
    IsAttackLeftDown = CBashBasicType('unarmedAnim', 28, 'IsAttackLeft')
    IsAttackLeftIS = CBashBasicType('unarmedAnim', 29, 'IsAttackLeft')
    IsAttackLeftISUp = CBashBasicType('unarmedAnim', 30, 'IsAttackLeft')
    IsAttackLeftISDown = CBashBasicType('unarmedAnim', 31, 'IsAttackLeft')
    IsAttackRight = CBashBasicType('unarmedAnim', 32, 'IsAttackLeft')
    IsAttackRightUp = CBashBasicType('unarmedAnim', 33, 'IsAttackLeft')
    IsAttackRightDown = CBashBasicType('unarmedAnim', 34, 'IsAttackLeft')
    IsAttackRightIS = CBashBasicType('unarmedAnim', 35, 'IsAttackLeft')
    IsAttackRightISUp = CBashBasicType('unarmedAnim', 36, 'IsAttackLeft')
    IsAttackRightISDown = CBashBasicType('unarmedAnim', 37, 'IsAttackLeft')
    IsAttack3 = CBashBasicType('unarmedAnim', 38, 'IsAttackLeft')
    IsAttack3Up = CBashBasicType('unarmedAnim', 39, 'IsAttackLeft')
    IsAttack3Down = CBashBasicType('unarmedAnim', 40, 'IsAttackLeft')
    IsAttack3IS = CBashBasicType('unarmedAnim', 41, 'IsAttackLeft')
    IsAttack3ISUp = CBashBasicType('unarmedAnim', 42, 'IsAttackLeft')
    IsAttack3ISDown = CBashBasicType('unarmedAnim', 43, 'IsAttackLeft')
    IsAttack4 = CBashBasicType('unarmedAnim', 44, 'IsAttackLeft')
    IsAttack4Up = CBashBasicType('unarmedAnim', 45, 'IsAttackLeft')
    IsAttack4Down = CBashBasicType('unarmedAnim', 46, 'IsAttackLeft')
    IsAttack4IS = CBashBasicType('unarmedAnim', 47, 'IsAttackLeft')
    IsAttack4ISUp = CBashBasicType('unarmedAnim', 48, 'IsAttackLeft')
    IsAttack4ISDown = CBashBasicType('unarmedAnim', 49, 'IsAttackLeft')
    IsAttack5 = CBashBasicType('unarmedAnim', 50, 'IsAttackLeft')
    IsAttack5Up = CBashBasicType('unarmedAnim', 51, 'IsAttackLeft')
    IsAttack5Down = CBashBasicType('unarmedAnim', 52, 'IsAttackLeft')
    IsAttack5IS = CBashBasicType('unarmedAnim', 53, 'IsAttackLeft')
    IsAttack5ISUp = CBashBasicType('unarmedAnim', 54, 'IsAttackLeft')
    IsAttack5ISDown = CBashBasicType('unarmedAnim', 55, 'IsAttackLeft')
    IsAttack6 = CBashBasicType('unarmedAnim', 56, 'IsAttackLeft')
    IsAttack6Up = CBashBasicType('unarmedAnim', 57, 'IsAttackLeft')
    IsAttack6Down = CBashBasicType('unarmedAnim', 58, 'IsAttackLeft')
    IsAttack6IS = CBashBasicType('unarmedAnim', 59, 'IsAttackLeft')
    IsAttack6ISUp = CBashBasicType('unarmedAnim', 60, 'IsAttackLeft')
    IsAttack6ISDown = CBashBasicType('unarmedAnim', 61, 'IsAttackLeft')
    IsAttack7 = CBashBasicType('unarmedAnim', 62, 'IsAttackLeft')
    IsAttack7Up = CBashBasicType('unarmedAnim', 63, 'IsAttackLeft')
    IsAttack7Down = CBashBasicType('unarmedAnim', 64, 'IsAttackLeft')
    IsAttack7IS = CBashBasicType('unarmedAnim', 65, 'IsAttackLeft')
    IsAttack7ISUp = CBashBasicType('unarmedAnim', 66, 'IsAttackLeft')
    IsAttack7ISDown = CBashBasicType('unarmedAnim', 67, 'IsAttackLeft')
    IsAttack8 = CBashBasicType('unarmedAnim', 68, 'IsAttackLeft')
    IsAttack8Up = CBashBasicType('unarmedAnim', 69, 'IsAttackLeft')
    IsAttack8Down = CBashBasicType('unarmedAnim', 70, 'IsAttackLeft')
    IsAttack8IS = CBashBasicType('unarmedAnim', 71, 'IsAttackLeft')
    IsAttack8ISUp = CBashBasicType('unarmedAnim', 72, 'IsAttackLeft')
    IsAttack8ISDown = CBashBasicType('unarmedAnim', 73, 'IsAttackLeft')
    IsAttackLoop = CBashBasicType('unarmedAnim', 74, 'IsAttackLeft')
    IsAttackLoopUp = CBashBasicType('unarmedAnim', 75, 'IsAttackLeft')
    IsAttackLoopDown = CBashBasicType('unarmedAnim', 76, 'IsAttackLeft')
    IsAttackLoopIS = CBashBasicType('unarmedAnim', 77, 'IsAttackLeft')
    IsAttackLoopISUp = CBashBasicType('unarmedAnim', 78, 'IsAttackLeft')
    IsAttackLoopISDown = CBashBasicType('unarmedAnim', 79, 'IsAttackLeft')
    IsAttackSpin = CBashBasicType('unarmedAnim', 80, 'IsAttackLeft')
    IsAttackSpinUp = CBashBasicType('unarmedAnim', 81, 'IsAttackLeft')
    IsAttackSpinDown = CBashBasicType('unarmedAnim', 82, 'IsAttackLeft')
    IsAttackSpinIS = CBashBasicType('unarmedAnim', 83, 'IsAttackLeft')
    IsAttackSpinISUp = CBashBasicType('unarmedAnim', 84, 'IsAttackLeft')
    IsAttackSpinISDown = CBashBasicType('unarmedAnim', 85, 'IsAttackLeft')
    IsAttackSpin2 = CBashBasicType('unarmedAnim', 86, 'IsAttackLeft')
    IsAttackSpin2Up = CBashBasicType('unarmedAnim', 87, 'IsAttackLeft')
    IsAttackSpin2Down = CBashBasicType('unarmedAnim', 88, 'IsAttackLeft')
    IsAttackSpin2IS = CBashBasicType('unarmedAnim', 89, 'IsAttackLeft')
    IsAttackSpin2ISUp = CBashBasicType('unarmedAnim', 90, 'IsAttackLeft')
    IsAttackSpin2ISDown = CBashBasicType('unarmedAnim', 91, 'IsAttackLeft')
    IsAttackPower = CBashBasicType('unarmedAnim', 92, 'IsAttackLeft')
    IsAttackForwardPower = CBashBasicType('unarmedAnim', 93, 'IsAttackLeft')
    IsAttackBackPower = CBashBasicType('unarmedAnim', 94, 'IsAttackLeft')
    IsAttackLeftPower = CBashBasicType('unarmedAnim', 95, 'IsAttackLeft')
    IsAttackRightPower = CBashBasicType('unarmedAnim', 96, 'IsAttackLeft')
    IsPlaceMine = CBashBasicType('unarmedAnim', 97, 'IsAttackLeft')
    IsPlaceMineUp = CBashBasicType('unarmedAnim', 98, 'IsAttackLeft')
    IsPlaceMineDown = CBashBasicType('unarmedAnim', 99, 'IsAttackLeft')
    IsPlaceMineIS = CBashBasicType('unarmedAnim', 100, 'IsAttackLeft')
    IsPlaceMineISUp = CBashBasicType('unarmedAnim', 101, 'IsAttackLeft')
    IsPlaceMineISDown = CBashBasicType('unarmedAnim', 102, 'IsAttackLeft')
    IsPlaceMine2 = CBashBasicType('unarmedAnim', 103, 'IsAttackLeft')
    IsPlaceMine2Up = CBashBasicType('unarmedAnim', 104, 'IsAttackLeft')
    IsPlaceMine2Down = CBashBasicType('unarmedAnim', 105, 'IsAttackLeft')
    IsPlaceMine2IS = CBashBasicType('unarmedAnim', 106, 'IsAttackLeft')
    IsPlaceMine2ISUp = CBashBasicType('unarmedAnim', 107, 'IsAttackLeft')
    IsPlaceMine2ISDown = CBashBasicType('unarmedAnim', 108, 'IsAttackLeft')
    IsAttackThrow = CBashBasicType('unarmedAnim', 109, 'IsAttackLeft')
    IsAttackThrowUp = CBashBasicType('unarmedAnim', 110, 'IsAttackLeft')
    IsAttackThrowDown = CBashBasicType('unarmedAnim', 111, 'IsAttackLeft')
    IsAttackThrowIS = CBashBasicType('unarmedAnim', 112, 'IsAttackLeft')
    IsAttackThrowISUp = CBashBasicType('unarmedAnim', 113, 'IsAttackLeft')
    IsAttackThrowISDown = CBashBasicType('unarmedAnim', 114, 'IsAttackLeft')
    IsAttackThrow2 = CBashBasicType('unarmedAnim', 115, 'IsAttackLeft')
    IsAttackThrow2Up = CBashBasicType('unarmedAnim', 116, 'IsAttackLeft')
    IsAttackThrow2Down = CBashBasicType('unarmedAnim', 117, 'IsAttackLeft')
    IsAttackThrow2IS = CBashBasicType('unarmedAnim', 118, 'IsAttackLeft')
    IsAttackThrow2ISUp = CBashBasicType('unarmedAnim', 119, 'IsAttackLeft')
    IsAttackThrow2ISDown = CBashBasicType('unarmedAnim', 120, 'IsAttackLeft')
    IsAttackThrow3 = CBashBasicType('unarmedAnim', 121, 'IsAttackLeft')
    IsAttackThrow3Up = CBashBasicType('unarmedAnim', 122, 'IsAttackLeft')
    IsAttackThrow3Down = CBashBasicType('unarmedAnim', 123, 'IsAttackLeft')
    IsAttackThrow3IS = CBashBasicType('unarmedAnim', 124, 'IsAttackLeft')
    IsAttackThrow3ISUp = CBashBasicType('unarmedAnim', 125, 'IsAttackLeft')
    IsAttackThrow3ISDown = CBashBasicType('unarmedAnim', 126, 'IsAttackLeft')
    IsAttackThrow4 = CBashBasicType('unarmedAnim', 127, 'IsAttackLeft')
    IsAttackThrow4Up = CBashBasicType('unarmedAnim', 128, 'IsAttackLeft')
    IsAttackThrow4Down = CBashBasicType('unarmedAnim', 129, 'IsAttackLeft')
    IsAttackThrow4IS = CBashBasicType('unarmedAnim', 130, 'IsAttackLeft')
    IsAttackThrow4ISUp = CBashBasicType('unarmedAnim', 131, 'IsAttackLeft')
    IsAttackThrow4ISDown = CBashBasicType('unarmedAnim', 132, 'IsAttackLeft')
    IsAttackThrow5 = CBashBasicType('unarmedAnim', 133, 'IsAttackLeft')
    IsAttackThrow5Up = CBashBasicType('unarmedAnim', 134, 'IsAttackLeft')
    IsAttackThrow5Down = CBashBasicType('unarmedAnim', 135, 'IsAttackLeft')
    IsAttackThrow5IS = CBashBasicType('unarmedAnim', 136, 'IsAttackLeft')
    IsAttackThrow5ISUp = CBashBasicType('unarmedAnim', 137, 'IsAttackLeft')
    IsAttackThrow5ISDown = CBashBasicType('unarmedAnim', 138, 'IsAttackLeft')
    IsPipBoy = CBashBasicType('unarmedAnim', 167, 'IsAttackLeft')
    IsPipBoyChild = CBashBasicType('unarmedAnim', 178, 'IsAttackLeft')
    IsANY = CBashBasicType('unarmedAnim', 255, 'IsAttackLeft')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'actorEffects', 'unarmedEffect',
                                           'unarmedAnim', 'bodyParts', 'nift_p',
                                           'flags', 'fatigue', 'barterGold',
                                           'level', 'calcMin', 'calcMax',
                                           'speedMult', 'karma', 'dispBase',
                                           'templateFlags', 'factions_list',
                                           'deathItem', 'voice', 'template',
                                           'destructable_list', 'script',
                                           'items_list', 'aggression',
                                           'confidence', 'energyLevel',
                                           'responsibility', 'mood',
                                           'services', 'trainSkill',
                                           'trainLevel', 'assistance',
                                           'aggroFlags', 'aggroRadius',
                                           'aiPackages', 'animations',
                                           'creatureType', 'combat', 'magic',
                                           'stealth', 'health', 'attackDamage',
                                           'strength', 'perception',
                                           'endurance', 'charisma',
                                           'intelligence', 'agility', 'luck',
                                           'attackReach', 'combatStyle',
                                           'partData', 'turningSpeed',
                                           'baseScale', 'footWeight',
                                           'impactType', 'soundLevel',
                                           'inheritsSoundsFrom',
                                           'soundTypes_list', 'impactData',
                                           'meleeList']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')
    exportattrs.remove('nift_p')

class FnvLVLCRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'LVLC'
    def mergeFilter(self, target):
        """Filter out items that don't come from specified modSet."""
        self.entries = [entry for entry in self.entries if entry.listId.ValidateFormID(target)]

    class Entry(ListComponent):
        __slots__ = []
        level = CBashGeneric_LIST(1, c_short)
        unused1 = CBashUINT8ARRAY_LIST(2, 2)
        listId = CBashFORMID_LIST(3)
        count = CBashGeneric_LIST(4, c_short)
        unused2 = CBashUINT8ARRAY_LIST(5, 2)
        owner = CBashFORMID_LIST(6)
        globalOrRank = CBashUNKNOWN_OR_FORMID_OR_UINT32_LIST(7)
        condition = CBashFLOAT32_LIST(8)
        exportattrs = copyattrs = ['level', 'listId', 'count', 'owner', 'globalOrRank', 'condition']

    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    chanceNone = CBashGeneric(13, c_ubyte)
    flags = CBashGeneric(14, c_ubyte)

    def create_entry(self):
        length = _CGetFieldAttribute(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Entry(self._RecordID, 15, length)
    entries = CBashLIST(15, Entry)
    entries_list = CBashLIST(15, Entry, True)

    modPath = CBashISTRING(16)
    modb = CBashFLOAT32(17)
    modt_p = CBashUINT8ARRAY(18)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 19, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 19, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 19, length)
    altTextures = CBashLIST(19, FNVAltTexture)
    altTextures_list = CBashLIST(19, FNVAltTexture, True)

    modelFlags = CBashGeneric(20, c_ubyte)

    IsCalcFromAllLevels = CBashBasicFlag('flags', 0x00000001)
    IsCalcForEachItem = CBashBasicFlag('flags', 0x00000002)
    IsUseAll = CBashBasicFlag('flags', 0x00000004)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'chanceNone', 'flags',
                                           'entries_list', 'modPath',
                                           'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvLVLNRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'LVLN'
    def mergeFilter(self, target):
        """Filter out items that don't come from specified modSet."""
        self.entries = [entry for entry in self.entries if entry.listId.ValidateFormID(target)]

    class Entry(ListComponent):
        __slots__ = []
        level = CBashGeneric_LIST(1, c_short)
        unused1 = CBashUINT8ARRAY_LIST(2, 2)
        listId = CBashFORMID_LIST(3)
        count = CBashGeneric_LIST(4, c_short)
        unused2 = CBashUINT8ARRAY_LIST(5, 2)
        owner = CBashFORMID_LIST(6)
        globalOrRank = CBashUNKNOWN_OR_FORMID_OR_UINT32_LIST(7)
        condition = CBashFLOAT32_LIST(8)
        exportattrs = copyattrs = ['level', 'listId', 'count', 'owner', 'globalOrRank', 'condition']

    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    chanceNone = CBashGeneric(13, c_ubyte)
    flags = CBashGeneric(14, c_ubyte)

    def create_entry(self):
        length = _CGetFieldAttribute(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Entry(self._RecordID, 15, length)
    entries = CBashLIST(15, Entry)
    entries_list = CBashLIST(15, Entry, True)

    modPath = CBashISTRING(16)
    modb = CBashFLOAT32(17)
    modt_p = CBashUINT8ARRAY(18)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 19, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 19, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 19, length)
    altTextures = CBashLIST(19, FNVAltTexture)
    altTextures_list = CBashLIST(19, FNVAltTexture, True)

    modelFlags = CBashGeneric(20, c_ubyte)

    IsCalcFromAllLevels = CBashBasicFlag('flags', 0x00000001)
    IsCalcForEachItem = CBashBasicFlag('flags', 0x00000002)
    IsUseAll = CBashBasicFlag('flags', 0x00000004)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'chanceNone', 'flags',
                                           'entries_list', 'modPath',
                                           'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvKEYMRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'KEYM'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    script = CBashFORMID(21)
    destructable = CBashGrouped(22, FNVDestructable)
    destructable_list = CBashGrouped(22, FNVDestructable, True)

    pickupSound = CBashFORMID(27)
    dropSound = CBashFORMID(28)
    value = CBashGeneric(29, c_long)
    weight = CBashFLOAT32(30)
    loopSound = CBashFORMID(31)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath',
                                           'script', 'destructable_list',
                                           'pickupSound', 'dropSound',
                                           'value', 'weight', 'loopSound']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvALCHRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ALCH'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    script = CBashFORMID(21)
    equipmentType = CBashGeneric(22, c_long)
    weight = CBashFLOAT32(23)
    value = CBashGeneric(24, c_long)
    flags = CBashGeneric(25, c_ubyte)
    unused1 = CBashUINT8ARRAY(26, 3)

    withdrawalEffect = CBashFORMID(27)
    addictionChance = CBashFLOAT32(28)
    consumeSound = CBashFORMID(29)

    def create_effect(self):
        length = _CGetFieldAttribute(self._RecordID, 30, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 30, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVEffect(self._RecordID, 30, length)
    effects = CBashLIST(30, FNVEffect)
    effects_list = CBashLIST(30, FNVEffect, True)

    destructable = CBashGrouped(31, FNVDestructable)
    destructable_list = CBashGrouped(31, FNVDestructable, True)

    pickupSound = CBashFORMID(36)
    dropSound = CBashFORMID(37)

    IsNoAutoCalc = CBashBasicFlag('flags', 0x00000001)
    IsAutoCalc = CBashInvertedFlag('IsNoAutoCalc')
    IsFood = CBashBasicFlag('flags', 0x00000002)
    IsMedicine = CBashBasicFlag('flags', 0x00000004)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsNone = CBashBasicType('equipmentType', -1, 'IsBigGuns')
    IsBigGuns = CBashBasicType('equipmentType', 0, 'IsNone')
    IsEnergyWeapons = CBashBasicType('equipmentType', 1, 'IsNone')
    IsSmallGuns = CBashBasicType('equipmentType', 2, 'IsNone')
    IsMeleeWeapons = CBashBasicType('equipmentType', 3, 'IsNone')
    IsUnarmedWeapon = CBashBasicType('equipmentType', 4, 'IsNone')
    IsThrownWeapons = CBashBasicType('equipmentType', 5, 'IsNone')
    IsMine = CBashBasicType('equipmentType', 6, 'IsNone')
    IsBodyWear = CBashBasicType('equipmentType', 7, 'IsNone')
    IsHeadWear = CBashBasicType('equipmentType', 8, 'IsNone')
    IsHandWear = CBashBasicType('equipmentType', 9, 'IsNone')
    IsChems = CBashBasicType('equipmentType', 10, 'IsNone')
    IsStimpack = CBashBasicType('equipmentType', 11, 'IsNone')
    IsEdible = CBashBasicType('equipmentType', 12, 'IsNone')
    IsAlcohol = CBashBasicType('equipmentType', 13, 'IsNone')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath',
                                           'script', 'equipmentType', 'weight',
                                           'value', 'flags', 'withdrawalEffect',
                                           'addictionChance', 'consumeSound',
                                           'effects_list', 'destructable_list',
                                           'pickupSound', 'dropSound']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvIDLMRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'IDLM'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    flags = CBashGeneric(13, c_ubyte)
    count = CBashGeneric(14, c_ubyte)
    timer = CBashFLOAT32(15)
    animations = CBashFORMIDARRAY(16)

    IsRunInSequence = CBashBasicFlag('flags', 0x00000001)
    IsDoOnce = CBashBasicFlag('flags', 0x00000004)
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                                         'boundX2', 'boundY2', 'boundZ2',
                                                         'flags', 'count', 'timer',
                                                         'animations']

class FnvNOTERecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'NOTE'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    pickupSound = CBashFORMID(21)
    dropSound = CBashFORMID(22)
    noteType = CBashGeneric(23, c_ubyte)
    quests = CBashFORMIDARRAY(24)
    texturePath = CBashISTRING(25)
    textOrTopic = CBashFORMID_OR_STRING(26) #Is a topic formID if IsVoice is true, otherwise text
    sound = CBashFORMID(27)

    IsSound = CBashBasicType('flags', 0, 'IsText')
    IsText = CBashBasicType('flags', 1, 'IsSound')
    IsImage = CBashBasicType('flags', 2, 'IsSound')
    IsVoice = CBashBasicType('flags', 3, 'IsSound')

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath',
                                           'pickupSound', 'dropSound',
                                           'noteType', 'quests', 'texturePath',
                                           'textOrTopic', 'sound']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvCOBJRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'COBJ'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    iconPath = CBashISTRING(19)
    smallIconPath = CBashISTRING(20)
    script = CBashFORMID(21)
    pickupSound = CBashFORMID(22)
    dropSound = CBashFORMID(23)
    value = CBashGeneric(24, c_long)
    weight = CBashFLOAT32(25)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'iconPath', 'smallIconPath',
                                           'script', 'pickupSound',
                                           'dropSound', 'value', 'weight']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvPROJRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'PROJ'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    destructable = CBashGrouped(19, FNVDestructable)
    destructable_list = CBashGrouped(19, FNVDestructable, True)

    flags = CBashGeneric(24, c_ushort)
    projType = CBashGeneric(25, c_ushort)
    gravity = CBashFLOAT32(26)
    speed = CBashFLOAT32(27)
    range = CBashFLOAT32(28)
    light = CBashFORMID(29)
    flash = CBashFORMID(30)
    tracerChance = CBashFLOAT32(31)
    altExplProximityTrigger = CBashFLOAT32(32)
    altExplProximityTimer = CBashFLOAT32(33)
    explosion = CBashFORMID(34)
    sound = CBashFORMID(35)
    flashDuration = CBashFLOAT32(36)
    fadeDuration = CBashFLOAT32(37)
    impactForce = CBashFLOAT32(38)
    soundCountdown = CBashFORMID(39)
    soundDisable = CBashFORMID(40)
    defaultWeaponSource = CBashFORMID(41)
    rotX = CBashFLOAT32(42)
    rotY = CBashFLOAT32(43)
    rotZ = CBashFLOAT32(44)
    bouncyMult = CBashFLOAT32(45)
    modelPath = CBashISTRING(46)
    nam2_p = CBashUINT8ARRAY(47)
    soundLevel = CBashGeneric(48, c_ulong)

    IsHitscan = CBashBasicFlag('flags', 0x0001)
    IsExplosion = CBashBasicFlag('flags', 0x0002)
    IsAltTrigger = CBashBasicFlag('flags', 0x0004)
    IsMuzzleFlash = CBashBasicFlag('flags', 0x0008)
    IsDisableable = CBashBasicFlag('flags', 0x0020)
    IsPickupable = CBashBasicFlag('flags', 0x0040)
    IsSupersonic = CBashBasicFlag('flags', 0x0080)
    IsPinsLimbs = CBashBasicFlag('flags', 0x0100)
    IsPassSmallTransparent = CBashBasicFlag('flags', 0x0200)
    IsDetonates = CBashBasicFlag('flags', 0x0400)
    IsRotation = CBashBasicFlag('flags', 0x0800)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsMissile = CBashBasicType('projType', 1, 'IsLobber')
    IsLobber = CBashBasicType('projType', 2, 'IsMissile')
    IsBeam = CBashBasicType('projType', 4, '')
    IsFlame = CBashBasicType('projType', 8, 'IsMissile')
    IsContinuousBeam = CBashBasicType('projType', 16, 'IsMissile')

    IsLoud = CBashBasicType('soundLevel', 0, 'IsNormal')
    IsNormal = CBashBasicType('soundLevel', 1, 'IsLoud')
    IsSilent = CBashBasicType('soundLevel', 2, 'IsLoud')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'destructable_list', 'flags',
                                           'projType', 'gravity', 'speed',
                                           'range', 'light', 'flash',
                                           'tracerChance',
                                           'altExplProximityTrigger',
                                           'altExplProximityTimer',
                                           'explosion', 'sound',
                                           'flashDuration', 'fadeDuration',
                                           'impactForce', 'soundCountdown',
                                           'soundDisable',
                                           'defaultWeaponSource', 'rotX',
                                           'rotY', 'rotZ', 'bouncyMult',
                                           'modelPath', 'nam2_p',
                                           'soundLevel']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')
    exportattrs.remove('nam2_p')

class FnvLVLIRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'LVLI'
    def mergeFilter(self, target):
        """Filter out items that don't come from specified modSet."""
        self.entries = [entry for entry in self.entries if entry.listId.ValidateFormID(target)]

    class Entry(ListComponent):
        __slots__ = []
        level = CBashGeneric_LIST(1, c_short)
        unused1 = CBashUINT8ARRAY_LIST(2, 2)
        listId = CBashFORMID_LIST(3)
        count = CBashGeneric_LIST(4, c_short)
        unused2 = CBashUINT8ARRAY_LIST(5, 2)
        owner = CBashFORMID_LIST(6)
        globalOrRank = CBashUNKNOWN_OR_FORMID_OR_UINT32_LIST(7)
        condition = CBashFLOAT32_LIST(8)
        exportattrs = copyattrs = ['level', 'listId', 'count', 'owner', 'globalOrRank', 'condition']

    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    chanceNone = CBashGeneric(13, c_ubyte)
    flags = CBashGeneric(14, c_ubyte)
    globalId = CBashFORMID(15)

    def create_entry(self):
        length = _CGetFieldAttribute(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Entry(self._RecordID, 16, length)
    entries = CBashLIST(16, Entry)
    entries_list = CBashLIST(16, Entry, True)

    IsCalcFromAllLevels = CBashBasicFlag('flags', 0x00000001)
    IsCalcForEachItem = CBashBasicFlag('flags', 0x00000002)
    IsUseAll = CBashBasicFlag('flags', 0x00000004)
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                                         'boundX2', 'boundY2', 'boundZ2',
                                                         'chanceNone', 'flags',
                                                         'globalId', 'entries_list']

class FnvWTHRRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'WTHR'
    class WTHRColor(BaseComponent):
        __slots__ = []
        riseRed = CBashGeneric_GROUP(0, c_ubyte)
        riseGreen = CBashGeneric_GROUP(1, c_ubyte)
        riseBlue = CBashGeneric_GROUP(2, c_ubyte)
        unused1 = CBashUINT8ARRAY_GROUP(3, 1)
        dayRed = CBashGeneric_GROUP(4, c_ubyte)
        dayGreen = CBashGeneric_GROUP(5, c_ubyte)
        dayBlue = CBashGeneric_GROUP(6, c_ubyte)
        unused2 = CBashUINT8ARRAY_GROUP(7, 1)
        setRed = CBashGeneric_GROUP(8, c_ubyte)
        setGreen = CBashGeneric_GROUP(9, c_ubyte)
        setBlue = CBashGeneric_GROUP(10, c_ubyte)
        unused3 = CBashUINT8ARRAY_GROUP(11, 1)
        nightRed = CBashGeneric_GROUP(12, c_ubyte)
        nightGreen = CBashGeneric_GROUP(13, c_ubyte)
        nightBlue = CBashGeneric_GROUP(14, c_ubyte)
        unused4 = CBashUINT8ARRAY_GROUP(15, 1)

        noonRed = CBashGeneric_GROUP(16, c_ubyte)
        noonGreen = CBashGeneric_GROUP(17, c_ubyte)
        noonBlue = CBashGeneric_GROUP(18, c_ubyte)
        unused5 = CBashUINT8ARRAY_GROUP(19, 1)

        midnightRed = CBashGeneric_GROUP(20, c_ubyte)
        midnightGreen = CBashGeneric_GROUP(21, c_ubyte)
        midnightBlue = CBashGeneric_GROUP(22, c_ubyte)
        unused6 = CBashUINT8ARRAY_GROUP(23, 1)
        exportattrs = copyattrs = ['riseRed', 'riseGreen', 'riseBlue',
                                   'dayRed', 'dayGreen', 'dayBlue',
                                   'setRed', 'setGreen', 'setBlue',
                                   'nightRed', 'nightGreen', 'nightBlue',
                                   'noonRed', 'noonGreen', 'noonBlue',
                                   'midnightRed', 'midnightGreen', 'midnightBlue']

    class Sound(ListComponent):
        __slots__ = []
        sound = CBashFORMID_LIST(1)
        type = CBashGeneric_LIST(2, c_ulong)
        IsDefault = CBashBasicType('type', 0, 'IsPrecip')
        IsPrecipitation = CBashBasicType('type', 1, 'IsDefault')
        IsPrecip = CBashAlias('IsPrecipitation')
        IsWind = CBashBasicType('type', 2, 'IsDefault')
        IsThunder = CBashBasicType('type', 3, 'IsDefault')
        exportattrs = copyattrs = ['sound', 'type']

    sunriseImageSpace = CBashFORMID(7)
    dayImageSpace = CBashFORMID(8)
    sunsetImageSpace = CBashFORMID(9)
    nightImageSpace = CBashFORMID(10)
    unknown1ImageSpace = CBashFORMID(11)
    unknown2ImageSpace = CBashFORMID(12)
    cloudLayer0Path = CBashISTRING(13)
    cloudLayer1Path = CBashISTRING(14)
    cloudLayer2Path = CBashISTRING(15)
    cloudLayer3Path = CBashISTRING(16)
    modPath = CBashISTRING(17)
    modb = CBashFLOAT32(18)
    modt_p = CBashUINT8ARRAY(19)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 20, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 20, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 20, length)
    altTextures = CBashLIST(20, FNVAltTexture)
    altTextures_list = CBashLIST(20, FNVAltTexture, True)

    modelFlags = CBashGeneric(21, c_ubyte)
    unknown1 = CBashGeneric(22, c_ulong)
    layer0Speed = CBashGeneric(23, c_ubyte)
    layer1Speed = CBashGeneric(24, c_ubyte)
    layer2Speed = CBashGeneric(25, c_ubyte)
    layer3Speed = CBashGeneric(26, c_ubyte)
    pnam_p = CBashUINT8ARRAY(27)
    upperSky = CBashGrouped(28, WTHRColor)
    upperSky_list = CBashGrouped(28, WTHRColor, True)

    fog = CBashGrouped(52, WTHRColor)
    fog_list = CBashGrouped(52, WTHRColor, True)

    lowerClouds = CBashGrouped(76, WTHRColor)
    lowerClouds_list = CBashGrouped(76, WTHRColor, True)

    ambient = CBashGrouped(100, WTHRColor)
    ambient_list = CBashGrouped(100, WTHRColor, True)

    sunlight = CBashGrouped(124, WTHRColor)
    sunlight_list = CBashGrouped(124, WTHRColor, True)

    sun = CBashGrouped(148, WTHRColor)
    sun_list = CBashGrouped(148, WTHRColor, True)

    stars = CBashGrouped(172, WTHRColor)
    stars_list = CBashGrouped(172, WTHRColor, True)

    lowerSky = CBashGrouped(196, WTHRColor)
    lowerSky_list = CBashGrouped(196, WTHRColor, True)

    horizon = CBashGrouped(220, WTHRColor)
    horizon_list = CBashGrouped(220, WTHRColor, True)

    upperClouds = CBashGrouped(244, WTHRColor)
    upperClouds_list = CBashGrouped(244, WTHRColor, True)

    fogDayNear = CBashFLOAT32(268)
    fogDayFar = CBashFLOAT32(269)
    fogNightNear = CBashFLOAT32(270)
    fogNightFar = CBashFLOAT32(271)
    fogDayPower = CBashFLOAT32(272)
    fogNightPower = CBashFLOAT32(273)
    inam_p = CBashUINT8ARRAY(274)
    windSpeed = CBashGeneric(275, c_ubyte)
    lowerCloudSpeed = CBashGeneric(276, c_ubyte)
    upperCloudSpeed = CBashGeneric(277, c_ubyte)
    transDelta = CBashGeneric(278, c_ubyte)
    sunGlare = CBashGeneric(279, c_ubyte)
    sunDamage = CBashGeneric(280, c_ubyte)
    rainFadeIn = CBashGeneric(281, c_ubyte)
    rainFadeOut = CBashGeneric(282, c_ubyte)
    boltFadeIn = CBashGeneric(283, c_ubyte)
    boltFadeOut = CBashGeneric(284, c_ubyte)
    boltFrequency = CBashGeneric(285, c_ubyte)
    weatherType = CBashGeneric(286, c_ubyte)
    boltRed = CBashGeneric(287, c_ubyte)
    boltGreen = CBashGeneric(288, c_ubyte)
    boltBlue = CBashGeneric(289, c_ubyte)

    def create_sound(self):
        length = _CGetFieldAttribute(self._RecordID, 290, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 290, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Sound(self._RecordID, 290, length)
    sounds = CBashLIST(290, Sound)
    sounds_list = CBashLIST(290, Sound, True)

    ##actually flags, but all are exclusive(except unknowns)...so like a Type
    ##Manual hackery will make the CS think it is multiple types. It isn't known how the game would react.
    IsNone = CBashMaskedType('weatherType', 0x0F, 0x00, 'IsPleasant')
    IsPleasant = CBashMaskedType('weatherType', 0x0F, 0x01, 'IsNone')
    IsCloudy = CBashMaskedType('weatherType', 0x0F, 0x02, 'IsNone')
    IsRainy = CBashMaskedType('weatherType', 0x0F, 0x04, 'IsNone')
    IsSnow = CBashMaskedType('weatherType', 0x0F, 0x08, 'IsNone')
    IsUnk1 = CBashBasicFlag('weatherType', 0x40)
    IsUnk2 = CBashBasicFlag('weatherType', 0x80)
    copyattrs = FnvBaseRecord.baseattrs + ['sunriseImageSpace', 'dayImageSpace',
                                           'sunsetImageSpace', 'nightImageSpace',
                                           'unknown1ImageSpace', 'unknown2ImageSpace',
                                           'cloudLayer0Path', 'cloudLayer1Path',
                                           'cloudLayer2Path', 'cloudLayer3Path',
                                           'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'unknown1', 'layer0Speed', 'layer1Speed',
                                           'layer2Speed', 'layer3Speed', 'pnam_p',
                                           'upperSky_list', 'fog_list',
                                           'lowerClouds_list', 'ambient_list',
                                           'sunlight_list', 'sun_list', 'stars_list',
                                           'lowerSky_list', 'horizon_list',
                                           'upperClouds_list', 'fogDayNear',
                                           'fogDayFar', 'fogNightNear',
                                           'fogNightFar', 'fogDayPower',
                                           'fogNightPower', 'inam_p', 'windSpeed',
                                           'lowerCloudSpeed', 'upperCloudSpeed',
                                           'transDelta', 'sunGlare', 'sunDamage',
                                           'rainFadeIn', 'rainFadeOut',
                                           'boltFadeIn', 'boltFadeOut',
                                           'boltFrequency', 'weatherType',
                                           'boltRed', 'boltGreen', 'boltBlue',
                                           'sounds_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')
    exportattrs.remove('pnam_p')
    exportattrs.remove('inam_p')
    exportattrs.remove('unknown1ImageSpace')
    exportattrs.remove('unknown2ImageSpace')

class FnvCLMTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CLMT'
    class Weather(ListComponent):
        __slots__ = []
        weather = CBashFORMID_LIST(1)
        chance = CBashGeneric_LIST(2, c_long)
        globalId = CBashFORMID_LIST(3)
        copyattrs = ['weather', 'chance', 'globalId']

    def create_weather(self):
        length = _CGetFieldAttribute(self._RecordID, 7, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 7, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Weather(self._RecordID, 7, length)
    weathers = CBashLIST(7, Weather)
    weathers_list = CBashLIST(7, Weather, True)

    sunPath = CBashISTRING(8)
    glarePath = CBashISTRING(9)
    modPath = CBashISTRING(10)
    modb = CBashFLOAT32(11)
    modt_p = CBashUINT8ARRAY(12)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 13, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 13, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 13, length)
    altTextures = CBashLIST(13, FNVAltTexture)
    altTextures_list = CBashLIST(13, FNVAltTexture, True)

    modelFlags = CBashGeneric(14, c_ubyte)
    riseBegin = CBashGeneric(15, c_ubyte)
    riseEnd = CBashGeneric(16, c_ubyte)
    setBegin = CBashGeneric(17, c_ubyte)
    setEnd = CBashGeneric(18, c_ubyte)
    volatility = CBashGeneric(19, c_ubyte)
    phaseLength = CBashGeneric(20, c_ubyte)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)
    copyattrs = FnvBaseRecord.baseattrs + ['weathers_list', 'sunPath',
                                           'glarePath', 'modPath',
                                           'modb', 'modt_p',
                                           'altTextures_list',
                                           'modelFlags', 'riseBegin',
                                           'riseEnd', 'setBegin',
                                           'setEnd', 'volatility',
                                           'phaseLength']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvREGNRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'REGN'
    class Area(ListComponent):
        __slots__ = []
        class Point(ListX2Component):
            __slots__ = []
            posX = CBashFLOAT32_LISTX2(1)
            posY = CBashFLOAT32_LISTX2(2)
            exportattrs = copyattrs = ['posX', 'posY']

        edgeFalloff = CBashGeneric_LIST(1, c_ulong)

        def create_point(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Point(self._RecordID, self._FieldID, self._ListIndex, 2, length)
        points = CBashLIST_LIST(2, Point)
        points_list = CBashLIST_LIST(2, Point, True)

        exportattrs = copyattrs = ['edgeFalloff', 'points_list']

    class Entry(ListComponent):
        __slots__ = []
        class Object(ListX2Component):
            __slots__ = []
            objectId = CBashFORMID_LISTX2(1)
            parentIndex = CBashGeneric_LISTX2(2, c_ushort)
            unused1 = CBashUINT8ARRAY_LISTX2(3, 2)
            density = CBashFLOAT32_LISTX2(4)
            clustering = CBashGeneric_LISTX2(5, c_ubyte)
            minSlope = CBashGeneric_LISTX2(6, c_ubyte)
            maxSlope = CBashGeneric_LISTX2(7, c_ubyte)
            flags = CBashGeneric_LISTX2(8, c_ubyte)
            radiusWRTParent = CBashGeneric_LISTX2(9, c_ushort)
            radius = CBashGeneric_LISTX2(10, c_ushort)
            unk1 = CBashUINT8ARRAY_LISTX2(11, 4)
            maxHeight = CBashFLOAT32_LISTX2(12)
            sink = CBashFLOAT32_LISTX2(13)
            sinkVar = CBashFLOAT32_LISTX2(14)
            sizeVar = CBashFLOAT32_LISTX2(15)
            angleVarX = CBashGeneric_LISTX2(16, c_ushort)
            angleVarY = CBashGeneric_LISTX2(17, c_ushort)
            angleVarZ = CBashGeneric_LISTX2(18, c_ushort)
            unused2 = CBashUINT8ARRAY_LISTX2(19, 1)
            unk2 = CBashUINT8ARRAY_LISTX2(20, 4)
            IsConformToSlope = CBashBasicFlag('flags', 0x00000001)
            IsPaintVertices = CBashBasicFlag('flags', 0x00000002)
            IsSizeVariance = CBashBasicFlag('flags', 0x00000004)
            IsXVariance = CBashBasicFlag('flags', 0x00000008)
            IsYVariance = CBashBasicFlag('flags', 0x00000010)
            IsZVariance = CBashBasicFlag('flags', 0x00000020)
            IsTree = CBashBasicFlag('flags', 0x00000040)
            IsHugeRock = CBashBasicFlag('flags', 0x00000080)
            copyattrs = ['objectId', 'parentIndex', 'density', 'clustering',
                         'minSlope', 'maxSlope', 'flags', 'radiusWRTParent',
                         'radius', 'unk1', 'maxHeight', 'sink', 'sinkVar',
                         'sizeVar', 'angleVarX', 'angleVarY', 'angleVarZ',
                         'unk2']
            exportattrs = copyattrs[:]
            exportattrs.remove('unk1')
            exportattrs.remove('unk2')

        class Grass(ListX2Component):
            __slots__ = []
            grass = CBashFORMID_LISTX2(1)
            unk1 = CBashUINT8ARRAY_LISTX2(2, 4)
            copyattrs = ['grass', 'unk1']
            exportattrs = copyattrs[:]
            exportattrs.remove('unk1')

        class Sound(ListX2Component):
            __slots__ = []
            sound = CBashFORMID_LISTX2(1)
            flags = CBashGeneric_LISTX2(2, c_ulong)
            chance = CBashGeneric_LISTX2(3, c_ulong)
            IsPleasant = CBashBasicFlag('flags', 0x00000001)
            IsCloudy = CBashBasicFlag('flags', 0x00000002)
            IsRainy = CBashBasicFlag('flags', 0x00000004)
            IsSnowy = CBashBasicFlag('flags', 0x00000008)
            exportattrs = copyattrs = ['sound', 'flags', 'chance']

        class Weather(ListX2Component):
            __slots__ = []
            weather = CBashFORMID_LISTX2(1)
            chance = CBashGeneric_LISTX2(2, c_ulong)
            globalId = CBashFORMID_LISTX2(1)
            exportattrs = copyattrs = ['weather', 'chance', 'globalId']

        entryType = CBashGeneric_LIST(1, c_ulong)
        flags = CBashGeneric_LIST(2, c_ubyte)
        priority = CBashGeneric_LIST(3, c_ubyte)
        unused1 = CBashUINT8ARRAY_LIST(4, 4)

        def create_object(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 5, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 5, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Object(self._RecordID, self._FieldID, self._ListIndex, 5, length)
        objects = CBashLIST_LIST(5, Object)
        objects_list = CBashLIST_LIST(5, Object, True)

        mapName = CBashSTRING_LIST(6)
        iconPath = CBashSTRING_LIST(7)

        def create_grass(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 8, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 8, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Grass(self._RecordID, self._FieldID, self._ListIndex, 8, length)
        grasses = CBashLIST_LIST(8, Grass)
        grasses_list = CBashLIST_LIST(8, Grass, True)

        musicType = CBashGeneric_LIST(9, c_ulong)
        music = CBashFORMID_LIST(10)
        incidentalMedia = CBashFORMID_LIST(11)
        battleMedias = CBashFORMIDARRAY_LIST(12)

        def create_sound(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 13, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 13, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Sound(self._RecordID, self._FieldID, self._ListIndex, 13, length)
        sounds = CBashLIST_LIST(13, Sound)
        sounds_list = CBashLIST_LIST(13, Sound, True)

        def create_weather(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 14, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 14, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Weather(self._RecordID, self._FieldID, self._ListIndex, 14, length)
        weathers = CBashLIST_LIST(14, Weather)
        weathers_list = CBashLIST_LIST(14, Weather, True)

        imposters = CBashFORMIDARRAY_LIST(15)

        IsOverride = CBashBasicFlag('flags', 0x00000001)

        IsObject = CBashBasicType('entryType', 2, 'IsWeather')
        IsWeather = CBashBasicType('entryType', 3, 'IsObject')
        IsMap = CBashBasicType('entryType', 4, 'IsObject')
        IsLand = CBashBasicType('entryType', 5, 'IsObject')
        IsGrass = CBashBasicType('entryType', 6, 'IsObject')
        IsSound = CBashBasicType('entryType', 7, 'IsObject')
        IsImposter = CBashBasicType('entryType', 8, 'IsObject')
        IsDefault = CBashBasicType('musicType', 0, 'IsPublic')
        IsPublic = CBashBasicType('musicType', 1, 'IsDefault')
        IsDungeon = CBashBasicType('musicType', 2, 'IsDefault')
        exportattrs = copyattrs = ['entryType', 'flags', 'priority', 'objects_list',
                                   'mapName', 'iconPath', 'grasses_list', 'musicType',
                                   'music', 'incidentalMedia', 'battleMedias',
                                   'sounds_list', 'weathers_list', 'imposters']

    iconPath = CBashISTRING(7)
    smallIconPath = CBashISTRING(8)
    mapRed = CBashGeneric(9, c_ubyte)
    mapGreen = CBashGeneric(10, c_ubyte)
    mapBlue = CBashGeneric(11, c_ubyte)
    unused1 = CBashUINT8ARRAY(12, 1)
    worldspace = CBashFORMID(13)

    def create_area(self):
        length = _CGetFieldAttribute(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 14, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Area(self._RecordID, 14, length)
    areas = CBashLIST(14, Area)
    areas_list = CBashLIST(14, Area, True)

    def create_entry(self):
        length = _CGetFieldAttribute(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Entry(self._RecordID, 15, length)
    entries = CBashLIST(15, Entry)
    entries_list = CBashLIST(15, Entry, True)

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['iconPath', 'smallIconPath',
                                                         'mapRed', 'mapGreen', 'mapBlue',
                                                         'worldspace', 'areas_list',
                                                         'entries_list']

class FnvNAVIRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'NAVI'
    class _NVMI(ListComponent):
        __slots__ = []
        unknown1 = CBashUINT8ARRAY_LIST(1, 4)
        mesh = CBashFORMID_LIST(2)
        location = CBashFORMID_LIST(3)
        xGrid = CBashGeneric_LIST(4, c_short)
        yGrid = CBashGeneric_LIST(5, c_short)
        unknown2_p = CBashUINT8ARRAY_LIST(6)
        copyattrs = ['unknown1', 'mesh', 'location',
                     'xGrid', 'yGrid', 'unknown2_p']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')
        exportattrs.remove('unknown2_p')

    class _NVCI(ListComponent):
        __slots__ = []
        unknown1 = CBashFORMID_LIST(1)
        unknown2 = CBashFORMIDARRAY_LIST(2)
        unknown3 = CBashFORMIDARRAY_LIST(3)
        doors = CBashFORMIDARRAY_LIST(4)
        copyattrs = ['unknown1', 'unknown2',
                     'unknown3', 'doors']
        exportattrs = copyattrs[:]
        exportattrs.remove('unknown1')
        exportattrs.remove('unknown2')
        exportattrs.remove('unknown3')

    version = CBashGeneric(7, c_ulong)

    def create_NVMI(self):
        length = _CGetFieldAttribute(self._RecordID, 8, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 8, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self._NVMI(self._RecordID, 8, length)
    NVMI = CBashLIST(8, _NVMI)
    NVMI_list = CBashLIST(8, _NVMI, True)

    def create_NVCI(self):
        length = _CGetFieldAttribute(self._RecordID, 9, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 9, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self._NVCI(self._RecordID, 9, length)
    NVCI = CBashLIST(9, _NVCI)
    NVCI_list = CBashLIST(9, _NVCI, True)

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['version', 'NVMI_list', 'NVCI_list']

class FnvCELLRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CELL'
    @property
    def _ParentID(self):
        _CGetField.restype = c_ulong
        return _CGetField(self._RecordID, 67, 0, 0, 0, 0, 0, 0, 0)

    @property
    def bsb(self):
        """Returns tesfile block and sub-block indices for cells in this group.
        For interior cell, bsb is (blockNum,subBlockNum). For exterior cell, bsb is
        ((blockX,blockY),(subblockX,subblockY))."""
        #--Interior cell
        if self.IsInterior:
            ObjectID = self.fid[1]
            return (ObjectID % 10, (ObjectID / 10) % 10)
        #--Exterior cell
        else:
            subblockX = int(math.floor((self.posX or 0) / 8.0))
            subblockY = int(math.floor((self.posY or 0) / 8.0))
            return ((int(math.floor(subblockX / 4.0)), int(math.floor(subblockY / 4.0))), (subblockX, subblockY))

    class SwappedImpact(ListComponent):
        __slots__ = []
        material = CBashGeneric_LIST(1, c_ulong)
        oldImpact = CBashFORMID_LIST(2)
        newImpact = CBashFORMID_LIST(3)

        IsStone = CBashBasicType('material', 0, 'IsDirt')
        IsDirt = CBashBasicType('material', 1, 'IsStone')
        IsGrass = CBashBasicType('material', 2, 'IsStone')
        IsGlass = CBashBasicType('material', 3, 'IsStone')
        IsMetal = CBashBasicType('material', 4, 'IsStone')
        IsWood = CBashBasicType('material', 5, 'IsStone')
        IsOrganic = CBashBasicType('material', 6, 'IsStone')
        IsCloth = CBashBasicType('material', 7, 'IsStone')
        IsWater = CBashBasicType('material', 8, 'IsStone')
        IsHollowMetal = CBashBasicType('material', 9, 'IsStone')
        IsOrganicBug = CBashBasicType('material', 10, 'IsStone')
        IsOrganicGlow = CBashBasicType('material', 11, 'IsStone')
        exportattrs = copyattrs = ['material', 'oldImpact', 'newImpact']

    full = CBashSTRING(7)
    flags = CBashGeneric(8, c_ubyte)
    posX = CBashUNKNOWN_OR_GENERIC(9, c_long)
    posY = CBashUNKNOWN_OR_GENERIC(10, c_long)
    quadFlags = CBashUNKNOWN_OR_GENERIC(11, c_ulong)
    ambientRed = CBashGeneric(12, c_ubyte)
    ambientGreen = CBashGeneric(13, c_ubyte)
    ambientBlue = CBashGeneric(14, c_ubyte)
    unused1 = CBashUINT8ARRAY(15, 1)
    directionalRed = CBashGeneric(16, c_ubyte)
    directionalGreen = CBashGeneric(17, c_ubyte)
    directionalBlue = CBashGeneric(18, c_ubyte)
    unused2 = CBashUINT8ARRAY(19, 1)
    fogRed = CBashGeneric(20, c_ubyte)
    fogGreen = CBashGeneric(21, c_ubyte)
    fogBlue = CBashGeneric(22, c_ubyte)
    unused3 = CBashUINT8ARRAY(23, 1)
    fogNear = CBashFLOAT32(24)
    fogFar = CBashFLOAT32(25)
    directionalXY = CBashGeneric(26, c_long)
    directionalZ = CBashGeneric(27, c_long)
    directionalFade = CBashFLOAT32(28)
    fogClip = CBashFLOAT32(29)
    fogPower = CBashFLOAT32(30)

    def create_swappedImpact(self):
        length = _CGetFieldAttribute(self._RecordID, 31, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 31, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.SwappedImpact(self._RecordID, 31, length)
    swappedImpacts = CBashLIST(31, SwappedImpact)
    swappedImpacts_list = CBashLIST(31, SwappedImpact, True)

    concSolid = CBashSTRING(32)
    concBroken = CBashSTRING(33)
    metalSolid = CBashSTRING(34)
    metalHollow = CBashSTRING(35)
    metalSheet = CBashSTRING(36)
    wood = CBashSTRING(37)
    sand = CBashSTRING(38)
    dirt = CBashSTRING(39)
    grass = CBashSTRING(40)
    water = CBashSTRING(41)
    lightTemplate = CBashFORMID(42)
    lightFlags = CBashGeneric(43, c_ulong)
    waterHeight = CBashFLOAT32(44)
    waterNoisePath = CBashISTRING(45)
    regions = CBashFORMIDARRAY(46)
    imageSpace = CBashFORMID(47)
    xcet_p = CBashUINT8ARRAY(48)
    encounterZone = CBashFORMID(49)
    climate = CBashFORMID(50)
    water = CBashFORMID(51)
    owner = CBashFORMID(52)
    rank = CBashGeneric(53, c_long)
    acousticSpace = CBashFORMID(54)
    xcmt_p = CBashUINT8ARRAY(55)
    music = CBashFORMID(56)
    def create_ACHR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("ACHR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvACHRRecord(RecordID) if RecordID else None
    ACHR = CBashSUBRECORDARRAY(57, FnvACHRRecord, "ACHR")

    def create_ACRE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("ACRE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvACRERecord(RecordID) if RecordID else None
    ACRE = CBashSUBRECORDARRAY(58, FnvACRERecord, "ACRE")

    def create_REFR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("REFR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvREFRRecord(RecordID) if RecordID else None
    REFR = CBashSUBRECORDARRAY(59, FnvREFRRecord, "REFR")

    def create_PGRE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("PGRE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvPGRERecord(RecordID) if RecordID else None
    PGRE = CBashSUBRECORDARRAY(60, FnvPGRERecord, "PGRE")

    def create_PMIS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("PMIS", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvPMISRecord(RecordID) if RecordID else None
    PMIS = CBashSUBRECORDARRAY(61, FnvPMISRecord, "PMIS")

    def create_PBEA(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("PBEA", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvPBEARecord(RecordID) if RecordID else None
    PBEA = CBashSUBRECORDARRAY(62, FnvPBEARecord, "PBEA")

    def create_PFLA(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("PFLA", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvPFLARecord(RecordID) if RecordID else None
    PFLA = CBashSUBRECORDARRAY(63, FnvPFLARecord, "PFLA")

    def create_PCBE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("PCBE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvPCBERecord(RecordID) if RecordID else None
    PCBE = CBashSUBRECORDARRAY(64, FnvPCBERecord, "PCBE")

    def create_NAVM(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("NAVM", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvNAVMRecord(RecordID) if RecordID else None
    NAVM = CBashSUBRECORDARRAY(65, FnvNAVMRecord, "NAVM")

    def create_LAND(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("LAND", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvLANDRecord(RecordID) if RecordID else None
    LAND = CBashSUBRECORD(66, FnvLANDRecord, "LAND")

    IsInterior = CBashBasicFlag('flags', 0x00000001)
    IsHasWater = CBashBasicFlag('flags', 0x00000002)
    IsInvertFastTravel = CBashBasicFlag('flags', 0x00000004)
    IsForceHideLand = CBashBasicFlag('flags', 0x00000008) #Exterior cells only
    IsOblivionInterior = CBashBasicFlag('flags', 0x00000008) #Interior cells only
    IsPublicPlace = CBashBasicFlag('flags', 0x00000020)
    IsHandChanged = CBashBasicFlag('flags', 0x00000040)
    IsBehaveLikeExterior = CBashBasicFlag('flags', 0x00000080)

    IsQuad1ForceHidden = CBashBasicFlag('quadFlags', 0x00000001)
    IsQuad2ForceHidden = CBashBasicFlag('quadFlags', 0x00000002)
    IsQuad3ForceHidden = CBashBasicFlag('quadFlags', 0x00000004)
    IsQuad4ForceHidden = CBashBasicFlag('quadFlags', 0x00000008)

    IsLightAmbientInherited = CBashBasicFlag('lightFlags', 0x00000001)
    IsLightDirectionalColorInherited = CBashBasicFlag('lightFlags', 0x00000002)
    IsLightFogColorInherited = CBashBasicFlag('lightFlags', 0x00000004)
    IsLightFogNearInherited = CBashBasicFlag('lightFlags', 0x00000008)
    IsLightFogFarInherited = CBashBasicFlag('lightFlags', 0x00000010)
    IsLightDirectionalRotationInherited = CBashBasicFlag('lightFlags', 0x00000020)
    IsLightDirectionalFadeInherited = CBashBasicFlag('lightFlags', 0x00000040)
    IsLightFogClipInherited = CBashBasicFlag('lightFlags', 0x00000080)
    IsLightFogPowerInherited = CBashBasicFlag('lightFlags', 0x00000100)
    copyattrs = FnvBaseRecord.baseattrs + ['full', 'flags', 'posX', 'posY', 'quadFlags',
                                           'ambientRed', 'ambientGreen', 'ambientBlue',
                                           'directionalRed', 'directionalGreen', 'directionalBlue',
                                           'fogRed', 'fogGreen', 'fogBlue',
                                           'fogNear', 'fogFar', 'directionalXY', 'directionalZ',
                                           'directionalFade', 'fogClip', 'fogPower', 'concSolid',
                                           'concBroken', 'metalSolid', 'metalHollow', 'metalSheet',
                                           'wood', 'sand', 'dirt', 'grass', 'water',
                                           'lightTemplate', 'lightFlags', 'waterHeight',
                                           'waterNoisePath', 'regions', 'imageSpace', 'xcet_p',
                                           'encounterZone', 'climate', 'water', 'owner',
                                           'rank', 'acousticSpace', 'xcmt_p', 'music']
    exportattrs = copyattrs[:]
    exportattrs.remove('xcet_p')
    exportattrs.remove('xcmt_p')

class FnvWRLDRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'WRLD'
    class SwappedImpact(ListComponent):
        __slots__ = []
        material = CBashGeneric_LIST(1, c_ulong)
        oldImpact = CBashFORMID_LIST(2)
        newImpact = CBashFORMID_LIST(3)

        IsStone = CBashBasicType('material', 0, 'IsDirt')
        IsDirt = CBashBasicType('material', 1, 'IsStone')
        IsGrass = CBashBasicType('material', 2, 'IsStone')
        IsGlass = CBashBasicType('material', 3, 'IsStone')
        IsMetal = CBashBasicType('material', 4, 'IsStone')
        IsWood = CBashBasicType('material', 5, 'IsStone')
        IsOrganic = CBashBasicType('material', 6, 'IsStone')
        IsCloth = CBashBasicType('material', 7, 'IsStone')
        IsWater = CBashBasicType('material', 8, 'IsStone')
        IsHollowMetal = CBashBasicType('material', 9, 'IsStone')
        IsOrganicBug = CBashBasicType('material', 10, 'IsStone')
        IsOrganicGlow = CBashBasicType('material', 11, 'IsStone')
        exportattrs = copyattrs = ['material', 'oldImpact', 'newImpact']

    full = CBashSTRING(7)
    encounterZone = CBashFORMID(8)
    parent = CBashFORMID(9)
    parentFlags = CBashGeneric(10, c_ushort)
    climate = CBashFORMID(11)
    water = CBashFORMID(12)
    lodWater = CBashFORMID(13)
    lodWaterHeight = CBashFLOAT32(14)
    defaultLandHeight = CBashFLOAT32(15)
    defaultWaterHeight = CBashFLOAT32(16)
    iconPath = CBashISTRING(17)
    smallIconPath = CBashISTRING(18)
    dimX = CBashGeneric(19, c_long)
    dimY = CBashGeneric(20, c_long)
    NWCellX = CBashGeneric(21, c_short)
    NWCellY = CBashGeneric(22, c_short)
    SECellX = CBashGeneric(23, c_short)
    SECellY = CBashGeneric(24, c_short)
    mapScale = CBashFLOAT32(25)
    xCellOffset = CBashFLOAT32(26)
    yCellOffset = CBashFLOAT32(27)
    imageSpace = CBashFORMID(28)
    flags = CBashGeneric(29, c_ubyte)
    xMinObjBounds = CBashFLOAT32(30)
    yMinObjBounds = CBashFLOAT32(31)
    xMaxObjBounds = CBashFLOAT32(32)
    yMaxObjBounds = CBashFLOAT32(33)
    music = CBashFORMID(34)
    canopyShadowPath = CBashISTRING(35)
    waterNoisePath = CBashISTRING(36)

    def create_swappedImpact(self):
        length = _CGetFieldAttribute(self._RecordID, 37, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 37, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.SwappedImpact(self._RecordID, 37, length)
    swappedImpacts = CBashLIST(37, SwappedImpact)
    swappedImpacts_list = CBashLIST(37, SwappedImpact, True)

    concSolid = CBashSTRING(38)
    concBroken = CBashSTRING(39)
    metalSolid = CBashSTRING(40)
    metalHollow = CBashSTRING(41)
    metalSheet = CBashSTRING(42)
    wood = CBashSTRING(43)
    sand = CBashSTRING(44)
    dirt = CBashSTRING(45)
    grass = CBashSTRING(46)
    water = CBashSTRING(47)
    ofst_p = CBashUINT8ARRAY(48)

    def create_WorldCELL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("WCEL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvCELLRecord(RecordID) if RecordID else None
    WorldCELL = CBashSUBRECORD(49, FnvCELLRecord, "WCEL")
##"WCEL" is an artificial type CBash uses to distinguish World Cells
    def create_CELLS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("CELL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvCELLRecord(RecordID) if RecordID else None
    CELLS = CBashSUBRECORDARRAY(50, FnvCELLRecord, "CELL")

    IsSmallWorld = CBashBasicFlag('flags', 0x01)
    IsNoFastTravel = CBashBasicFlag('flags', 0x02)
    IsUnknown2 = CBashBasicFlag('flags', 0x04)
    IsNoLODWater = CBashBasicFlag('flags', 0x10)
    IsNoLODNoise = CBashBasicFlag('flags', 0x20)
    IsNoNPCFallDmg = CBashBasicFlag('flags', 0x40)

    IsUseLandData = CBashBasicFlag('parentFlags', 0x0001)
    IsUseLODData = CBashBasicFlag('parentFlags', 0x0002)
    IsUseMapData = CBashBasicFlag('parentFlags', 0x0004)
    IsUseWaterData = CBashBasicFlag('parentFlags', 0x0008)
    IsUseClimateData = CBashBasicFlag('parentFlags', 0x0010)
    IsUseImageSpaceData = CBashBasicFlag('parentFlags', 0x0020)
    IsUnknown1 = CBashBasicFlag('parentFlags', 0x0040)
    IsNeedsWaterAdjustment = CBashBasicFlag('parentFlags', 0x0080)
    copyattrs = FnvBaseRecord.baseattrs + ['full', 'encounterZone', 'parent',
                                           'parentFlags', 'climate', 'water',
                                           'lodWater', 'lodWaterHeight',
                                           'defaultLandHeight',
                                           'defaultWaterHeight', 'iconPath',
                                           'smallIconPath', 'dimX', 'dimY',
                                           'NWCellX', 'NWCellY', 'SECellX',
                                           'SECellY', 'mapScale', 'xCellOffset',
                                           'yCellOffset', 'imageSpace', 'flags',
                                           'xMinObjBounds', 'yMinObjBounds',
                                           'xMaxObjBounds', 'yMaxObjBounds',
                                           'music', 'canopyShadowPath',
                                           'waterNoisePath',
                                           'swappedImpacts_list', 'concSolid',
                                           'concBroken', 'metalSolid',
                                           'metalHollow', 'metalSheet', 'wood',
                                           'sand', 'dirt', 'grass', 'water',
                                           'ofst_p']
    exportattrs = copyattrs[:]
    exportattrs.remove('ofst_p')

class FnvDIALRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'DIAL'
    class Quest(ListComponent):
        __slots__ = []
        class QuestUnknown(ListX2Component):
            __slots__ = []
            unknownId = CBashFORMID_LISTX2(1)
            unknown = CBashGeneric_LISTX2(2, c_long)
            copyattrs = ['unknownId', 'unknown']
            exportattrs = copyattrs[:]
            exportattrs.remove('unknownId')
            exportattrs.remove('unknown')

        quest = CBashFORMID_LIST(1)

        def create_unknown(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.QuestUnknown(self._RecordID, self._FieldID, self._ListIndex, 2, length)
        unknowns = CBashLIST_LIST(2, QuestUnknown)
        unknowns_list = CBashLIST_LIST(2, QuestUnknown, True)

        exportattrs = copyattrs = ['quest', 'unknowns_list']

    def create_quest(self):
        length = _CGetFieldAttribute(self._RecordID, 7, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 7, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Quest(self._RecordID, 7, length)
    quests = CBashLIST(7, Quest)
    quests_list = CBashLIST(7, Quest, True)

    def create_removedQuest(self):
        length = _CGetFieldAttribute(self._RecordID, 8, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 8, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Quest(self._RecordID, 8, length)
    removedQuests = CBashLIST(8, Quest)
    removedQuests_list = CBashLIST(8, Quest, True)

    full = CBashSTRING(9)
    priority = CBashFLOAT32(10)
    unknown = CBashSTRING(11)
    dialType = CBashGeneric(12, c_ubyte)
    flags = CBashGeneric(13, c_ubyte)
    def create_INFO(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self.GetParentMod()._ModID, cast("INFO", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, self._RecordID)
        return FnvINFORecord(RecordID) if RecordID else None
    INFO = CBashSUBRECORDARRAY(14, FnvINFORecord, "INFO")

    IsRumors = CBashBasicFlag('flags', 0x01)
    IsTopLevel = CBashBasicFlag('flags', 0x02)

    IsTopic = CBashBasicType('dialType', 0, 'IsConversation')
    IsConversation = CBashBasicType('dialType', 1, 'IsTopic')
    IsCombat = CBashBasicType('dialType', 2, 'IsTopic')
    IsPersuasion = CBashBasicType('dialType', 3, 'IsTopic')
    IsDetection = CBashBasicType('dialType', 4, 'IsTopic')
    IsService = CBashBasicType('dialType', 5, 'IsTopic')
    IsMisc = CBashBasicType('dialType', 6, 'IsTopic')
    IsRadio = CBashBasicType('dialType', 7, 'IsTopic')
    copyattrs = FnvBaseRecord.baseattrs + ['quests_list', 'removedQuests_list',
                                           'full', 'priority', 'unknown',
                                           'dialType', 'flags']
    exportattrs = copyattrs[:]
    exportattrs.remove('unknown')

class FnvQUSTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'QUST'
    def mergeFilter(self, target):
        """Filter out items that don't come from specified modSet.
        Filters items."""
        self.conditions = [x for x in self.conditions if (
            (not isinstance(x.param1,FormID) or x.param1.ValidateFormID(target))
            and
            (not isinstance(x.param2,FormID) or x.param2.ValidateFormID(target))
        )]
        #for target in self.targets_list:
        #    target.conditions = [x for x in target.conditions_list if (
        #        (not isinstance(x.param1,FormID) or x.param1[0] in modSet)
        #        and
        #        (not isinstance(x.param2,FormID) or x.param2[0] in modSet)
        #        )]

    class Stage(ListComponent):
        __slots__ = []
        class Entry(ListX2Component):
            __slots__ = []
            flags = CBashGeneric_LISTX2(1, c_ubyte)

            def create_condition(self):
                length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, self._ListFieldID, self._ListX2Index, 2, 0, 0, 1)
                _CSetField(self._RecordID, self._FieldID, self._ListIndex, self._ListFieldID, self._ListX2Index, 2, 0, 0, 0, c_ulong(length + 1))
                return FNVConditionX3(self._RecordID, self._FieldID, self._ListIndex, self._ListFieldID, self._ListX2Index, 2, length)
            conditions = CBashLIST_LISTX2(2, FNVConditionX3)
            conditions_list = CBashLIST_LISTX2(2, FNVConditionX3, True)

            text = CBashSTRING_LISTX2(3)
            unused1 = CBashUINT8ARRAY_LISTX2(4, 4)
            numRefs = CBashGeneric_LISTX2(5, c_ulong)
            compiledSize = CBashGeneric_LISTX2(6, c_ulong)
            lastIndex = CBashGeneric_LISTX2(7, c_ulong)
            scriptType = CBashGeneric_LISTX2(8, c_ulong)
            scriptFlags = CBashGeneric_LISTX2(9, c_ushort)
            compiled_p = CBashUINT8ARRAY_LISTX2(10)
            scriptText = CBashISTRING_LISTX2(11)

            def create_var(self):
                length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, self._ListFieldID, self._ListX2Index, 12, 0, 0, 1)
                _CSetField(self._RecordID, self._FieldID, self._ListIndex, self._ListFieldID, self._ListX2Index, 12, 0, 0, 0, c_ulong(length + 1))
                return VarX3(self._RecordID, self._FieldID, self._ListIndex, self._ListFieldID, self._ListX2Index, 12, length)
            vars = CBashLIST_LISTX2(12, VarX3)
            vars_list = CBashLIST_LISTX2(12, VarX3, True)

            references = CBashFORMID_OR_UINT32_ARRAY_LISTX2(13)
            nextQuest = CBashFORMID_LISTX2(14)

            IsCompletes = CBashBasicFlag('flags', 0x00000001)
            IsFailed = CBashBasicFlag('flags', 0x00000002)

            IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

            IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
            IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
            IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')
            copyattrs = ['flags', 'conditions_list', 'text',
                         'numRefs', 'compiledSize',
                         'lastIndex', 'scriptType', 'flags',
                         'compiled_p', 'scriptText',
                         'vars_list', 'references',
                         'nextQuest']
            exportattrs = copyattrs[:]
            exportattrs.remove('compiled_p')

        stage = CBashGeneric_LIST(1, c_short)

        def create_entry(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 2, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Entry(self._RecordID, self._FieldID, self._ListIndex, 2, length)
        entries = CBashLIST_LIST(2, Entry)
        entries_list = CBashLIST_LIST(2, Entry, True)

        exportattrs = copyattrs = ['stage', 'entries_list']

    class Objective(ListComponent):
        __slots__ = []
        class Target(ListX2Component):
            __slots__ = []
            targetId = CBashFORMID_LISTX2(1)
            flags = CBashGeneric_LISTX2(2, c_ubyte)
            unused1 = CBashUINT8ARRAY_LISTX2(3, 3)

            def create_condition(self):
                length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, self._ListFieldID, self._ListX2Index, 4, 0, 0, 1)
                _CSetField(self._RecordID, self._FieldID, self._ListIndex, self._ListFieldID, self._ListX2Index, 4, 0, 0, 0, c_ulong(length + 1))
                return FNVConditionX3(self._RecordID, self._FieldID, self._ListIndex, self._ListFieldID, self._ListX2Index, 4, length)
            conditions = CBashLIST_LISTX2(4, FNVConditionX3)
            conditions_list = CBashLIST_LISTX2(4, FNVConditionX3, True)

            IsIgnoresLocks = CBashBasicFlag('flags', 0x00000001)
            exportattrs = copyattrs = ['targetId', 'flags', 'conditions_list']

        objective = CBashGeneric_LIST(1, c_long)
        text = CBashSTRING_LIST(2)

        def create_target(self):
            length = _CGetFieldAttribute(self._RecordID, self._FieldID, self._ListIndex, 3, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, self._FieldID, self._ListIndex, 3, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return self.Target(self._RecordID, self._FieldID, self._ListIndex, 3, length)
        targets = CBashLIST_LIST(3, Target)
        targets_list = CBashLIST_LIST(3, Target, True)

        exportattrs = copyattrs = ['objective', 'text', 'targets_list']

    script = CBashFORMID(7)
    full = CBashSTRING(8)
    iconPath = CBashISTRING(9)
    smallIconPath = CBashISTRING(10)
    flags = CBashGeneric(11, c_ubyte)
    priority = CBashGeneric(12, c_ubyte)
    unused1 = CBashUINT8ARRAY(13, 2)
    delay = CBashFLOAT32(14)

    def create_condition(self):
        length = _CGetFieldAttribute(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 15, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVCondition(self._RecordID, 15, length)
    conditions = CBashLIST(15, FNVCondition)
    conditions_list = CBashLIST(15, FNVCondition, True)

    def create_stage(self):
        length = _CGetFieldAttribute(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 16, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Stage(self._RecordID, 16, length)
    stages = CBashLIST(16, Stage)
    stages_list = CBashLIST(16, Stage, True)

    def create_objectiv(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Objective(self._RecordID, 17, length)
    objectives = CBashLIST(17, Objective)
    objectives_list = CBashLIST(17, Objective, True)

    IsStartEnabled = CBashBasicFlag('flags', 0x00000001)
    IsRepeatedTopics = CBashBasicFlag('flags', 0x00000004)
    IsRepeatedStages = CBashBasicFlag('flags', 0x00000008)
    IsUnknown = CBashBasicFlag('flags', 0x00000010)
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['script', 'full', 'iconPath',
                                                         'smallIconPath', 'flags',
                                                         'priority', 'delay',
                                                         'conditions_list',
                                                         'stages_list', 'objectives_list']

class FnvIDLERecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'IDLE'
    modPath = CBashISTRING(7)
    modb = CBashFLOAT32(8)
    modt_p = CBashUINT8ARRAY(9)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 10, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 10, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 10, length)
    altTextures = CBashLIST(10, FNVAltTexture)
    altTextures_list = CBashLIST(10, FNVAltTexture, True)

    modelFlags = CBashGeneric(11, c_ubyte)
    def create_condition(self):
        length = _CGetFieldAttribute(self._RecordID, 12, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 12, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVCondition(self._RecordID, 12, length)
    conditions = CBashLIST(12, FNVCondition)
    conditions_list = CBashLIST(12, FNVCondition, True)

    animations = CBashFORMIDARRAY(13)
    group = CBashGeneric(14, c_ubyte)
    minLooping = CBashGeneric(15, c_ubyte)
    maxLooping = CBashGeneric(16, c_ubyte)
    unused1 = CBashUINT8ARRAY(17, 1)
    replayDelay = CBashGeneric(18, c_short)
    flags = CBashGeneric(19, c_ubyte)
    unused2 = CBashUINT8ARRAY(20, 1)

    IsNoAttacking = CBashBasicFlag('flags', 0x00000001)
    IsAttacking = CBashInvertedFlag('IsNoAttacking')

    IsIdle = CBashMaskedType('group', ~0xC0, 0, 'IsIdle')
    IsMovement = CBashMaskedType('group', ~0xC0, 1, 'IsMovement')
    IsLeftArm = CBashMaskedType('group', ~0xC0, 2, 'IsMovement')
    IsLeftHand = CBashMaskedType('group', ~0xC0, 3, 'IsMovement')
    IsWeapon = CBashMaskedType('group', ~0xC0, 4, 'IsMovement')
    IsWeaponUp = CBashMaskedType('group', ~0xC0, 5, 'IsMovement')
    IsWeaponDown = CBashMaskedType('group', ~0xC0, 6, 'IsMovement')
    IsSpecialIdle = CBashMaskedType('group', ~0xC0, 7, 'IsMovement')
    IsWholeBody = CBashMaskedType('group', ~0xC0, 20, 'IsMovement')
    IsUpperBody = CBashMaskedType('group', ~0xC0, 21, 'IsMovement')

    IsUnknown1 = CBashBasicFlag('group', 0x40)
    IsNotReturnFile = CBashBasicFlag('group', 0x80)
    IsReturnFile = CBashInvertedFlag('IsNotReturnFile')
    copyattrs = FnvBaseRecord.baseattrs + ['modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'conditions_list', 'animations',
                                           'group', 'minLooping',
                                           'maxLooping', 'replayDelay',
                                           'flags']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvPACKRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'PACK'
    class PackScript(BaseComponent):
        __slots__ = []
        idle = CBashFORMID_GROUP(0)
        unused1 = CBashUINT8ARRAY_GROUP(1, 4)
        numRefs = CBashGeneric_GROUP(2, c_ulong)
        compiledSize = CBashGeneric_GROUP(3, c_ulong)
        lastIndex = CBashGeneric_GROUP(4, c_ulong)
        scriptType = CBashGeneric_GROUP(5, c_ushort)
        scriptFlags = CBashGeneric_GROUP(6, c_ushort)
        compiled_p = CBashUINT8ARRAY_GROUP(7)
        scriptText = CBashISTRING_GROUP(8)
        def create_var(self):
            FieldID = self._FieldID + 9
            length = _CGetFieldAttribute(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1)
            _CSetField(self._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
            return Var(self._RecordID, FieldID, length)
        vars = CBashLIST_GROUP(9, Var)
        vars_list = CBashLIST_GROUP(9, Var, True)
        references = CBashFORMID_OR_UINT32_ARRAY_GROUP(10)
        topic = CBashFORMID_GROUP(11)

        IsEnabled = CBashBasicFlag('scriptFlags', 0x0001)

        IsObject = CBashBasicType('scriptType', 0x0000, 'IsQuest')
        IsQuest = CBashBasicType('scriptType', 0x0001, 'IsObject')
        IsEffect = CBashBasicType('scriptType', 0x0100, 'IsObject')
        copyattrs = ['idle', 'numRefs', 'compiledSize',
                     'lastIndex', 'scriptType', 'scriptFlags',
                     'compiled_p', 'scriptText',
                     'vars_list', 'references', 'topic']
        exportattrs = copyattrs[:]
        exportattrs.remove('compiled_p')

    flags = CBashGeneric(7, c_ulong)
    aiType = CBashGeneric(8, c_ubyte)
    unused1 = CBashUINT8ARRAY(9, 1)
    behaviorFlags = CBashGeneric(10, c_ushort)
    specificFlags = CBashGeneric(11, c_ushort)
    unused2 = CBashUINT8ARRAY(12, 2)
    loc1Type = CBashGeneric(13, c_long)
    loc1Id = CBashFORMID_OR_UINT32(14)
    loc1Radius = CBashGeneric(15, c_long)
    loc2Type = CBashGeneric(16, c_long)
    loc2Id = CBashFORMID_OR_UINT32(17)
    loc2Radius = CBashGeneric(18, c_long)
    month = CBashGeneric(19, c_byte)
    day = CBashGeneric(20, c_byte)
    date = CBashGeneric(21, c_ubyte)
    time = CBashGeneric(22, c_byte)
    duration = CBashGeneric(23, c_long)
    target1Type = CBashGeneric(24, c_long)
    target1Id = CBashFORMID_OR_UINT32(25)
    target1CountOrDistance = CBashGeneric(26, c_long)
    target1Unknown = CBashFLOAT32(27)

    def create_condition(self):
        length = _CGetFieldAttribute(self._RecordID, 28, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 28, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVCondition(self._RecordID, 28, length)
    conditions = CBashLIST(28, FNVCondition)
    conditions_list = CBashLIST(28, FNVCondition, True)

    idleAnimFlags = CBashGeneric(29, c_ubyte)
    idleAnimCount = CBashGeneric(30, c_ubyte)
    idleTimer = CBashFLOAT32(31)
    animations = CBashFORMIDARRAY(32)
    unusedIDLB_p = CBashUINT8ARRAY(33)
    escortDistance = CBashGeneric(34, c_ulong)
    combatStyle = CBashFORMID(35)
    followTriggerRadius = CBashFLOAT32(36)
    patrolType = CBashGeneric(37, c_ushort)
    weaponFlags = CBashGeneric(38, c_ulong)
    fireRate = CBashGeneric(39, c_ubyte)
    fireType = CBashGeneric(40, c_ubyte)
    burstNum = CBashGeneric(41, c_ushort)
    minShots = CBashGeneric(42, c_ushort)
    maxShots = CBashGeneric(43, c_ushort)
    minPause = CBashFLOAT32(44)
    maxPause = CBashFLOAT32(45)
    unused3 = CBashUINT8ARRAY(46, 4)
    target2Type = CBashGeneric(47, c_long)
    target2Id = CBashFORMID_OR_UINT32(48)
    target2CountOrDistance = CBashGeneric(49, c_long)
    target2Unknown = CBashFLOAT32(50)
    FOV = CBashFLOAT32(51)
    topic = CBashFORMID(52)
    dialFlags = CBashGeneric(53, c_ulong)
    unused4 = CBashUINT8ARRAY(54, 4)
    dialType = CBashGeneric(55, c_ulong)
    dialUnknown = CBashUINT8ARRAY(56)
    begin = CBashGrouped(57, PackScript)
    begin_list = CBashGrouped(57, PackScript, True)

    end = CBashGrouped(69, PackScript)
    end_list = CBashGrouped(69, PackScript, True)

    change = CBashGrouped(81, PackScript)
    change_list = CBashGrouped(81, PackScript, True)

    IsOffersServices = CBashBasicFlag('flags', 0x00000001)
    IsMustReachLocation = CBashBasicFlag('flags', 0x00000002)
    IsMustComplete = CBashBasicFlag('flags', 0x00000004)
    IsLockAtStart = CBashBasicFlag('flags', 0x00000008)
    IsLockAtEnd = CBashBasicFlag('flags', 0x00000010)
    IsLockAtLocation = CBashBasicFlag('flags', 0x00000020)
    IsUnlockAtStart = CBashBasicFlag('flags', 0x00000040)
    IsUnlockAtEnd = CBashBasicFlag('flags', 0x00000080)
    IsUnlockAtLocation = CBashBasicFlag('flags', 0x00000100)
    IsContinueIfPcNear = CBashBasicFlag('flags', 0x00000200)
    IsOncePerDay = CBashBasicFlag('flags', 0x00000400)
    IsSkipFallout = CBashBasicFlag('flags', 0x00001000)
    IsAlwaysRun = CBashBasicFlag('flags', 0x00002000)
    IsAlwaysSneak = CBashBasicFlag('flags', 0x00020000)
    IsAllowSwimming = CBashBasicFlag('flags', 0x00040000)
    IsAllowFalls = CBashBasicFlag('flags', 0x00080000)
    IsHeadTrackingOff = CBashBasicFlag('flags', 0x00100000)
    IsUnequipWeapons = CBashBasicFlag('flags', 0x00200000)
    IsDefensiveCombat = CBashBasicFlag('flags', 0x00400000)
    IsWeaponDrawn = CBashBasicFlag('flags', 0x00800000)
    IsNoIdleAnims = CBashBasicFlag('flags', 0x01000000)
    IsPretendInCombat = CBashBasicFlag('flags', 0x02000000)
    IsContinueDuringCombat = CBashBasicFlag('flags', 0x04000000)
    IsNoCombatAlert = CBashBasicFlag('flags', 0x08000000)
    IsNoWarnAttackBehavior = CBashBasicFlag('flags', 0x10000000)

    IsHellosToPlayer = CBashBasicFlag('behaviorFlags', 0x00000001)
    IsRandomConversations = CBashBasicFlag('behaviorFlags', 0x00000002)
    IsObserveCombatBehavior = CBashBasicFlag('behaviorFlags', 0x00000004)
    IsUnknown4 = CBashBasicFlag('behaviorFlags', 0x00000008)
    IsReactionToPlayerActions = CBashBasicFlag('behaviorFlags', 0x00000010)
    IsFriendlyFireComments = CBashBasicFlag('behaviorFlags', 0x00000020)
    IsAggroRadiusBehavior = CBashBasicFlag('behaviorFlags', 0x00000040)
    IsAllowIdleChatter = CBashBasicFlag('behaviorFlags', 0x00000080)
    IsAvoidRadiation = CBashBasicFlag('behaviorFlags', 0x00000100)

    IsHide = CBashBasicFlag('specificFlags', 0x00000001) #Ambush only
    IsNoEating = CBashBasicFlag('specificFlags', 0x00000001)
    IsNoSleeping = CBashBasicFlag('specificFlags', 0x00000002)
    IsSitDown = CBashBasicFlag('specificFlags', 0x00000002) #Use Item At only
    IsNoConversation = CBashBasicFlag('specificFlags', 0x00000004)
    IsRemainNearReference = CBashBasicFlag('specificFlags', 0x00000004) #Guard only
    IsNoIdleMarkers = CBashBasicFlag('specificFlags', 0x00000008)
    IsNoFurniture = CBashBasicFlag('specificFlags', 0x00000010)
    IsNoWandering = CBashBasicFlag('specificFlags', 0x00000020)
    IsAllowBuying = CBashBasicFlag('specificFlags', 0x00000100)
    IsAllowKilling = CBashBasicFlag('specificFlags', 0x00000200)
    IsAllowStealing = CBashBasicFlag('specificFlags', 0x00000400)

    IsRunInSequence = CBashBasicFlag('idleAnimFlags', 0x00000001)
    IsDoOnce = CBashBasicFlag('idleAnimFlags', 0x00000004)

    IsAlwaysHit = CBashBasicFlag('weaponFlags', 0x00000001)
    IsDoNoDamage = CBashBasicFlag('weaponFlags', 0x00000100)
    IsCrouchToReload = CBashBasicFlag('weaponFlags', 0x00010000)
    IsHoldFireWhenBlocked = CBashBasicFlag('weaponFlags', 0x01000000)

    IsNoHeadtracking = CBashBasicFlag('dialFlags', 0x00000001)
    IsDontControlTargetMovement = CBashBasicFlag('dialFlags', 0x00000100)

    IsAIFind = CBashBasicType('aiType', 0, 'IsAIFollow')
    IsAIFollow = CBashBasicType('aiType', 1, 'IsAIFind')
    IsAIEscort = CBashBasicType('aiType', 2, 'IsAIFind')
    IsAIEat = CBashBasicType('aiType', 3, 'IsAIFind')
    IsAISleep = CBashBasicType('aiType', 4, 'IsAIFind')
    IsAIWander = CBashBasicType('aiType', 5, 'IsAIFind')
    IsAITravel = CBashBasicType('aiType', 6, 'IsAIFind')
    IsAIAccompany = CBashBasicType('aiType', 7, 'IsAIFind')
    IsAIUseItemAt = CBashBasicType('aiType', 8, 'IsAIFind')
    IsAIAmbush = CBashBasicType('aiType', 9, 'IsAIFind')
    IsAIFleeNotCombat = CBashBasicType('aiType', 10, 'IsAIFind')
    IsAISandbox = CBashBasicType('aiType', 12, 'IsAIFind')
    IsAIPatrol = CBashBasicType('aiType', 13, 'IsAIFind')
    IsAIGuard = CBashBasicType('aiType', 14, 'IsAIFind')
    IsAIDialogue = CBashBasicType('aiType', 15, 'IsAIFind')
    IsAIUseWeapon = CBashBasicType('aiType', 16, 'IsAIFind')

    IsLoc1NearReference = CBashBasicType('loc1Type', 0, 'IsLoc1InCell')
    IsLoc1InCell = CBashBasicType('loc1Type', 1, 'IsLoc1NearReference')
    IsLoc1NearCurrentLocation = CBashBasicType('loc1Type', 2, 'IsLoc1NearReference')
    IsLoc1NearEditorLocation = CBashBasicType('loc1Type', 3, 'IsLoc1NearReference')
    IsLoc1ObjectID = CBashBasicType('loc1Type', 4, 'IsLoc1NearReference')
    IsLoc1ObjectType = CBashBasicType('loc1Type', 5, 'IsLoc1NearReference')
    IsLoc1NearLinkedReference = CBashBasicType('loc1Type', 6, 'IsLoc1NearReference')
    IsLoc1AtPackageLocation = CBashBasicType('loc1Type', 7, 'IsLoc1NearReference')

    IsLoc2NearReference = CBashBasicType('loc2Type', 0, 'IsLoc2InCell')
    IsLoc2InCell = CBashBasicType('loc2Type', 1, 'IsLoc2NearReference')
    IsLoc2NearCurrentLocation = CBashBasicType('loc2Type', 2, 'IsLoc2NearReference')
    IsLoc2NearEditorLocation = CBashBasicType('loc2Type', 3, 'IsLoc2NearReference')
    IsLoc2ObjectID = CBashBasicType('loc2Type', 4, 'IsLoc2NearReference')
    IsLoc2ObjectType = CBashBasicType('loc2Type', 5, 'IsLoc2NearReference')
    IsLoc2NearLinkedReference = CBashBasicType('loc2Type', 6, 'IsLoc2NearReference')
    IsLoc2AtPackageLocation = CBashBasicType('loc2Type', 7, 'IsLoc2NearReference')

    IsAnyDay = CBashBasicType('day', -1, 'IsSunday')
    IsSunday = CBashBasicType('day', 0, 'IsAnyDay')
    IsMonday = CBashBasicType('day', 1, 'IsAnyDay')
    IsTuesday = CBashBasicType('day', 2, 'IsAnyDay')
    IsWednesday = CBashBasicType('day', 3, 'IsAnyDay')
    IsThursday = CBashBasicType('day', 4, 'IsAnyDay')
    IsFriday = CBashBasicType('day', 5, 'IsAnyDay')
    IsSaturday = CBashBasicType('day', 6, 'IsAnyDay')
    IsWeekdays = CBashBasicType('day', 7, 'IsAnyDay')
    IsWeekends = CBashBasicType('day', 8, 'IsAnyDay')
    IsMWF = CBashBasicType('day', 9, 'IsAnyDay')
    IsTTh = CBashBasicType('day', 10, 'IsAnyDay')

    IsTarget1Reference = CBashBasicType('target1Type', 0, 'IsTarget1Reference')
    IsTarget1ObjectID = CBashBasicType('target1Type', 1, 'IsTarget1Reference')
    IsTarget1ObjectType = CBashBasicType('target1Type', 2, 'IsTarget1Reference')
    IsTarget1LinkedReference = CBashBasicType('target1Type', 3, 'IsTarget1Reference')

    IsTarget2Reference = CBashBasicType('target2Type', 0, 'IsTarget2Reference')
    IsTarget2ObjectID = CBashBasicType('target2Type', 1, 'IsTarget2Reference')
    IsTarget2ObjectType = CBashBasicType('target2Type', 2, 'IsTarget2Reference')
    IsTarget2LinkedReference = CBashBasicType('target2Type', 3, 'IsTarget2Reference')

    IsNotRepeatable = CBashBasicType('patrolType', 0, 'IsRepeatable')
    IsRepeatable = CBashBasicType('patrolType', 1, 'IsNotRepeatable')

    IsAutoFire = CBashBasicType('fireRate', 0, 'IsVolleyFire')
    IsVolleyFire = CBashBasicType('fireRate', 1, 'IsAutoFire')

    IsNumberOfBursts = CBashBasicType('fireType', 0, 'IsRepeatFire')
    IsRepeatFire = CBashBasicType('fireType', 1, 'IsNumberOfBursts')

    IsConversation = CBashBasicType('dialType', 0, 'IsSayTo')
    IsSayTo = CBashBasicType('dialType', 1, 'IsConversation')
    copyattrs = FnvBaseRecord.baseattrs + ['flags', 'aiType', 'behaviorFlags',
                                           'specificFlags', 'loc1Type', 'loc1Id',
                                           'loc1Radius', 'loc2Type', 'loc2Id',
                                           'loc2Radius', 'month', 'day', 'date',
                                           'time', 'duration', 'target1Type',
                                           'target1Id', 'target1CountOrDistance',
                                           'target1Unknown', 'conditions_list',
                                           'idleAnimFlags', 'idleAnimCount',
                                           'idleTimer', 'animations',
                                           'escortDistance', 'combatStyle',
                                           'followTriggerRadius', 'patrolType',
                                           'weaponFlags', 'fireRate', 'fireType',
                                           'burstNum', 'minShots', 'maxShots',
                                           'minPause', 'maxPause', 'target2Type',
                                           'target2Id', 'target2CountOrDistance',
                                           'target2Unknown', 'FOV', 'topic',
                                           'dialFlags', 'dialType', 'dialUnknown',
                                           'begin_list', 'end_list', 'change_list']
    exportattrs = copyattrs[:]
    exportattrs.remove('target1Unknown')
    exportattrs.remove('target2Unknown')
    exportattrs.remove('dialUnknown')

class FnvCSTYRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CSTY'
    dodgeChance = CBashGeneric(7, c_ubyte)
    lrChance = CBashGeneric(8, c_ubyte)
    unused1 = CBashUINT8ARRAY(9, 2)
    lrTimerMin = CBashFLOAT32(10)
    lrTimerMax = CBashFLOAT32(11)
    forTimerMin = CBashFLOAT32(12)
    forTimerMax = CBashFLOAT32(13)
    backTimerMin = CBashFLOAT32(14)
    backTimerMax = CBashFLOAT32(15)
    idleTimerMin = CBashFLOAT32(16)
    idleTimerMax = CBashFLOAT32(17)
    blkChance = CBashGeneric(18, c_ubyte)
    atkChance = CBashGeneric(19, c_ubyte)
    unused2 = CBashUINT8ARRAY(20, 2)
    atkBRecoil = CBashFLOAT32(21)
    atkBUnc = CBashFLOAT32(22)
    atkBh2h = CBashFLOAT32(23)
    pAtkChance = CBashGeneric(24, c_ubyte)
    unused3 = CBashUINT8ARRAY(25, 3)
    pAtkBRecoil = CBashFLOAT32(26)
    pAtkBUnc = CBashFLOAT32(27)
    pAtkNormal = CBashGeneric(28, c_ubyte)
    pAtkFor = CBashGeneric(29, c_ubyte)
    pAtkBack = CBashGeneric(30, c_ubyte)
    pAtkL = CBashGeneric(31, c_ubyte)
    pAtkR = CBashGeneric(32, c_ubyte)
    unused4 = CBashUINT8ARRAY(33, 3)
    holdTimerMin = CBashFLOAT32(34)
    holdTimerMax = CBashFLOAT32(35)
    flags = CBashGeneric(36, c_ushort)
    unused5 = CBashUINT8ARRAY(37, 2)
    acroDodge = CBashGeneric(38, c_ubyte)
    rushChance = CBashGeneric(39, c_ubyte)
    unused6 = CBashUINT8ARRAY(40, 2)
    rushMult = CBashFLOAT32(41)
    dodgeFMult = CBashFLOAT32(42)
    dodgeFBase = CBashFLOAT32(43)
    encSBase = CBashFLOAT32(44)
    encSMult = CBashFLOAT32(45)
    dodgeAtkMult = CBashFLOAT32(46)
    dodgeNAtkMult = CBashFLOAT32(47)
    dodgeBAtkMult = CBashFLOAT32(48)
    dodgeBNAtkMult = CBashFLOAT32(49)
    dodgeFAtkMult = CBashFLOAT32(50)
    dodgeFNAtkMult = CBashFLOAT32(51)
    blockMult = CBashFLOAT32(52)
    blockBase = CBashFLOAT32(53)
    blockAtkMult = CBashFLOAT32(54)
    blockNAtkMult = CBashFLOAT32(55)
    atkMult = CBashFLOAT32(56)
    atkBase = CBashFLOAT32(57)
    atkAtkMult = CBashFLOAT32(58)
    atkNAtkMult = CBashFLOAT32(59)
    atkBlockMult = CBashFLOAT32(60)
    pAtkFBase = CBashFLOAT32(61)
    pAtkFMult = CBashFLOAT32(62)
    coverRadius = CBashFLOAT32(63)
    coverChance = CBashFLOAT32(64)
    waitTimerMin = CBashFLOAT32(65)
    waitTimerMax = CBashFLOAT32(66)
    waitFireTimerMin = CBashFLOAT32(67)
    waitFireTimerMax = CBashFLOAT32(68)
    fireTimerMin = CBashFLOAT32(69)
    fireTimerMax = CBashFLOAT32(70)
    rangedRangeMultMin = CBashFLOAT32(71)
    unused7 = CBashUINT8ARRAY(72, 4)
    weaponRestrictions = CBashGeneric(73, c_ulong)
    rangedRangeMultMax = CBashFLOAT32(74)
    targetMaxFOV = CBashFLOAT32(75)
    combatRadius = CBashFLOAT32(76)
    semiAutoFireDelayMultMin = CBashFLOAT32(77)
    semiAutoFireDelayMultMax = CBashFLOAT32(78)

    IsUseChanceForAttack = CBashBasicFlag('flags', 0x00000001)
    IsMeleeAlertOK = CBashBasicFlag('flags', 0x00000002)
    IsFleeForSurvival = CBashBasicFlag('flags', 0x00000004)
    IsIgnoreThreats = CBashBasicFlag('flags', 0x00000010)
    IsIgnoreDamagingSelf = CBashBasicFlag('flags', 0x00000020)
    IsIgnoreDamagingGroup = CBashBasicFlag('flags', 0x00000040)
    IsIgnoreDamagingSpectator = CBashBasicFlag('flags', 0x00000080)
    IsNoUseStealthboy = CBashBasicFlag('flags', 0x00000100)

    IsNone = CBashBasicType('weaponRestrictions', 0, 'IsMeleeOnly')
    IsMeleeOnly = CBashBasicType('weaponRestrictions', 1, 'IsNone')
    IsRangedOnly = CBashBasicType('weaponRestrictions', 2, 'IsNone')
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['dodgeChance', 'lrChance', 'lrTimerMin',
                                                         'lrTimerMax', 'forTimerMin', 'forTimerMax',
                                                         'backTimerMin', 'backTimerMax', 'idleTimerMin',
                                                         'idleTimerMax', 'blkChance', 'atkChance',
                                                         'atkBRecoil', 'atkBUnc', 'atkBh2h', 'pAtkChance',
                                                         'pAtkBRecoil', 'pAtkBUnc', 'pAtkNormal',
                                                         'pAtkFor', 'pAtkBack', 'pAtkL', 'pAtkR',
                                                         'holdTimerMin', 'holdTimerMax', 'flags',
                                                         'acroDodge', 'rushChance', 'rushMult',
                                                         'dodgeFMult', 'dodgeFBase', 'encSBase',
                                                         'encSMult', 'dodgeAtkMult', 'dodgeNAtkMult',
                                                         'dodgeBAtkMult', 'dodgeBNAtkMult',
                                                         'dodgeFAtkMult', 'dodgeFNAtkMult', 'blockMult',
                                                         'blockBase', 'blockAtkMult', 'blockNAtkMult',
                                                         'atkMult', 'atkBase', 'atkAtkMult',
                                                         'atkNAtkMult', 'atkBlockMult', 'pAtkFBase',
                                                         'pAtkFMult', 'coverRadius', 'coverChance',
                                                         'waitTimerMin', 'waitTimerMax',
                                                         'waitFireTimerMin', 'waitFireTimerMax',
                                                         'fireTimerMin', 'fireTimerMax',
                                                         'rangedRangeMultMin', 'weaponRestrictions',
                                                         'rangedRangeMultMax', 'targetMaxFOV',
                                                         'combatRadius', 'semiAutoFireDelayMultMin',
                                                         'semiAutoFireDelayMultMax']

class FnvLSCRRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'LSCR'
    class Location(ListComponent):
        __slots__ = []
        direct = CBashFORMID_LIST(1)
        indirect = CBashFORMID_LIST(2)
        gridY = CBashGeneric_LIST(3, c_short)
        gridX = CBashGeneric_LIST(4, c_short)
        exportattrs = copyattrs = ['direct', 'indirect', 'gridY', 'gridX']

    iconPath = CBashISTRING(7)
    smallIconPath = CBashISTRING(8)
    text = CBashSTRING(9)

    def create_location(self):
        length = _CGetFieldAttribute(self._RecordID, 10, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 10, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.Location(self._RecordID, 10, length)
    locations = CBashLIST(10, Location)
    locations_list = CBashLIST(10, Location, True)

    screentype = CBashFORMID(11)
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['iconPath', 'smallIconPath', 'text',
                                                         'locations_list', 'screentype']

class FnvANIORecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ANIO'
    modPath = CBashISTRING(7)
    modb = CBashFLOAT32(8)
    modt_p = CBashUINT8ARRAY(9)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 10, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 10, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 10, length)
    altTextures = CBashLIST(10, FNVAltTexture)
    altTextures_list = CBashLIST(10, FNVAltTexture, True)

    modelFlags = CBashGeneric(11, c_ubyte)
    animation = CBashFORMID(12)
    copyattrs = FnvBaseRecord.baseattrs + ['modPath', 'modb', 'modt_p',
                                           'altTextures_list',
                                           'modelFlags', 'animation']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvWATRRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'WATR'
    full = CBashSTRING(7)
    noisePath = CBashISTRING(8)
    opacity = CBashGeneric(9, c_ubyte)
    flags = CBashGeneric(10, c_ubyte)
    material = CBashISTRING(11)
    sound = CBashFORMID(12)
    effect = CBashFORMID(13)
    damage = CBashGeneric(14, c_ushort)
    unknown1 = CBashFLOAT32(15)
    unknown2 = CBashFLOAT32(16)
    unknown3 = CBashFLOAT32(17)
    unknown4 = CBashFLOAT32(18)
    sunPower = CBashFLOAT32(19)
    reflectAmt = CBashFLOAT32(20)
    fresnelAmt = CBashFLOAT32(21)
    unused1 = CBashUINT8ARRAY(22, 4)
    fogNear = CBashFLOAT32(23)
    fogFar = CBashFLOAT32(24)
    shallowRed = CBashGeneric(25, c_ubyte)
    shallowGreen = CBashGeneric(26, c_ubyte)
    shallowBlue = CBashGeneric(27, c_ubyte)
    unused2 = CBashUINT8ARRAY(28, 1)
    deepRed = CBashGeneric(29, c_ubyte)
    deepGreen = CBashGeneric(30, c_ubyte)
    deepBlue = CBashGeneric(31, c_ubyte)
    unused3 = CBashUINT8ARRAY(32, 1)
    reflRed = CBashGeneric(33, c_ubyte)
    reflGreen = CBashGeneric(34, c_ubyte)
    reflBlue = CBashGeneric(35, c_ubyte)
    unused4 = CBashUINT8ARRAY(36, 1)
    unused5 = CBashUINT8ARRAY(37, 4)
    rainForce = CBashFLOAT32(38)
    rainVelocity = CBashFLOAT32(39)
    rainFalloff = CBashFLOAT32(40)
    rainDampner = CBashFLOAT32(41)
    dispSize = CBashFLOAT32(42)
    dispForce = CBashFLOAT32(43)
    dispVelocity = CBashFLOAT32(44)
    dispFalloff = CBashFLOAT32(45)
    dispDampner = CBashFLOAT32(46)
    rainSize = CBashFLOAT32(47)
    normalsNoiseScale = CBashFLOAT32(48)
    noise1Direction = CBashFLOAT32(49)
    noise2Direction = CBashFLOAT32(50)
    noise3Direction = CBashFLOAT32(51)
    noise1Speed = CBashFLOAT32(52)
    noise2Speed = CBashFLOAT32(53)
    noise3Speed = CBashFLOAT32(54)
    normalsFalloffStart = CBashFLOAT32(55)
    normalsFalloffEnd = CBashFLOAT32(56)
    fogAmt = CBashFLOAT32(57)
    normalsUVScale = CBashFLOAT32(58)
    underFogAmt = CBashFLOAT32(59)
    underFogNear = CBashFLOAT32(60)
    underFogFar = CBashFLOAT32(61)
    distAmt = CBashFLOAT32(62)
    shininess = CBashFLOAT32(63)
    hdrMult = CBashFLOAT32(64)
    lightRadius = CBashFLOAT32(65)
    lightBright = CBashFLOAT32(66)
    noise1UVScale = CBashFLOAT32(67)
    noise2UVScale = CBashFLOAT32(68)
    noise3UVScale = CBashFLOAT32(69)
    noise1AmpScale = CBashFLOAT32(70)
    noise2AmpScale = CBashFLOAT32(71)
    noise3AmpScale = CBashFLOAT32(72)
    dayWater = CBashFORMID(73)
    nightWater = CBashFORMID(74)
    underWater = CBashFORMID(75)
    IsCausesDamage = CBashBasicFlag('flags', 0x01)
    IsReflective = CBashBasicFlag('flags', 0x02)
    copyattrs = FnvBaseRecord.baseattrs + ['full', 'noisePath', 'opacity', 'flags',
                                           'material', 'sound', 'effect', 'damage',
                                           'unknown1', 'unknown2', 'unknown3', 'unknown4',
                                           'sunPower', 'reflectAmt', 'fresnelAmt',
                                           'fogNear', 'fogFar',
                                           'shallowRed', 'shallowGreen', 'shallowBlue',
                                           'deepRed', 'deepGreen', 'deepBlue',
                                           'reflRed', 'reflGreen', 'reflBlue',
                                           'rainForce', 'rainVelocity', 'rainFalloff',
                                           'rainDampner', 'dispSize', 'dispForce',
                                           'dispVelocity', 'dispFalloff', 'dispDampner',
                                           'rainSize', 'normalsNoiseScale',
                                           'noise1Direction', 'noise2Direction', 'noise3Direction',
                                           'noise1Speed', 'noise2Speed', 'noise3Speed',
                                           'normalsFalloffStart', 'normalsFalloffEnd',
                                           'fogAmt', 'normalsUVScale', 'underFogAmt', 'underFogNear',
                                           'underFogFar', 'distAmt', 'shininess', 'hdrMult',
                                           'lightRadius', 'lightBright',
                                           'noise1UVScale', 'noise2UVScale', 'noise3UVScale',
                                           'noise1AmpScale', 'noise2AmpScale', 'noise3AmpScale',
                                           'dayWater', 'nightWater', 'underWater']
    exportattrs = copyattrs[:]
    exportattrs.remove('unknown1')
    exportattrs.remove('unknown2')
    exportattrs.remove('unknown3')
    exportattrs.remove('unknown4')

class FnvEFSHRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'EFSH'
    fillPath = CBashISTRING(7)
    particlePath = CBashISTRING(8)
    holesPath = CBashISTRING(9)
    flags = CBashGeneric(10, c_ubyte)
    unused1 = CBashUINT8ARRAY(11, 3)
    memSBlend = CBashGeneric(12, c_ulong)
    memBlendOp = CBashGeneric(13, c_ulong)
    memZFunc = CBashGeneric(14, c_ulong)
    fillRed = CBashGeneric(15, c_ubyte)
    fillGreen = CBashGeneric(16, c_ubyte)
    fillBlue = CBashGeneric(17, c_ubyte)
    unused2 = CBashUINT8ARRAY(18, 1)
    fillAIn = CBashFLOAT32(19)
    fillAFull = CBashFLOAT32(20)
    fillAOut = CBashFLOAT32(21)
    fillAPRatio = CBashFLOAT32(22)
    fillAAmp = CBashFLOAT32(23)
    fillAFreq = CBashFLOAT32(24)
    fillAnimSpdU = CBashFLOAT32(25)
    fillAnimSpdV = CBashFLOAT32(26)
    edgeEffOff = CBashFLOAT32(27)
    edgeEffRed = CBashGeneric(28, c_ubyte)
    edgeEffGreen = CBashGeneric(29, c_ubyte)
    edgeEffBlue = CBashGeneric(30, c_ubyte)
    unused3 = CBashUINT8ARRAY(31, 1)
    edgeEffAIn = CBashFLOAT32(32)
    edgeEffAFull = CBashFLOAT32(33)
    edgeEffAOut = CBashFLOAT32(34)
    edgeEffAPRatio = CBashFLOAT32(35)
    edgeEffAAmp = CBashFLOAT32(36)
    edgeEffAFreq = CBashFLOAT32(37)
    fillAFRatio = CBashFLOAT32(38)
    edgeEffAFRatio = CBashFLOAT32(39)
    memDBlend = CBashGeneric(40, c_ulong)
    partSBlend = CBashGeneric(41, c_ulong)
    partBlendOp = CBashGeneric(42, c_ulong)
    partZFunc = CBashGeneric(43, c_ulong)
    partDBlend = CBashGeneric(44, c_ulong)
    partBUp = CBashFLOAT32(45)
    partBFull = CBashFLOAT32(46)
    partBDown = CBashFLOAT32(47)
    partBFRatio = CBashFLOAT32(48)
    partBPRatio = CBashFLOAT32(49)
    partLTime = CBashFLOAT32(50)
    partLDelta = CBashFLOAT32(51)
    partNSpd = CBashFLOAT32(52)
    partNAcc = CBashFLOAT32(53)
    partVel1 = CBashFLOAT32(54)
    partVel2 = CBashFLOAT32(55)
    partVel3 = CBashFLOAT32(56)
    partAcc1 = CBashFLOAT32(57)
    partAcc2 = CBashFLOAT32(58)
    partAcc3 = CBashFLOAT32(59)
    partKey1 = CBashFLOAT32(60)
    partKey2 = CBashFLOAT32(61)
    partKey1Time = CBashFLOAT32(62)
    partKey2Time = CBashFLOAT32(63)
    key1Red = CBashGeneric(64, c_ubyte)
    key1Green = CBashGeneric(65, c_ubyte)
    key1Blue = CBashGeneric(66, c_ubyte)
    unused4 = CBashUINT8ARRAY(67, 1)
    key2Red = CBashGeneric(68, c_ubyte)
    key2Green = CBashGeneric(69, c_ubyte)
    key2Blue = CBashGeneric(70, c_ubyte)
    unused5 = CBashUINT8ARRAY(71, 1)
    key3Red = CBashGeneric(72, c_ubyte)
    key3Green = CBashGeneric(73, c_ubyte)
    key3Blue = CBashGeneric(74, c_ubyte)
    unused6 = CBashUINT8ARRAY(75, 1)
    key1A = CBashFLOAT32(76)
    key2A = CBashFLOAT32(77)
    key3A = CBashFLOAT32(78)
    key1Time = CBashFLOAT32(79)
    key2Time = CBashFLOAT32(80)
    key3Time = CBashFLOAT32(81)
    partInitSpd = CBashFLOAT32(82)
    partInitRot = CBashFLOAT32(83)
    partInitRotDelta = CBashFLOAT32(84)
    partRotSpd = CBashFLOAT32(85)
    partRotDelta = CBashFLOAT32(86)
    addon = CBashFORMID(87)
    holesSTime = CBashFLOAT32(88)
    holesETime = CBashFLOAT32(89)
    holesSValue = CBashFLOAT32(90)
    holesEValue = CBashFLOAT32(91)
    edgeWidth = CBashFLOAT32(92)
    edgeRed = CBashGeneric(93, c_ubyte)
    edgeGreen = CBashGeneric(94, c_ubyte)
    edgeBlue = CBashGeneric(95, c_ubyte)
    unused7 = CBashUINT8ARRAY(96, 1)
    explWindSpd = CBashFLOAT32(97)
    textCountU = CBashGeneric(98, c_ulong)
    textCountV = CBashGeneric(99, c_ulong)
    addonFITime = CBashFLOAT32(100)
    addonFOTime = CBashFLOAT32(101)
    addonScaleStart = CBashFLOAT32(102)
    addonScaleEnd = CBashFLOAT32(103)
    addonScaleInTime = CBashFLOAT32(104)
    addonScaleOutTime = CBashFLOAT32(105)

    IsNoMemShader = CBashBasicFlag('flags', 0x00000001)
    IsNoPartShader = CBashBasicFlag('flags', 0x00000008)
    IsEdgeInverse = CBashBasicFlag('flags', 0x00000010)
    IsMemSkinOnly = CBashBasicFlag('flags', 0x00000020)
    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['fillPath', 'particlePath', 'holesPath',
                                                         'flags', 'memSBlend', 'memBlendOp',
                                                         'memZFunc',
                                                         'fillRed', 'fillGreen', 'fillBlue',
                                                         'fillAIn', 'fillAFull', 'fillAOut',
                                                         'fillAPRatio', 'fillAAmp', 'fillAFreq',
                                                         'fillAnimSpdU', 'fillAnimSpdV',
                                                         'edgeEffOff',
                                                         'edgeEffRed', 'edgeEffGreen', 'edgeEffBlue',
                                                         'edgeEffAIn', 'edgeEffAFull', 'edgeEffAOut',
                                                         'edgeEffAPRatio', 'edgeEffAAmp',
                                                         'edgeEffAFreq', 'fillAFRatio',
                                                         'edgeEffAFRatio', 'memDBlend', 'partSBlend',
                                                         'partBlendOp', 'partZFunc', 'partDBlend',
                                                         'partBUp', 'partBFull', 'partBDown',
                                                         'partBFRatio', 'partBPRatio', 'partLTime',
                                                         'partLDelta', 'partNSpd', 'partNAcc',
                                                         'partVel1', 'partVel2', 'partVel3',
                                                         'partAcc1', 'partAcc2', 'partAcc3',
                                                         'partKey1', 'partKey2',
                                                         'partKey1Time', 'partKey2Time',
                                                         'key1Red', 'key1Green', 'key1Blue',
                                                         'key2Red', 'key2Green', 'key2Blue',
                                                         'key3Red', 'key3Green', 'key3Blue',
                                                         'key1A', 'key2A', 'key3A',
                                                         'key1Time', 'key2Time', 'key3Time',
                                                         'partInitSpd', 'partInitRot',
                                                         'partInitRotDelta', 'partRotSpd',
                                                         'partRotDelta', 'addon', 'holesSTime',
                                                         'holesETime', 'holesSValue', 'holesEValue',
                                                         'edgeWidth',
                                                         'edgeRed', 'edgeGreen', 'edgeBlue',
                                                         'explWindSpd', 'textCountU', 'textCountV',
                                                         'addonFITime', 'addonFOTime',
                                                         'addonScaleStart', 'addonScaleEnd',
                                                         'addonScaleInTime', 'addonScaleOutTime']

class FnvEXPLRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'EXPL'
    boundX1 = CBashGeneric(7, c_short)
    boundY1 = CBashGeneric(8, c_short)
    boundZ1 = CBashGeneric(9, c_short)
    boundX2 = CBashGeneric(10, c_short)
    boundY2 = CBashGeneric(11, c_short)
    boundZ2 = CBashGeneric(12, c_short)
    full = CBashSTRING(13)
    modPath = CBashISTRING(14)
    modb = CBashFLOAT32(15)
    modt_p = CBashUINT8ARRAY(16)

    def create_altTexture(self):
        length = _CGetFieldAttribute(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 17, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return FNVAltTexture(self._RecordID, 17, length)
    altTextures = CBashLIST(17, FNVAltTexture)
    altTextures_list = CBashLIST(17, FNVAltTexture, True)

    modelFlags = CBashGeneric(18, c_ubyte)
    effect = CBashFORMID(19)
    imageSpace = CBashFORMID(20)
    force = CBashFLOAT32(21)
    damage = CBashFLOAT32(22)
    radius = CBashFLOAT32(23)
    light = CBashFORMID(24)
    sound1 = CBashFORMID(25)
    flags = CBashGeneric(26, c_ulong)
    ISRadius = CBashFLOAT32(27)
    impactDataSet = CBashFORMID(28)
    sound2 = CBashFORMID(29)
    radLevel = CBashFLOAT32(30)
    radTime = CBashFLOAT32(31)
    radRadius = CBashFLOAT32(32)
    soundLevel = CBashGeneric(33, c_ulong)
    impact = CBashFORMID(34)

    IsUnknown1 = CBashBasicFlag('flags', 0x00000001)
    IsAlwaysUsesWorldOrientation = CBashBasicFlag('flags', 0x00000002)
    IsAlwaysKnockDown = CBashBasicFlag('flags', 0x00000004)
    IsFormulaKnockDown = CBashBasicFlag('flags', 0x00000008)
    IsIgnoreLOS = CBashBasicFlag('flags', 0x00000010)
    IsPushExplosionSourceRefOnly = CBashBasicFlag('flags', 0x00000020)
    IsIgnoreImageSpaceSwap = CBashBasicFlag('flags', 0x00000040)

    IsHead = CBashBasicFlag('modelFlags', 0x01)
    IsTorso = CBashBasicFlag('modelFlags', 0x02)
    IsRightHand = CBashBasicFlag('modelFlags', 0x04)
    IsLeftHand = CBashBasicFlag('modelFlags', 0x08)

    IsLoud = CBashBasicType('soundLevel', 0, 'IsNormal')
    IsNormal = CBashBasicType('soundLevel', 1, 'IsLoud')
    IsSilent = CBashBasicType('soundLevel', 2, 'IsLoud')
    copyattrs = FnvBaseRecord.baseattrs + ['boundX1', 'boundY1', 'boundZ1',
                                           'boundX2', 'boundY2', 'boundZ2',
                                           'full', 'modPath', 'modb', 'modt_p',
                                           'altTextures_list', 'modelFlags',
                                           'effect', 'imageSpace', 'force',
                                           'damage', 'radius', 'light',
                                           'sound1', 'flags', 'ISRadius',
                                           'impactDataSet', 'sound2',
                                           'radLevel', 'radTime',
                                           'radRadius', 'soundLevel', 'impact']
    exportattrs = copyattrs[:]
    exportattrs.remove('modt_p')

class FnvDEBRRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'DEBR'
    class DebrisModel(ListComponent):
        __slots__ = []
        percentage = CBashGeneric_LIST(1, c_ubyte)
        modPath = CBashISTRING_LIST(2)
        flags = CBashGeneric_LIST(3, c_ubyte)
        modt_p = CBashUINT8ARRAY_LIST(4)

        IsHasCollisionData = CBashBasicFlag('flags', 0x01)
        copyattrs = ['percentage', 'modPath', 'flags', 'modt_p']
        exportattrs = copyattrs[:]
        exportattrs.remove('modt_p')

    def create_model(self):
        length = _CGetFieldAttribute(self._RecordID, 7, 0, 0, 0, 0, 0, 0, 1)
        _CSetField(self._RecordID, 7, 0, 0, 0, 0, 0, 0, 0, c_ulong(length + 1))
        return self.DebrisModel(self._RecordID, 7, length)
    models = CBashLIST(7, DebrisModel)
    models_list = CBashLIST(7, DebrisModel, True)

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + ['models_list']

class FnvIMGSRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'IMGS'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvIMADRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'IMAD'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvFLSTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'FLST'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvPERKRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'PERK'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvBPTDRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'BPTD'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvADDNRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ADDN'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvAVIFRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'AVIF'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvRADSRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'RADS'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvCAMSRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CAMS'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvCPTHRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CPTH'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvVTYPRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'VTYP'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvIPCTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'IPCT'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvIPDSRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'IPDS'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvARMARecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ARMA'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvECZNRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ECZN'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvMESGRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'MESG'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvRGDLRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'RGDL'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvDOBJRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'DOBJ'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvLGTMRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'LGTM'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvMUSCRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'MUSC'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvIMODRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'IMOD'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvREPURecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'REPU'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvRCPERecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'RCPE'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvRCCTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'RCCT'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvCHIPRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CHIP'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvCSNORecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CSNO'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvLSCTRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'LSCT'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvMSETRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'MSET'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvALOCRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'ALOC'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvCHALRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CHAL'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvAMEFRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'AMEF'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvCCRDRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CCRD'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvCMNYRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CMNY'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvCDCKRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'CDCK'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvDEHYRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'DEHY'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvHUNGRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'HUNG'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

class FnvSLPDRecord(FnvBaseRecord):
    __slots__ = []
    _Type = 'SLPD'

    exportattrs = copyattrs = FnvBaseRecord.baseattrs + []

fnv_type_record = dict([('BASE',FnvBaseRecord),(None,None),('',None),
                        ('GMST',FnvGMSTRecord),('TXST',FnvTXSTRecord),('MICN',FnvMICNRecord),
                        ('GLOB',FnvGLOBRecord),('CLAS',FnvCLASRecord),('FACT',FnvFACTRecord),
                        ('HDPT',FnvHDPTRecord),('HAIR',FnvHAIRRecord),('EYES',FnvEYESRecord),
                        ('RACE',FnvRACERecord),('SOUN',FnvSOUNRecord),('ASPC',FnvASPCRecord),
                        ('MGEF',FnvMGEFRecord),('SCPT',FnvSCPTRecord),('LTEX',FnvLTEXRecord),
                        ('ENCH',FnvENCHRecord),('SPEL',FnvSPELRecord),('ACTI',FnvACTIRecord),
                        ('TACT',FnvTACTRecord),('TERM',FnvTERMRecord),('ARMO',FnvARMORecord),
                        ('BOOK',FnvBOOKRecord),('CONT',FnvCONTRecord),('DOOR',FnvDOORRecord),
                        ('INGR',FnvINGRRecord),('LIGH',FnvLIGHRecord),('MISC',FnvMISCRecord),
                        ('STAT',FnvSTATRecord),('SCOL',FnvSCOLRecord),('MSTT',FnvMSTTRecord),
                        ('PWAT',FnvPWATRecord),('GRAS',FnvGRASRecord),('TREE',FnvTREERecord),
                        ('FURN',FnvFURNRecord),('WEAP',FnvWEAPRecord),('AMMO',FnvAMMORecord),
                        ('NPC_',FnvNPC_Record),('CREA',FnvCREARecord),('LVLC',FnvLVLCRecord),
                        ('LVLN',FnvLVLNRecord),('KEYM',FnvKEYMRecord),('ALCH',FnvALCHRecord),
                        ('IDLM',FnvIDLMRecord),('NOTE',FnvNOTERecord),('COBJ',FnvCOBJRecord),
                        ('PROJ',FnvPROJRecord),('LVLI',FnvLVLIRecord),('WTHR',FnvWTHRRecord),
                        ('CLMT',FnvCLMTRecord),('REGN',FnvREGNRecord),('NAVI',FnvNAVIRecord),
                        ('CELL',FnvCELLRecord),('ACHR',FnvACHRRecord),('ACRE',FnvACRERecord),
                        ('REFR',FnvREFRRecord),('PGRE',FnvPGRERecord),('PMIS',FnvPMISRecord),
                        ('PBEA',FnvPBEARecord),('NAVM',FnvNAVMRecord),('WRLD',FnvWRLDRecord),
                        ('LAND',FnvLANDRecord),('DIAL',FnvDIALRecord),('INFO',FnvINFORecord),
                        ('QUST',FnvQUSTRecord),('IDLE',FnvIDLERecord),('PACK',FnvPACKRecord),
                        ('CSTY',FnvCSTYRecord),('LSCR',FnvLSCRRecord),('ANIO',FnvANIORecord),
                        ('WATR',FnvWATRRecord),('EFSH',FnvEFSHRecord),('EXPL',FnvEXPLRecord),
                        ('DEBR',FnvDEBRRecord),('IMGS',FnvIMGSRecord),('IMAD',FnvIMADRecord),
                        ('FLST',FnvFLSTRecord),('PERK',FnvPERKRecord),('BPTD',FnvBPTDRecord),
                        ('ADDN',FnvADDNRecord),('AVIF',FnvAVIFRecord),('RADS',FnvRADSRecord),
                        ('CAMS',FnvCAMSRecord),('CPTH',FnvCPTHRecord),('VTYP',FnvVTYPRecord),
                        ('IPCT',FnvIPCTRecord),('IPDS',FnvIPDSRecord),('ARMA',FnvARMARecord),
                        ('ECZN',FnvECZNRecord),('MESG',FnvMESGRecord),('RGDL',FnvRGDLRecord),
                        ('DOBJ',FnvDOBJRecord),('LGTM',FnvLGTMRecord),('MUSC',FnvMUSCRecord),
                        ('IMOD',FnvIMODRecord),('REPU',FnvREPURecord),('RCPE',FnvRCPERecord),
                        ('RCCT',FnvRCCTRecord),('CHIP',FnvCHIPRecord),('CSNO',FnvCSNORecord),
                        ('LSCT',FnvLSCTRecord),('MSET',FnvMSETRecord),('ALOC',FnvALOCRecord),
                        ('CHAL',FnvCHALRecord),('AMEF',FnvAMEFRecord),('CCRD',FnvCCRDRecord),
                        ('CMNY',FnvCMNYRecord),('CDCK',FnvCDCKRecord),('DEHY',FnvDEHYRecord),
                        ('HUNG',FnvHUNGRecord),('SLPD',FnvSLPDRecord),])

class FnvModFile(object):
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
            RecordType = fnv_type_record[_CGetFieldAttribute(RecordID, 0, 0, 0, 0, 0, 0, 0, 0).value]
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
            values = [fnv_type_record[_CGetFieldAttribute(x, 0, 0, 0, 0, 0, 0, 0, 0).value](x) for x in cRecords]
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
        return FnvTES4Record(_CGetRecordID(self._ModID, 0, 0))

    def create_GMST(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("GMST", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvGMSTRecord(RecordID) if RecordID else None
    GMST = CBashRECORDARRAY(FnvGMSTRecord, 'GMST')

    def create_TXST(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("TXST", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvTXSTRecord(RecordID) if RecordID else None
    TXST = CBashRECORDARRAY(FnvTXSTRecord, 'TXST')

    def create_MICN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("MICN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvMICNRecord(RecordID) if RecordID else None
    MICN = CBashRECORDARRAY(FnvMICNRecord, 'MICN')

    def create_GLOB(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("GLOB", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvGLOBRecord(RecordID) if RecordID else None
    GLOB = CBashRECORDARRAY(FnvGLOBRecord, 'GLOB')

    def create_CLAS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CLAS", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCLASRecord(RecordID) if RecordID else None
    CLAS = CBashRECORDARRAY(FnvCLASRecord, 'CLAS')

    def create_FACT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("FACT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvFACTRecord(RecordID) if RecordID else None
    FACT = CBashRECORDARRAY(FnvFACTRecord, 'FACT')

    def create_HDPT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("HDPT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvHDPTRecord(RecordID) if RecordID else None
    HDPT = CBashRECORDARRAY(FnvHDPTRecord, 'HDPT')

    def create_HAIR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("HAIR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvHAIRRecord(RecordID) if RecordID else None
    HAIR = CBashRECORDARRAY(FnvHAIRRecord, 'HAIR')

    def create_EYES(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("EYES", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvEYESRecord(RecordID) if RecordID else None
    EYES = CBashRECORDARRAY(FnvEYESRecord, 'EYES')

    def create_RACE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("RACE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvRACERecord(RecordID) if RecordID else None
    RACE = CBashRECORDARRAY(FnvRACERecord, 'RACE')

    def create_SOUN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SOUN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvSOUNRecord(RecordID) if RecordID else None
    SOUN = CBashRECORDARRAY(FnvSOUNRecord, 'SOUN')

    def create_ASPC(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ASPC", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvASPCRecord(RecordID) if RecordID else None
    ASPC = CBashRECORDARRAY(FnvASPCRecord, 'ASPC')

    def create_MGEF(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("MGEF", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvMGEFRecord(RecordID) if RecordID else None
    MGEF = CBashRECORDARRAY(FnvMGEFRecord, 'MGEF')

    def create_SCPT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SCPT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvSCPTRecord(RecordID) if RecordID else None
    SCPT = CBashRECORDARRAY(FnvSCPTRecord, 'SCPT')

    def create_LTEX(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LTEX", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvLTEXRecord(RecordID) if RecordID else None
    LTEX = CBashRECORDARRAY(FnvLTEXRecord, 'LTEX')

    def create_ENCH(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ENCH", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvENCHRecord(RecordID) if RecordID else None
    ENCH = CBashRECORDARRAY(FnvENCHRecord, 'ENCH')

    def create_SPEL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SPEL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvSPELRecord(RecordID) if RecordID else None
    SPEL = CBashRECORDARRAY(FnvSPELRecord, 'SPEL')

    def create_ACTI(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ACTI", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvACTIRecord(RecordID) if RecordID else None
    ACTI = CBashRECORDARRAY(FnvACTIRecord, 'ACTI')

    def create_TACT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("TACT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvTACTRecord(RecordID) if RecordID else None
    TACT = CBashRECORDARRAY(FnvTACTRecord, 'TACT')

    def create_TERM(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("TERM", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvTERMRecord(RecordID) if RecordID else None
    TERM = CBashRECORDARRAY(FnvTERMRecord, 'TERM')

    def create_ARMO(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ARMO", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvARMORecord(RecordID) if RecordID else None
    ARMO = CBashRECORDARRAY(FnvARMORecord, 'ARMO')

    def create_BOOK(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("BOOK", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvBOOKRecord(RecordID) if RecordID else None
    BOOK = CBashRECORDARRAY(FnvBOOKRecord, 'BOOK')

    def create_CONT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CONT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCONTRecord(RecordID) if RecordID else None
    CONT = CBashRECORDARRAY(FnvCONTRecord, 'CONT')

    def create_DOOR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("DOOR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvDOORRecord(RecordID) if RecordID else None
    DOOR = CBashRECORDARRAY(FnvDOORRecord, 'DOOR')

    def create_INGR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("INGR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvINGRRecord(RecordID) if RecordID else None
    INGR = CBashRECORDARRAY(FnvINGRRecord, 'INGR')

    def create_LIGH(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LIGH", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvLIGHRecord(RecordID) if RecordID else None
    LIGH = CBashRECORDARRAY(FnvLIGHRecord, 'LIGH')

    def create_MISC(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("MISC", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvMISCRecord(RecordID) if RecordID else None
    MISC = CBashRECORDARRAY(FnvMISCRecord, 'MISC')

    def create_STAT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("STAT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvSTATRecord(RecordID) if RecordID else None
    STAT = CBashRECORDARRAY(FnvSTATRecord, 'STAT')

    def create_SCOL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SCOL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvSCOLRecord(RecordID) if RecordID else None
    SCOL = CBashRECORDARRAY(FnvSCOLRecord, 'SCOL')

    def create_MSTT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("MSTT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvMSTTRecord(RecordID) if RecordID else None
    MSTT = CBashRECORDARRAY(FnvMSTTRecord, 'MSTT')

    def create_PWAT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("PWAT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvPWATRecord(RecordID) if RecordID else None
    PWAT = CBashRECORDARRAY(FnvPWATRecord, 'PWAT')

    def create_GRAS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("GRAS", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvGRASRecord(RecordID) if RecordID else None
    GRAS = CBashRECORDARRAY(FnvGRASRecord, 'GRAS')

    def create_TREE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("TREE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvTREERecord(RecordID) if RecordID else None
    TREE = CBashRECORDARRAY(FnvTREERecord, 'TREE')

    def create_FURN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("FURN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvFURNRecord(RecordID) if RecordID else None
    FURN = CBashRECORDARRAY(FnvFURNRecord, 'FURN')

    def create_WEAP(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("WEAP", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvWEAPRecord(RecordID) if RecordID else None
    WEAP = CBashRECORDARRAY(FnvWEAPRecord, 'WEAP')

    def create_AMMO(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("AMMO", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvAMMORecord(RecordID) if RecordID else None
    AMMO = CBashRECORDARRAY(FnvAMMORecord, 'AMMO')

    def create_NPC_(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("NPC_", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvNPC_Record(RecordID) if RecordID else None
    NPC_ = CBashRECORDARRAY(FnvNPC_Record, 'NPC_')

    def create_CREA(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CREA", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCREARecord(RecordID) if RecordID else None
    CREA = CBashRECORDARRAY(FnvCREARecord, 'CREA')

    def create_LVLC(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LVLC", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvLVLCRecord(RecordID) if RecordID else None
    LVLC = CBashRECORDARRAY(FnvLVLCRecord, 'LVLC')

    def create_LVLN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LVLN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvLVLNRecord(RecordID) if RecordID else None
    LVLN = CBashRECORDARRAY(FnvLVLNRecord, 'LVLN')

    def create_KEYM(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("KEYM", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvKEYMRecord(RecordID) if RecordID else None
    KEYM = CBashRECORDARRAY(FnvKEYMRecord, 'KEYM')

    def create_ALCH(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ALCH", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvALCHRecord(RecordID) if RecordID else None
    ALCH = CBashRECORDARRAY(FnvALCHRecord, 'ALCH')

    def create_IDLM(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("IDLM", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvIDLMRecord(RecordID) if RecordID else None
    IDLM = CBashRECORDARRAY(FnvIDLMRecord, 'IDLM')

    def create_NOTE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("NOTE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvNOTERecord(RecordID) if RecordID else None
    NOTE = CBashRECORDARRAY(FnvNOTERecord, 'NOTE')

    def create_COBJ(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("COBJ", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCOBJRecord(RecordID) if RecordID else None
    COBJ = CBashRECORDARRAY(FnvCOBJRecord, 'COBJ')

    def create_PROJ(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("PROJ", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvPROJRecord(RecordID) if RecordID else None
    PROJ = CBashRECORDARRAY(FnvPROJRecord, 'PROJ')

    def create_LVLI(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LVLI", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvLVLIRecord(RecordID) if RecordID else None
    LVLI = CBashRECORDARRAY(FnvLVLIRecord, 'LVLI')

    def create_WTHR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("WTHR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvWTHRRecord(RecordID) if RecordID else None
    WTHR = CBashRECORDARRAY(FnvWTHRRecord, 'WTHR')

    def create_CLMT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CLMT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCLMTRecord(RecordID) if RecordID else None
    CLMT = CBashRECORDARRAY(FnvCLMTRecord, 'CLMT')

    def create_REGN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("REGN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvREGNRecord(RecordID) if RecordID else None
    REGN = CBashRECORDARRAY(FnvREGNRecord, 'REGN')

    def create_NAVI(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("NAVI", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvNAVIRecord(RecordID) if RecordID else None
    NAVI = CBashRECORDARRAY(FnvNAVIRecord, 'NAVI')

    def create_CELL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CELL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCELLRecord(RecordID) if RecordID else None
    CELL = CBashRECORDARRAY(FnvCELLRecord, 'CELL')

    def create_WRLD(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("WRLD", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvWRLDRecord(RecordID) if RecordID else None
    WRLD = CBashRECORDARRAY(FnvWRLDRecord, 'WRLD')

    def create_DIAL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("DIAL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvDIALRecord(RecordID) if RecordID else None
    DIAL = CBashRECORDARRAY(FnvDIALRecord, 'DIAL')

    def create_QUST(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("QUST", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvQUSTRecord(RecordID) if RecordID else None
    QUST = CBashRECORDARRAY(FnvQUSTRecord, 'QUST')

    def create_IDLE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("IDLE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvIDLERecord(RecordID) if RecordID else None
    IDLE = CBashRECORDARRAY(FnvIDLERecord, 'IDLE')

    def create_PACK(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("PACK", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvPACKRecord(RecordID) if RecordID else None
    PACK = CBashRECORDARRAY(FnvPACKRecord, 'PACK')

    def create_CSTY(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CSTY", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCSTYRecord(RecordID) if RecordID else None
    CSTY = CBashRECORDARRAY(FnvCSTYRecord, 'CSTY')

    def create_LSCR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LSCR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvLSCRRecord(RecordID) if RecordID else None
    LSCR = CBashRECORDARRAY(FnvLSCRRecord, 'LSCR')

    def create_ANIO(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ANIO", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvANIORecord(RecordID) if RecordID else None
    ANIO = CBashRECORDARRAY(FnvANIORecord, 'ANIO')

    def create_WATR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("WATR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvWATRRecord(RecordID) if RecordID else None
    WATR = CBashRECORDARRAY(FnvWATRRecord, 'WATR')

    def create_EFSH(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("EFSH", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvEFSHRecord(RecordID) if RecordID else None
    EFSH = CBashRECORDARRAY(FnvEFSHRecord, 'EFSH')

    def create_EXPL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("EXPL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvEXPLRecord(RecordID) if RecordID else None
    EXPL = CBashRECORDARRAY(FnvEXPLRecord, 'EXPL')

    def create_DEBR(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("DEBR", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvDEBRRecord(RecordID) if RecordID else None
    DEBR = CBashRECORDARRAY(FnvDEBRRecord, 'DEBR')

    def create_IMGS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("IMGS", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvIMGSRecord(RecordID) if RecordID else None
    IMGS = CBashRECORDARRAY(FnvIMGSRecord, 'IMGS')

    def create_IMAD(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("IMAD", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvIMADRecord(RecordID) if RecordID else None
    IMAD = CBashRECORDARRAY(FnvIMADRecord, 'IMAD')

    def create_FLST(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("FLST", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvFLSTRecord(RecordID) if RecordID else None
    FLST = CBashRECORDARRAY(FnvFLSTRecord, 'FLST')

    def create_PERK(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("PERK", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvPERKRecord(RecordID) if RecordID else None
    PERK = CBashRECORDARRAY(FnvPERKRecord, 'PERK')

    def create_BPTD(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("BPTD", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvBPTDRecord(RecordID) if RecordID else None
    BPTD = CBashRECORDARRAY(FnvBPTDRecord, 'BPTD')

    def create_ADDN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ADDN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvADDNRecord(RecordID) if RecordID else None
    ADDN = CBashRECORDARRAY(FnvADDNRecord, 'ADDN')

    def create_AVIF(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("AVIF", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvAVIFRecord(RecordID) if RecordID else None
    AVIF = CBashRECORDARRAY(FnvAVIFRecord, 'AVIF')

    def create_RADS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("RADS", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvRADSRecord(RecordID) if RecordID else None
    RADS = CBashRECORDARRAY(FnvRADSRecord, 'RADS')

    def create_CAMS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CAMS", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCAMSRecord(RecordID) if RecordID else None
    CAMS = CBashRECORDARRAY(FnvCAMSRecord, 'CAMS')

    def create_CPTH(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CPTH", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCPTHRecord(RecordID) if RecordID else None
    CPTH = CBashRECORDARRAY(FnvCPTHRecord, 'CPTH')

    def create_VTYP(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("VTYP", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvVTYPRecord(RecordID) if RecordID else None
    VTYP = CBashRECORDARRAY(FnvVTYPRecord, 'VTYP')

    def create_IPCT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("IPCT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvIPCTRecord(RecordID) if RecordID else None
    IPCT = CBashRECORDARRAY(FnvIPCTRecord, 'IPCT')

    def create_IPDS(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("IPDS", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvIPDSRecord(RecordID) if RecordID else None
    IPDS = CBashRECORDARRAY(FnvIPDSRecord, 'IPDS')

    def create_ARMA(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ARMA", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvARMARecord(RecordID) if RecordID else None
    ARMA = CBashRECORDARRAY(FnvARMARecord, 'ARMA')

    def create_ECZN(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ECZN", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvECZNRecord(RecordID) if RecordID else None
    ECZN = CBashRECORDARRAY(FnvECZNRecord, 'ECZN')

    def create_MESG(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("MESG", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvMESGRecord(RecordID) if RecordID else None
    MESG = CBashRECORDARRAY(FnvMESGRecord, 'MESG')

    def create_RGDL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("RGDL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvRGDLRecord(RecordID) if RecordID else None
    RGDL = CBashRECORDARRAY(FnvRGDLRecord, 'RGDL')

    def create_DOBJ(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("DOBJ", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvDOBJRecord(RecordID) if RecordID else None
    DOBJ = CBashRECORDARRAY(FnvDOBJRecord, 'DOBJ')

    def create_LGTM(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LGTM", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvLGTMRecord(RecordID) if RecordID else None
    LGTM = CBashRECORDARRAY(FnvLGTMRecord, 'LGTM')

    def create_MUSC(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("MUSC", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvMUSCRecord(RecordID) if RecordID else None
    MUSC = CBashRECORDARRAY(FnvMUSCRecord, 'MUSC')

    def create_IMOD(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("IMOD", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvIMODRecord(RecordID) if RecordID else None
    IMOD = CBashRECORDARRAY(FnvIMODRecord, 'IMOD')

    def create_REPU(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("REPU", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvREPURecord(RecordID) if RecordID else None
    REPU = CBashRECORDARRAY(FnvREPURecord, 'REPU')

    def create_RCPE(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("RCPE", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvRCPERecord(RecordID) if RecordID else None
    RCPE = CBashRECORDARRAY(FnvRCPERecord, 'RCPE')

    def create_RCCT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("RCCT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvRCCTRecord(RecordID) if RecordID else None
    RCCT = CBashRECORDARRAY(FnvRCCTRecord, 'RCCT')

    def create_CHIP(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CHIP", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCHIPRecord(RecordID) if RecordID else None
    CHIP = CBashRECORDARRAY(FnvCHIPRecord, 'CHIP')

    def create_CSNO(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CSNO", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCSNORecord(RecordID) if RecordID else None
    CSNO = CBashRECORDARRAY(FnvCSNORecord, 'CSNO')

    def create_LSCT(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("LSCT", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvLSCTRecord(RecordID) if RecordID else None
    LSCT = CBashRECORDARRAY(FnvLSCTRecord, 'LSCT')

    def create_MSET(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("MSET", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvMSETRecord(RecordID) if RecordID else None
    MSET = CBashRECORDARRAY(FnvMSETRecord, 'MSET')

    def create_ALOC(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("ALOC", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvALOCRecord(RecordID) if RecordID else None
    ALOC = CBashRECORDARRAY(FnvALOCRecord, 'ALOC')

    def create_CHAL(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CHAL", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCHALRecord(RecordID) if RecordID else None
    CHAL = CBashRECORDARRAY(FnvCHALRecord, 'CHAL')

    def create_AMEF(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("AMEF", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvAMEFRecord(RecordID) if RecordID else None
    AMEF = CBashRECORDARRAY(FnvAMEFRecord, 'AMEF')

    def create_CCRD(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CCRD", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCCRDRecord(RecordID) if RecordID else None
    CCRD = CBashRECORDARRAY(FnvCCRDRecord, 'CCRD')

    def create_CMNY(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CMNY", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCMNYRecord(RecordID) if RecordID else None
    CMNY = CBashRECORDARRAY(FnvCMNYRecord, 'CMNY')

    def create_CDCK(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("CDCK", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvCDCKRecord(RecordID) if RecordID else None
    CDCK = CBashRECORDARRAY(FnvCDCKRecord, 'CDCK')

    def create_DEHY(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("DEHY", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvDEHYRecord(RecordID) if RecordID else None
    DEHY = CBashRECORDARRAY(FnvDEHYRecord, 'DEHY')

    def create_HUNG(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("HUNG", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvHUNGRecord(RecordID) if RecordID else None
    HUNG = CBashRECORDARRAY(FnvHUNGRecord, 'HUNG')

    def create_SLPD(self, EditorID=0, formID=FormID(None, None)):
        RecordID = _CCreateRecord(self._ModID, cast("SLPD", POINTER(c_ulong)).contents.value, formID.GetShortFormID(self), _encode(EditorID) if EditorID else EditorID, 0)
        return FnvSLPDRecord(RecordID) if RecordID else None
    SLPD = CBashRECORDARRAY(FnvSLPDRecord, 'SLPD')

    ##Aggregate properties. Useful for iterating through all records without going through the parent records.
    WorldCELLS = CBashRECORDARRAY(FnvCELLRecord, 'WCEL') ##"WCEL" is an artificial type CBash uses to distinguish World Cells
    CELLS = CBashRECORDARRAY(FnvCELLRecord, 'CLLS') ##"CLLS" is an artificial type CBash uses to distinguish all cells (includes WCEL)
    INFOS = CBashRECORDARRAY(FnvINFORecord, 'INFO')
    ACHRS = CBashRECORDARRAY(FnvACHRRecord, 'ACHR')
    ACRES = CBashRECORDARRAY(FnvACRERecord, 'ACRE')
    REFRS = CBashRECORDARRAY(FnvREFRRecord, 'REFR')
    PGRES = CBashRECORDARRAY(FnvPGRERecord, 'PGRE')
    PMISS = CBashRECORDARRAY(FnvPMISRecord, 'PMIS')
    PBEAS = CBashRECORDARRAY(FnvPBEARecord, 'PBEA')
    PFLAS = CBashRECORDARRAY(FnvPFLARecord, 'PFLA')
    PCBES = CBashRECORDARRAY(FnvPCBERecord, 'PCBE')
    NAVMS = CBashRECORDARRAY(FnvNAVMRecord, 'NAVM')
    LANDS = CBashRECORDARRAY(FnvLANDRecord, 'LAND')

    @property
    def tops(self):
        return dict((("GMST", self.GMST),("TXST", self.TXST),("MICN", self.MICN),
                     ("GLOB", self.GLOB),("CLAS", self.CLAS),("FACT", self.FACT),
                     ("HDPT", self.HDPT),("HAIR", self.HAIR),("EYES", self.EYES),
                     ("RACE", self.RACE),("SOUN", self.SOUN),("ASPC", self.ASPC),
                     ("MGEF", self.MGEF),("SCPT", self.SCPT),("LTEX", self.LTEX),
                     ("ENCH", self.ENCH),("SPEL", self.SPEL),("ACTI", self.ACTI),
                     ("TACT", self.TACT),("TERM", self.TERM),("ARMO", self.ARMO),
                     ("BOOK", self.BOOK),("CONT", self.CONT),("DOOR", self.DOOR),
                     ("INGR", self.INGR),("LIGH", self.LIGH),("MISC", self.MISC),
                     ("STAT", self.STAT),("SCOL", self.SCOL),("MSTT", self.MSTT),
                     ("PWAT", self.PWAT),("GRAS", self.GRAS),("TREE", self.TREE),
                     ("FURN", self.FURN),("WEAP", self.WEAP),("AMMO", self.AMMO),
                     ("NPC_", self.NPC_),("CREA", self.CREA),("LVLC", self.LVLC),
                     ("LVLN", self.LVLN),("KEYM", self.KEYM),("ALCH", self.ALCH),
                     ("IDLM", self.IDLM),("NOTE", self.NOTE),("COBJ", self.COBJ),
                     ("PROJ", self.PROJ),("LVLI", self.LVLI),("WTHR", self.WTHR),
                     ("CLMT", self.CLMT),("REGN", self.REGN),("NAVI", self.NAVI),
                     ("CELL", self.CELL),("WRLD", self.WRLD),("DIAL", self.DIAL),
                     ("QUST", self.QUST),("IDLE", self.IDLE),("PACK", self.PACK),
                     ("CSTY", self.CSTY),("LSCR", self.LSCR),("ANIO", self.ANIO),
                     ("WATR", self.WATR),("EFSH", self.EFSH),("EXPL", self.EXPL),
                     ("DEBR", self.DEBR),("IMGS", self.IMGS),("IMAD", self.IMAD),
                     ("FLST", self.FLST),("PERK", self.PERK),("BPTD", self.BPTD),
                     ("ADDN", self.ADDN),("AVIF", self.AVIF),("RADS", self.RADS),
                     ("CAMS", self.CAMS),("CPTH", self.CPTH),("VTYP", self.VTYP),
                     ("IPCT", self.IPCT),("IPDS", self.IPDS),("ARMA", self.ARMA),
                     ("ECZN", self.ECZN),("MESG", self.MESG),("RGDL", self.RGDL),
                     ("DOBJ", self.DOBJ),("LGTM", self.LGTM),("MUSC", self.MUSC),
                     ("IMOD", self.IMOD),("REPU", self.REPU),("RCPE", self.RCPE),
                     ("RCCT", self.RCCT),("CHIP", self.CHIP),("CSNO", self.CSNO),
                     ("LSCT", self.LSCT),("MSET", self.MSET),("ALOC", self.ALOC),
                     ("CHAL", self.CHAL),("AMEF", self.AMEF),("CCRD", self.CCRD),
                     ("CMNY", self.CMNY),("CDCK", self.CDCK),("DEHY", self.DEHY),
                     ("HUNG", self.HUNG),("SLPD", self.SLPD),))

    @property
    def aggregates(self):
        return dict((("GMST", self.GMST),("TXST", self.TXST),("MICN", self.MICN),
                     ("GLOB", self.GLOB),("CLAS", self.CLAS),("FACT", self.FACT),
                     ("HDPT", self.HDPT),("HAIR", self.HAIR),("EYES", self.EYES),
                     ("RACE", self.RACE),("SOUN", self.SOUN),("ASPC", self.ASPC),
                     ("MGEF", self.MGEF),("SCPT", self.SCPT),("LTEX", self.LTEX),
                     ("ENCH", self.ENCH),("SPEL", self.SPEL),("ACTI", self.ACTI),
                     ("TACT", self.TACT),("TERM", self.TERM),("ARMO", self.ARMO),
                     ("BOOK", self.BOOK),("CONT", self.CONT),("DOOR", self.DOOR),
                     ("INGR", self.INGR),("LIGH", self.LIGH),("MISC", self.MISC),
                     ("STAT", self.STAT),("SCOL", self.SCOL),("MSTT", self.MSTT),
                     ("PWAT", self.PWAT),("GRAS", self.GRAS),("TREE", self.TREE),
                     ("FURN", self.FURN),("WEAP", self.WEAP),("AMMO", self.AMMO),
                     ("NPC_", self.NPC_),("CREA", self.CREA),("LVLC", self.LVLC),
                     ("LVLN", self.LVLN),("KEYM", self.KEYM),("ALCH", self.ALCH),
                     ("IDLM", self.IDLM),("NOTE", self.NOTE),("COBJ", self.COBJ),
                     ("PROJ", self.PROJ),("LVLI", self.LVLI),("WTHR", self.WTHR),
                     ("CLMT", self.CLMT),("REGN", self.REGN),("NAVI", self.NAVI),
                     ("CELL", self.CELLS),("ACHR", self.ACHRS),("ACRE", self.ACRES),
                     ("REFR", self.REFRS),("PGRE", self.PGRES),("PMIS", self.PMISS),
                     ("PBEA", self.PBEAS),("PFLA", self.PFLAS),("PCBE", self.PCBES),
                     ("NAVM", self.NAVMS),("WRLD", self.WRLD),("LAND", self.LANDS),
                     ("DIAL", self.DIAL),("INFO", self.INFOS),
                     ("QUST", self.QUST),("IDLE", self.IDLE),("PACK", self.PACK),
                     ("CSTY", self.CSTY),("LSCR", self.LSCR),("ANIO", self.ANIO),
                     ("WATR", self.WATR),("EFSH", self.EFSH),("EXPL", self.EXPL),
                     ("DEBR", self.DEBR),("IMGS", self.IMGS),("IMAD", self.IMAD),
                     ("FLST", self.FLST),("PERK", self.PERK),("BPTD", self.BPTD),
                     ("ADDN", self.ADDN),("AVIF", self.AVIF),("RADS", self.RADS),
                     ("CAMS", self.CAMS),("CPTH", self.CPTH),("VTYP", self.VTYP),
                     ("IPCT", self.IPCT),("IPDS", self.IPDS),("ARMA", self.ARMA),
                     ("ECZN", self.ECZN),("MESG", self.MESG),("RGDL", self.RGDL),
                     ("DOBJ", self.DOBJ),("LGTM", self.LGTM),("MUSC", self.MUSC),
                     ("IMOD", self.IMOD),("REPU", self.REPU),("RCPE", self.RCPE),
                     ("RCCT", self.RCCT),("CHIP", self.CHIP),("CSNO", self.CSNO),
                     ("LSCT", self.LSCT),("MSET", self.MSET),("ALOC", self.ALOC),
                     ("CHAL", self.CHAL),("AMEF", self.AMEF),("CCRD", self.CCRD),
                     ("CMNY", self.CMNY),("CDCK", self.CDCK),("DEHY", self.DEHY),
                     ("HUNG", self.HUNG),("SLPD", self.SLPD),))
