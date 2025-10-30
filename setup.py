from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="csv-processor",
    version="0.1.0",
    author="Your Name",
    description="A tool for processing CSV files with product ratings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "csv-processor=csv_processor.cli:main",
        ],
    },

    