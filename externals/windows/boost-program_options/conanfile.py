# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "any",
    "assert",
    "config",
    "container_hash",
    "core",
    "detail",
    "function",
    "iterator",
    "lexical_cast",
    "mpl",
    "preprocessor",
    "smart_ptr",
    "static_assert",
    "throw_exception",
    "type_index",
    "type_traits",
    "bind",
    "tokenizer",
]

class BoostProgram_options(ConanFile, metaclass=BoostMeta, module="program_options", boost_deps=DEPS, libs=["boost_program_options"]):
    pass
