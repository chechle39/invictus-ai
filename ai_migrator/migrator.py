"""
Core migration logic for AI Code Migrator
"""

import re
from pathlib import Path
from typing import Optional
from openai import OpenAI

from .config import Config

class CodeMigrator:
    """Main code migration engine using OpenAI"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(**config.get_openai_config())
        
    def migrate(self, source_code: str, source_lang: Optional[str], 
                target_lang: str, input_file: str) -> str:
        """
        Migrate source code from one language to another using OpenAI
        
        Args:
            source_code: The source code to migrate
            source_lang: Source language (None for auto-detection)
            target_lang: Target language
            input_file: Original file path for context
            
        Returns:
            Migrated code as string
        """
        
        # Auto-detect source language if not provided
        if not source_lang:
            source_lang = self._detect_language(input_file, source_code)
        
        # Build migration prompt
        prompt = self._build_migration_prompt(source_code, source_lang, target_lang)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert software engineer specializing in code migration. "
                                 f"Convert code accurately while maintaining functionality and following "
                                 f"{target_lang} best practices. Return only clean code without explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            
            migrated_code = response.choices[0].message.content
            
            # Clean up the response
            return self._clean_ai_response(migrated_code)
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def apply_fix(self, code: str, fix_instructions: str, 
                  source_lang: str, target_lang: str) -> str:
        """
        Apply custom fix instructions to existing code
        
        Args:
            code: The code to fix
            fix_instructions: User's fix instructions
            source_lang: Original source language
            target_lang: Target language
            
        Returns:
            Fixed code as string
        """
        
        prompt = f"""Fix the following {target_lang} code based on user instructions.

Current {target_lang} code:
```{target_lang}
{code}
```

User's fix instructions:
{fix_instructions}

Requirements:
- Apply the requested fixes
- Maintain code functionality
- Follow {target_lang} best practices
- Return only the corrected code

Fixed code:"""

        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a code fixing expert. Apply user instructions precisely "
                                 "and return only clean, working code without explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
            )
            
            fixed_code = response.choices[0].message.content
            return self._clean_ai_response(fixed_code)
            
        except Exception as e:
            raise Exception(f"Fix application failed: {str(e)}")
    
    def _detect_language(self, file_path: str, source_code: str) -> str:
        """Auto-detect programming language from file extension and content"""
        
        # First try file extension
        path = Path(file_path)
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.cpp': 'cpp',
            '.c': 'c',
            '.php': 'php'
        }
        
        detected = extension_map.get(path.suffix.lower())
        if detected:
            return detected
        
        # Fallback to content analysis
        if 'def ' in source_code and 'import ' in source_code:
            return 'python'
        elif 'function ' in source_code and ('var ' in source_code or 'let ' in source_code):
            return 'javascript'
        elif 'public class' in source_code and 'public static void main' in source_code:
            return 'java'
        elif 'using System' in source_code and 'namespace ' in source_code:
            return 'csharp'
        
        return 'unknown'
    
    def _build_migration_prompt(self, source_code: str, source_lang: str, target_lang: str) -> str:
        """Build the migration prompt for OpenAI"""
        
        return f"""Convert the following {source_lang} code to {target_lang}.

Requirements:
- Maintain exact same functionality
- Use idiomatic {target_lang} patterns and conventions
- Handle imports/dependencies appropriately for {target_lang}
- Add appropriate error handling
- Follow {target_lang} best practices and naming conventions
- Preserve comments and documentation
- Ensure the code is production-ready

Source Code ({source_lang}):
```{source_lang}
{source_code}
```

Convert this to clean, production-ready {target_lang} code:"""
    
    def _clean_ai_response(self, response: str) -> str:
        """Clean up AI response to extract only the code"""
        
        # Remove markdown code blocks
        response = re.sub(r'```[\w]*\n', '', response)
        response = re.sub(r'```', '', response)
        
        # Remove common AI explanatory phrases
        cleanup_patterns = [
            r'^Here is the .+ version.*?:\s*',
            r'^Here\'s the .+ version.*?:\s*',
            r'^This .+ code maintains.*?\n',
            r'^The .+ code maintains.*?\n',
            r'.*uses idiomatic .+ patterns.*\n',
            r'.*handles errors gracefully.*\n',
            r'.*follows best practices.*\n',
            r'^Note:.*$',
            r'^Important:.*$',
            r'.*Please note that.*$',
            r'.*You can install.*$',
            r'.*npm install.*$',
            r'.*pip install.*$',
            r'.*To run this.*$',
            r'.*This requires.*$',
            r'.*Make sure to install.*$',
        ]
        
        for pattern in cleanup_patterns:
            response = re.sub(pattern, '', response, flags=re.MULTILINE | re.IGNORECASE)
        
        # Remove lines that look like installation instructions
        lines = response.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line_lower = line.strip().lower()
            skip_line = any([
                line_lower.startswith('please note'),
                line_lower.startswith('npm install'),
                line_lower.startswith('pip install'),
                line_lower.startswith('you can install'),
                line_lower.startswith('this requires'),
                line_lower.startswith('make sure'),
                line_lower.startswith('don\'t forget'),
                'install them using' in line_lower,
                ('javascript code' in line_lower and 'node.js' in line_lower),
            ])
            
            if not skip_line:
                cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
