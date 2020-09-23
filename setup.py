import setuptools


version = "0.0.1"


setuptools.setup(
    name="terraform-provider-freebox",
    version=version,
    install_requires=open("requirements.txt").readlines(),
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": ["terraform-provider-freebox=terraform_provider_freebox:main"],
    },
    command_options={
        "build_sphinx": {
            "version": ("setup.py", version),
            "release": ("setup.py", version),
            "source_dir": ("setup.py", "development/doc"),
        },
    },
)
