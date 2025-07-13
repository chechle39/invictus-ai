"""
AI Migration Map Generator
FPT Software - AI-Powered System Migration Tool

A sophisticated AI-driven tool that analyzes legacy systems and generates 
comprehensive migration maps for system transitions.
"""

__version__ = "1.0.0"
__author__ = "FPT Software AI Team"
__email__ = "ai-migration@fpt-software.com"

from analyzer import SystemAnalyzer
from mapper import MigrationMapper
from config import Config

__all__ = [
    "SystemAnalyzer",
    "MigrationMapper", 
    "Config",
] 