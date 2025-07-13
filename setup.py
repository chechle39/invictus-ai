#!/usr/bin/env python3
"""
Setup script for AI Code Migrator - Python Version
Makes the tool installable globally via pip
"""

from setuptools import setup, find_packages
import os

# Read README for long description
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "AI-powered code migration tool"

setup(
    name="ai-migrator",
    version="1.0.0",
    description="AI-powered code migration tool with human validation",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="AI Migrator Team",
    author_email="team@aimigrator.dev",
    url="https://github.com/yourusername/ai-migrator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "click>=8.0.0",
        "rich>=10.0.0",
        "python-dotenv>=0.19.0",
        "pathspec>=0.9.0",
        "colorama>=0.4.4",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
        ],
        "web": [
            "fastapi>=0.70.0",
            "uvicorn>=0.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-migrator=ai_migrator.cli:main",
            "migrate-code=ai_migrator.cli:main",
        ],
    },
    package_data={
        "ai_migrator": [
            "prompts/*.txt",
            "templates/*.j2",
            "data/*.json",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
