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
from ctypes import CDLL, CFUNCTYPE, POINTER, byref, c_bool, c_char, c_char_p, c_float, \
    c_long, c_short, c_ubyte, c_ulong, cast, string_at
from os.path import exists, join

from ..bolt import CBash as CBashEnabled
from ..bolt import GPath, Path
from ..bolt import decode as _uni
from ..bolt import deprint
from ..bolt import encode as _enc
from .utils import ISTRING, IUNICODE, ExtractCopyList, SetCopyList, _encode, _unicode


class CBashError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def ZeroIsErrorCheck(result, function, cArguments, *args):
    if result == 0: raise CBashError("Function returned error code 0.")
    return result

def NegativeIsErrorCheck(result, function, cArguments, *args):
    if result < 0:
        raise CBashError("Function returned error code %i." % result)
    return result

def PositiveIsErrorCheck(result, function, cArguments, *args):
    if result > 0:
        raise CBashError("Function returned error code %i" % result)
    return result

_CBash = None
# Have to hardcode this relative to the cwd, because passing any non-unicode
# characters to CDLL tries to encode them as ASCII and crashes
# TODO(inf) fixed in py3, remove this on upgrade
cb_path = join(u'bash', u'compiled', u'CBash.dll')
if CBashEnabled != 1 and exists(cb_path):
    try:
        from ..env import get_file_version
        if get_file_version(cb_path) < (0, 7):
            raise ImportError(u'Bundled CBash version is too old for this '
                              u'Wrye Bash version. Only 0.7.0+ is '
                              u'supported.')
        _CBash = CDLL(cb_path)
    except (AttributeError, ImportError, OSError):
        _CBash = None
        deprint(u'Failed to import CBash.', traceback=True)
    except:
        _CBash = None
        raise

if _CBash:
    def LoggingCB(logString):
        print logString,
        return 0

    def RaiseCB(raisedString):
        #Raising is mostly worthless in a callback
        #CTypes prints the error, but the traceback is useless
        #and it doesn't propagate properly

        #Apparently...
        #"The standard way of doing something meaningful with the exception is
        #to catch it in the callback, set a global flag, somehow encourage the
        #C code to unwind back to the original Python call and there check the
        #flag and re-raise the exception."

        #But this would lead to a large performance hit if it were checked after
        #every CBash call. An alternative might be to start a separate thread
        #that then raises the error in the main thread after control returns from
        #CBash. Dunno.

        #This particular callback may disappear, or be morphed into something else
        print "CBash encountered an error", raisedString, "Check the log."
##        raise CBashError("Check the log.")
        return

    _CGetVersionMajor = _CBash.cb_GetVersionMajor
    _CGetVersionMinor = _CBash.cb_GetVersionMinor
    _CGetVersionRevision = _CBash.cb_GetVersionRevision
    _CGetVersionMajor.restype = c_ulong
    _CGetVersionMinor.restype = c_ulong
    _CGetVersionRevision.restype = c_ulong
    _CCreateCollection = _CBash.cb_CreateCollection
    _CCreateCollection.errcheck = ZeroIsErrorCheck
    _CDeleteCollection = _CBash.cb_DeleteCollection
    _CDeleteCollection.errcheck = NegativeIsErrorCheck
    _CLoadCollection = _CBash.cb_LoadCollection
    _CLoadCollection.errcheck = NegativeIsErrorCheck
    _CUnloadCollection = _CBash.cb_UnloadCollection
    _CUnloadCollection.errcheck = NegativeIsErrorCheck
    _CGetCollectionType = _CBash.cb_GetCollectionType
    _CGetCollectionType.errcheck = NegativeIsErrorCheck
    _CUnloadAllCollections = _CBash.cb_UnloadAllCollections
    _CUnloadAllCollections.errcheck = NegativeIsErrorCheck
    _CDeleteAllCollections = _CBash.cb_DeleteAllCollections
    _CDeleteAllCollections.errcheck = NegativeIsErrorCheck
    _CAddMod = _CBash.cb_AddMod
    _CAddMod.errcheck = ZeroIsErrorCheck
    _CLoadMod = _CBash.cb_LoadMod
    _CLoadMod.errcheck = NegativeIsErrorCheck
    _CUnloadMod = _CBash.cb_UnloadMod
    _CUnloadMod.errcheck = NegativeIsErrorCheck
    _CCleanModMasters = _CBash.cb_CleanModMasters
    _CCleanModMasters.errcheck = NegativeIsErrorCheck
    _CSaveMod = _CBash.cb_SaveMod
    _CSaveMod.errcheck = NegativeIsErrorCheck
    _CGetAllNumMods = _CBash.cb_GetAllNumMods
    _CGetAllModIDs = _CBash.cb_GetAllModIDs
    _CGetLoadOrderNumMods = _CBash.cb_GetLoadOrderNumMods
    _CGetLoadOrderModIDs = _CBash.cb_GetLoadOrderModIDs
    _CGetFileNameByID = _CBash.cb_GetFileNameByID
    _CGetFileNameByLoadOrder = _CBash.cb_GetFileNameByLoadOrder
    _CGetModNameByID = _CBash.cb_GetModNameByID
    _CGetModNameByLoadOrder = _CBash.cb_GetModNameByLoadOrder
    _CGetModIDByName = _CBash.cb_GetModIDByName
    _CGetModIDByLoadOrder = _CBash.cb_GetModIDByLoadOrder
    _CGetModLoadOrderByName = _CBash.cb_GetModLoadOrderByName
    _CGetModLoadOrderByID = _CBash.cb_GetModLoadOrderByID
    _CGetModIDByRecordID = _CBash.cb_GetModIDByRecordID
    _CGetCollectionIDByRecordID = _CBash.cb_GetCollectionIDByRecordID
    _CGetCollectionIDByModID = _CBash.cb_GetCollectionIDByModID
    _CIsModEmpty = _CBash.cb_IsModEmpty
    _CGetModNumTypes = _CBash.cb_GetModNumTypes
    _CGetModNumTypes.errcheck = NegativeIsErrorCheck
    _CGetModTypes = _CBash.cb_GetModTypes
    _CGetModTypes.errcheck = NegativeIsErrorCheck
    _CGetModNumEmptyGRUPs = _CBash.cb_GetModNumEmptyGRUPs
    _CGetModNumEmptyGRUPs.errcheck = NegativeIsErrorCheck
    _CGetModNumOrphans = _CBash.cb_GetModNumOrphans
    _CGetModNumOrphans.errcheck = NegativeIsErrorCheck
    _CGetModOrphansFormIDs = _CBash.cb_GetModOrphansFormIDs
    _CGetModOrphansFormIDs.errcheck = NegativeIsErrorCheck

    _CGetLongIDName = _CBash.cb_GetLongIDName
    _CMakeShortFormID = _CBash.cb_MakeShortFormID
    _CCreateRecord = _CBash.cb_CreateRecord
    _CCopyRecord = _CBash.cb_CopyRecord
    _CUnloadRecord = _CBash.cb_UnloadRecord
    _CResetRecord = _CBash.cb_ResetRecord
    _CDeleteRecord = _CBash.cb_DeleteRecord
    _CGetRecordID = _CBash.cb_GetRecordID
    _CGetNumRecords = _CBash.cb_GetNumRecords
    _CGetRecordIDs = _CBash.cb_GetRecordIDs
    _CIsRecordWinning = _CBash.cb_IsRecordWinning
    _CGetNumRecordConflicts = _CBash.cb_GetNumRecordConflicts
    _CGetRecordConflicts = _CBash.cb_GetRecordConflicts
    _CGetRecordHistory = _CBash.cb_GetRecordHistory
    _CGetNumIdenticalToMasterRecords = _CBash.cb_GetNumIdenticalToMasterRecords
    _CGetIdenticalToMasterRecords = _CBash.cb_GetIdenticalToMasterRecords
    _CIsRecordFormIDsInvalid = _CBash.cb_IsRecordFormIDsInvalid
    _CUpdateReferences = _CBash.cb_UpdateReferences
    _CGetRecordUpdatedReferences = _CBash.cb_GetRecordUpdatedReferences
    _CSetIDFields = _CBash.cb_SetIDFields
    _CSetField = _CBash.cb_SetField
    _CDeleteField = _CBash.cb_DeleteField
    _CGetFieldAttribute = _CBash.cb_GetFieldAttribute
    _CGetField = _CBash.cb_GetField

    _CCreateCollection.restype = c_ulong
    _CDeleteCollection.restype = c_long
    _CLoadCollection.restype = c_long
    _CUnloadCollection.restype = c_long
    _CGetCollectionType.restype = c_long
    _CUnloadAllCollections.restype = c_long
    _CDeleteAllCollections.restype = c_long
    _CAddMod.restype = c_ulong
    _CLoadMod.restype = c_long
    _CUnloadMod.restype = c_long
    _CCleanModMasters.restype = c_long
    _CSaveMod.restype = c_long
    _CGetAllNumMods.restype = c_long
    _CGetAllModIDs.restype = c_long
    _CGetLoadOrderNumMods.restype = c_long
    _CGetLoadOrderModIDs.restype = c_long
    _CGetFileNameByID.restype = c_char_p
    _CGetFileNameByLoadOrder.restype = c_char_p
    _CGetModNameByID.restype = c_char_p
    _CGetModNameByLoadOrder.restype = c_char_p
    _CGetModIDByName.restype = c_ulong
    _CGetModIDByLoadOrder.restype = c_ulong
    _CGetModLoadOrderByName.restype = c_long
    _CGetModLoadOrderByID.restype = c_long
    _CGetModIDByRecordID.restype = c_ulong
    _CGetCollectionIDByRecordID.restype = c_ulong
    _CGetCollectionIDByModID.restype = c_ulong
    _CIsModEmpty.restype = c_ulong
    _CGetModNumTypes.restype = c_long
    _CGetModTypes.restype = c_long
    _CGetModNumEmptyGRUPs.restype = c_long
    _CGetModNumOrphans.restype = c_long
    _CGetModOrphansFormIDs.restype = c_long
    _CGetLongIDName.restype = c_char_p
    _CMakeShortFormID.restype = c_ulong
    _CCreateRecord.restype = c_ulong
    _CCopyRecord.restype = c_ulong
    _CUnloadRecord.restype = c_long
    _CResetRecord.restype = c_long
    _CDeleteRecord.restype = c_long
    _CGetRecordID.restype = c_ulong
    _CGetNumRecords.restype = c_long
    _CGetRecordIDs.restype = c_long
    _CIsRecordWinning.restype = c_long
    _CGetNumRecordConflicts.restype = c_long
    _CGetRecordConflicts.restype = c_long
    _CGetRecordHistory.restype = c_long
    _CGetNumIdenticalToMasterRecords.restype = c_long
    _CGetIdenticalToMasterRecords.restype = c_long
    _CIsRecordFormIDsInvalid.restype = c_long
    _CUpdateReferences.restype = c_long
    _CGetRecordUpdatedReferences.restype = c_long
    _CSetIDFields.restype = c_long
    _CGetFieldAttribute.restype = c_ulong
    LoggingCallback = CFUNCTYPE(c_long, c_char_p)(LoggingCB)
    RaiseCallback = CFUNCTYPE(None, c_char_p)(RaiseCB)
    _CBash.cb_RedirectMessages(LoggingCallback)
    _CBash.cb_AllowRaising(RaiseCallback)

