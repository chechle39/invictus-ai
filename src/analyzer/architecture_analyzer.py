"""
Architecture Analyzer - Analyzes system architecture patterns and technology stack
"""

import re
from pathlib import Path
from typing import Dict, List, Any


class ArchitectureAnalyzer:
    """Analyzes architecture patterns and technology stack in legacy systems"""
    
    def __init__(self, config):
        self.config = config
        self.architecture_patterns = {
            'monolith': ['global.asax', 'startup.cs', 'program.cs', 'main.py', 'app.py'],
            'microservices': ['dockerfile', 'docker-compose', 'kubernetes', 'service-discovery'],
            'mvc': ['controller', 'model', 'view', 'mvc'],
            'mvvm': ['viewmodel', 'binding', 'mvvm'],
            'repository': ['repository', 'irepository', 'dataaccess'],
            'unit_of_work': ['unitofwork', 'uow', 'transaction'],
            'dependency_injection': ['di', 'dependency', 'servicecollection', 'autofac'],
            'authentication': ['auth', 'authentication', 'identity', 'jwt', 'oauth'],
            'authorization': ['authorize', 'permission', 'role', 'policy'],
            'logging': ['log', 'logger', 'ilogger', 'serilog', 'nlog'],
            'caching': ['cache', 'memorycache', 'distributedcache', 'redis'],
            'database': ['database', 'dbcontext', 'entity', 'sql', 'nosql'],
            'api': ['api', 'controller', 'endpoint', 'rest', 'graphql'],
            'async': ['async', 'await', 'task', 'promise'],
            'testing': ['test', 'spec', 'mock', 'stub', 'fixture']
        }
        
        self.technology_stack_patterns = {
            'framework': {
                'dotnet_framework': ['system.web', 'system.web.http', 'web.config'],
                'dotnet_core': ['microsoft.aspnetcore', 'aspnetcore', 'program.cs'],
                'dotnet_6': ['net6.0', 'microsoft.net.sdk'],
                'java_spring': ['spring', 'springboot', '@springbootapplication'],
                'java_ee': ['javax', 'servlet', 'ejb'],
                'python_django': ['django', 'settings.py', 'urls.py'],
                'python_flask': ['flask', 'app.py', 'flask_app'],
                'node_express': ['express', 'app.js', 'package.json'],
                'node_nest': ['nest', '@nestjs', 'nest-cli.json']
            },
            'database': {
                'sql_server': ['sqlserver', 'microsoft.sql', 'connectionstring'],
                'mysql': ['mysql', 'mariadb', 'connectionstring'],
                'postgresql': ['postgres', 'postgresql', 'npgsql'],
                'oracle': ['oracle', 'oracleconnection'],
                'mongodb': ['mongodb', 'mongo', 'bson'],
                'redis': ['redis', 'stackexchange.redis'],
                'elasticsearch': ['elasticsearch', 'nest', 'elasticsearch.net']
            },
            'orm': {
                'entity_framework': ['entityframework', 'dbcontext', 'ef'],
                'nhibernate': ['nhibernate', 'sessionfactory'],
                'dapper': ['dapper', 'micro-orm'],
                'sqlalchemy': ['sqlalchemy', 'alembic'],
                'prisma': ['prisma', 'prisma-client'],
                'typeorm': ['typeorm', 'entity']
            },
            'authentication': {
                'aspnet_identity': ['microsoft.aspnetcore.identity', 'identity'],
                'jwt': ['jwt', 'jsonwebtoken', 'bearer'],
                'oauth': ['oauth', 'openidconnect', 'microsoft.identity'],
                'ldap': ['ldap', 'activedirectory'],
                'saml': ['saml', 'saml2']
            },
            'logging': {
                'serilog': ['serilog', 'ilogger'],
                'nlog': ['nlog', 'ilogger'],
                'log4net': ['log4net'],
                'winston': ['winston', 'logger'],
                'pino': ['pino', 'logger']
            },
            'caching': {
                'memory_cache': ['memorycache', 'imemorycache'],
                'redis_cache': ['redis', 'idistributedcache'],
                'sql_cache': ['sqlcachedependency'],
                'memcached': ['memcached']
            }
        }
    
    def analyze_architecture(self, project_path: Path) -> Dict[str, Any]:
        """
        Analyze architecture patterns and technology stack
        
        Args:
            project_path: Path to the project
            
        Returns:
            Dictionary containing architecture analysis results
        """
        analysis_result = {
            'patterns': [],
            'technology_stack': {},
            'architecture_type': 'unknown',
            'complexity_score': 0
        }
        
        # Collect all files for analysis
        all_files = list(project_path.rglob('*'))
        file_contents = {}
        
        # Read file contents (limited to avoid memory issues)
        for file_path in all_files[:1000]:  # Limit to first 1000 files
            if file_path.is_file() and file_path.suffix.lower() in ['.cs', '.java', '.py', '.js', '.ts', '.xml', '.json', '.yaml', '.yml']:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
                    file_contents[str(file_path)] = content
                except:
                    continue
        
        # Analyze architecture patterns
        patterns = self._detect_architecture_patterns(file_contents)
        analysis_result['patterns'] = patterns
        
        # Analyze technology stack
        tech_stack = self._detect_technology_stack(file_contents)
        analysis_result['technology_stack'] = tech_stack
        
        # Determine architecture type
        architecture_type = self._determine_architecture_type(patterns, tech_stack)
        analysis_result['architecture_type'] = architecture_type
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(patterns, tech_stack)
        analysis_result['complexity_score'] = complexity_score
        
        return analysis_result
    
    def _detect_architecture_patterns(self, file_contents: Dict[str, str]) -> List[str]:
        """Detect architecture patterns in the codebase"""
        detected_patterns = []
        
        for pattern_name, keywords in self.architecture_patterns.items():
            pattern_count = 0
            
            for file_path, content in file_contents.items():
                # Check file path
                if any(keyword in file_path.lower() for keyword in keywords):
                    pattern_count += 1
                
                # Check content
                if any(keyword in content for keyword in keywords):
                    pattern_count += 1
            
            # If pattern is detected in multiple files, consider it present
            if pattern_count >= 2:
                detected_patterns.append(pattern_name)
        
        return detected_patterns
    
    def _detect_technology_stack(self, file_contents: Dict[str, str]) -> Dict[str, str]:
        """Detect technology stack components"""
        detected_tech = {}
        
        for category, technologies in self.technology_stack_patterns.items():
            for tech_name, keywords in technologies.items():
                tech_count = 0
                
                for file_path, content in file_contents.items():
                    # Check file path
                    if any(keyword in file_path.lower() for keyword in keywords):
                        tech_count += 1
                    
                    # Check content
                    if any(keyword in content for keyword in keywords):
                        tech_count += 1
                
                # If technology is detected, add it to stack
                if tech_count >= 1:
                    detected_tech[category] = tech_name
                    break  # Use first detected technology in category
        
        return detected_tech
    
    def _determine_architecture_type(self, patterns: List[str], tech_stack: Dict[str, str]) -> str:
        """Determine the overall architecture type"""
        
        if 'microservices' in patterns:
            return 'microservices'
        elif 'monolith' in patterns:
            return 'monolith'
        elif 'mvc' in patterns:
            return 'mvc'
        elif 'mvvm' in patterns:
            return 'mvvm'
        else:
            # Try to determine from technology stack
            if 'framework' in tech_stack:
                framework = tech_stack['framework']
                if 'dotnet_framework' in framework:
                    return 'monolith'
                elif 'dotnet_core' in framework or 'dotnet_6' in framework:
                    return 'modern_monolith'
                elif 'java_spring' in framework:
                    return 'spring_monolith'
                elif 'python_django' in framework:
                    return 'django_monolith'
                elif 'node_express' in framework:
                    return 'express_monolith'
        
        return 'unknown'
    
    def _calculate_complexity_score(self, patterns: List[str], tech_stack: Dict[str, str]) -> int:
        """Calculate architecture complexity score"""
        score = 0
        
        # Base complexity from patterns
        score += len(patterns) * 2
        
        # Additional complexity from technology stack
        score += len(tech_stack) * 3
        
        # Specific complexity factors
        if 'microservices' in patterns:
            score += 10
        if 'authentication' in patterns:
            score += 5
        if 'database' in tech_stack:
            score += 3
        if 'caching' in tech_stack:
            score += 2
        if 'logging' in tech_stack:
            score += 1
        
        return min(score, 100)  # Cap at 100 