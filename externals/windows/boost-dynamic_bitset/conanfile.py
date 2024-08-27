# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

class BoostDynamic_bitset(ConanFile, metaclass=BoostMeta, module="dynamic_bitset", package_type="header-library"):
    pass
