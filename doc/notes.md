Here are some notes about this implementation, to be transformed in a robust
documentation at the end.

# Targets
This implementation builds `pyluxcore` target and a script `pyluxcoretest`
to test it, package them into a wheel and upload the wheel to PyPi.

The wheel is build for Linux, Windows, MacOS-13 (x86) and MacOS-14 (arm64).

Please remember Linux build is specific as it occurs in a docker container, in
a manylinux image (see pypa doc). Chosen manylinux is `manylinux_2_28`.

# Tool chain
The tool chain involves:
- Github Actions
- cibuildwheel
- build
- scikit-build-core
- auditwheel (for Linux); delvewheel (for Windows) ; delocate-wheel (for MacOS)

The entry point is **.github/workflow/wheel.yml**
It triggers `cibuildwheel`, which in turns triggers `build`, which in turns
triggers `scikit-build-core` via `pyproject.toml`.

# Test
`pyluxcoretest` is also used as a minimal test for the built targets during the
CI process.

# LuxCore
LuxCore is fetched via a git submodule. Choice has been made not to fork
LuxCore but to rely on a certain commit. Small adjustements, if needed, are
made via text manipulation (sed etc.): see `.github/actions/...`

# Dependencies
In LuxCore, dependencies were provided in two forms:
- Binaries to be linked with LuxCore.
- Sources to be compiled together with LuxCore, in `deps` folder.
For binaries, the design choice is not to rely on them. For sources, we got rid
of the provided ones as soon as there was an equivalent in the deps managers we
used; but we kept a few.

We use `conan` dependencies manager. We mainly use recipes from the repo, but a
few ones were written specifically for this implementation. They are located in
`deps/conan` folder.
For caching reasons, we use `deployment` feature of `conan`: the paths we get
after deployment are more suited for caching.

# Dependency caching
Dependencies full build can take dozens of minutes, so caching is a real need.
To cache dependencies, we use `conan cache save` and `conan cache restore`
features, associated with `cache` action of Github. For Linux build, we create
a special mounted folder in the docker container to pass the cached deps forth
and back.


# Cmake
Our implementation provides its own `CMakeLists.txt` that wraps LuxCore one.
The wrapper allows to look for dependencies and set some variables.

# OpenCL, CUDA and Optix
OpenCL, Cuda and Optix uses are enabled during the build.  However, by design,
they are not linked statically by LuxCore.  Instead, they are dynamically
loaded by `pyluxcore` at runtime. This is the job of `clew` and `cuew`
dependencies, which are called by `Init` function. The enabled/disabled
features are given by `GetPlatformDesc` function; beware not to call it before
`Init`, as the result would be irrelevant.  Therefore, the needed libs
(`libOpenCL.so`, `OpenCL.dll` etc.) should be made foundable (`PATH`, `RPATH`
etc.) by the system for `pyluxcore`.

<A complement of doc "how to use OpenCL/CUDA/Optix" may be necessary>
<Containerized execution may be tricky>

# Caching
At now, we use `sccache` for caching.

Perhaps we should use `ccache` nevertheless. Although its application is more
complex than `sccache`, it is dramatically more efficient in our context of
many simultaneous jobs.  Indeed, `sccache` rapidly stumbles against Github's
rate limits when the number of concurrent builds increases, thus generating
many misses when running all the jobs we need (5 Python versions * 4 OSes). The
trickiest part of `ccache` application is for Linux wheel, where the build is
hosted in a Docker container. To address it, we may follow the tip provided
here: https://github.com/pypa/cibuildwheel/issues/1030 (many thanks to the
author).

# Conan Settings & Conf
## MacOS 13 (notes)
`compiler.cppstd` must be greater or equal than 17 (aka C++17), for
`llvm-openmp` to compile.
`os.version` is the minimal version for the target to be compatible with. We
tried to have it minimal and it's 10.13. For the delocation to succeed, we also
have to set `MACOSX_DEPLOYMENT_TARGET` environment variable to 10.13.

## Vectorization
For Intel, we stick to x86-64-v3 (Haswell, 2013), no more. For all platform
except MacOS Intel, we rely on "-O" option.
For MacOS Intel: Github runner is not standard, we have to deactivate avx2
extensions. Otherwise `pyluxcore.so` cannot be tested ("Illegal instruction").
See https://github.com/ggerganov/whisper.cpp/issues/358 and `sysctl -a
machdep.cpu`


