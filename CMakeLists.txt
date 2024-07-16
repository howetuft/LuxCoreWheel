# SPDX-FileCopyrightText: 2024 Howetuft
#
# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.15...3.27)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

add_subdirectory(LuxCore)

install(TARGETS pyluxcorelib DESTINATION ${SKBUILD_PROJECT_NAME})
