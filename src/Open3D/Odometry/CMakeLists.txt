# build
file(GLOB_RECURSE ALL_SOURCE_FILES "*.cpp")

# create object library
add_library(Odometry OBJECT ${ALL_SOURCE_FILES})
ShowAndAbortOnWarning(Odometry)

# Enforce 3rd party dependencies
add_dependencies(Odometry build_all_3rd_party_libs)

if(ENABLE_CONAN)
    target_link_libraries(Odometry PUBLIC CONAN_PKG::Eigen3)
    target_link_libraries(Odometry PUBLIC CONAN_PKG::fmt)
endif()