#Helper functions
class API_FIELDS(object):
    """These fields MUST be defined in the same order as in CBash's Common.h"""
    __slots__ = ['UNKNOWN', 'MISSING', 'JUNK', 'BOOL', 'SINT8', 'UINT8',
                 'SINT16', 'UINT16', 'SINT32', 'UINT32', 'FLOAT32', 'RADIAN',
                 'FORMID', 'MGEFCODE', 'ACTORVALUE', 'FORMID_OR_UINT32',
                 'FORMID_OR_FLOAT32', 'UINT8_OR_UINT32', 'FORMID_OR_STRING',
                 'UNKNOWN_OR_FORMID_OR_UINT32', 'UNKNOWN_OR_SINT32',
                 'UNKNOWN_OR_UINT32_FLAG', 'MGEFCODE_OR_CHAR4',
                 'FORMID_OR_MGEFCODE_OR_ACTORVALUE_OR_UINT32',
                 'RESOLVED_MGEFCODE', 'STATIC_MGEFCODE', 'RESOLVED_ACTORVALUE',
                 'STATIC_ACTORVALUE', 'CHAR', 'CHAR4', 'STRING', 'ISTRING',
                 'STRING_OR_FLOAT32_OR_SINT32', 'LIST', 'PARENTRECORD',
                 'SUBRECORD', 'SINT8_FLAG', 'SINT8_TYPE', 'SINT8_FLAG_TYPE',
                 'SINT8_ARRAY', 'UINT8_FLAG', 'UINT8_TYPE', 'UINT8_FLAG_TYPE',
                 'UINT8_ARRAY', 'SINT16_FLAG', 'SINT16_TYPE',
                 'SINT16_FLAG_TYPE', 'SINT16_ARRAY', 'UINT16_FLAG', 'UINT16_TYPE',
                 'UINT16_FLAG_TYPE', 'UINT16_ARRAY', 'SINT32_FLAG', 'SINT32_TYPE',
                 'SINT32_FLAG_TYPE', 'SINT32_ARRAY', 'UINT32_FLAG', 'UINT32_TYPE',
                 'UINT32_FLAG_TYPE', 'UINT32_ARRAY', 'FLOAT32_ARRAY',
                 'RADIAN_ARRAY', 'FORMID_ARRAY', 'FORMID_OR_UINT32_ARRAY',
                 'MGEFCODE_OR_UINT32_ARRAY', 'STRING_ARRAY', 'ISTRING_ARRAY',
                 'SUBRECORD_ARRAY', 'UNDEFINED']

for value, attr in enumerate(API_FIELDS.__slots__):
    setattr(API_FIELDS, attr, value)

class FormID(object):
    """Represents a FormID"""
    __slots__ = ['formID']

    class UnvalidatedFormID(object):
        """Represents an unchecked FormID. This the most common case by far.

        These occur when:
          1) A hard-coded Long FormID is used
          2) A Long FormID from a csv file is used
          3) Any CBash FormID is used

        It must be tested to see if it is safe for use in a particular
        collection. This class should never be instantiated except by class
        FormID(object)."""
        __slots__ = ['master','objectID']

        def __init__(self, master, objectID):
            self.master, self.objectID = master, objectID

        def __hash__(self):
            return hash((self.master, self.objectID))

        def __getitem__(self, x):
            return self.master if x == 0 else int(self.objectID & 0x00FFFFFFL)

        def __repr__(self):
            return u"UnvalidatedFormID('%s', 0x%06X)" % (self.master, int(self.objectID & 0x00FFFFFFL))

        def Validate(self, target):
            """Unvalidated FormIDs have to be tested for each destination
            collection. A FormID is valid if its master is part of the
            destination collection."""
            targetID = target.GetParentCollection()._CollectionID
            modID = _CGetModIDByName(targetID, _encode(self.master))
            return FormID.ValidFormID(self.master, self.objectID, _CMakeShortFormID(modID, self.objectID , 0), targetID) if modID else self

        def GetShortFormID(self, target):
            """Tries to resolve the formID for the given target. This should
            only get called if the FormID isn't validated prior to it being
            used by CBash."""
            formID = self.Validate(target)
            if isinstance(formID, FormID.ValidFormID): return formID.shortID
            raise TypeError(_("Attempted to set an invalid formID"))

    class InvalidFormID(object):
        """Represents an unsafe FormID. The FormIDs ModIndex won't properly
        match with the Collection's Load Order, so using it would cause the
        wrong record to become referenced.

        These occur when CBash is told to skip new records on loading a mod.
        This is most often done for scanned mods in Wrye Bash's Bashed Patch
        process.

        Invalid FormIDs are unsafe to use for any record in any collection.
        This class should never be instantiated except by class
        FormID(object)."""
        __slots__ = ['objectID']

        def __init__(self, objectID):
            self.objectID = objectID

        def __hash__(self):
            return hash((None, self.objectID))

        def __getitem__(self, x):
            return None if x == 0 else int(self.objectID & 0x00FFFFFFL)

        def __repr__(self):
            return "InvalidFormID(None, 0x%06X)" % (self.objectID,)

        def Validate(self, target):
            """No validation is needed. It's invalid."""
            return self

        def GetShortFormID(self, target):
            """It isn't safe to use this formID. Any attempt to resolve it will
            be wrong."""
            raise TypeError(_("Attempted to set an invalid formID"))

    class ValidFormID(object):
        """Represents a safe FormID.

        These occur when an unvalidated FormID is validated for a specific
        record. Technically, the validation is good for an entire
        collection, but it's rare for the same FormID instance to be used for
        multiple records.

        This class should never be instantiated except by class
        FormID(object)."""
        __slots__ = ['master','objectID','shortID','_CollectionID']

        def __init__(self, master, objectID, shortID, collectionID):
            self.master, self.objectID, self.shortID, self._CollectionID = master, objectID, shortID, collectionID

        def __hash__(self):
            return hash((self.master, self.objectID))

        def __getitem__(self, x):
            return self.master if x == 0 else int(self.objectID & 0x00FFFFFFL)

        def __repr__(self):
            return u"ValidFormID('%s', 0x%06X)" % (self.master, int(self.objectID & 0x00FFFFFFL))

        def Validate(self, target):
            """This FormID has already been validated for a specific
            collection. It must be revalidated if the target being used doesn't
            match the earlier validation."""
            return self if target.GetParentCollection()._CollectionID == self._CollectionID else FormID.UnvalidatedFormID(self.master, self.objectID).Validate(target)

        def GetShortFormID(self, target):
            """This FormID has already been resolved for a specific record.
            It must be re-resolved if the target being used doesn't match the
            earlier validation."""
            if target.GetParentCollection()._CollectionID == self._CollectionID: return self.shortID
            test = FormID.UnvalidatedFormID(self.master, self.objectID).Validate(target)
            if isinstance(test, FormID.ValidFormID): return test.shortID
            raise TypeError(_("Attempted to set an invalid formID"))

    class EmptyFormID(ValidFormID):
        """Represents an empty FormID.

        These occur when a particular field isn't set, or is set to 0.

        Empty FormIDs are safe to use for any record in any collection. This
        class should never be instantiated except by class FormID(object)."""
        __slots__ = []

        def __init__(self):
            pass

        def __hash__(self):
            return hash(0)

        def __getitem__(self, x):
            return None

        def __repr__(self):
            return "EmptyFormID(None, None)"

        def Validate(self, target):
            """No validation is needed. There's nothing to validate."""
            return self

        def GetShortFormID(self, target):
            """An empty FormID is always valid, so it isn't resolved. That's why it subclasses ValidFormID."""
            return None

    class RawFormID(ValidFormID):
        """Represents a non-checkable FormID. Should rarely be used due to
        safety issues. This class should never be instantiated except by class
        FormID(object)."""
        __slots__ = ['shortID']

        def __init__(self, shortID):
            self.shortID = shortID

        def __hash__(self):
            return hash((self.shortID, None))

        def __getitem__(self, x):
            return self.shortID >> 24 if x == 0 else int(self.shortID & 0x00FFFFFFL)

        def __repr__(self):
            return "RawFormID(0x%08X)" % (self.shortID,)

        def Validate(self, target):
            """No validation is possible. It is impossible to tell what
            collection the value came from."""
            return self

        def GetShortFormID(self, target):
            """The raw FormID isn't resolved, so it's always valid. That's why
            it subclasses ValidFormID."""
            return self.shortID

    def __init__(self, master, objectID=None):
        """Initializes a FormID from these possible inputs:

            - CBash FormID = (int(RecordID)   , int(FormID))
              [Internal use by CBash / cint only!]
            - Long FormID  = (string(ModName) , int(ObjectID))
            - FormID       = (FormID()        , None)
            - Raw FormID   = (int(FormID)     , None)
            - Empty FormID = (None            , None)"""
        self.formID = FormID.EmptyFormID() if master is None else master.formID if isinstance(master, FormID) else FormID.RawFormID(master) if objectID is None else FormID.UnvalidatedFormID(GPath(master), objectID) if isinstance(master, (basestring, Path)) else None
        if self.formID is None:
            masterstr = _CGetLongIDName(master, objectID, 0)
            self.formID = FormID.ValidFormID(GPath(masterstr), objectID, objectID, _CGetCollectionIDByRecordID(master)) if masterstr else FormID.InvalidFormID(objectID)

    def __hash__(self):
        return hash(self.formID)

    def __eq__(self, other):
        if other is None and isinstance(self.formID, FormID.EmptyFormID): return True
        try: return other[1] == self.formID[1] and other[0] == self.formID[0]
        except TypeError: return False

    def __ne__(self, other):
        try: return other[1] != self.formID[1] or other[0] != self.formID[0]
        except TypeError: return False

    def __nonzero__(self):
        return not isinstance(self.formID, (FormID.EmptyFormID, FormID.InvalidFormID))

    def __getitem__(self, x):
        return self.formID[0] if x == 0 else self.formID[1]

    def __setitem__(self, x, nValue):
        if x == 0: self.formID = FormID.EmptyFormID() if nValue is None else FormID.UnvalidatedFormID(nValue, self.formID[1]) if isinstance(nValue, basestring) else FormID.RawFormID(nValue)
        else: self.formID = FormID.UnvalidatedFormID(self.formID[0], nValue) if nValue is not None else FormID.EmptyFormID() if self.formID[0] is None else FormID.RawFormID(self.formID[0])

    def __len__(self):
        return 2

    def __repr__(self):
        return self.formID.__repr__()

    def __str__(self):
        return self.formID.__repr__()

    @staticmethod
    def FilterValid(formIDs, target, AsShort=False):
        if AsShort: return [x.GetShortFormID(target) for x in formIDs if x.ValidateFormID(target)]
        return [x for x in formIDs if x.ValidateFormID(target)]

    @staticmethod
    def FilterValidDict(formIDs, target, KeysAreFormIDs, ValuesAreFormIDs, AsShort=False):
        if KeysAreFormIDs:
            if ValuesAreFormIDs:
                if AsShort: return dict([(key.GetShortFormID(target), value.GetShortFormID(target)) for key, value in formIDs.iteritems() if key.ValidateFormID(target) and value.ValidateFormID(target)])
                return dict([(key, value) for key, value in formIDs.iteritems() if key.ValidateFormID(target) and value.ValidateFormID(target)])
            if AsShort: return dict([(key.GetShortFormID(target), value) for key, value in formIDs.iteritems() if key.ValidateFormID(target)])
            return dict([(key, value) for key, value in formIDs.iteritems() if key.ValidateFormID(target)])
        if ValuesAreFormIDs:
            if AsShort: return dict([(key, value.GetShortFormID(target)) for key, value in formIDs.iteritems() if value.ValidateFormID(target)])
            return dict([(key, value) for key, value in formIDs.iteritems() if value.ValidateFormID(target)])
        return formIDs

    def ValidateFormID(self, target):
        """Tests whether the FormID is valid for the destination.
        The test result is saved, so work isn't duplicated if FormIDs are first
        filtered for validity before being set by CBash with GetShortFormID."""
        self.formID = self.formID.Validate(target)
        return isinstance(self.formID, FormID.ValidFormID)

    def GetShortFormID(self, target):
        """Resolves the various FormID classes to a single 32-bit value used by
        CBash"""
        return self.formID.GetShortFormID(target)

