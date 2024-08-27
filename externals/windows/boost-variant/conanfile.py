# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

class BoostVariant(ConanFile, metaclass=BoostMeta, module="variant", package_type="header-library"):
    pass
