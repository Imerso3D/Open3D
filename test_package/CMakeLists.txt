cmake_minimum_required(VERSION 3.10)
project(open3d_test_package VERSION 5.1.0 LANGUAGES CXX)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(OpenMP REQUIRED)

add_executable(open3d_test_package "src/main.cpp")

target_include_directories(open3d_test_package PRIVATE ${CONAN_INCLUDE_DIRS})
target_link_directories(open3d_test_package PRIVATE ${CONAN_LIB_DIRS})

target_link_libraries(open3d_test_package PRIVATE OpenMP::OpenMP_CXX)
target_link_libraries(open3d_test_package PRIVATE ${CONAN_LIBS})

include(CTest)
enable_testing()
add_test(open3d_ctest bin/open3d_test_package)
