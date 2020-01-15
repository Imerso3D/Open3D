# Build
file(GLOB_RECURSE CLASS_IO_SOURCE_FILES "ClassIO/*.cpp")
file(GLOB_RECURSE FILE_FORMAT_SOURCE_FILES "FileFormat/*.cpp")
set(IO_ALL_SOURCE_FILES ${CLASS_IO_SOURCE_FILES} ${FILE_FORMAT_SOURCE_FILES})

if (NOT ENABLE_CONAN)
    file(GLOB         RPLY_SOURCE_FILES "../../../3rdparty/rply/*.c")
    file(GLOB         LIBLZF_SOURCE_FILES "../../../3rdparty/liblzf/*.c")
endif ()

if (BUILD_AZURE_KINECT)
    file(GLOB_RECURSE SENSOR_SOURCE_FILES "Sensor/*.cpp")
    set(IO_ALL_SOURCE_FILES ${IO_ALL_SOURCE_FILES} ${SENSOR_SOURCE_FILES})
endif ()

# Create object library
add_library(IO OBJECT
            ${IO_ALL_SOURCE_FILES}
            ${RPLY_SOURCE_FILES}
            ${LIBLZF_SOURCE_FILES})
ShowAndAbortOnWarning(IO)

# Enforce 3rd party dependencies
add_dependencies(IO build_all_3rd_party_libs)

if(ENABLE_CONAN)
    target_link_libraries(IO PUBLIC CONAN_PKG::Eigen3)
    target_link_libraries(IO PUBLIC CONAN_PKG::fmt)
    target_link_libraries(IO PUBLIC CONAN_PKG::jsoncpp)
    target_link_libraries(IO PUBLIC CONAN_PKG::libjpeg-turbo)
    target_link_libraries(IO PUBLIC CONAN_PKG::libpng)
    target_link_libraries(IO PUBLIC CONAN_PKG::lzf)
    target_link_libraries(IO PUBLIC CONAN_PKG::rply)
    target_link_libraries(IO PUBLIC CONAN_PKG::stb)
    target_link_libraries(IO PUBLIC CONAN_PKG::tinygltf)
    target_link_libraries(IO PUBLIC CONAN_PKG::tinyobjloader)
endif()
