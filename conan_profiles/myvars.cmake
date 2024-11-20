option(EMBREE_STACK_PROTECTOR "Embree stack protector" ON)
if (${CMAKE_PROJECT_NAME} EQUAL "embree3")
  add_compile_options(-g -fno-common)
endif()
