#!/usr/bin/env python3
"""
Switchipy Setup Script

This script handles the installation and distribution of Switchipy.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="switchipy",
    version="1.0.0",
    author="Prabin Thapa",
    author_email="prabin@example.com",
    description="XFCE Theme Switcher with automatic time-based switching",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/switchipy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Desktop Environment :: Window Managers",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.6",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "flake8>=3.8",
            "black>=21.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "switchipy=app:main",
            "switchipy-cli=switchipy_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "switchipy": ["*.md", "*.txt"],
    },
    data_files=[
        ("share/applications", ["scripts/switchipy.desktop"]),
        ("share/icons", ["scripts/switchipy.svg"]),
    ],
    keywords="xfce theme switcher dark light automatic",
    project_urls={
        "Bug Reports": "https://github.com/username/switchipy/issues",
        "Source": "https://github.com/username/switchipy",
        "Documentation": "https://github.com/username/switchipy/docs",
    },
)
