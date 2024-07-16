# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

echo "BEFORE ALL LINUX"

echo $ACTIONS_CACHE_URL
echo $ACTIONS_RUNTIME_TOKEN

# sccache
tar -xvzf /project/externals/linux/sccache-v0.8.1-x86_64-unknown-linux-musl.tar.gz -C .
mv sccache-v0.8.1-x86_64-unknown-linux-musl/sccache /usr/bin
export SCCACHE_DIRECT=1
export SCCACHE_GHA_ENABLED=1
sccache --show-stats

# Embree
EMBREE_VERSION=3.8.0  # Last version with rpm (Apr 7, 2020)
tar -xvzf /project/externals/linux/embree-${EMBREE_VERSION}.x86_64.rpm.tar.gz -C .
dnf -y localinstall embree3-devel-${EMBREE_VERSION}-1.noarch.rpm
dnf -y localinstall embree3-lib-${EMBREE_VERSION}-1.x86_64.rpm

# OIDN
OIDN_VERSION=1.2.4  # Last release with libtbb.so.2
OIDN_DIR=oidn-${OIDN_VERSION}.x86_64.linux
tar -xvzf /project/externals/linux/oidn-${OIDN_VERSION}.x86_64.linux.tar.gz -C .
cp ${OIDN_DIR}/bin/* /usr/bin
mkdir /usr/share/doc/OpenImageDenoise
cp ${OIDN_DIR}/doc/* /usr/share/doc/OpenImageDenoise
cp -r ${OIDN_DIR}/include/OpenImageDenoise /usr/include
cp -r ${OIDN_DIR}/lib/* /usr/lib

dnf -y install epel-release && /usr/bin/crb enable
dnf -y install libtiff-devel libjpeg-devel libpng-devel gtk3-devel OpenImageIO-devel OpenEXR-devel boost-devel boost-python3-devel boost-numpy3 flex tbb-devel blosc-devel

