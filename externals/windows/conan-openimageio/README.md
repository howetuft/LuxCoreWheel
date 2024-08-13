[ ![Download](https://api.bintray.com/packages/ppodsiadly/conan/openimageio%3Appodsiadly/images/download.svg) ](https://bintray.com/ppodsiadly/conan/openimageio%3Appodsiadly/_latestVersion)

[![Build status](https://ci.appveyor.com/api/projects/status/x2xag9l8bsh0jgd2?svg=true)](https://ci.appveyor.com/project/p-podsiadly/conan-openimageio)
[![Build status](https://api.travis-ci.org/p-podsiadly/conan-openimageio.svg)](https://travis-ci.org/p-podsiadly/conan-openimageio)


## Conan package recipe for *openimageio*

OpenImageIO is a library for reading and writing images, and a bunch of related classes, utilities, and applications.

The packages generated with this **conanfile** can be found on [Bintray](https://bintray.com/ppodsiadly/conan/openimageio%3Appodsiadly).


## For Users

### Basic setup

    $ conan install openimageio/2.1.11.2@ppodsiadly/stable

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    openimageio/2.1.11.2@ppodsiadly/stable

    [generators]
    cmake

Complete the installation of requirements for your project running:

    $ mkdir build && cd build && conan install ..

Note: It is recommended that you run conan install from a build directory and not the root of the project directory.  This is because conan generates *conanbuildinfo* files specific to a single build configuration which by default comes from an autodetected default profile located in ~/.conan/profiles/default .  If you pass different build configuration options to conan install, it will generate different *conanbuildinfo* files.  Thus, they should not be added to the root of the project, nor committed to git.


## Build and package

The following command both runs all the steps of the conan file, and publishes the package to the local system cache.  This includes downloading dependencies from "build_requires" and "requires" , and then running the build() method.

    $ conan create . ppodsiadly/testing


### Available Options
| Option           | Default           | Possible Values |
| -------------    |:----------------- |:---------------:|
| shared           | False             | [True, False]   |
| with_tools       | False             | [True, False]   |
| with_webp        | True              | [True, False]   |
| with_jpeg2000    | True              | [True, False]   |
| with_freetype    | True              | [True, False]   |
| with_opencolorio | True              | [True, False]   |


## Conan Recipe License

NOTE: The conan recipe license applies only to the files of this recipe, which can be used to build and package openexr.
It does *not* in any way apply or is related to the actual software being packaged.

[BSL-1.0](LICENSE)
