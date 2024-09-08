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
    "random",
    "range",
    "smart_ptr",
    "static_assert",
    "throw_exception",
    "type_traits",
    "utility",
    "numeric_conversion",
]

class BoostIostreams(ConanFile, metaclass=BoostMeta, module="iostreams", boost_deps=DEPS, other_deps=["zlib/1.3.1", "bzip2/1.0.8"], libs=["boost_iostreams"]):
    pass
