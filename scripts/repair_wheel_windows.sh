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

pip install delvewheel

# Find system folders
# (list folders, enclose in double quotes and concat)
redist_paths=`find "${VCToolsRedistDir}" -type d | paste -s -d ":"`

echo "Paths: ${redist_paths}"

delvewheel repair -v \
  --add-path="$GITHUB_WORKSPACE/libs" \
  --add-path="${redist_paths}" \
  --add-path="C:/Users/runneradmin/full_deploy/host/onetbb/${TBB_VERSION}/Release/x86_64/bin" \
  --add-path="C:/Users/runneradmin/full_deploy/host/oidn/${OIDN_VERSION}/Release/x86_64/bin" \
  --add-path="C:/Users/runneradmin/full_deploy/host/embree3/${EMBREE3_VERSION}/Release/x86_64/bin" \
  -w "${dest_dir}" \
  "${wheel}"

# Rename oidnDenoise
pip install wheel
dest_dir2=$(cygpath "${dest_dir}")
files=$(ls -1 ${dest_dir2}/*.whl)
# There should be only one wheel, but strictly speaking, we need a loop
for filename in $files;
do
  python $GITHUB_WORKSPACE/scripts/recompose_wheel_windows.py -- ${filename}
done
