# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "assert",
    "config",
    "core",
    "integer",
    "move",
    "mpl",
    "predef",
    "ratio",
    "static_assert",
    "throw_exception",
    "type_traits",
    "typeof",
    "utility",
    "winapi",
]

class BoostChrono(ConanFile, metaclass=BoostMeta, module="chrono", boost_deps=DEPS, libs=["boost_chrono"]):
    pass
