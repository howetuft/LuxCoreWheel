# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

class BoostIntrusive(ConanFile, metaclass=BoostMeta, module="intrusive"):
    pass
