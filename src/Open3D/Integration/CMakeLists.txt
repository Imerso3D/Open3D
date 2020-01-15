# build
file(GLOB_RECURSE ALL_SOURCE_FILES "*.cpp")

# create object library
add_library(Integration OBJECT ${ALL_SOURCE_FILES})
ShowAndAbortOnWarning(Integration)

# Enforce 3rd party dependencies
add_dependencies(Integration build_all_3rd_party_libs)

if(ENABLE_CONAN)
    target_link_libraries(Integration PUBLIC CONAN_PKG::Eigen3)
    target_link_libraries(Integration PUBLIC CONAN_PKG::fmt)
endif()
