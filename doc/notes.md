Here are some notes about this implementation, to be transformed in a robust
documentation at the end.

# Tool chain
The tool chain involves:
- cibuildwheel
- build
- scikit-build-core
- auditwheel (for Linux); delvewheel (for Windows)

The entry point is **.github/workflow/wheel.yml**
It triggers `cibuildwheel`, which in turns triggers `build`, which in turns
triggers `scikit-build-core` via `pyproject.toml`.

# LuxCore
LuxCore is fetched via a git submodule. Choice has been made not to fork
LuxCore but to rely on a certain commit. Small adjustements, if needed, are
made via text manipulation (sed etc.): see `.github/actions/...`

# Targets
This implementation only builds `pyluxcore` target.

# Dependencies
In LuxCore, dependencies are provided in two forms:
- Binaries to be linked with LuxCore.
- Sources to be compiled together with LuxCore, in `deps` folder.
For binaries, the design choice is not to rely on them. For sources, we got rid
of the provided ones as soon as there was an equivalent in the deps managers we
used; but we kept a few.

## Linux
Linux build is made in a container based on AlmaLinux 8.  Dependencies are
provided as distro packages.  We mainly use packages from AlmaLinux, but a few
ones were missing, so imported from other sources: see `externals/linux`
folder.

## Windows
We use `conan` dependencies manager. We mainly use recipes from the repo, but a
few ones were written specifically for this implementation. They are located in
`externals/windows`. Please note local recipes are used in "editable" mode, for
caching reasons.

# Cmake
The implementation provides its own `CMakeLists.txt` that wraps LuxCore one.
The wrapper allows to look for dependencies and set some variables.

# OpenCL, CUDA and Optix
OpenCL, Cuda and Optix uses are enabled during the build.  However, by design,
they are not linked statically by LuxCore.  Instead, they are dynamically
loaded by `pyluxcore` at runtime. This the job of `clew` and `cuew`
dependencies, which are called by `Init` function. The enabled/disabled
features are given by `GetPlatformDesc` function; beware not to call it before
`Init`, as the result would be irrelevant.  Therefore, the needed libs
(`libOpenCL.so`, `OpenCL.dll` etc.) should be made foundable (`PATH`, `RPATH`
etc.) by the system for `pyluxcore`.

<A complement of doc "how to use OpenCL/CUDA/Optix" may be necessary>
<Containerized execution may be tricky>

# Caching
We use `ccache` for caching. Although its application is more complex than
`sccache`, it is dramatically more efficient in our context of many
simultaneous jobs.  Indeed, `sccache` rapidly stumbles against Github's rate
limits when the number of concurrent builds increases, thus generating many
misses when running all the jobs we need (5 Python versions * 4 OSes).  The
trickiest part of `ccache` application is for Linux wheel, where the build is
hosted in a Docker container. To address it, we follow the tip provided here:
https://github.com/pypa/cibuildwheel/issues/1030 (many thanks to the author).


