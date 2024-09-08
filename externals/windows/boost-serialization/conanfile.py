# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "array",
    "assert",
    "config",
    "core",
    "detail",
    "integer",
    "io",
    "iterator",
    "move",
    "mpl",
    "optional",
    "predef",
    "preprocessor",
    "smart_ptr",
    "spirit",
    "static_assert",
    "throw_exception",
    "type_index",
    "type_traits",
    "unordered",
    "utility",
    "variant",
    "function",
]

class BoostSerialization(ConanFile, metaclass=BoostMeta, module="serialization", boost_deps=DEPS, libs=["boost_serialization", "boost_wserialization"]):
    pass
