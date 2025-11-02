#!/usr/bin/env python3
"""
Terminal Chat - Setup Configuration
Secure encrypted terminal-based chat application
"""

from setuptools import setup, find_packages
import os

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from a single source
VERSION = "1.2.0"

setup(
    name="terminal-chat",
    version=VERSION,
    author="Terminal Chat Team",
    description="Secure encrypted terminal-based chat with file sharing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/Terminal-Chat-Program",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=41.0.0",
    ],
    entry_points={
        "console_scripts": [
            "terminal-chat=lib.launcher:main",
        ],
    },
    include_package_data=True,
    package_data={
        "lib": ["*.py"],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/Terminal-Chat-Program/issues",
        "Source": "https://github.com/yourusername/Terminal-Chat-Program",
        "Documentation": "https://github.com/yourusername/Terminal-Chat-Program/blob/main/docs/",
    },
)