# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "any",
    "assert",
    "bind",
    "concept_check",
    "config",
    "container_hash",
    "core",
    "detail",
    "function",
    "integer",
    "iterator",
    "lexical_cast",
    "mpl",
    "preprocessor",
    "range",
    "smart_ptr",
    "static_assert",
    "throw_exception",
    "type_index",
    "type_traits",
    "tokenizer",
]

class BoostProgram_options(ConanFile, metaclass=BoostMeta, module="program_options", boost_deps=DEPS, libs=["boost_program_options"]):
    pass
