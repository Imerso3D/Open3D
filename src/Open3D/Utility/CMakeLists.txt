# build
file(GLOB_RECURSE ALL_SOURCE_FILES "*.cpp")

# create object library
add_library(Utility OBJECT ${ALL_SOURCE_FILES})
ShowAndAbortOnWarning(Utility)

# Enforce 3rd party dependencies
add_dependencies(Utility build_all_3rd_party_libs)

if(ENABLE_CONAN)
    target_link_libraries(Utility PUBLIC CONAN_PKG::Eigen3)
    target_link_libraries(Utility PUBLIC CONAN_PKG::flann)
    target_link_libraries(Utility PUBLIC CONAN_PKG::jsoncpp)
    target_link_libraries(Utility PUBLIC CONAN_PKG::fmt)
endif()
