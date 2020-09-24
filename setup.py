import setuptools


version = "0.0.1"


setuptools.setup(
    name="terraform-provider-freebox",
    version=version,
    description="Terraform provider to configure Freebox xDSL/FTTH modems",
    long_description=open("README.rst").read(),

    author="Vincent Jacques",
    author_email="vincent@vincent-jacques.net",
    url="http://jacquev6.github.io/terraform-provider-freebox",
    license="MIT",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],

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
