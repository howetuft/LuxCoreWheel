# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

echo "BEFORE ALL LINUX"

## dnf configuration
#echo "cachedir = /host/home/runner/cache/dnf" >> /etc/dnf/dnf.conf
# dnf -y install flex

# sccache
echo "Installing sccache"
tar -xzf /project/externals/linux/sccache-v0.8.1-x86_64-unknown-linux-musl.tar.gz -C .
mv sccache-v0.8.1-x86_64-unknown-linux-musl/sccache /usr/bin

# Install Ninja
echo "Installing ninja"
pip install ninja