class ActorValue(object):
    """Represents an OBME ActorValue. It is mostly identical to a FormID in
    resolution. The difference lays in that it is only resolved if the value is
    >= 0x800"""
    __slots__ = ['actorValue']

    class UnvalidatedActorValue(object):
        __slots__ = ['master','objectID']
        """Represents an unchecked ActorValue. This the most common case by far.

           These occur when:
            1) A hard-coded Long ActorValue is used
            2) A Long ActorValue from a csv file is used
            3) Any CBash ActorValue is used

           It must be tested to see if it is safe for use in a particular collection.
           This class should never be instantiated except by class ActorValue(object)."""
        def __init__(self, master, objectID):
            self.master, self.objectID = master, objectID

        def __hash__(self):
            return hash((self.master, self.objectID))

        def __getitem__(self, x):
            return self.master if x == 0 else int(self.objectID & 0x00FFFFFFL)

        def __repr__(self):
            return u"UnvalidatedActorValue('%s', 0x%06X)" % (self.master, int(self.objectID & 0x00FFFFFFL))

        def Validate(self, target):
            """Unvalidated ActorValues have to be tested for each destination collection.
               A ActorValue is valid if its master is part of the destination collection.

               Resolved Actor Value's are not formIDs, but can be treated as such for resolution."""
            targetID = target.GetParentCollection()._CollectionID
            modID = _CGetModIDByName(targetID, _encode(self.master))
            return ActorValue.ValidActorValue(self.master, self.objectID, _CMakeShortFormID(modID, self.objectID , 0), targetID) if modID else self

        def GetShortActorValue(self, target):
            """Tries to resolve the ActorValue for the given record.
               This should only get called if the ActorValue isn't validated prior to it being used by CBash."""
            actorValue = self.Validate(target)
            if isinstance(actorValue, ActorValue.ValidActorValue): return actorValue.shortID
            raise TypeError(_("Attempted to set an invalid actorValue"))

    class InvalidActorValue(object):
        __slots__ = ['objectID']
        """Represents an unsafe ActorValue.
           The ActorValues ModIndex won't properly match with the Collection's Load Order,
           so using it would cause the wrong record to become referenced.

           These occur when CBash is told to skip new records on loading a mod.
           This is most often done for scanned mods in Wrye Bash's Bashed Patch process.

           Invalid ActorValues are unsafe to use for any record in any collection.
           This class should never be instantiated except by class ActorValue(object)."""
        def __init__(self, objectID):
            self.objectID = objectID

        def __hash__(self):
            return hash((None, self.objectID))

        def __getitem__(self, x):
            return None if x == 0 else int(self.objectID & 0x00FFFFFFL)

        def __repr__(self):
            return "InvalidActorValue(None, 0x%06X)" % (self.objectID,)

        def Validate(self, target):
            """No validation is needed. It's invalid."""
            return self

        def GetShortActorValue(self, target):
            """It isn't safe to use this ActorValue. Any attempt to resolve it will be wrong."""
            raise TypeError(_("Attempted to set an invalid actorValue"))

    class ValidActorValue(object):
        __slots__ = ['master','objectID','shortID','_CollectionID']
        """Represents a safe ActorValue.

           These occur when an unvalidated ActorValue is validated for a specific record.
           Technically, the validation is good for an entire collection, but it's rare
           for the same ActorValue instance to be used for multiple records.

           This class should never be instantiated except by class ActorValue(object)."""
        def __init__(self, master, objectID, shortID, collectionID):
            self.master, self.objectID, self.shortID, self._CollectionID = master, objectID, shortID, collectionID

        def __hash__(self):
            return hash((self.master, self.objectID))

        def __getitem__(self, x):
            return self.master if x == 0 else int(self.objectID & 0x00FFFFFFL)

        def __repr__(self):
            return u"ValidActorValue('%s', 0x%06X)" % (self.master, int(self.objectID & 0x00FFFFFFL))

        def Validate(self, target):
            """This ActorValue has already been validated for a specific record.
               It must be revalidated if the record being used doesn't match the earlier validation."""
            return self if target.GetParentCollection()._CollectionID == self._CollectionID else ActorValue.UnvalidatedActorValue(self.master, self.objectID).Validate(target)

        def GetShortActorValue(self, target):
            """This ActorValue has already been resolved for a specific record.
               It must be re-resolved if the record being used doesn't match the earlier validation."""
            if target.GetParentCollection()._CollectionID == self._CollectionID: return self.shortID
            test = ActorValue.UnvalidatedActorValue(self.master, self.objectID).Validate(target)
            if isinstance(test, ActorValue.ValidActorValue): return test.shortID
            raise TypeError(_("Attempted to set an invalid actorValue"))

    class EmptyActorValue(ValidActorValue):
        __slots__ = []
        """Represents an empty ActorValue.

           These occur when a particular field isn't set, or is set to 0.

           Empty ActorValues are safe to use for any record in any collection.
           This class should never be instantiated except by class ActorValue(object)."""
        def __init__(self):
            pass

        def __hash__(self):
            return hash(0)

        def __getitem__(self, x):
            return None

        def __repr__(self):
            return "EmptyActorValue(None, None)"

        def Validate(self, target):
            """No validation is needed. There's nothing to validate."""
            return self

        def GetShortActorValue(self, target):
            """An empty ActorValue isn't resolved, because it's always valid. That's why it subclasses ValidActorValue."""
            return None

    class RawActorValue(ValidActorValue):
        __slots__ = ['shortID']
        """Represents a non-checked ActorValue. It is either a static ActorValue, or a non-checkable ActorValue.
           Raw ActorValues < 0x800 (static) are safe since they aren't resolved,
           but raw values >= 0x800 should rarely be used due to safety issues.
           This class should never be instantiated except by class ActorValue(object)."""

        def __init__(self, shortID):
            self.shortID = shortID

        def __hash__(self):
            return hash((self.shortID, None))

        def __getitem__(self, x):
            return self.shortID >> 24 if x == 0 else int(self.shortID & 0x00FFFFFFL)

        def __repr__(self):
            return "RawActorValue(0x%08X)" % (self.shortID,)

        def Validate(self, target):
            """No validation is possible. It is impossible to tell what collection the value came from."""
            return self

        def GetShortActorValue(self, target):
            """The raw ActorValue isn't resolved, so it's always valid. That's why it subclasses ValidActorValue."""
            return self.shortID

    def __init__(self, master, objectID=None):
        """Initializes an OBME ActorValue from these possible inputs:
           CBash ActorValue  = (int(RecordID)   , int(ActorValue)) Internal use by CBash / cint only!
           Long ActorValue   = (string(ModName) , int(ObjectID))
           ActorValue        = (ActorValue()    , None)
           Raw ActorValue    = (int(ActorValue) , None)
           Empty ActorValue  = (None            , None))"""
        self.actorValue = ActorValue.EmptyActorValue() if master is None else master.actorValue if isinstance(master, ActorValue) else ActorValue.RawActorValue(master) if objectID is None else ActorValue.UnvalidatedActorValue(GPath(master), objectID) if isinstance(master, (basestring, Path)) else ActorValue.RawActorValue(objectID) if objectID < 0x800 else None
        if self.actorValue is None:
            masterstr = _CGetLongIDName(master, objectID, 0)
            self.actorValue = ActorValue.ValidActorValue(GPath(masterstr), objectID, objectID, _CGetCollectionIDByRecordID(master)) if masterstr else ActorValue.InvalidActorValue(objectID)

    def __hash__(self):
        return hash(self.actorValue)

    def __eq__(self, other):
        if other is None and isinstance(self.actorValue, ActorValue.EmptyActorValue): return True
        try: return other[1] == self.actorValue[1] and other[0] == self.actorValue[0]
        except TypeError: return False

    def __ne__(self, other):
        try: return other[1] != self.actorValue[1] or other[0] != self.actorValue[0]
        except TypeError: return False

    def __nonzero__(self):
        return not isinstance(self.actorValue, (ActorValue.EmptyActorValue, ActorValue.InvalidActorValue))

    def __getitem__(self, x):
        return self.actorValue[0] if x == 0 else self.actorValue[1]

    def __setitem__(self, x, nValue):
        if x == 0: self.actorValue = ActorValue.EmptyActorValue() if nValue is None else ActorValue.UnvalidatedActorValue(nValue, self.actorValue[1]) if isinstance(nValue, basestring) else ActorValue.RawActorValue(nValue)
        else:
            if nValue is None: self.actorValue = ActorValue.EmptyActorValue() if self.actorValue[0] is None else ActorValue.RawActorValue(self.actorValue[0])
            else: self.actorValue = ActorValue.RawActorValue(nValue) if nValue < 0x800 else ActorValue.UnvalidatedActorValue(self.actorValue[0], nValue)

    def __len__(self):
        return 2

    def __repr__(self):
        return self.actorValue.__repr__()

    def __str__(self):
        return self.actorValue.__repr__()

    @staticmethod
    def FilterValid(ActorValues, target, AsShort=False):
        if AsShort: return [x.GetShortActorValue(target) for x in ActorValues if x.ValidateActorValue(target)]
        return [x for x in ActorValues if x.ValidateActorValue(target)]

    @staticmethod
    def FilterValidDict(ActorValues, target, KeysAreActorValues, ValuesAreActorValues, AsShort=False):
        if KeysAreActorValues:
            if ValuesAreActorValues:
                if AsShort: return dict([(key.GetShortActorValue(target), value.GetShortFormID(target)) for key, value in ActorValues.iteritems() if key.ValidateActorValue(target) and value.ValidateActorValue(target)])
                return dict([(key, value) for key, value in ActorValues.iteritems() if key.ValidateActorValue(target) and value.ValidateActorValue(target)])
            if AsShort: return dict([(key.GetShortActorValue(target), value) for key, value in ActorValues.iteritems() if key.ValidateActorValue(target)])
            return dict([(key, value) for key, value in ActorValues.iteritems() if key.ValidateActorValue(target)])
        if ValuesAreActorValues:
            if AsShort: return dict([(key, value.GetShortActorValue(target)) for key, value in ActorValues.iteritems() if value.ValidateActorValue(target)])
            return dict([(key, value) for key, value in ActorValues.iteritems() if value.ValidateActorValue(target)])
        return ActorValues

    def ValidateActorValue(self, target):
        """Tests whether the ActorValue is valid for the destination target.
           The test result is saved, so work isn't duplicated if ActorValues are first
           filtered for validity before being set by CBash with GetShortActorValue."""
        self.actorValue = self.actorValue.Validate(target)
        return isinstance(self.actorValue, ActorValue.ValidActorValue)

    def GetShortActorValue(self, target):
        """Resolves the various ActorValue classes to a single 32-bit value used by CBash"""
        return self.actorValue.GetShortActorValue(target)

