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

"""This module contains the Fallout 4 record classes. Since they're identical
to the Fallout 4 classes, we just import those."""
from ..fallout4.records import *

# Only difference from FO4 is the default version, but this seems less hacky
# than adding a game var just for this and dynamically importing it in FO4
class MreTes4(MreHeaderBase):
    """TES4 Record. File header."""
    classType = b'TES4'

    melSet = MelSet(
        MelStruct(b'HEDR', u'f2I', (u'version', 0.95), u'numRecords',
                  (u'nextObject', 0x800)),
        MelBase(b'TNAM', u'tnam_p'),
        MelUnicode(b'CNAM', u'author', u'', 512),
        MelUnicode(b'SNAM', u'description', u'', 512),
        MreHeaderBase.MelMasterNames(),
        MelFidList(b'ONAM', u'overrides',),
        MelBase(b'SCRN', u'screenshot'),
        MelBase(b'INTV', u'unknownINTV'),
        MelBase(b'INCC', u'unknownINCC'),
    )
    __slots__ = melSet.getSlotsUsed()
