"""
Configuration management for AI Migration Map Generator
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
from pydantic import BaseModel, Field


class AnalysisConfig(BaseModel):
    """Configuration for system analysis"""
    max_file_size: int = Field(default=10000, description="Maximum file size in bytes")
    supported_languages: List[str] = Field(
        default=["csharp", "java", "python", "javascript", "typescript"],
        description="Supported programming languages"
    )
    ignore_patterns: List[str] = Field(
        default=["*.log", "node_modules/*", "bin/*", "obj/*", ".git/*"],
        description="File patterns to ignore during analysis"
    )
    analysis_depth: str = Field(
        default="medium", 
        description="Analysis depth: light, medium, deep"
    )


class GenerationConfig(BaseModel):
    """Configuration for migration map generation"""
    default_template: str = Field(
        default="dotnet-framework-to-core",
        description="Default migration template"
    )
    output_format: str = Field(
        default="markdown",
        description="Output format: markdown, json, yaml"
    )
    include_tests: bool = Field(default=True, description="Include test generation")
    include_documentation: bool = Field(default=True, description="Include documentation")
    include_timeline: bool = Field(default=True, description="Include timeline estimation")


class ValidationConfig(BaseModel):
    """Configuration for validation and quality assurance"""
    enable_code_review: bool = Field(default=True, description="Enable AI code review")
    enable_test_generation: bool = Field(default=True, description="Enable test generation")
    quality_threshold: float = Field(
        default=0.8, 
        description="Minimum quality score (0.0-1.0)"
    )
    security_scan: bool = Field(default=True, description="Enable security scanning")


@dataclass
class Config:
    """Main configuration class for AI Migration Map Generator"""
    
    # OpenAI Configuration
    api_key: Optional[str] = None
    model: str = "gpt-4"
    max_tokens: int = 8000
    temperature: float = 0.1
    timeout: int = 300
    
    # Analysis Configuration
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
    
    # Generation Configuration  
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    
    # Validation Configuration
    validation: ValidationConfig = field(default_factory=ValidationConfig)
    
    # Migration Templates
    templates_path: Path = field(default_factory=lambda: Path("templates"))
    
    def __post_init__(self):
        """Initialize configuration from environment variables and config files"""
        self._load_env_variables()
        self._load_config_file()
        self._validate_config()
    
    def _load_env_variables(self):
        """Load configuration from environment variables"""
        # OpenAI settings
        if not self.api_key:
            self.api_key = os.getenv('OPENAI_API_KEY')
        
        self.model = os.getenv('OPENAI_MODEL', self.model)
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', self.max_tokens))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', self.temperature))
        self.timeout = int(os.getenv('MIGRATION_TIMEOUT', self.timeout))
        
        # Analysis settings
        if os.getenv('MAX_FILE_SIZE'):
            self.analysis.max_file_size = int(os.getenv('MAX_FILE_SIZE'))
        
        # Generation settings
        if os.getenv('DEFAULT_TEMPLATE'):
            self.generation.default_template = os.getenv('DEFAULT_TEMPLATE')
        
        if os.getenv('OUTPUT_FORMAT'):
            self.generation.output_format = os.getenv('OUTPUT_FORMAT')
    
    def _load_config_file(self):
        """Load configuration from config.yaml file"""
        config_files = [
            Path("config.yaml"),
            Path("config.yml"),
            Path.home() / ".ai-migration-map" / "config.yaml",
        ]
        
        for config_file in config_files:
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                    
                    # Update analysis config
                    if 'analysis' in config_data:
                        for key, value in config_data['analysis'].items():
                            if hasattr(self.analysis, key):
                                setattr(self.analysis, key, value)
                    
                    # Update generation config
                    if 'generation' in config_data:
                        for key, value in config_data['generation'].items():
                            if hasattr(self.generation, key):
                                setattr(self.generation, key, value)
                    
                    # Update validation config
                    if 'validation' in config_data:
                        for key, value in config_data['validation'].items():
                            if hasattr(self.validation, key):
                                setattr(self.validation, key, value)
                    
                    break
                except Exception as e:
                    print(f"Warning: Could not load config file {config_file}: {e}")
    
    def _validate_config(self):
        """Validate configuration settings"""
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        if self.max_tokens < 1000 or self.max_tokens > 32000:
            raise ValueError("max_tokens must be between 1000 and 32000")
        
        if self.temperature < 0.0 or self.temperature > 2.0:
            raise ValueError("temperature must be between 0.0 and 2.0")
        
        if self.validation.quality_threshold < 0.0 or self.validation.quality_threshold > 1.0:
            raise ValueError("quality_threshold must be between 0.0 and 1.0")
    
    @property
    def is_valid(self) -> bool:
        """Check if configuration is valid"""
        try:
            self._validate_config()
            return True
        except ValueError:
            return False
    
    def get_openai_config(self) -> Dict[str, Any]:
        """Get configuration dict for OpenAI client"""
        return {
            'api_key': self.api_key,
            'timeout': self.timeout
        }
    
    def save_config(self, file_path: Path):
        """Save current configuration to file"""
        config_data = {
            'analysis': self.analysis.dict(),
            'generation': self.generation.dict(),
            'validation': self.validation.dict(),
            'openai': {
                'model': self.model,
                'max_tokens': self.max_tokens,
                'temperature': self.temperature,
                'timeout': self.timeout
            }
        }
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)
    
    def get_migration_templates(self) -> List[str]:
        """Get available migration templates"""
        if not self.templates_path.exists():
            return []
        
        templates = []
        for template_file in self.templates_path.glob("*.yaml"):
            templates.append(template_file.stem)
        
        return templates 