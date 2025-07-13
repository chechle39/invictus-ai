"""
Configuration management for AI Code Migrator
"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

@dataclass
class Config:
    """Configuration class for the AI Code Migrator"""
    
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini"
    max_tokens: int = 4000
    temperature: float = 0.1
    timeout: int = 60
    
    def __post_init__(self):
        """Initialize configuration from environment variables if not provided"""
        # Load from .env file if it exists
        self._load_env_file()
        
        if not self.api_key:
            self.api_key = os.getenv('OPENAI_API_KEY')
        
        # Override with environment variables if available
        self.model = os.getenv('OPENAI_MODEL', self.model)
        self.max_tokens = int(os.getenv('OPENAI_MAX_TOKENS', self.max_tokens))
        self.temperature = float(os.getenv('OPENAI_TEMPERATURE', self.temperature))
        self.timeout = int(os.getenv('OPENAI_TIMEOUT', self.timeout))
    
    def _load_env_file(self):
        """Load environment variables from .env file"""
        env_file = Path('.env')
        if env_file.exists():
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
    
    @property
    def is_valid(self) -> bool:
        """Check if configuration is valid"""
        return bool(self.api_key)
    
    def get_openai_config(self) -> dict:
        """Get configuration dict for OpenAI client"""
        return {
            'api_key': self.api_key,
            'timeout': self.timeout
        }
