"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="repoupdater",
    version="0.1.3",
    author="Timmo",
    author_email="contact@timmo.xyz",
    description="",
    long_description=LONG,
    install_requires=['alpinepkgs', 'click', 'PyGithub>=1.43.4', 'requests'],
    long_description_content_type="text/markdown",
    url="https://github.com/timmo001/repoupdater",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'repoupdater = repoupdater.cli:cli'
        ]
    }
)
