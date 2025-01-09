# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

# Debug linux build locally


# Script to run build locally. You need 'act' to be installed in your
# system

#export CIBW_DEBUG_KEEP_CONTAINER=TRUE
act \
  --action-offline-mode \
  --job build_wheels \
  -s GITHUB_TOKEN="$(gh auth token)" \
  --matrix os:ubuntu-latest --matrix python-minor:'13' \
  --artifact-server-path /tmp/pyluxcore

cd /tmp/pyluxcore/1/cibw-wheels-ubuntu-latest-13
unzip cibw-wheels-ubuntu-latest-13.zip

