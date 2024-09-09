# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "algorithm",
    "any",
    "array",
    "assert",
    "concept",
    "concept_check",
    "config",
    "detail",
    "foreach",
    "function",
    "integer",
    "iterator",
    "math",
    "mpl",
    "optional",
    "parameter",
    "property_map",
    "range",
    "serialization",
    "smart_ptr",
    "static_assert",
    "throw_exception",
    "tuple",
    "type_traits",
    "typeof",
    "unordered",
    "utility",
]

class BoostGraph(ConanFile, metaclass=BoostMeta, module="graph", boost_deps=DEPS):
    pass