class MGEFCode(object):
    __slots__ = ['mgefCode']
    """Represents an OBME MGEFCode. It is mostly identical to a FormID in resolution.
       The difference lay in that it is only resolved if the value is >= 0x80000000,
       and that the ModIndex is in the lower bits."""

    class UnvalidatedMGEFCode(object):
        __slots__ = ['master','objectID']
        """Represents an unchecked MGEFCode. This the most common case by far.

           These occur when:
            1) A hard-coded Long MGEFCode is used
            2) A Long MGEFCode from a csv file is used
            3) Any CBash MGEFCode is used

           It must be tested to see if it is safe for use in a particular collection.
           This class should never be instantiated except by class MGEFCode(object)."""
        def __init__(self, master, objectID):
            self.master, self.objectID = master, objectID

        def __hash__(self):
            return hash((self.master, self.objectID))

        def __getitem__(self, x):
            return self.master if x == 0 else int(self.objectID & 0xFFFFFF00L)

        def __repr__(self):
            return u"UnvalidatedMGEFCode('%s', 0x%06X)" % (self.master, int(self.objectID & 0xFFFFFF00L))

        def Validate(self, target):
            """Unvalidated MGEFCodes have to be tested for each destination collection.
               A MGEFCode is valid if its master is part of the destination collection.

               Resolved MGEFCode's are not formIDs, but can be treated as such for resolution."""
            targetID = target.GetParentCollection()._CollectionID
            modID = _CGetModIDByName(targetID, _encode(self.master))
            return MGEFCode.ValidMGEFCode(self.master, self.objectID, _CMakeShortFormID(modID, self.objectID , 1), targetID) if modID else self

        def GetShortMGEFCode(self, target):
            """Tries to resolve the MGEFCode for the given record.
               This should only get called if the MGEFCode isn't validated prior to it being used by CBash."""
            mgefCode = self.Validate(target)
            if isinstance(mgefCode, MGEFCode.ValidMGEFCode): return mgefCode.shortID
            raise TypeError(_("Attempted to set an invalid mgefCode"))

    class InvalidMGEFCode(object):
        __slots__ = ['objectID']
        """Represents an unsafe MGEFCode.
           The MGEFCodes ModIndex won't properly match with the Collection's Load Order,
           so using it would cause the wrong record to become referenced.

           These occur when CBash is told to skip new records on loading a mod.
           This is most often done for scanned mods in Wrye Bash's Bashed Patch process.

           Invalid MGEFCodes are unsafe to use for any record in any collection.
           This class should never be instantiated except by class MGEFCode(object)."""
        def __init__(self, objectID):
            self.objectID = objectID

        def __hash__(self):
            return hash((None, self.objectID))

        def __getitem__(self, x):
            return None if x == 0 else int(self.objectID & 0xFFFFFF00L)

        def __repr__(self):
            return "InvalidMGEFCode(None, 0x%06X)" % (self.objectID,)

        def Validate(self, target):
            """No validation is needed. It's invalid."""
            return self

        def GetShortMGEFCode(self, target):
            """It isn't safe to use this MGEFCode. Any attempt to resolve it will be wrong."""
            raise TypeError(_("Attempted to set an invalid mgefCode"))

    class ValidMGEFCode(object):
        __slots__ = ['master','objectID','shortID','_CollectionID']
        """Represents a safe MGEFCode.

           These occur when an unvalidated MGEFCode is validated for a specific record.
           Technically, the validation is good for an entire collection, but it's rare
           for the same MGEFCode instance to be used for multiple records.

           This class should never be instantiated except by class MGEFCode(object)."""
        def __init__(self, master, objectID, shortID, collectionID):
            self.master, self.objectID, self.shortID, self._CollectionID = master, objectID, shortID, collectionID

        def __hash__(self):
            return hash((self.master, self.objectID))

        def __getitem__(self, x):
            return self.master if x == 0 else int(self.objectID & 0xFFFFFF00L)

        def __repr__(self):
            return u"ValidMGEFCode('%s', 0x%06X)" % (self.master, int(self.objectID & 0xFFFFFF00L))

        def Validate(self, target):
            """This MGEFCode has already been validated for a specific record.
               It must be revalidated if the record being used doesn't match the earlier validation."""
            return self if target.GetParentCollection()._CollectionID == self._CollectionID else MGEFCode.UnvalidatedMGEFCode(self.master, self.objectID).Validate(target)

        def GetShortMGEFCode(self, target):
            """This MGEFCode has already been resolved for a specific record.
               It must be re-resolved if the record being used doesn't match the earlier validation."""
            if target.GetParentCollection()._CollectionID == self._CollectionID: return self.shortID
            test = MGEFCode.UnvalidatedMGEFCode(self.master, self.objectID).Validate(target)
            if isinstance(test, MGEFCode.ValidMGEFCode): return test.shortID
            raise TypeError(_("Attempted to set an invalid mgefCode"))

    class EmptyMGEFCode(ValidMGEFCode):
        __slots__ = []
        """Represents an empty MGEFCode.

           These occur when a particular field isn't set, or is set to 0.

           Empty MGEFCodes are safe to use for any record in any collection.
           This class should never be instantiated except by class MGEFCode(object)."""
        def __init__(self):
            pass

        def __hash__(self):
            return hash(0)

        def __getitem__(self, x):
            return None

        def __repr__(self):
            return "EmptyMGEFCode(None, None)"

        def Validate(self, target):
            """No validation is needed. There's nothing to validate."""
            return self

        def GetShortMGEFCode(self, target):
            """An empty MGEFCode isn't resolved, because it's always valid. That's why it subclasses ValidMGEFCode."""
            return None

    class RawMGEFCode(ValidMGEFCode):
        __slots__ = ['shortID']
        """Represents a non-checked MGEFCode. It is either a static MGEFCode, or a non-checkable MGEFCode.
           Raw MGEFCodes < 0x80000000 (static) are safe since they aren't resolved,
           but raw values >= 0x80000000 should rarely be used due to safety issues.

           Without OBME, all MGEFCodes may be displayed as a 4 character sequence.
           Ex: SEFF for Script Effect

           This class should never be instantiated except by class MGEFCode(object)."""

        def __init__(self, shortID):
            self.shortID = (str(shortID) if isinstance(shortID,ISTRING)
                            else _encode(shortID) if isinstance(shortID,unicode)
                            else shortID)

        def __hash__(self):
            return hash((self.shortID, None))

        def __getitem__(self, x):
            return self.shortID if isinstance(self.shortID, basestring) else self.shortID >> 24 if x == 0 else int(self.shortID & 0xFFFFFF00L)

        def __repr__(self):
            return "RawMGEFCode(%s)" % (self.shortID,) if isinstance(self.shortID, basestring) else "RawMGEFCode(0x%08X)" % (self.shortID,)

        def Validate(self, target):
            """No validation is possible. It is impossible to tell what collection the value came from."""
            return self

        def GetShortMGEFCode(self, target):
            """The raw MGEFCode isn't resolved, so it's always valid. That's why it subclasses ValidMGEFCode.
               If it is using a 4 character sequence, it needs to be cast as a 32 bit integer."""
            return cast(self.shortID, POINTER(c_ulong)).contents.value if isinstance(self.shortID, basestring) else self.shortID

    def __init__(self, master, objectID=None):
        """Initializes an OBME MGEFCode from these possible inputs:
           CBash MGEFCode     = (int(RecordID)   , int(MGEFCode)) Internal use by CBash / cint only!
           CBash Raw MGEFCode = (int(RecordID)   , string(MGEFCode)) Internal use by CBash / cint only!
           Long MGEFCode      = (string(ModName) , int(ObjectID))
           MGEFCode           = (MGEFCode()      , None)
           Raw MGEFCode       = (int(MGEFCode)   , None)
           Raw MGEFCode       = (string(MGEFCode), None)
           Empty MGEFCode     = (None            , None))"""
        self.mgefCode = MGEFCode.EmptyMGEFCode() if master is None else master.mgefCode if isinstance(master, MGEFCode) else MGEFCode.RawMGEFCode(master) if objectID is None else MGEFCode.RawMGEFCode(objectID) if isinstance(objectID, basestring) else MGEFCode.UnvalidatedMGEFCode(GPath(master), objectID) if isinstance(master, (basestring, Path)) else MGEFCode.RawMGEFCode(objectID) if objectID < 0x80000000 else None
        if self.mgefCode is None:
            masterstr = _CGetLongIDName(master, objectID, 1)
            self.mgefCode = MGEFCode.ValidMGEFCode(GPath(masterstr), objectID, objectID, _CGetCollectionIDByRecordID(master)) if masterstr else MGEFCode.InvalidMGEFCode(objectID)

    def __hash__(self):
        return hash(self.mgefCode)

    def __eq__(self, other):
        if other is None and isinstance(self.mgefCode, MGEFCode.EmptyMGEFCode): return True
        try: return other[1] == self.mgefCode[1] and other[0] == self.mgefCode[0]
        except TypeError: return False

    def __ne__(self, other):
        return other[1] != self.mgefCode[1] or other[0] != self.mgefCode[0]

    def __nonzero__(self):
        return not isinstance(self.mgefCode, (MGEFCode.EmptyMGEFCode, MGEFCode.InvalidMGEFCode))

    def __getitem__(self, x):
        return self.mgefCode[0] if x == 0 else self.mgefCode[1]

    def __setitem__(self, x, nValue):
        if x == 0: self.mgefCode = MGEFCode.EmptyMGEFCode() if nValue is None else MGEFCode.UnvalidatedMGEFCode(nValue, self.mgefCode[1]) if isinstance(nValue, basestring) else MGEFCode.RawMGEFCode(nValue)
        else:
            if nValue is None: self.mgefCode = MGEFCode.EmptyMGEFCode() if self.mgefCode[0] is None else MGEFCode.RawMGEFCode(self.mgefCode[0])
            else: self.mgefCode = MGEFCode.RawMGEFCode(nValue) if nValue < 0x80000000 else MGEFCode.UnvalidatedMGEFCode(self.mgefCode[0], nValue)

    def __len__(self):
        return 2

    def __repr__(self):
        return self.mgefCode.__repr__()

    def __str__(self):
        return self.mgefCode.__repr__()

    @staticmethod
    def FilterValid(mgefCodes, target, AsShort=False):
        if AsShort: return [x.GetShortMGEFCode(target) for x in mgefCodes if x.ValidateMGEFCode(target)]
        return [x for x in mgefCodes if x.ValidateMGEFCode(target)]

    @staticmethod
    def FilterValidDict(mgefCodes, target, KeysAreMGEFCodes, ValuesAreMGEFCodes, AsShort=False):
        if KeysAreMGEFCodes:
            if ValuesAreMGEFCodes:
                if AsShort: return dict([(key.GetShortMGEFCode(target), value.GetShortFormID(target)) for key, value in mgefCodes.iteritems() if key.ValidateMGEFCode(target) and value.ValidateMGEFCode(target)])
                return dict([(key, value) for key, value in mgefCodes.iteritems() if key.ValidateMGEFCode(target) and value.ValidateMGEFCode(target)])
            if AsShort: return dict([(key.GetShortMGEFCode(target), value) for key, value in mgefCodes.iteritems() if key.ValidateMGEFCode(target)])
            return dict([(key, value) for key, value in mgefCodes.iteritems() if key.ValidateMGEFCode(target)])
        if ValuesAreMGEFCodes:
            if AsShort: return dict([(key, value.GetShortMGEFCode(target)) for key, value in mgefCodes.iteritems() if value.ValidateMGEFCode(target)])
            return dict([(key, value) for key, value in mgefCodes.iteritems() if value.ValidateMGEFCode(target)])
        return mgefCodes

    def ValidateMGEFCode(self, target):
        """Tests whether the MGEFCode is valid for the destination RecordID.
           The test result is saved, so work isn't duplicated if MGEFCodes are first
           filtered for validity before being set by CBash with GetShortMGEFCode."""
        self.mgefCode = self.mgefCode.Validate(target)
        return isinstance(self.mgefCode, MGEFCode.ValidMGEFCode)

    def GetShortMGEFCode(self, target):
        """Resolves the various MGEFCode classes to a single 32-bit value used by CBash"""
        return self.mgefCode.GetShortMGEFCode(target)

