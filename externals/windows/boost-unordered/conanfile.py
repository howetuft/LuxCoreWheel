# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

class BoostUnordered(ConanFile, metaclass=BoostMeta, module="unordered", package_type="header-library"):
    pass
