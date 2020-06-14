import setuptools


with open("pytapable/version.py", "r") as f:
    __version__ = None
    exec(f.read())  # evaluate to fill in __verison__

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="PyTapable",
    version=__version__,
    author="Vidhu Bhatnagar",
    author_email="vidhu1911@gmail.com",
    description="Provides utilities to implement a hookable interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vidhu/pytapable",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
)
