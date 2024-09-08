# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile
from sys import version_info as vi

DEPS = [
    "algorithm",
    "align",
    "assert",
    "bind",
    "concept_check",
    "config",
    "container_hash",
    "conversion",
    "core",
    "detail",
    "foreach",
    "function",
    "graph",
    "iterator",
    "lexical_cast",
    "mpl",
    "numeric_conversion",
    "parameter",
    "preprocessor",
    "smart_ptr",
    "static_assert",
    "throw_exception",
    "tuple",
    "type_index",
    "typeof",
    "type_traits",
    "utility",
    "integer",
    "property_map",
]

LIBS = [f"boost_python{vi.major}{vi.minor}", f"boost_numpy{vi.major}{vi.minor}"]

class BoostPython(ConanFile, metaclass=BoostMeta, module="python", boost_deps=DEPS, libs=LIBS):
    pass
