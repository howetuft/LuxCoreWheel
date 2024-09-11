# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import os
import re
from boost_helper import BoostMeta, ConanFile

DEPS = [
    "any",
    "assert",
    "bind",
    "config",
    "core",
    "format",
    "iterator",
    "mpl",
    "multi_index",
    "optional",
    "range",
    "serialization",
    "static_assert",
    "throw_exception",
    "type_traits",
]

def _post_source(self):
    print(f"BoostMeta -- Post source {self.module}")
    # Remove test build
    cmakelists_file = os.path.join(self.source_folder, "CMakeLists.txt")
    with open(cmakelists_file, encoding="utf-8") as f:
        read_data = f.read()

    with open(cmakelists_file, "w", encoding="utf-8") as f:
        f.write(f'set(BOOST_SUPERPROJECT_VERSION "{self.version}")\n')
        f.write(read_data)


class BoostProperty_tree(
    ConanFile,
    metaclass=BoostMeta,
    module="property_tree",
    boost_deps=DEPS,
    boost_post_source=_post_source
):
    pass
