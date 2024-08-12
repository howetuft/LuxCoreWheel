# CMake variable injection for Windows

# Conan defines OpenImageIO_FOUND, whereas LuxCore
# expects OPENIMAGEIO_FOUND. We will lure LuxCore:
set(OPENIMAGEIO_FOUND "TRUE")
set(EMBREE_FOUND "TRUE")
