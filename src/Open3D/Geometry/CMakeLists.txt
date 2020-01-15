# build
file(GLOB_RECURSE ALL_SOURCE_FILES "*.cpp")

# create object library
add_library(Geometry OBJECT ${ALL_SOURCE_FILES})
ShowAndAbortOnWarning(Geometry)

# Enforce 3rd party dependencies
add_dependencies(Geometry build_all_3rd_party_libs)

if(ENABLE_CONAN)
    target_link_libraries(Geometry PUBLIC CONAN_PKG::Eigen3)
    target_link_libraries(Geometry PUBLIC CONAN_PKG::flann)
    target_link_libraries(Geometry PUBLIC CONAN_PKG::fmt)
    target_link_libraries(Geometry PUBLIC CONAN_PKG::jsoncpp)
    target_link_libraries(Geometry PUBLIC CONAN_PKG::qhull)
    target_link_libraries(Geometry PUBLIC CONAN_PKG::tinyobjloader)
    target_link_libraries(Geometry PUBLIC CONAN_PKG::tritriintersect)
endif()
