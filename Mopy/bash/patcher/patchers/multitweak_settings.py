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
"""This module contains oblivion multitweak item patcher classes that belong
to the Gmst Multitweaker - as well as the GmstTweaker itself. Gmst stands
for game settings."""
from __future__ import print_function
from ... import bush # for game
from ...bolt import SubProgress, floats_equal
from ...brec import MreRecord, RecHeader
from ...exception import StateError
from ...patcher.base import AMultiTweaker, DynamicTweak
from ...patcher.patchers.base import MultiTweakItem, CBash_MultiTweakItem
from ...patcher.patchers.base import MultiTweaker, CBash_MultiTweaker

# Patchers: 30 ----------------------------------------------------------------
class _AGlobalsTweak(DynamicTweak):
    """Sets a global to specified value."""
    tweak_read_classes = b'GLOB',
    show_key_for_custom = True

    @property
    def chosen_value(self):
        # Globals are always stored as floats, regardless of what the CS says
        return float(self.choiceValues[self.chosen][0])

    def wants_record(self, record):
        return (getattr(record, u'eid', None) and # skip missing and empty EDID
                record.eid.lower() == self.tweak_key and
                record.value != self.chosen_value)

    def tweak_record(self, record):
        record.value = self.chosen_value

    def tweak_log(self, log, count):
        if count: log(u'* ' + _(u'%s set to: %4.2f') % (
            self.tweak_name, self.chosen_value))

class GlobalsTweak(_AGlobalsTweak, MultiTweakItem): pass
class CBash_GlobalsTweak(_AGlobalsTweak, CBash_MultiTweakItem):
    scanOrder = 29
    editOrder = 29

#------------------------------------------------------------------------------
class _AGmstTweak(DynamicTweak):
    """Sets a GMST to specified value."""
    tweak_read_classes = b'GMST',
    show_key_for_custom = True

    @property
    def chosen_eids(self):
        return ((self.tweak_key,), self.tweak_key)[isinstance(self.tweak_key,
                                                              tuple)]

    @property
    def chosen_values(self): return self.choiceValues[self.chosen]

    @property
    def eid_was_itpo(self):
        try:
            return self._eid_was_itpo
        except AttributeError:
            self._eid_was_itpo = {e.lower(): False for e in self.chosen_eids}
            return self._eid_was_itpo

    def _find_chosen_value(self, wanted_eid):
        """Returns the value the user chose for the game setting with the
        specified editor ID. Note that wanted_eid must be lower-case!"""
        for test_eid, test_val in zip(self.chosen_eids, self.chosen_values):
            if wanted_eid == test_eid.lower():
                return test_val
        return None

    def _find_original_eid(self, lower_eid):
        """We need to find the original case of the EDID, otherwise getFMSTFid
        blows - plus the dumped record will look nicer :)."""
        for orig_eid in self.chosen_eids:
            if lower_eid == orig_eid.lower():
                return orig_eid
        return lower_eid # fallback, should never happen

    def validate_values(self, chosen_values):
        if bush.game.fsName == u'Oblivion': ##: add a comment why TES4 only!
            for target_value in chosen_values:
                if target_value < 0:
                    return _(u"Oblivion GMST values can't be negative")
        for target_eid, target_value in zip(self.chosen_eids, chosen_values):
            if target_eid.startswith(u'f') and type(target_value) != float:
                    return _(u"The value chosen for GMST '%s' must be a "
                             u'float, but is currently of type %s (%s).') % (
                        target_eid, type(target_value).__name__, target_value)
        return None

    def wants_record(self, record):
        rec_eid = record.eid.lower()
        if rec_eid not in self.eid_was_itpo: return False # not needed
        target_val = self._find_chosen_value(rec_eid)
        if rec_eid.startswith(u'f'):
            ret_val = not floats_equal(record.value, target_val)
        else:
            ret_val = record.value != target_val
        # Remember whether the last entry was ITPO or not
        self.eid_was_itpo[rec_eid] = not ret_val
        return ret_val

    def tweak_record(self, record):
        rec_eid = record.eid.lower()
        # We don't need to inject a GMST for this EDID anymore
        self.eid_was_itpo[rec_eid] = True
        record.value = self._find_chosen_value(rec_eid)

    def tweak_log(self, log, count): # count is ignored here
        if len(self.choiceLabels) > 1:
            if self.choiceLabels[self.chosen].startswith(_(u'Custom')):
                if isinstance(self.chosen_values[0], basestring):
                    log(u'* %s: %s %s' % (
                        self.tweak_name, self.choiceLabels[self.chosen],
                        self.chosen_values[0]))
                else:
                    log(u'* %s: %s %4.2f' % (
                        self.tweak_name, self.choiceLabels[self.chosen],
                        self.chosen_values[0]))
            else:
                log(u'* %s: %s' % (
                    self.tweak_name, self.choiceLabels[self.chosen]))
        else:
            log(u'* ' + self.tweak_name)

