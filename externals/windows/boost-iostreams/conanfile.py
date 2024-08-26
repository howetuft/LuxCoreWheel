# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "assert",
    "config",
    "core",
    "detail",
    "function",
    "integer",
    "iterator",
    "mpl",
    "preprocessor",
    "range",
    "smart_ptr",
    "static_assert",
    "throw_exception",
    "type_traits",
    "utility",
    "numeric_conversion",
]

class BoostIostreams(ConanFile, metaclass=BoostMeta, module="iostreams", boost_deps=DEPS):
    pass
