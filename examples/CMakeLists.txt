# CPP examples
if (BUILD_CPP_EXAMPLES)
    add_subdirectory(Cpp)
endif ()

# Python examples
if (BUILD_PYTHON_MODULE AND NOT ENABLE_CONAN)
    add_subdirectory(Python)
endif ()
