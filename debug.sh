# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

# Debug linux build locally


# Script to run build locally for Linux.
# You need 'act' to be installed in your system

#export CIBW_DEBUG_KEEP_CONTAINER=TRUE

python_minor=13
zipfolder=/tmp/pyluxcore/1/cibw-wheels-ubuntu-latest-${python_minor}

act \
  --action-offline-mode \
  --job build_wheels \
  -s GITHUB_TOKEN="$(gh auth token)" \
  --matrix os:ubuntu-latest \
  --matrix python-minor:$python_minor \
  --artifact-server-path /tmp/pyluxcore \
  | tee /tmp/pyluxcore.log \
  && unzip -o ${zipfolder}/cibw-wheels-ubuntu-latest-13.zip -d ${zipfolder}

