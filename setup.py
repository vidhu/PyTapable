import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="PyTapable",
    version="0.0.2",
    author="Vidhu Bhatnagar",
    author_email="vidhu1911@gmail.com",
    description="Provides utilities to implement a hookable interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vidhu/pytapable",
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=2.7',
)
