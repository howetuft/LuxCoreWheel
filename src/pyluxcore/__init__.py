# ****************************************************************************
# *                                                                          *
# * Copyright 2024 Howetuft <howetuft-at-gmail-dot-com>                      *
# *                                                                          *
# * Licensed under the Apache License, Version 2.0 (the "License");          *
# * you may not use this file except in compliance with the License.         *
# * You may obtain a copy of the License at                                  *
# *                                                                          *
# * http://www.apache.org/licenses/LICENSE-2.0                               *
# *                                                                          *
# * Unless required by applicable law or agreed to in writing, software      *
# * distributed under the License is distributed on an "AS IS" BASIS,        *
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. *
# * See the License for the specific language governing permissions and      *
# * limitations under the License.                                           *
# *                                                                          *
# ****************************************************************************

import platform
from pathlib import Path
import shutil

from .pyluxcore import *

_LUXFOLDER = Path(pyluxcore.__file__).parent

_OIDN_PATHS = {
    "Linux": (_LUXFOLDER / ".." / "pyluxcore.oidn", "oidnDenoise"),
    "Windows": (_LUXFOLDER / ".." / "pyluxcore.libs", "oidnDenoise.exe"),
    "Darwin": (_LUXFOLDER / ".." / "pyluxcore.oidn", "oidnDenoise"),
}

def which_oidn():
    """Retrieve external oidn path."""
    path, executable = _OIDN_PATHS[platform.system()]
    denoiser_path = shutil.which(executable, path=path)
    return denoiser_path
