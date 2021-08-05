from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="azcam-flaskserver",
    version="21.2.0",
    description="azcam extension for flask web server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Michael Lesser",
    author_email="mlesser@arizona.edu",
    keywords="python",
    packages=find_packages(),
    zip_safe=False,
    url="https://mplesser.github.io/azcam/",
    install_requires=["azcam"],
    include_package_data=True,
)
