#! /usr/bin/env python
import pathlib

import setuptools

name = "nauert"


def read_version():
    root_path = pathlib.Path(__file__).parent
    version_path = root_path / "abjadext" / name / "_version.py"
    with version_path.open() as file_pointer:
        file_contents = file_pointer.read()
    local_dict = {}
    exec(file_contents, None, local_dict)
    return local_dict["__version__"]


author = ["Josiah Wolf Oberholtzer", "Tsz Kiu Pang"]

author_email = [
    "josiah.oberholtzer@gmail.com",
    "osamupang@gmail.com",
]

description = "Nauert extends Abjad with tools for rhythmic quantization."

if __name__ == "__main__":
    setuptools.setup(
        author=", ".join(author),
        author_email=", ".join(author_email),
        classifiers=[
            "Development Status :: 3 - Alpha",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: Implementation :: CPython",
            "Topic :: Artistic Software",
        ],
        description=description,
        include_package_data=True,
        install_requires=[
            "abjad>=3.13",
        ],
        license="MIT",
        long_description=pathlib.Path("README.md").read_text(),
        keywords=", ".join(
            [
                "music composition",
                "music notation",
                "lilypond",
            ]
        ),
        name=f"abjad-ext-{name}",
        packages=["abjadext"],
        platforms="Any",
        python_requires="<3.12,>=3.10.*",
        url="http://abjad.github.io",
        version=read_version(),
    )
