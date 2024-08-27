# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import os
import sys
here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..'))

from boost_helper import BoostMeta, ConanFile

class BoostArray(ConanFile, metaclass=BoostMeta, module="array", package_type="header-library"):
    pass
