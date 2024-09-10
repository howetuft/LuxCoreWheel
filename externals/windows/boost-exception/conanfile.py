# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

DEPS = [
    "assert",
]

class BoostException(ConanFile, metaclass=BoostMeta, module="exception", boost_deps=DEPS, ):
    pass
