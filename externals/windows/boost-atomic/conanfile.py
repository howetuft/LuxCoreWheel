# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "assert",
    "config",
    "static_assert",
    "type_traits",
    "align",
    "predef",
    "preprocessor",
]

class BoostAtomic(ConanFile, metaclass=BoostMeta, module="atomic", boost_deps=DEPS):
    pass
