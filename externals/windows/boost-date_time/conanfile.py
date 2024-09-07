# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "algorithm",
    "assert",
    "config",
    "core",
    "io",
    "lexical_cast",
    "numeric_conversion",
    "range",
    "smart_ptr",
    "static_assert",
    "throw_exception",
    "tokenizer",
    "type_traits",
    "utility",
    "winapi",
]

class BoostDate_time(ConanFile, metaclass=BoostMeta, module="date_time", boost_deps=DEPS, libs=["boost_date_time"]):
    pass
