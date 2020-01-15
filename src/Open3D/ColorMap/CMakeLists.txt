# build
file(GLOB_RECURSE ALL_SOURCE_FILES "*.cpp")

# create object library
add_library(ColorMap OBJECT ${ALL_SOURCE_FILES})
ShowAndAbortOnWarning(ColorMap)

# Enforce 3rd party dependencies
add_dependencies(ColorMap build_all_3rd_party_libs)

if(ENABLE_CONAN)
    target_link_libraries(ColorMap PUBLIC CONAN_PKG::Eigen3)
    target_link_libraries(ColorMap PUBLIC CONAN_PKG::fmt)
    target_link_libraries(ColorMap PUBLIC CONAN_PKG::jsoncpp)
endif()
