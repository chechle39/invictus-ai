"""
Dependency Analyzer - Analyzes project dependencies and external libraries
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Set, Any


class DependencyAnalyzer:
    """Analyzes dependencies and external libraries in legacy systems"""
    
    def __init__(self, config):
        self.config = config
        self.dependency_files = {
            'csharp': ['packages.config', '*.csproj', '*.sln'],
            'java': ['pom.xml', 'build.gradle', '*.jar'],
            'python': ['requirements.txt', 'setup.py', 'Pipfile', 'poetry.lock'],
            'javascript': ['package.json', 'package-lock.json', 'yarn.lock'],
            'php': ['composer.json', 'composer.lock']
        }
    
    def analyze_dependencies(self, project_path: Path) -> Dict[str, List[str]]:
        """
        Analyze project dependencies and external libraries
        
        Args:
            project_path: Path to the project
            
        Returns:
            Dictionary containing dependency analysis results
        """
        analysis_result = {
            'external': [],
            'internal': [],
            'dev': [],
            'runtime': [],
            'framework': [],
            'database': [],
            'logging': [],
            'testing': []
        }
        
        # Analyze different types of dependencies
        for language, patterns in self.dependency_files.items():
            dependencies = self._analyze_language_dependencies(project_path, language, patterns)
            
            # Categorize dependencies
            for dep in dependencies:
                category = self._categorize_dependency(dep, language)
                if category in analysis_result:
                    analysis_result[category].append(dep)
                else:
                    analysis_result['external'].append(dep)
        
        # Remove duplicates
        for category in analysis_result:
            analysis_result[category] = list(set(analysis_result[category]))
        
        return analysis_result
    
    def _analyze_language_dependencies(self, project_path: Path, language: str, patterns: List[str]) -> List[str]:
        """Analyze dependencies for a specific language"""
        dependencies = []
        
        for pattern in patterns:
            for file_path in project_path.rglob(pattern):
                if file_path.is_file():
                    deps = self._parse_dependency_file(file_path, language)
                    dependencies.extend(deps)
        
        return dependencies
    
    def _parse_dependency_file(self, file_path: Path, language: str) -> List[str]:
        """Parse dependency file and extract package names"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            
            if language == 'csharp':
                return self._parse_csharp_dependencies(content)
            elif language == 'java':
                return self._parse_java_dependencies(content)
            elif language == 'python':
                return self._parse_python_dependencies(content)
            elif language == 'javascript':
                return self._parse_javascript_dependencies(content)
            elif language == 'php':
                return self._parse_php_dependencies(content)
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return []
    
    def _parse_csharp_dependencies(self, content: str) -> List[str]:
        """Parse C# dependencies from packages.config or .csproj"""
        dependencies = []
        
        # Parse packages.config
        package_pattern = r'package\s+id="([^"]+)"'
        for match in re.finditer(package_pattern, content):
            dependencies.append(match.group(1))
        
        # Parse .csproj PackageReference
        package_ref_pattern = r'PackageReference\s+Include="([^"]+)"'
        for match in re.finditer(package_ref_pattern, content):
            dependencies.append(match.group(1))
        
        # Parse .csproj Reference
        reference_pattern = r'Reference\s+Include="([^"]+)"'
        for match in re.finditer(reference_pattern, content):
            dependencies.append(match.group(1))
        
        return dependencies
    
    def _parse_java_dependencies(self, content: str) -> List[str]:
        """Parse Java dependencies from pom.xml or build.gradle"""
        dependencies = []
        
        # Parse Maven dependencies
        dependency_pattern = r'<artifactId>([^<]+)</artifactId>'
        for match in re.finditer(dependency_pattern, content):
            dependencies.append(match.group(1))
        
        # Parse Gradle dependencies (simplified)
        gradle_pattern = r'implementation\s+[\'"]([^\'"]+)[\'"]'
        for match in re.finditer(gradle_pattern, content):
            dependencies.append(match.group(1))
        
        return dependencies
    
    def _parse_python_dependencies(self, content: str) -> List[str]:
        """Parse Python dependencies from requirements.txt or setup.py"""
        dependencies = []
        
        # Parse requirements.txt
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package name (before version specifiers)
                package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0]
                dependencies.append(package_name)
        
        # Parse setup.py (simplified)
        setup_pattern = r'install_requires\s*=\s*\[(.*?)\]'
        for match in re.finditer(setup_pattern, content, re.DOTALL):
            requires_content = match.group(1)
            for line in requires_content.split(','):
                line = line.strip().strip('"\'')
                if line and not line.startswith('#'):
                    package_name = line.split('==')[0].split('>=')[0].split('<=')[0]
                    dependencies.append(package_name)
        
        return dependencies
    
    def _parse_javascript_dependencies(self, content: str) -> List[str]:
        """Parse JavaScript dependencies from package.json"""
        dependencies = []
        
        try:
            data = json.loads(content)
            
            # Parse dependencies
            if 'dependencies' in data:
                dependencies.extend(data['dependencies'].keys())
            
            # Parse devDependencies
            if 'devDependencies' in data:
                dependencies.extend(data['devDependencies'].keys())
            
            # Parse peerDependencies
            if 'peerDependencies' in data:
                dependencies.extend(data['peerDependencies'].keys())
            
        except json.JSONDecodeError:
            # Fallback to regex parsing
            dep_pattern = r'"([^"]+)":\s*"[^"]*"'
            for match in re.finditer(dep_pattern, content):
                dependencies.append(match.group(1))
        
        return dependencies
    
    def _parse_php_dependencies(self, content: str) -> List[str]:
        """Parse PHP dependencies from composer.json"""
        dependencies = []
        
        try:
            data = json.loads(content)
            
            # Parse require
            if 'require' in data:
                dependencies.extend(data['require'].keys())
            
            # Parse require-dev
            if 'require-dev' in data:
                dependencies.extend(data['require-dev'].keys())
            
        except json.JSONDecodeError:
            # Fallback to regex parsing
            dep_pattern = r'"([^"]+)":\s*"[^"]*"'
            for match in re.finditer(dep_pattern, content):
                dependencies.append(match.group(1))
        
        return dependencies
    
    def _categorize_dependency(self, dependency: str, language: str) -> str:
        """Categorize a dependency based on its name and language"""
        dependency_lower = dependency.lower()
        
        # Framework dependencies
        framework_keywords = ['aspnet', 'spring', 'django', 'flask', 'express', 'laravel', 'symfony']
        if any(keyword in dependency_lower for keyword in framework_keywords):
            return 'framework'
        
        # Database dependencies
        db_keywords = ['sql', 'mysql', 'postgres', 'oracle', 'mongo', 'redis', 'elasticsearch', 'entity', 'nhibernate', 'dapper']
        if any(keyword in dependency_lower for keyword in db_keywords):
            return 'database'
        
        # Logging dependencies
        logging_keywords = ['log', 'serilog', 'nlog', 'log4net', 'winston', 'pino']
        if any(keyword in dependency_lower for keyword in logging_keywords):
            return 'logging'
        
        # Testing dependencies
        test_keywords = ['test', 'spec', 'mock', 'stub', 'fixture', 'nunit', 'xunit', 'mstest', 'junit', 'pytest', 'jest', 'mocha']
        if any(keyword in dependency_lower for keyword in test_keywords):
            return 'testing'
        
        # Development dependencies
        dev_keywords = ['dev', 'development', 'build', 'compile', 'lint', 'format']
        if any(keyword in dependency_lower for keyword in dev_keywords):
            return 'dev'
        
        # Runtime dependencies (default)
        return 'runtime' 