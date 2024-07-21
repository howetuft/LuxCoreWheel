:: SPDX-FileCopyrightText: 2024 Howetuft
::
:: SPDX-License-Identifier: Apache-2.0

@echo off

cd %GITHUB_WORKSPACE%

SETLOCAL ENABLEEXTENSIONS

:: Line 117
for %%a in (.) do set LUX_WINDOWS_BUILD_ROOT=%%~fa
for %%a in (support\bin) do set SUPPORT_BIN=%%~fa
for %%a in (..\LuxCore) do set LUXCORE_ROOT=%%~fa
for %%a in (..\WindowsCompileDeps) do set DEPS_DIR=%%~fa

set CMAKE_GENERATOR="Visual Studio 16 2019"
set CMAKE_TOOLSET=-T v142,host=x64
set CMAKE_PLATFORM=-A x64
set CMAKE_CXX_STANDARD=17

for %%a in (..\WindowsCompileDeps\include) do set INCLUDE_DIR=%%~fa
for %%a in (..\WindowsCompileDeps\x64\Release\lib) do set LIB_DIR=%%~fa
echo LIB_DIR: %LIB_DIR%

set DLL_OPTION=-DBUILD_LUXCORE_DLL=1

:: Line 202
set SKBUILD_CMAKE_ARGS=-G %CMAKE_GENERATOR% %CMAKE_PLATFORM% %CMAKE_TOOLSET% -D CMAKE_INCLUDE_PATH="%INCLUDE_DIR%" -D CMAKE_LIBRARY_PATH="%LIB_DIR%" -D PYTHON_LIBRARY="%LIB_DIR%" -D PYTHON_V="%PYTHON_VERSION%" -D PYTHON_INCLUDE_DIR="%INCLUDE_DIR%\Python%PYTHON_VERSION%" -D CMAKE_BUILD_TYPE=%BUILD_TYPE% %OCL_OPTION% %CUDA_OPTION% %DLL_OPTION% %MINIMAL_OPTION% %LUXCORE_ROOT%
echo SKBUILD_CMAKE_ARGS=%SKBUILD_CMAKE_ARGS%

:: Line 206
set MSBUILD_OPTS=/nologo %CPUCOUNT% /verbosity:normal /property:"Platform=%MSBUILD_PLATFORM%" /property:"Configuration=%BUILD_TYPE%" /p:WarningLevel=0

mkdir Build_CMake
cd Build_CMake

set LUXCORE_BUILD_ROOT=%CD%\LuxCore

set CMAKE_CACHE=CMakeCache.txt

:: Line 219
mkdir %LUXCORE_BUILD_ROOT%
cd /d %LUXCORE_BUILD_ROOT%
if exist %CMAKE_CACHE% del %CMAKE_CACHE%
