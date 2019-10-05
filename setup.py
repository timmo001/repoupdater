"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="repoupdater",
    version="0.2.5",
    author="Timmo",
    author_email="contact@timmo.xyz",
    description="",
    long_description=LONG,
    install_requires=[
        'alpinepkgs==1.0.5',
        'click==7.0',
        'PyGithub==1.43.8',
        'requests==2.22.0'
    ],
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
