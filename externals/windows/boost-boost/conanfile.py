# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "thread",
    "program_options",
    "filesystem",
    "iostreams",
    "regex",
    "system",
    "python",
    "chrono",
    "serialization"
]

class BoostBoost(ConanFile, metaclass=BoostMeta, module="boost", boost_deps=DEPS):
    pass