# Classes
# Any level Descriptors
class CBashAlias(object):
    __slots__ = ['_AttrName']
    def __init__(self, AttrName):
        self._AttrName = AttrName

    def __get__(self, instance, owner):
        return getattr(instance, self._AttrName, None)

    def __set__(self, instance, nValue):
        setattr(instance, self._AttrName, nValue)

class CBashGrouped(object):
    __slots__ = ['_FieldID','_Type','_AsList']
    def __init__(self, FieldID, Type, AsList=False):
        self._FieldID, self._Type, self._AsList = FieldID, Type, AsList

    def __get__(self, instance, owner):
        oElement = self._Type(instance._RecordID, self._FieldID)
        return tuple([getattr(oElement, attr) for attr in oElement.copyattrs]) if self._AsList else oElement

    def __set__(self, instance, nElement):
        oElement = self._Type(instance._RecordID, self._FieldID)
        for nValue, attr in zip(nElement if isinstance(nElement, tuple) else tuple([None for attr in oElement.copyattrs]) if nElement is None else tuple([getattr(nElement, attr) for attr in nElement.copyattrs]), oElement.copyattrs):
            setattr(oElement, attr, nValue)

class CBashJunk(object):
    __slots__ = []
    def __init__(self, FieldID):
        pass

    def __get__(self, instance, owner):
        return None

    def __set__(self, instance, nValue):
        pass

class CBashBasicFlag(object):
    __slots__ = ['_AttrName','_Value']
    def __init__(self, AttrName, Value):
        self._AttrName, self._Value = AttrName, Value

    def __get__(self, instance, owner):
        field = getattr(instance, self._AttrName, None)
        return None if field is None else (field & self._Value) != 0

    def __set__(self, instance, nValue):
        field = getattr(instance, self._AttrName, None)
        setattr(instance, self._AttrName, field & ~self._Value if field and not nValue else field | self._Value if field else self._Value)

class CBashInvertedFlag(object):
    __slots__ = ['_AttrName']
    def __init__(self, AttrName):
        self._AttrName = AttrName

    def __get__(self, instance, owner):
        field = getattr(instance, self._AttrName, None)
        return None if field is None else not field

    def __set__(self, instance, nValue):
        setattr(instance, self._AttrName, not nValue)

class CBashBasicType(object):
    __slots__ = ['_AttrName','_Value','_DefaultFieldName']
    def __init__(self, AttrName, value, default):
        self._AttrName, self._Value, self._DefaultFieldName = AttrName, value, default

    def __get__(self, instance, owner):
        field = getattr(instance, self._AttrName, None)
        return None if field is None else field == self._Value

    def __set__(self, instance, nValue):
        setattr(instance, self._AttrName if nValue else self._DefaultFieldName, self._Value if nValue else True)

class CBashMaskedType(object):
    __slots__ = ['_AttrName','_TypeMask','_Value','_DefaultFieldName']
    def __init__(self, AttrName, typeMask, value, default):
        self._AttrName, self._TypeMask, self._Value, self._DefaultFieldName = AttrName, typeMask, value & typeMask, default

    def __get__(self, instance, owner):
        field = getattr(instance, self._AttrName, None)
        return None if field is None else (field & self._TypeMask) == self._Value

    def __set__(self, instance, nValue):
        setattr(instance, self._AttrName if nValue else self._DefaultFieldName, (getattr(instance, self._AttrName, 0) & ~self._TypeMask) | self._Value if nValue else True)

# Grouped Top Descriptors
class CBashGeneric_GROUP(object):
    __slots__ = ['_FieldID','_Type','_ResType']
    def __init__(self, FieldID, Type):
        self._FieldID, self._Type, self._ResType = FieldID, Type, POINTER(Type)

    def __get__(self, instance, owner):
        _CGetField.restype = self._ResType
        retValue = _CGetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, byref(self._Type(nValue)), 0)

class CBashFORMID_GROUP(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)

    def __set__(self, instance, nValue):
        nValue = None if nValue is None else nValue.GetShortFormID(instance)
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, byref(c_ulong(nValue), 0))

class CBashFORMID_OR_UINT32_ARRAY_GROUP(object):
    __slots__ = ['_FieldID','_Size']
    def __init__(self, FieldID, Size=None):
        self._FieldID, self._Size = FieldID, Size

    def __get__(self, instance, owner):
        FieldID = self._FieldID + instance._FieldID
        numRecords = _CGetFieldAttribute(instance._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = (c_ulong * numRecords)()
            _CGetField(instance._RecordID, FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [FormID(instance._RecordID, cRecord) if _CGetFieldAttribute(instance._RecordID, FieldID, x, 1, 0, 0, 0, 0, 2) == API_FIELDS.FORMID else cRecord for x, cRecord in enumerate(cRecords)]
        return []

    def __set__(self, instance, nValue):
        FieldID = self._FieldID + instance._FieldID
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, FieldID, 0, 0, 0, 0, 0, 0)
        else:
            nValue = [x for x in nValue if x is not None or (isinstance(x, FormID) and x.GetShortFormID(instance) is not None)]
            length = len(nValue)
            if self._Size and length != self._Size: return
            #Each element can be either a formID or UINT32, so they have to be set separately
            #Resize the list
            _CSetField(instance._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 0, c_long(length))
            for x, value in enumerate(nValue):
                #Borrowing ArraySize to flag if the new value is a formID
                IsFormID = isinstance(value, FormID)
                _CSetField(instance._RecordID, FieldID, x, 1, 0, 0, 0, 0, byref(c_ulong(value.GetShortFormID(instance) if IsFormID else value)), IsFormID)

class CBashUINT8ARRAY_GROUP(object):
    __slots__ = ['_FieldID','_Size']
    def __init__(self, FieldID, Size=None):
        self._FieldID, self._Size = FieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ubyte * numRecords)()
            _CGetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [cRecords.contents[x] for x in range(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            length = len(nValue)
            if self._Size and length != self._Size: return
            cRecords = (c_ubyte * length)(*nValue)
            _CSetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords), length)

