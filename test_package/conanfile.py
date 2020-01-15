import os

from conans import ConanFile, CMake, tools


class FlannTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {
        }
    default_options = {
        "open3d:with_visualization": False,
        "open3d:with_headless_rendering": False,
        "open3d:with_python": False,
    }


    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("*.so*", dst="bin", src="lib")

    def test(self):
        os.environ["CTEST_OUTPUT_ON_FAILURE"] = "1"

        if not tools.cross_building(self.settings):
            self.run("bin/open3d_test_package pointcloud /home/birger/tmp/multi-align/output/t_0.ply")
            # self.run("ctest")
