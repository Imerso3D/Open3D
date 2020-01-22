import os

from conans import ConanFile, CMake, tools
from conans.tools import os_info, SystemPackageTool


class TinyobjloaderConan(ConanFile):
    version = "0.8.0"

    name = "open3d"
    license = "https://github.com/IntelVCL/Open3D/raw/master/LICENSE"
    description = "Open3D: A Modern Library for 3D Data Processing http://www.open3d.org (Forked for use with Ubitrack"
    url = "https://github.com/ulricheck/Open3D"
    settings = "os", "compiler", "build_type", "arch", "python_version"
    generators = "pkg_config", "cmake"
    short_paths = True
    exports_sources = (
        "*",
        "!build",
        "!*-build-*",
        "!conan*",
        "!test_package",
        "!graph_info.json",
        "!imerso_library.cmake",
        "!.idea",
        "!test",
    )

    requires = (
        "eigen/3.3.7@conan/stable",
        "tritriintersect/0.1.0@imerso/master",
        "rply/1.1.4@imerso/master",
        "lzf/3.6.0@imerso/master",
        "jsoncpp/1.9.0@theirix/stable",
        "libjpeg-turbo/2.0.2@bincrafters/stable",
        "qhull/7.3.2@imerso/master",
        "libpng/1.6.34@bincrafters/stable",
        "flann/1.9.1@imerso/master",
        "tinyobjloader/2.0.0-rc1@imerso/master",
        "fmt/5.3.0@bincrafters/stable",
        "tinygltf/2.2.0@imerso/master",
    )

    options = {
        "fPIC": [True, False],
        "shared": [True, False],
        "with_visualization": [True, False],
        "with_headless_rendering": [True, False],
        "with_python": [True, False],
    }

    default_options = {
        "fPIC": True,
        "shared": False,
        "with_visualization": False,
        "with_headless_rendering": False,
        "with_python": False,
    }

    @property
    def _source_subfolder(self):
        return "."

    def system_requirements(self):
        installer = SystemPackageTool()

        if os_info.linux_distro == "ubuntu" and self.settings.compiler == "clang":
            installer.install("libomp-dev")

        if self.options.with_visualization:
            if os_info.linux_distro == "ubuntu":
                installer.install("xorg-dev")
                installer.install("libglu1-mesa-dev")
                installer.install("libgl1-mesa-glx")

        if self.options.with_headless_rendering:
            if os_info.linux_distro == "ubuntu":
                installer.install("libosmesa6-dev")

    def requirements(self):
        if self.options.with_visualization:
            self.requires("tinyfd/3.4.1@imerso/master")
            # self.requires("glfw/3.3@bincrafters/stable")
            # self.requires("glew/2.1.0@bincrafters/stable")
            # self.requires("mesa/0.1@imerso/master")

        if self.options.with_python:
            self.requires("pybind11/2.3.0@conan/stable")
            self.requires("tinyfd/3.4.1@imerso/master")
            self.requires("lz4/1.8.3@bincrafters/stable")

    def configure_cmake(self):
        cmake = CMake(self)

        if "CCACHE" in os.environ:
            cmake.definitions["CMAKE_CXX_COMPILER_LAUNCHER"] = os.environ["CCACHE"]

        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        cmake.definitions["ENABLE_CONAN"] = True

        # Third party dependencies
        cmake.definitions["BUILD_EIGEN3"] = False
        cmake.definitions["BUILD_FLANN"] = False
        cmake.definitions["BUILD_FMT"] = False
        cmake.definitions["BUILD_GLEW"] = False
        cmake.definitions["BUILD_GLFW"] = False
        cmake.definitions["BUILD_JPEG"] = False
        cmake.definitions["BUILD_JSONCPP"] = False
        cmake.definitions["BUILD_LIBREALSENSE"] = False
        cmake.definitions["BUILD_LZF"] = False
        cmake.definitions["BUILD_PNG"] = False
        cmake.definitions["BUILD_PYBIND11"] = False
        cmake.definitions["BUILD_PYBIND11"] = False
        cmake.definitions["BUILD_QHULL"] = False
        cmake.definitions["BUILD_TINYOBJLOADER"] = False
        cmake.definitions["BUILD_RPLY"] = False
        cmake.definitions["BUILD_TINYFILEDIALOGS"] = False
        cmake.definitions["BUILD_TINYGLTF"] = False
        cmake.definitions["BUILD_TRIINTERSECT"] = False

        cmake.definitions["EIGEN3_FOUND"] = True
        cmake.definitions["GLEW_FOUND"] = True
        cmake.definitions["GLFW_FOUND"] = True
        cmake.definitions["JPEG_FOUND"] = True
        cmake.definitions["JSONCPP_FOUND"] = True
        cmake.definitions["LIBREALSENSE_FOUND"] = True
        cmake.definitions["PNG_FOUND"] = True
        cmake.definitions["PYBIND11_FOUND"] = True
        cmake.definitions["PYBIND11_FOUND"] = True
        cmake.definitions["QHULL_FOUND"] = True
        cmake.definitions["TINYFILEDIALOGS_FOUND"] = True

        # Open3d targets
        cmake.definitions["BUILD_CPP_EXAMPLES"] = False
        cmake.definitions["BUILD_PYTHON_MODULE"] = False
        cmake.definitions["BUILD_TOOLS"] = False
        cmake.definitions["BUILD_UNIT_TESTS"] = False
        cmake.definitions["BUILD_VISUALIZATION"] = False

        cmake.definitions["ENABLE_HEADLESS_RENDERING"] = False
        cmake.definitions["ENABLE_JUPYTER"] = False

        if self.options.with_visualization:
            cmake.definitions["BUILD_VISUALIZATION"] = True
            cmake.definitions["BUILD_TOOLS"] = True
            cmake.definitions["BUILD_GLEW"] = True
            cmake.definitions["BUILD_GLFW"] = True

        if self.options.with_headless_rendering:
            cmake.definitions["ENABLE_HEADLESS_RENDERING"] = True

        if self.options.with_python:
            if not (self.options.with_visualization):
                raise Exception("Need with_visualization when using with_python")

            cmake.definitions["BUILD_PYTHON_MODULE"] = True

        cmake.configure(source_folder=self._source_subfolder)

        return cmake

    def build(self):
        cmake = cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = cmake = self.configure_cmake()
        cmake.install()

        if self.options.with_python:
            self.copy(
                "*open3d*python*.so", dst="python_package/open3d", keep_path=False
            )
            self.copy("*open3d/*.py", dst="python_package/open3d", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if self.options.with_python:
            self.env_info.PYTHONPATH.append(
                os.path.join(self.package_folder, "python_package")
            )

        if self.options.with_python and not self.in_local_cache:
            self.env_info.PYTHONPATH.append(
                os.path.join(
                    self.package_folder,
                    "build",
                    self.settings.compiler.value,
                    self.settings.build_type.value,
                )
            )

        if self.settings.compiler == "gcc":
            self.cpp_info.libs.append("gomp")
