# build
file(GLOB_RECURSE ALL_SOURCE_FILES "*.cpp")

# create object library
add_library(Registration OBJECT ${ALL_SOURCE_FILES})
ShowAndAbortOnWarning(Registration)

# Enforce 3rd party dependencies
add_dependencies(Registration build_all_3rd_party_libs)

if(ENABLE_CONAN)
    target_link_libraries(Registration PUBLIC CONAN_PKG::Eigen3)
    target_link_libraries(Registration PUBLIC CONAN_PKG::fmt)
    target_link_libraries(Registration PUBLIC CONAN_PKG::jsoncpp)
endif()