class CBashFLOAT32_GROUP(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_float)
        retValue = _CGetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return round(retValue.contents.value,6) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, byref(c_float(round(nValue,6))), 0)

class CBashSTRING_GROUP(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return _unicode(retValue) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, _encode(nValue), 0)

class CBashISTRING_GROUP(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return IUNICODE(_unicode(retValue)) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID + instance._FieldID, 0, 0, 0, 0, 0, 0, _encode(nValue), 0)

class CBashLIST_GROUP(object):
    __slots__ = ['_FieldID','_Type','_AsList']
    def __init__(self, FieldID, Type, AsList=False):
        self._FieldID, self._Type, self._AsList = FieldID, Type, AsList

    def __get__(self, instance, owner):
        FieldID = self._FieldID + instance._FieldID
        return ExtractCopyList([self._Type(instance._RecordID, FieldID, x) for x in range(_CGetFieldAttribute(instance._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1))]) if self._AsList else [self._Type(instance._RecordID, FieldID, x) for x in range(_CGetFieldAttribute(instance._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1))]

    def __set__(self, instance, nElements):
        FieldID = self._FieldID + instance._FieldID
        if nElements is None or not len(nElements): _CDeleteField(instance._RecordID, FieldID, 0, 0, 0, 0, 0, 0)
        else:
            length = len(nElements)
            if not isinstance(nElements[0], tuple): nElements = ExtractCopyList(nElements)
            ##Resizes the list
            _CSetField(instance._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 0, c_long(length))
            SetCopyList([self._Type(instance._RecordID, FieldID, x) for x in range(_CGetFieldAttribute(instance._RecordID, FieldID, 0, 0, 0, 0, 0, 0, 1))], nElements)

# Top level Descriptors
class CBashLIST(object):
    __slots__ = ['_FieldID','_Type','_AsList']
    def __init__(self, FieldID, Type, AsList=False):
        self._FieldID, self._Type, self._AsList = FieldID, Type, AsList

    def __get__(self, instance, owner):
        return ExtractCopyList([self._Type(instance._RecordID, self._FieldID, x) for x in range(_CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1))]) if self._AsList else [self._Type(instance._RecordID, self._FieldID, x) for x in range(_CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1))]

    def __set__(self, instance, nElements):
        if nElements is None or not len(nElements): _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            length = len(nElements)
            if not isinstance(nElements[0], tuple): nElements = ExtractCopyList(nElements)
            ##Resizes the list
            _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0, c_long(length))
            SetCopyList([self._Type(instance._RecordID, self._FieldID, x) for x in xrange(_CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1))], nElements)

class CBashUNKNOWN_OR_GENERIC(object):
    __slots__ = ['_FieldID','_Type','_ResType']
    def __init__(self, FieldID, Type):
        self._FieldID, self._Type, self._ResType = FieldID, Type, POINTER(Type)

    def __get__(self, instance, owner):
        if _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 2) == API_FIELDS.UNKNOWN: return None
        _CGetField.restype = self._ResType
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        if _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 2) == API_FIELDS.UNKNOWN: return
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(self._Type(nValue)), 0)

class CBashXSED(object):
    __slots__ = ['_FieldID','_AsOffset','_ResType']
    """To delete the field, you have to set the current accessor to None."""
    def __init__(self, FieldID, AsOffset=False):
        self._FieldID, self._AsOffset = FieldID, AsOffset
        self._ResType = POINTER(c_ubyte) if AsOffset else POINTER(c_ulong)

    def __get__(self, instance, owner):
        if (_CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 2) != API_FIELDS.UINT32) != self._AsOffset: return None
        _CGetField.restype = self._ResType
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None:
            if (_CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 2) != API_FIELDS.UINT32) != self._AsOffset: return
            _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        #Borrowing ArraySize to flag if the new value is an offset
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(c_ubyte(nValue) if self._AsOffset else c_ulong(nValue)), c_bool(self._AsOffset))

class CBashISTRINGARRAY(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = (POINTER(c_char_p) * numRecords)()
            _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [IUNICODE(_unicode(string_at(cRecords[x]))) for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            length = len(nValue)
            nValue = [_encode(value) for value in nValue]
            _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref((c_char_p * length)(*nValue)), length)

class CBashIUNICODEARRAY(object):
    # Almost exactly like CBashISTRINGARRAY, but instead of using the bolt.pluginEncoding
    # for encoding, uses the automatic encoding detection.  Only really useful for TES4
    # record (masters)
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if (numRecords > 0):
            cRecords = (POINTER(c_char_p) * numRecords)()
            _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [IUNICODE(_uni(string_at(cRecords[x]))) for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            length = len(nValue)
            nValue = [_enc(value) for value in nValue]
            _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref((c_char_p * length)(*nValue)), length)

class CBashGeneric(object):
    __slots__ = ['_FieldID','_Type','_ResType']
    def __init__(self, FieldID, Type):
        self._FieldID, self._Type, self._ResType = FieldID, Type, POINTER(Type)

    def __get__(self, instance, owner):
        _CGetField.restype = self._ResType
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(self._Type(nValue)), 0)

class CBashFORMID(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)

    def __set__(self, instance, nValue):
        nValue = None if nValue is None else nValue.GetShortFormID(instance)
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(c_ulong(nValue)), 0)

class CBashMGEFCODE(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_char * 4) if _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 2) == API_FIELDS.CHAR4 else POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return MGEFCode(instance._RecordID, retValue.contents.value) if retValue else MGEFCode(None,None)

    def __set__(self, instance, nValue):
        nValue = None if nValue is None else nValue.GetShortMGEFCode(instance)
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(c_ulong(nValue)), 0)

class CBashFORMIDARRAY(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ulong * numRecords)()
            _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [FormID(instance._RecordID, cRecords.contents[x]) for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            nValue = [x.GetShortFormID(instance) for x in nValue if x.GetShortFormID(instance) is not None]
            length = len(nValue)
            _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref((c_ulong * length)(*nValue)), length)

class CBashFORMID_OR_UINT32(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return (FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)) if _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 2) == API_FIELDS.FORMID else retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        nValue = nValue.GetShortFormID(instance) if isinstance(nValue, FormID) else nValue
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(c_ulong(nValue)), 0)

class CBashFORMID_OR_STRING(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        IsFormID = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 2) == API_FIELDS.FORMID
        _CGetField.restype = POINTER(c_ulong) if IsFormID else c_char_p
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return (FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)) if IsFormID else _unicode(retValue) if retValue else None

    def __set__(self, instance, nValue):
        IsFormID = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 2) == API_FIELDS.FORMID
        nValue = None if nValue is None else nValue.GetShortFormID(instance) if IsFormID else nValue
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(c_ulong(nValue)) if IsFormID else _encode(nValue), 0)

class CBashFORMID_OR_UINT32_ARRAY(object):
    __slots__ = ['_FieldID','_Size']
    def __init__(self, FieldID, Size=None):
        self._FieldID, self._Size = FieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = (c_ulong * numRecords)()
            _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [FormID(instance._RecordID, cRecord) if _CGetFieldAttribute(instance._RecordID, self._FieldID, x, 1, 0, 0, 0, 0, 2) == API_FIELDS.FORMID else cRecord for x, cRecord in enumerate(cRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            nValue = [x for x in nValue if x is not None or (isinstance(x, FormID) and x.GetShortFormID(instance) is not None)]
            length = len(nValue)
            if self._Size and length != self._Size: return
            #Each element can be either a formID or UINT32, so they have to be set separately
            #Resize the list
            _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0, c_long(length))
            for x, value in enumerate(nValue):
                #Borrowing ArraySize to flag if the new value is a formID
                IsFormID = isinstance(value, FormID)
                _CSetField(instance._RecordID, self._FieldID, x, 1, 0, 0, 0, 0, byref(c_ulong(value.GetShortFormID(instance) if IsFormID else value)), IsFormID)

class CBashMGEFCODE_ARRAY(object):
    __slots__ = ['_FieldID','_Size']
    def __init__(self, FieldID, Size=None):
        self._FieldID, self._Size = FieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ulong * numRecords)()
            _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [MGEFCode(instance._RecordID, cast(POINTER(c_ulong)(c_ulong(cRecords.contents[x])), POINTER(c_char * 4)).contents.value if _CGetFieldAttribute(instance._RecordID, self._FieldID, x, 1, 0, 0, 0, 0, 2) == API_FIELDS.CHAR4 else cRecords.contents[x]) for x in range(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            nValue = [x.GetShortMGEFCode(instance) for x in nValue if x.GetShortMGEFCode(instance) is not None]
            length = len(nValue)
            if self._Size and length != self._Size: return
            _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref((c_ulong * length)(*nValue)), length)

class CBashUINT8ARRAY(object):
    __slots__ = ['_FieldID','_Size']
    def __init__(self, FieldID, Size=None):
        self._FieldID, self._Size = FieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ubyte * numRecords)()
            _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [cRecords.contents[x] for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            length = len(nValue)
            if self._Size and length != self._Size: return
            _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref((c_ubyte * length)(*nValue)), length)

class CBashUINT32ARRAY(object):
    __slots__ = ['_FieldID','_Size']
    def __init__(self, FieldID, Size=None):
        self._FieldID, self._Size = FieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ulong * numRecords)()
            _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [cRecords.contents[x] for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            length = len(nValue)
            if self._Size and length != self._Size: return
            _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref((c_ulong * length)(*nValue)), length)

class CBashSINT16ARRAY(object):
    __slots__ = ['_FieldID','_Size']
    def __init__(self, FieldID, Size=None):
        self._FieldID, self._Size = FieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_short * numRecords)()
            _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [cRecords.contents[x] for x in range(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else:
            length = len(nValue)
            if self._Size and length != self._Size: return
            _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref((c_short * length)(*nValue)), length)

class CBashFLOAT32(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_float)
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return round(retValue.contents.value,6) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(c_float(round(nValue,6))), 0)

