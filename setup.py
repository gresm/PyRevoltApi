import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyRevoltApi",
    version="0.0.1",
    author="gresm",
    author_email="not now",
    description="Package that handles Revolt api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gresm/PyRevoltApp",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
