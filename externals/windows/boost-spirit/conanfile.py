# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

class BoostSpirit(ConanFile, metaclass=BoostMeta, module="spirit", package_type="header-library"):
    pass
