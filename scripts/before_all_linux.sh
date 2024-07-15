# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: LGPL-3.0-or-later


# TODO Pre-download tar.gz (when it is fully established the version are OK)
# Move everything to a script
dnf -y install wget almalinux-release-devel

# Embree
EMBREE_VERSION=3.8.0  # Last version with rpm (Apr 7, 2020)
if wget -q "https://github.com/RenderKit/embree/releases/download/v${EMBREE_VERSION}/embree-${EMBREE_VERSION}.x86_64.rpm.tar.gz"
then
  tar -xvzf embree-${EMBREE_VERSION}.x86_64.rpm.tar.gz -C .
  dnf -y localinstall embree3-devel-${EMBREE_VERSION}-1.noarch.rpm
  dnf -y localinstall embree3-lib-${EMBREE_VERSION}-1.x86_64.rpm
else
  echo "Failed"
fi

# OIDN
OIDN_VERSION=1.2.4  # Last release with libtbb.so.2
if wget -q "https://github.com/RenderKit/oidn/releases/download/v${OIDN_VERSION}/oidn-${OIDN_VERSION}.x86_64.linux.tar.gz"
then
  export OIDN_DIR=oidn-${OIDN_VERSION}.x86_64.linux
  tar -xvzf oidn-${OIDN_VERSION}.x86_64.linux.tar.gz -C .
  cp ${OIDN_DIR}/bin/* /usr/bin
  mkdir /usr/share/doc/OpenImageDenoise
  cp ${OIDN_DIR}/doc/* /usr/share/doc/OpenImageDenoise
  cp -r ${OIDN_DIR}/include/OpenImageDenoise /usr/include
  cp -r ${OIDN_DIR}/lib/* /usr/lib
else
  echo "Failed"
fi
dnf -y install epel-release && /usr/bin/crb enable
dnf -y install libtiff-devel libjpeg-devel libpng-devel gtk3-devel OpenImageIO-devel OpenEXR-devel boost-devel boost-python3-devel boost-numpy3 flex tbb-devel blosc-devel

