from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mkdocs-slides",
    version="0.1.0",
    author="Ian Derrington",
    author_email="Ian.Derrington@gmail.com",
    description="A MkDocs plugin for creating slide presentations within documentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ianderrington/mkdocs-slides",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={
        "mkdocs_slides": [
            "static/css/*.css",
            "static/js/*.js",
            "templates/*.html",
        ],
    },
    install_requires=requirements,
    entry_points={
        'mkdocs.plugins': [
            'slides = mkdocs_slides:SlidesPlugin',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: MkDocs",
        "Topic :: Documentation",
    ],
    python_requires=">=3.7",
) 