class CBashDEGREES(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_float)
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return round(math.degrees(retValue.contents.value),6) if retValue else None

    def __set__(self, instance, nValue):
        try: nValue = math.radians(nValue)
        except TypeError: nValue = None
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(c_float(round(nValue,6))), 0)

class CBashSTRING(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return _unicode(retValue,avoidEncodings=('utf8','utf-8')) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, _encode(nValue), 0)

class CBashUNICODE(object):
    # Almost exactly like CBashSTRING, only instead of using the bolt.pluginEncoding
    # specified encoding first, uses the automatic encoding detection.  Only really
    # useful for the TES4 record
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return _uni(retValue,avoidEncodings=('utf8','utf-8')) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, _enc(nValue), 0)

class CBashISTRING(object):
    __slots__ = ['_FieldID']
    def __init__(self, FieldID):
        self._FieldID = FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return IUNICODE(_unicode(retValue)) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, _encode(nValue), 0)

class CBashRECORDARRAY(object):
    __slots__ = ['_Type','_TypeName']
    def __init__(self, Type, TypeName):
        self._Type, self._TypeName = Type, cast(TypeName, POINTER(c_ulong)).contents.value

    def __get__(self, instance, owner):
        numRecords = _CGetNumRecords(instance._ModID, self._TypeName)
        if(numRecords > 0):
            cRecords = (c_ulong * numRecords)()
            _CGetRecordIDs(instance._ModID, self._TypeName, byref(cRecords))
            return [self._Type(x) for x in cRecords]
        return []

    def __set__(self, instance, nValue):
        return

class CBashSUBRECORD(object):
    __slots__ = ['_FieldID','_Type','_TypeName']
    def __init__(self, FieldID, Type, TypeName):
        self._FieldID, self._Type, self._TypeName = FieldID, Type, cast(TypeName, POINTER(c_ulong)).contents.value

    def __get__(self, instance, owner):
        _CGetField.restype = c_ulong
        retValue = _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 0)
        return self._Type(retValue) if retValue else None

    def __set__(self, instance, nValue):
        return

class CBashSUBRECORDARRAY(object):
    __slots__ = ['_FieldID','_Type']
    def __init__(self, FieldID, Type, TypeName): #TypeName not currently used
        self._FieldID, self._Type = FieldID, Type

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = (c_ulong * numRecords)()
            _CGetField(instance._RecordID, self._FieldID, 0, 0, 0, 0, 0, 0, byref(cRecords))
            return [self._Type(x) for x in cRecords]
        return []

    def __set__(self, instance, nValue):
        return

# ListX1 Descriptors
class CBashLIST_LIST(object):
    __slots__ = ['_ListFieldID','_Type','_AsList']
    def __init__(self, ListFieldID, Type, AsList=False):
        self._ListFieldID, self._Type, self._AsList = ListFieldID, Type, AsList

    def __get__(self, instance, owner):
        return ExtractCopyList([self._Type(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, x) for x in xrange(_CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 1))]) if self._AsList else [self._Type(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, x) for x in range(_CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 1))]

    def __set__(self, instance, nElements):
        if nElements is None or not len(nElements): _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else:
            length = len(nElements)
            if not isinstance(nElements[0], tuple): nElements = ExtractCopyList(nElements)
            ##Resizes the list
            _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0, c_long(length))
            SetCopyList([self._Type(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, x) for x in xrange(_CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 1))], nElements)

class CBashGeneric_LIST(object):
    __slots__ = ['_ListFieldID','_Type','_ResType']
    def __init__(self, ListFieldID, Type):
        self._ListFieldID, self._Type, self._ResType = ListFieldID, Type, POINTER(Type)

    def __get__(self, instance, owner):
        _CGetField.restype = self._ResType
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0)
        return retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(self._Type(nValue)), 0)

class CBashFORMID_LIST(object):
    __slots__ = ['_ListFieldID']
    def __init__(self, ListFieldID):
        self._ListFieldID = ListFieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0)
        return FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)

    def __set__(self, instance, nValue):
        nValue = None if nValue is None else nValue.GetShortFormID(instance)
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(c_ulong(nValue)), 0)

class CBashACTORVALUE_LIST(object):
    __slots__ = ['_ListFieldID']
    def __init__(self, ListFieldID):
        self._ListFieldID = ListFieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0)
        return ActorValue(instance._RecordID, retValue.contents.value) if retValue else ActorValue(None,None)

    def __set__(self, instance, nValue):
        nValue = None if nValue is None else nValue.GetShortActorValue(instance)
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(c_ulong(nValue)), 0)

class CBashFORMIDARRAY_LIST(object):
    __slots__ = ['_ListFieldID']
    def __init__(self, ListFieldID):
        self._ListFieldID = ListFieldID

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ulong * numRecords)()
            _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(cRecords))
            return [FormID(instance._RecordID, cRecords.contents[x]) for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else:
            nValue = [x.GetShortFormID(instance) for x in nValue if x.GetShortFormID(instance) is not None]
            length = len(nValue)
            _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref((c_ulong * length)(*nValue)), length)

class CBashUNKNOWN_OR_FORMID_OR_UINT32_LIST(object):
    __slots__ = ['_ListFieldID']
    def __init__(self, ListFieldID):
        self._ListFieldID = ListFieldID

    def __get__(self, instance, owner):
        fieldtype = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 2)
        if fieldtype == API_FIELDS.UNKNOWN: return None
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0)
        return (FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)) if fieldtype == API_FIELDS.FORMID else retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        fieldtype = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 2)
        if fieldtype == API_FIELDS.UNKNOWN: return
        nValue = None if nValue is None else nValue.GetShortFormID(instance) if fieldtype == API_FIELDS.FORMID else nValue
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(c_ulong(nValue)), 0)

class CBashMGEFCODE_LIST(object):
    __slots__ = ['_ListFieldID']
    def __init__(self, ListFieldID):
        self._ListFieldID = ListFieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_char * 4) if _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 2) == API_FIELDS.CHAR4 else POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0)
        return MGEFCode(instance._RecordID, retValue.contents.value) if retValue else MGEFCode(None,None)

    def __set__(self, instance, nValue):
        nValue = None if nValue is None else nValue.GetShortMGEFCode(instance)
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(c_ulong(nValue)), 0)

class CBashFORMID_OR_MGEFCODE_OR_ACTORVALUE_OR_UINT32_LIST(object):
    __slots__ = ['_ListFieldID']
    def __init__(self, ListFieldID):
        self._ListFieldID = ListFieldID

    def __get__(self, instance, owner):
        fieldtype = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 2)
        _CGetField.restype = POINTER(c_char * 4) if fieldtype == API_FIELDS.CHAR4 else POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0)
        return (FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)) if fieldtype == API_FIELDS.FORMID else (ActorValue(instance._RecordID, retValue.contents.value) if retValue else ActorValue(None,None)) if fieldtype in (API_FIELDS.STATIC_ACTORVALUE, API_FIELDS.RESOLVED_ACTORVALUE) else (MGEFCode(instance._RecordID, retValue.contents.value) if retValue else MGEFCode(None,None)) if fieldtype in (API_FIELDS.STATIC_MGEFCODE, API_FIELDS.RESOLVED_MGEFCODE) else retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        fieldtype = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 2)
        nValue = None if nValue is None else nValue.GetShortFormID(instance) if fieldtype == API_FIELDS.FORMID else nValue.GetShortActorValue(instance) if fieldtype in (API_FIELDS.STATIC_ACTORVALUE, API_FIELDS.RESOLVED_ACTORVALUE) else nValue.GetShortMGEFCode(instance) if fieldtype in (API_FIELDS.STATIC_MGEFCODE, API_FIELDS.RESOLVED_MGEFCODE) else nValue
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(c_ulong(nValue)), 0)

class CBashUINT8ARRAY_LIST(object):
    __slots__ = ['_ListFieldID','_Size']
    def __init__(self, ListFieldID, Size=None):
        self._ListFieldID, self._Size = ListFieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ubyte * numRecords)()
            _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(cRecords))
            return [cRecords.contents[x] for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else:
            length = len(nValue)
            if self._Size and length != self._Size: return
            _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref((c_ubyte * length)(*nValue)), length)

class CBashUINT32ARRAY_LIST(object):
    __slots__ = ['_ListFieldID','_Size']
    def __init__(self, ListFieldID, Size=None):
        self._ListFieldID, self._Size = ListFieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ulong * numRecords)()
            _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(cRecords))
            return [cRecords.contents[x] for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else:
            length = len(nValue)
            if self._Size and length != self._Size: return
            _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref((c_ulong * length)(*nValue)), length)

class CBashFORMID_OR_UINT32_ARRAY_LIST(object):
    __slots__ = ['_ListFieldID','_Size']
    def __init__(self, ListFieldID, Size=None):
        self._ListFieldID, self._Size = ListFieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 1)
        if(numRecords > 0):
            cRecords = (c_ulong * numRecords)()
            _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(cRecords))
            return [FormID(instance._RecordID, cRecord) if _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, x, 1, 0, 0, 2) == API_FIELDS.FORMID else cRecord for x, cRecord in enumerate(cRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else:
            nValue = [x for x in nValue if x is not None or (isinstance(x, FormID) and x.GetShortFormID(instance) is not None)]
            length = len(nValue)
            if self._Size and length != self._Size: return
            #Each element can be either a formID or UINT32, so they have to be set separately
            #Resize the list
            _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0, c_long(length))
            for x, value in enumerate(nValue):
                #Borrowing ArraySize to flag if the new value is a formID
                IsFormID = isinstance(value, FormID)
                _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, x, 1, 0, 0, byref(c_ulong(value.GetShortFormID(instance) if IsFormID else value)), IsFormID)

class CBashFLOAT32_LIST(object):
    __slots__ = ['_ListFieldID']
    def __init__(self, ListFieldID):
        self._ListFieldID = ListFieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_float)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0)
        return round(retValue.contents.value,6) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, byref(c_float(round(nValue,6))), 0)

class CBashSTRING_LIST(object):
    __slots__ = ['_ListFieldID']
    def __init__(self, ListFieldID):
        self._ListFieldID = ListFieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0)
        return _unicode(retValue) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, _encode(nValue), 0)

class CBashISTRING_LIST(object):
    __slots__ = ['_ListFieldID']
    def __init__(self, ListFieldID):
        self._ListFieldID = ListFieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, 0)
        return IUNICODE(_unicode(retValue)) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, self._ListFieldID, 0, 0, 0, 0, _encode(nValue), 0)

