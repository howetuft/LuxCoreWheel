# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "align",
    "bind",
    "config",
    "conversion",
    "core",
    "detail",
    "foreach",
    "function",
    "iterator",
    "lexical_cast",
    "mpl",
    "numeric_conversion",
    "preprocessor",
    "smart_ptr",
    "static_assert",
    "tuple",
    "type_traits",
    "utility",
    "integer",
    "property_map",
]

class BoostPython(ConanFile, metaclass=BoostMeta, module="python", boost_deps=DEPS):
    pass
