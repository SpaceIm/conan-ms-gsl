import os
from conans import ConanFile, tools

class MicrosoftGslConan(ConanFile):
    name = "ms-gsl"
    description = "Microsoft implementation of the Guidelines Support Library"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/microsoft/GSL"
    license = "MIT"
    topics = ("gsl", "guidelines", "core", "span")
    no_copy_source = True
    settings = "compiler"
    options = {
        "on_contract_violation": ["terminate", "throw", "unenforced"]
    }
    default_options = {
        "on_contract_violation": "terminate"
    }

    @property
    def _contract_map(self):
        return {
            "terminate": "GSL_TERMINATE_ON_CONTRACT_VIOLATION",
            "throw": "GSL_THROW_ON_CONTRACT_VIOLATION",
            "unenforced": "GSL_UNENFORCED_ON_CONTRACT_VIOLATION",
        }

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if tools.Version(self.version) >= "3.0.0":
            del self.options.on_contract_violation

    def configure(self):
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, 14)

    def package_id(self):
        self.info.header_only()

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "GSL-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*", dst="include", src=os.path.join(self._source_subfolder, "include"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "Microsoft.GSL"
        self.cpp_info.names["cmake_find_package_multi"] = "Microsoft.GSL"
        self.cpp_info.components["_ms-gsl"].names["cmake_find_package"] = "GSL"
        self.cpp_info.components["_ms-gsl"].names["cmake_find_package_multi"] = "GSL"
        if tools.Version(self.version) < "3.0.0":
            self.cpp_info.components["_ms-gsl"].defines = [
                self._contract_map[str(self.options.on_contract_violation)]
            ]
