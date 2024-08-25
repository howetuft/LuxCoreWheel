# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

class BoostSystem(ConanFile, metaclass=BoostMeta, module="system"):
    pass
