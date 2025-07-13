"""
Code Analyzer - Analyzes code structure, metrics, and patterns
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Any
from collections import defaultdict
import ast
import tokenize
from io import StringIO


class CodeAnalyzer:
    """Analyzes code structure, metrics, and patterns in legacy systems"""
    
    def __init__(self, config):
        self.config = config
        self.supported_extensions = {
            '.cs': 'csharp',
            '.java': 'java', 
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.php': 'php',
            '.rb': 'ruby',
            '.go': 'go',
            '.rs': 'rust'
        }
    
    def analyze_codebase(self, project_path: Path) -> Dict[str, Any]:
        """
        Analyze codebase structure and metrics
        
        Args:
            project_path: Path to the project
            
        Returns:
            Dictionary containing code analysis results
        """
        analysis_result = {
            'total_files': 0,
            'total_lines': 0,
            'language_distribution': {},
            'file_types': {},
            'code_complexity': {},
            'largest_files': [],
            'code_patterns': {},
            'imports': defaultdict(set),
            'dependencies': defaultdict(set)
        }
        
        # Collect all code files
        code_files = self._collect_code_files(project_path)
        analysis_result['total_files'] = len(code_files)
        
        # Analyze each file
        for file_path in code_files:
            file_analysis = self._analyze_file(file_path)
            
            # Update metrics
            analysis_result['total_lines'] += file_analysis.get('lines', 0)
            
            # Update language distribution
            language = file_analysis.get('language', 'unknown')
            analysis_result['language_distribution'][language] = \
                analysis_result['language_distribution'].get(language, 0) + 1
            
            # Update file types
            file_type = file_analysis.get('type', 'unknown')
            analysis_result['file_types'][file_type] = \
                analysis_result['file_types'].get(file_type, 0) + 1
            
            # Update complexity
            complexity = file_analysis.get('complexity', 0)
            if complexity > 0:
                analysis_result['code_complexity'][str(file_path)] = complexity
            
            # Update imports and dependencies
            imports = file_analysis.get('imports', [])
            for imp in imports:
                analysis_result['imports'][language].add(imp)
            
            deps = file_analysis.get('dependencies', [])
            for dep in deps:
                analysis_result['dependencies'][language].add(dep)
        
        # Find largest files
        analysis_result['largest_files'] = self._find_largest_files(code_files)
        
        # Analyze code patterns
        analysis_result['code_patterns'] = self._analyze_code_patterns(code_files)
        
        return analysis_result
    
    def _collect_code_files(self, project_path: Path) -> List[Path]:
        """Collect all code files in the project"""
        code_files = []
        
        for file_path in project_path.rglob('*'):
            if file_path.is_file():
                # Check if file should be ignored
                if self._should_ignore_file(file_path):
                    continue
                
                # Check if it's a code file
                if file_path.suffix.lower() in self.supported_extensions:
                    code_files.append(file_path)
        
        return code_files
    
    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored based on patterns"""
        ignore_patterns = self.config.analysis.ignore_patterns
        
        for pattern in ignore_patterns:
            if pattern.startswith('*'):
                # Wildcard pattern
                if file_path.name.endswith(pattern[1:]):
                    return True
            elif pattern.endswith('/*'):
                # Directory pattern
                dir_pattern = pattern[:-2]
                if dir_pattern in str(file_path):
                    return True
            else:
                # Exact pattern
                if pattern in str(file_path):
                    return True
        
        return False
    
    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single code file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            language = self.supported_extensions.get(file_path.suffix.lower(), 'unknown')
            
            analysis = {
                'language': language,
                'lines': len(content.splitlines()),
                'size': len(content),
                'complexity': 0,
                'imports': [],
                'dependencies': [],
                'type': self._detect_file_type(file_path, content)
            }
            
            # Language-specific analysis
            if language == 'python':
                analysis.update(self._analyze_python_file(content))
            elif language == 'csharp':
                analysis.update(self._analyze_csharp_file(content))
            elif language == 'java':
                analysis.update(self._analyze_java_file(content))
            elif language in ['javascript', 'typescript']:
                analysis.update(self._analyze_js_file(content))
            
            return analysis
            
        except Exception as e:
            return {
                'language': 'unknown',
                'lines': 0,
                'size': 0,
                'complexity': 0,
                'imports': [],
                'dependencies': [],
                'type': 'unknown',
                'error': str(e)
            }
    
    def _detect_file_type(self, file_path: Path, content: str) -> str:
        """Detect the type of file based on content and path"""
        file_name = file_path.name.lower()
        
        # Configuration files
        if file_name in ['web.config', 'app.config', 'packages.config']:
            return 'config'
        elif file_name in ['package.json', 'requirements.txt', 'pom.xml']:
            return 'dependency'
        elif file_name in ['global.asax', 'startup.cs', 'program.cs']:
            return 'entry_point'
        elif 'controller' in file_name:
            return 'controller'
        elif 'service' in file_name:
            return 'service'
        elif 'model' in file_name or 'entity' in file_name:
            return 'model'
        elif 'test' in file_name:
            return 'test'
        elif 'middleware' in file_name:
            return 'middleware'
        else:
            return 'code'
    
    def _analyze_python_file(self, content: str) -> Dict[str, Any]:
        """Analyze Python file"""
        try:
            tree = ast.parse(content)
            
            imports = []
            dependencies = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            # Calculate complexity (simplified)
            complexity = len([n for n in ast.walk(tree) if isinstance(n, (ast.If, ast.For, ast.While))])
            
            return {
                'complexity': complexity,
                'imports': imports,
                'dependencies': dependencies
            }
        except:
            return {'complexity': 0, 'imports': [], 'dependencies': []}
    
    def _analyze_csharp_file(self, content: str) -> Dict[str, Any]:
        """Analyze C# file"""
        imports = []
        dependencies = []
        
        # Extract using statements
        using_pattern = r'using\s+([^;]+);'
        for match in re.finditer(using_pattern, content):
            imports.append(match.group(1).strip())
        
        # Extract package references
        package_pattern = r'PackageReference\s+Include="([^"]+)"'
        for match in re.finditer(package_pattern, content):
            dependencies.append(match.group(1))
        
        # Calculate complexity (simplified)
        complexity = len(re.findall(r'\b(if|for|while|foreach)\b', content, re.IGNORECASE))
        
        return {
            'complexity': complexity,
            'imports': imports,
            'dependencies': dependencies
        }
    
    def _analyze_java_file(self, content: str) -> Dict[str, Any]:
        """Analyze Java file"""
        imports = []
        dependencies = []
        
        # Extract import statements
        import_pattern = r'import\s+([^;]+);'
        for match in re.finditer(import_pattern, content):
            imports.append(match.group(1).strip())
        
        # Calculate complexity (simplified)
        complexity = len(re.findall(r'\b(if|for|while)\b', content, re.IGNORECASE))
        
        return {
            'complexity': complexity,
            'imports': imports,
            'dependencies': dependencies
        }
    
    def _analyze_js_file(self, content: str) -> Dict[str, Any]:
        """Analyze JavaScript/TypeScript file"""
        imports = []
        dependencies = []
        
        # Extract import statements
        import_patterns = [
            r'import\s+.*?from\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]',
        ]
        
        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                imports.append(match.group(1).strip())
        
        # Calculate complexity (simplified)
        complexity = len(re.findall(r'\b(if|for|while)\b', content, re.IGNORECASE))
        
        return {
            'complexity': complexity,
            'imports': imports,
            'dependencies': dependencies
        }
    
    def _find_largest_files(self, code_files: List[Path]) -> List[Dict[str, Any]]:
        """Find the largest files in the codebase"""
        file_sizes = []
        
        for file_path in code_files:
            try:
                size = file_path.stat().st_size
                file_sizes.append({
                    'path': str(file_path),
                    'size': size,
                    'lines': len(file_path.read_text(encoding='utf-8', errors='ignore').splitlines())
                })
            except:
                continue
        
        # Sort by size and return top 10
        file_sizes.sort(key=lambda x: x['size'], reverse=True)
        return file_sizes[:10]
    
    def _analyze_code_patterns(self, code_files: List[Path]) -> Dict[str, Any]:
        """Analyze common code patterns"""
        patterns = {
            'authentication': 0,
            'database_access': 0,
            'api_endpoints': 0,
            'logging': 0,
            'error_handling': 0,
            'async_await': 0,
            'dependency_injection': 0
        }
        
        for file_path in code_files:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
                
                # Check for patterns
                if any(word in content for word in ['auth', 'authentication', 'login']):
                    patterns['authentication'] += 1
                
                if any(word in content for word in ['database', 'dbcontext', 'entity']):
                    patterns['database_access'] += 1
                
                if any(word in content for word in ['controller', 'api', 'endpoint']):
                    patterns['api_endpoints'] += 1
                
                if any(word in content for word in ['log', 'logger', 'console.log']):
                    patterns['logging'] += 1
                
                if any(word in content for word in ['try', 'catch', 'exception']):
                    patterns['error_handling'] += 1
                
                if any(word in content for word in ['async', 'await', 'promise']):
                    patterns['async_await'] += 1
                
                if any(word in content for word in ['di', 'dependency', 'servicecollection']):
                    patterns['dependency_injection'] += 1
                    
            except:
                continue
        
        return patterns 