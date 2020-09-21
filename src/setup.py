import setuptools

setuptools.setup(
    name="terraform-provider-freebox",
    version="0.0.1",
    install_requires=open("requirements.txt").readlines(),
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": ["terraform-provider-freebox=terraform_provider_freebox:main"],
    },
)