class GmstTweak(_AGmstTweak, MultiTweakItem):
    def finish_tweaking(self, patch_file):
        keep = patch_file.getKeeper()
        add_gmst = patch_file.GMST.setRecord
        # Inject new records for any remaining EDIDs
        for remaining_eid, was_itpo in self.eid_was_itpo.iteritems():
            if not was_itpo:
                new_gmst = MreRecord.type_class[b'GMST'](
                    RecHeader(b'GMST', 0, 0, 0, 0))
                new_gmst.eid = self._find_original_eid(remaining_eid)
                new_gmst.value = self._find_chosen_value(remaining_eid)
                new_gmst.longFids = True
                new_gmst.fid = new_gmst.getGMSTFid()
                if new_gmst.fid is not None: # None if missing from pickle
                    keep(new_gmst.fid)
                    add_gmst(new_gmst)

class CBash_GmstTweak(_AGmstTweak, CBash_MultiTweakItem):
    """Sets a GMST to specified value."""
    scanOrder = 29
    editOrder = 29

    def finishPatch(self, patchFile, progress):
        subProgress = SubProgress(progress)
        subProgress.setFull(max(len(self.chosen_values), 1))
        pstate = 0
        for remaining_eid, was_itpo in self.eid_was_itpo.iteritems():
            subProgress(pstate, _(u'Finishing GMST Tweaks...'))
            if not was_itpo:
                orig_eid = self._find_original_eid(remaining_eid)
                record = patchFile.create_GMST(orig_eid)
                if not record:
                    print(orig_eid)
                    print(patchFile.Current.Debug_DumpModFiles())
                    for conflict in patchFile.Current.LookupRecords(orig_eid,
                                                                    False):
                        print(conflict.GetParentMod().ModName)
                    raise StateError(u'Tweak Settings: Unable to create GMST!')
                record.value = self._find_chosen_value(remaining_eid)
            pstate += 1

#------------------------------------------------------------------------------
class _AGmstTweaker(AMultiTweaker):
    """Tweaks GMST records in various ways."""
    _class_tweaks = [] # override in implemententations

    @classmethod
    def tweak_instances(cls):
        instances = []
        for clazz, game_tweaks in cls._class_tweaks:
            for tweak in game_tweaks:
                if isinstance(tweak, tuple):
                    new_tweak = clazz(*tweak)
                elif isinstance(tweak, list):
                    new_tweak = clazz(*tweak[0])
                    new_tweak.default_enabled = tweak[1].get(
                        u'default_enabled', False)
                else:
                    raise SyntaxError(u'Invalid GMST tweak syntax: tuple or '
                                      u'list expected, got %r' % type(tweak))
                instances.append(new_tweak)
        instances.sort(key=lambda a: a.tweak_name.lower())
        return instances

class GmstTweaker(MultiTweaker, _AGmstTweaker):
    scanOrder = 29
    editOrder = 29
    _class_tweaks = [(GlobalsTweak, bush.game.GlobalsTweaks),
                    (GmstTweak, bush.game.GmstTweaks)]

class CBash_GmstTweaker(CBash_MultiTweaker, _AGmstTweaker):
    _class_tweaks = [(CBash_GlobalsTweak, bush.game.GlobalsTweaks),
                     (CBash_GmstTweak, bush.game.GmstTweaks)]
