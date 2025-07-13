#!/usr/bin/env python3
"""
Setup script for AI Migration Map Generator
FPT Software - AI-Powered System Migration Tool
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-migration-map",
    version="1.0.0",
    author="FPT Software AI Team",
    author_email="ai-migration@fpt-software.com",
    description="AI-powered system migration tool for analyzing legacy systems and generating migration maps",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/fpt-software/ai-migration-map",
    project_urls={
        "Bug Tracker": "https://github.com/fpt-software/ai-migration-map/issues",
        "Documentation": "https://github.com/fpt-software/ai-migration-map/docs",
        "Source Code": "https://github.com/fpt-software/ai-migration-map",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Documentation",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "mkdocs>=1.4.0",
            "mkdocs-material>=9.0.0",
            "mkdocstrings>=0.20.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-migration-map=cli.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": [
            "templates/*.yaml",
            "templates/*.json",
            "templates/*.md",
            "config/*.yaml",
        ],
    },
    keywords=[
        "migration",
        "ai",
        "legacy",
        "system",
        "analysis",
        "code-generation",
        "dotnet",
        "microservices",
        "modernization",
    ],
    platforms=["any"],
    license="MIT",
    zip_safe=False,
) 