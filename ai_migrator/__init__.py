"""
AI Code Migrator - Python Package
A powerful, AI-driven code migration tool with human validation
"""

__version__ = "1.0.0"
__author__ = "AI Migrator Team"
__email__ = "team@aimigrator.dev"
__description__ = "AI-powered code migration tool with human validation"

from .migrator import CodeMigrator
from .validator import HumanValidator
from .config import Config

__all__ = ['CodeMigrator', 'HumanValidator', 'Config']
