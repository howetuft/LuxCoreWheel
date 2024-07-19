# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

echo "BEFORE ALL LINUX"

# dnf configuration
echo "cachedir = /host/home/runner/cache/dnf" >> /etc/dnf/dnf.conf

# sccache
echo "Installing sccache"
tar -xzf /project/externals/linux/sccache-v0.8.1-x86_64-unknown-linux-musl.tar.gz -C .
mv sccache-v0.8.1-x86_64-unknown-linux-musl/sccache /usr/bin

# Embree
echo "Installing embree"
EMBREE_VERSION=3.8.0  # Last version with rpm (Apr 7, 2020)
tar -xzf /project/externals/linux/embree-${EMBREE_VERSION}.x86_64.rpm.tar.gz -C .
dnf -y localinstall embree3-devel-${EMBREE_VERSION}-1.noarch.rpm
dnf -y localinstall embree3-lib-${EMBREE_VERSION}-1.x86_64.rpm

# OIDN
echo "Installing OIDN"
OIDN_VERSION=1.2.4  # Last release with libtbb.so.2
OIDN_DIR=oidn-${OIDN_VERSION}.x86_64.linux
tar -xzf /project/externals/linux/oidn-${OIDN_VERSION}.x86_64.linux.tar.gz -C .
cp ${OIDN_DIR}/bin/* /usr/bin
mkdir /usr/share/doc/OpenImageDenoise
cp ${OIDN_DIR}/doc/* /usr/share/doc/OpenImageDenoise
cp -r ${OIDN_DIR}/include/OpenImageDenoise /usr/include
cp -r ${OIDN_DIR}/lib/* /usr/lib

# Distro Packages
dnf -y install epel-release && /usr/bin/crb enable
dnf -y install libtiff-devel libjpeg-devel libpng-devel gtk3-devel OpenImageIO-devel OpenEXR-devel boost-devel boost-python3-devel boost-numpy3 flex tbb-devel blosc-devel

