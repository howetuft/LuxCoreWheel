# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "assert",
    "atomic",
    "bind",
    "chrono",
    "concept_check",
    "config",
    "container",
    "container_hash",
    "core",
    "function",
    "intrusive",
    "io",
    "iterator",
    "move",
    "optional",
    "predef",
    "preprocessor",
    "smart_ptr",
    "static_assert",
    "throw_exception",
    "tuple",
    "type_traits",
    "utility",
    "winapi",
    "algorithm",
    "lexical_cast",
]

class BoostThread(ConanFile, metaclass=BoostMeta, module="thread", boost_deps=DEPS, libs=["boost_thread"]):
    pass
