# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "algorithm",
    "assert",
    "atomic",
    "bind",
    "chrono",
    "concept_check",
    "config",
    "container",
    "container_hash",
    "core",
    "date_time",
    "detail",
    "exception",
    "function",
    "integer",
    "intrusive",
    "io",
    "iterator",
    "move",
    "mpl",
    "numeric_conversion",
    "optional",
    "predef",
    "preprocessor",
    "ratio",
    "smart_ptr",
    "static_assert",
    "system",
    "throw_exception",
    "tuple",
    "type_index",
    "type_traits",
    "utility",
    "winapi",
    "lexical_cast",
]

class BoostThread(ConanFile, metaclass=BoostMeta, module="thread", boost_deps=DEPS, libs=["boost_thread"]):
    pass
