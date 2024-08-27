# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

from boost_helper import BoostMeta, ConanFile

class BoostConcept_check(ConanFile, metaclass=BoostMeta, module="concept_check", package_type="header-library"):
    pass
