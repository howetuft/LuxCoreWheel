# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "algorithm",
    "any",
    "array",
]

class BoostGraph(ConanFile, metaclass=BoostMeta, module="graph", boost_deps=DEPS):
    pass
