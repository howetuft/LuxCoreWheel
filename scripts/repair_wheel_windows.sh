# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

set -o pipefail

wheel=$1
dest_dir=$2
VCToolsRedistDir=`cygpath -u "$3"`


echo "Repairing:"
echo "- wheel=${wheel}"
echo "- dest_dir=${dest_dir}"
echo "- VCToolsRedistDir=${VCToolsRedistDir}"

# Find system folders
# (list folders, enclose in double quotes and concat)
# redist_paths=`find "${VCToolsRedistDir}" -type d | awk '{ print "\""$0"\""}' - | paste -s -d ":"`
redist_paths=`find "${VCToolsRedistDir}" -type d | paste -s -d ":"`

echo "Paths: ${redist_paths}"

delvewheel repair -v \
  --add-path="$GITHUB_WORKSPACE/libs" \
  --add-path="${redist_paths}" \
  -w "${dest_dir}" \
  "${wheel}"

# ;$VCToolsInstallDir
