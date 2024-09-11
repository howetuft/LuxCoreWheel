# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "algorithm",
    "any",
    "array",
    "assert",
    "bimap",
    "bind",
    "concept_check",
    "config",
    "container",
    "container_hash",
    "conversion",
    "core",
    "detail",
    "foreach",
    "function",
    "integer",
    "iterator",
    "lexical_cast",
    "math",
    "move",
    "mpl",
    "multi_index",
    "numeric_conversion",
    "optional",
    "parameter",
    "preprocessor",
    "property_map",
    "property_tree",
    "random",
    "range",
    "regex",
    "serialization",
    "smart_ptr",
    "spirit",
    "static_assert",
    "throw_exception",
    "type_index",
    "tti",
    "tuple",
    "type_traits",
    "typeof",
    "unordered",
    "utility",
    "xpressive",
]

class BoostGraph(ConanFile, metaclass=BoostMeta, module="graph", libs=["boost_graph"], boost_deps=DEPS):
    pass
