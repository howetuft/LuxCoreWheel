# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "assert",
    "config",
    "static_assert",
    "type_traits",
    "align",
    "predef",
    "preprocessor",
    "winapi",
]

class BoostAtomic(ConanFile, metaclass=BoostMeta, module="atomic", boost_deps=DEPS, libs=["boost_atomic"]):
    pass
