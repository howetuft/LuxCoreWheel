# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

import os
import re
from boost_helper import BoostMeta, ConanFile

DEPS = [
    "assert",
    "concept_check",
    "config",
    "core",
    "integer",
    "lexical_cast",
    "predef",
    "random",
    "range",
    "static_assert",
    "throw_exception",
]

def _post_source(self):
    print(f"BoostMeta -- Post source {self.module}")
    # Remove test build
    cmakelists_file = os.path.join(self.source_folder, "CMakeLists.txt")
    with open(cmakelists_file, encoding="utf-8") as f:
        read_data = f.read()

    write_data = re.sub(r"(add_subdirectory\(test\))", "", read_data)
    write_data = re.sub(r"(include\(CTest\))", "", write_data)

    with open(cmakelists_file, "w", encoding="utf-8") as f:
        f.write(write_data)


class BoostMath(
    ConanFile,
    metaclass=BoostMeta,
    module="math",
    boost_deps=DEPS,
    boost_post_source=_post_source
):
    pass
