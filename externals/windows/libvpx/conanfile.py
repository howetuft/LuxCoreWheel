from conan import ConanFile

class Libvpx(ConanFile):
  requires= ["libvpx/1.13.1",]
  win_bash=True