# ListX2 Descriptors
class CBashLIST_LISTX2(object):
    __slots__ = ['_ListX2FieldID','_Type','_AsList']
    def __init__(self, ListX2FieldID, Type, AsList=False):
        self._ListX2FieldID, self._Type, self._AsList = ListX2FieldID, Type, AsList

    def __get__(self, instance, owner):
        return ExtractCopyList([self._Type(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, x) for x in xrange(_CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 1))]) if self._AsList else [self._Type(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, x) for x in range(_CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 1))]

    def __set__(self, instance, nElements):
        if nElements is None or not len(nElements): _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else:
            length = len(nElements)
            if not isinstance(nElements[0], tuple): nElements = ExtractCopyList(nElements)
            ##Resizes the list
            _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0, c_long(length))
            SetCopyList([self._Type(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, x) for x in xrange(_CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 1))], nElements)

class CBashGeneric_LISTX2(object):
    __slots__ = ['_ListX2FieldID','_Type','_ResType']
    def __init__(self, ListX2FieldID, Type):
        self._ListX2FieldID, self._Type, self._ResType = ListX2FieldID, Type, POINTER(Type)

    def __get__(self, instance, owner):
        _CGetField.restype = self._ResType
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0)
        return retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, byref(self._Type(nValue)), 0)

class CBashFLOAT32_LISTX2(object):
    __slots__ = ['_ListX2FieldID']
    def __init__(self, ListX2FieldID):
        self._ListX2FieldID = ListX2FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_float)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0)
        return round(retValue.contents.value,6) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, byref(c_float(round(nValue,6))), 0)

class CBashDEGREES_LISTX2(object):
    __slots__ = ['_ListX2FieldID']
    def __init__(self, ListX2FieldID):
        self._ListX2FieldID = ListX2FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_float)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0)
        return round(math.degrees(retValue.contents.value),6) if retValue else None

    def __set__(self, instance, nValue):
        try: nValue = math.radians(nValue)
        except TypeError: nValue = None
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, byref(c_float(round(nValue,6))), 0)

class CBashUINT8ARRAY_LISTX2(object):
    __slots__ = ['_ListX2FieldID','_Size']
    def __init__(self, ListX2FieldID, Size=None):
        self._ListX2FieldID, self._Size = ListX2FieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ubyte * numRecords)()
            _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, byref(cRecords))
            return [cRecords.contents[x] for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else:
            length = len(nValue)
            if self._Size and length != self._Size: return
            _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, byref((c_ubyte * length)(*nValue)), length)

class CBashFORMID_OR_UINT32_ARRAY_LISTX2(object):
    __slots__ = ['_ListX2FieldID','_Size']
    def __init__(self, ListX2FieldID, Size=None):
        self._ListX2FieldID, self._Size = ListX2FieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 1)
        if(numRecords > 0):
            cRecords = (c_ulong * numRecords)()
            _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, byref(cRecords))
            return [FormID(instance._RecordID, cRecord) if _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, x, 1, 2) == API_FIELDS.FORMID else cRecord for x, cRecord in enumerate(cRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else:
            nValue = [x for x in nValue if x is not None or (isinstance(x, FormID) and x.GetShortFormID(instance) is not None)]
            length = len(nValue)
            if self._Size and length != self._Size: return
            #Each element can be either a formID or UINT32, so they have to be set separately
            #Resize the list
            _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0, c_long(length))
            for x, value in enumerate(nValue):
                #Borrowing ArraySize to flag if the new value is a formID
                IsFormID = isinstance(value, FormID)
                _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, x, 1, byref(c_ulong(value.GetShortFormID(instance) if IsFormID else value)), IsFormID)

class CBashFORMID_LISTX2(object):
    __slots__ = ['_ListX2FieldID']
    def __init__(self, ListX2FieldID):
        self._ListX2FieldID = ListX2FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0)
        return FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)

    def __set__(self, instance, nValue):
        nValue = None if nValue is None else nValue.GetShortFormID(instance)
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, byref(c_ulong(nValue)), 0)

class CBashFORMID_OR_FLOAT32_LISTX2(object):
    __slots__ = ['_ListX2FieldID']
    def __init__(self, ListX2FieldID):
        self._ListX2FieldID = ListX2FieldID

    def __get__(self, instance, owner):
        IsFormID = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 2) == API_FIELDS.FORMID
        _CGetField.restype = POINTER(c_ulong) if IsFormID else POINTER(c_float)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0)
        return (FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)) if IsFormID else round(retValue.contents.value,6) if retValue else None

    def __set__(self, instance, nValue):
        IsFormID = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 2) == API_FIELDS.FORMID
        try: nValue = None if nValue is None else nValue.GetShortFormID(instance) if IsFormID else float(round(nValue,6))
        except TypeError: nValue = None
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, byref(c_ulong(nValue)) if IsFormID else byref(nValue), 0)

class CBashSTRING_LISTX2(object):
    __slots__ = ['_ListX2FieldID']
    def __init__(self, ListX2FieldID):
        self._ListX2FieldID = ListX2FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0)
        return _unicode(retValue) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, _encode(nValue), 0)

class CBashISTRING_LISTX2(object):
    __slots__ = ['_ListX2FieldID']
    def __init__(self, ListX2FieldID):
        self._ListX2FieldID = ListX2FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0)
        return IUNICODE(_unicode(retValue)) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, _encode(nValue), 0)

class CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX2(object):
    __slots__ = ['_ListX2FieldID']
    def __init__(self, ListX2FieldID):
        self._ListX2FieldID = ListX2FieldID

    def __get__(self, instance, owner):
        fieldtype = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 2)
        if fieldtype == API_FIELDS.UNKNOWN: return None
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 0)
        return (FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)) if fieldtype == API_FIELDS.FORMID else retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        fieldtype = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, 2)
        if fieldtype == API_FIELDS.UNKNOWN: return
        nValue = None if nValue is None else nValue.GetShortFormID(instance) if fieldtype == API_FIELDS.FORMID else nValue
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, self._ListX2FieldID, 0, 0, byref(c_ulong(nValue)), 0)

# ListX3 Descriptors
class CBashGeneric_LISTX3(object):
    __slots__ = ['_ListX3FieldID','_Type','_ResType']
    def __init__(self, ListX3FieldID, Type):
        self._ListX3FieldID, self._Type, self._ResType = ListX3FieldID, Type, POINTER(Type)

    def __get__(self, instance, owner):
        _CGetField.restype = self._ResType
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 0)
        return retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, byref(self._Type(nValue)), 0)

class CBashUINT8ARRAY_LISTX3(object):
    __slots__ = ['_ListX3FieldID','_Size']
    def __init__(self, ListX3FieldID, Size=None):
        self._ListX3FieldID, self._Size = ListX3FieldID, Size

    def __get__(self, instance, owner):
        numRecords = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 1)
        if(numRecords > 0):
            cRecords = POINTER(c_ubyte * numRecords)()
            _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, byref(cRecords))
            return [cRecords.contents[x] for x in xrange(numRecords)]
        return []

    def __set__(self, instance, nValue):
        if nValue is None or not len(nValue): _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID)
        else:
            length = len(nValue)
            if self._Size and length != self._Size: return
            _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, byref((c_ubyte * length)(*nValue)), length)

class CBashFORMID_OR_FLOAT32_LISTX3(object):
    __slots__ = ['_ListX3FieldID']
    def __init__(self, ListX3FieldID):
        self._ListX3FieldID = ListX3FieldID

    def __get__(self, instance, owner):
        IsFormID = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 2) == API_FIELDS.FORMID
        _CGetField.restype = POINTER(c_ulong) if IsFormID else POINTER(c_float)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 0)
        return (FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)) if IsFormID else round(retValue.contents.value,6) if retValue else None

    def __set__(self, instance, nValue):
        IsFormID = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 2) == API_FIELDS.FORMID
        try: nValue = None if nValue is None else nValue.GetShortFormID(instance) if IsFormID else float(round(nValue,6))
        except TypeError: nValue = None
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, byref(c_ulong(nValue)) if IsFormID else byref(nValue), 0)

class CBashFLOAT32_LISTX3(object):
    __slots__ = ['_ListX3FieldID']
    def __init__(self, ListX3FieldID):
        self._ListX3FieldID = ListX3FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = POINTER(c_float)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 0)
        return round(retValue.contents.value,6) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, byref(c_float(round(nValue,6))), 0)

class CBashSTRING_LISTX3(object):
    __slots__ = ['_ListX3FieldID']
    def __init__(self, ListX3FieldID):
        self._ListX3FieldID = ListX3FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 0)
        return _unicode(retValue) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, _encode(nValue), 0)

class CBashISTRING_LISTX3(object):
    __slots__ = ['_ListX3FieldID']
    def __init__(self, ListX3FieldID):
        self._ListX3FieldID = ListX3FieldID

    def __get__(self, instance, owner):
        _CGetField.restype = c_char_p
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 0)
        return IUNICODE(_unicode(retValue)) if retValue else None

    def __set__(self, instance, nValue):
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, _encode(nValue), 0)

class CBashUNKNOWN_OR_FORMID_OR_UINT32_LISTX3(object):
    __slots__ = ['_ListX3FieldID']
    def __init__(self, ListX3FieldID):
        self._ListX3FieldID = ListX3FieldID

    def __get__(self, instance, owner):
        fieldtype = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 2)
        if fieldtype == API_FIELDS.UNKNOWN: return None
        _CGetField.restype = POINTER(c_ulong)
        retValue = _CGetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 0)
        return (FormID(instance._RecordID, retValue.contents.value) if retValue else FormID(None,None)) if fieldtype == API_FIELDS.FORMID else retValue.contents.value if retValue else None

    def __set__(self, instance, nValue):
        fieldtype = _CGetFieldAttribute(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, 2)
        if fieldtype == API_FIELDS.UNKNOWN: return
        nValue = None if nValue is None else nValue.GetShortFormID(instance) if fieldtype == API_FIELDS.FORMID else nValue
        if nValue is None: _CDeleteField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID)
        else: _CSetField(instance._RecordID, instance._FieldID, instance._ListIndex, instance._ListFieldID, instance._ListX2Index, instance._ListX2FieldID, instance._ListX3Index, self._ListX3FieldID, byref(c_ulong(nValue)), 0)
