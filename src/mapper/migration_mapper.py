"""
Migration Mapper - Generates migration maps from analysis results
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from openai import OpenAI

from config import Config


class MigrationMapper:
    """Generates migration maps from analysis results using AI"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(**config.get_openai_config())
        
        # Migration templates for different target technologies
        self.migration_templates = {
            'dotnet-core': {
                'source_patterns': ['dotnet_framework', 'system.web'],
                'target_stack': '.NET Core',
                'technology_mapping': {
                    'System.Web.Http': 'Microsoft.AspNetCore.Mvc',
                    'Entity Framework 6': 'Entity Framework Core',
                    'Web.config': 'appsettings.json',
                    'Global.asax': 'Program.cs'
                }
            },
            'dotnet-6': {
                'source_patterns': ['dotnet_framework', 'system.web'],
                'target_stack': '.NET 6',
                'technology_mapping': {
                    'System.Web.Http': 'Microsoft.AspNetCore.Mvc',
                    'Entity Framework 6': 'Entity Framework Core',
                    'Web.config': 'appsettings.json',
                    'Global.asax': 'Program.cs',
                    'System.Web.SessionState': 'Microsoft.AspNetCore.Session'
                }
            },
            'java-17': {
                'source_patterns': ['java_8', 'javax'],
                'target_stack': 'Java 17',
                'technology_mapping': {
                    'Java 8': 'Java 17',
                    'javax.servlet': 'jakarta.servlet',
                    'javax.persistence': 'jakarta.persistence',
                    'javax.validation': 'jakarta.validation'
                }
            },
            'java-spring-boot': {
                'source_patterns': ['java_ee', 'spring_mvc'],
                'target_stack': 'Spring Boot 3',
                'technology_mapping': {
                    'Spring MVC': 'Spring Boot',
                    'javax.servlet': 'jakarta.servlet',
                    'web.xml': 'application.properties',
                    'JSP': 'Thymeleaf'
                }
            },
            'python-3': {
                'source_patterns': ['python_2', 'print_statement'],
                'target_stack': 'Python 3',
                'technology_mapping': {
                    'Python 2': 'Python 3',
                    'print statement': 'print() function',
                    'urllib2': 'urllib.request',
                    'xrange': 'range'
                }
            },
            'node-express': {
                'source_patterns': ['php', 'asp_classic'],
                'target_stack': 'Node.js Express',
                'technology_mapping': {
                    'PHP': 'Node.js',
                    'MySQL': 'MongoDB/PostgreSQL',
                    'Apache': 'Express.js',
                    'PHP Sessions': 'JWT Tokens'
                }
            },
            'node-nest': {
                'source_patterns': ['monolith', 'mvc'],
                'target_stack': 'NestJS',
                'technology_mapping': {
                    'MVC Pattern': 'NestJS Architecture',
                    'Traditional ORM': 'TypeORM/Prisma',
                    'REST API': 'NestJS Controllers',
                    'Authentication': 'Passport.js'
                }
            },
            'go-microservices': {
                'source_patterns': ['monolith', 'java_spring'],
                'target_stack': 'Go Microservices',
                'technology_mapping': {
                    'Spring Boot': 'Go + Gin/Echo',
                    'Java': 'Go',
                    'Maven/Gradle': 'Go Modules',
                    'JPA': 'GORM'
                }
            },
            'rust-web': {
                'source_patterns': ['csharp', 'java'],
                'target_stack': 'Rust Web',
                'technology_mapping': {
                    'C#/Java': 'Rust',
                    'ASP.NET Core': 'Actix-web/Rocket',
                    'Entity Framework': 'SQLx/Diesel',
                    'Managed Memory': 'Ownership System'
                }
            },
            'php-laravel': {
                'source_patterns': ['php_legacy', 'wordpress'],
                'target_stack': 'Laravel',
                'technology_mapping': {
                    'Legacy PHP': 'Laravel Framework',
                    'WordPress': 'Laravel CMS',
                    'MySQL': 'Eloquent ORM',
                    'Apache': 'Laravel Artisan'
                }
            },
            'microservices': {
                'source_patterns': ['monolith', 'mvc'],
                'target_stack': 'Microservices Architecture',
                'technology_mapping': {
                    'Monolithic Application': 'Microservices',
                    'Shared Database': 'Database per Service',
                    'REST API': 'API Gateway + Services',
                    'Session State': 'Stateless Services'
                }
            },
            'cloud-native': {
                'source_patterns': ['on-premise', 'traditional'],
                'target_stack': 'Cloud-Native',
                'technology_mapping': {
                    'On-premise Infrastructure': 'Cloud Infrastructure',
                    'Traditional Deployment': 'Container Deployment',
                    'Monolithic Database': 'Cloud Database Services',
                    'File System Storage': 'Cloud Storage'
                }
            }
        }
    
    def generate_migration_map(self, analysis_file: str, target: str, template: Optional[str] = None, 
                              source_language: Optional[str] = None, target_language: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate migration map from analysis results
        
        Args:
            analysis_file: Path to analysis results JSON file
            target: Target technology stack
            template: Optional custom template
            source_language: Source programming language (auto-detected if not specified)
            target_language: Target programming language
            
        Returns:
            Migration map dictionary
        """
        # Load analysis results
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # Auto-detect source language if not specified
        if not source_language:
            source_language = self._detect_source_language(analysis_data)
        
        # Get migration template
        migration_template = self._get_migration_template(target, template)
        
        # Update template with language-specific mappings if target_language is specified
        if target_language:
            migration_template = self._update_template_for_language(migration_template, source_language, target_language)
        
        # Generate migration map using AI
        migration_map = self._generate_migration_map_with_ai(analysis_data, migration_template, source_language, target_language)
        
        return migration_map
    
    def suggest_target_technologies(self, analysis_file: str, use_case: str, performance_requirement: str = 'medium',
                                   team_expertise: str = None, budget_constraint: str = 'medium') -> Dict[str, Any]:
        """
        Suggest target technologies based on project analysis and requirements
        
        Args:
            analysis_file: Path to analysis results JSON file
            use_case: Primary use case of the application
            performance_requirement: Performance requirements (high/medium/low)
            team_expertise: Team programming language expertise
            budget_constraint: Budget constraints for migration
            
        Returns:
            Dictionary containing technology suggestions
        """
        # Load analysis results
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_data = json.load(f)
        
        # Generate suggestions using AI
        suggestions = self._generate_technology_suggestions_with_ai(
            analysis_data, use_case, performance_requirement, team_expertise, budget_constraint
        )
        
        return suggestions
    
    def _get_migration_template(self, target: str, template: Optional[str] = None) -> Dict[str, Any]:
        """Get migration template for target technology"""
        if template and template in self.migration_templates:
            return self.migration_templates[template]
        
        if target in self.migration_templates:
            return self.migration_templates[target]
        
        # Default template
        return {
            'source_patterns': [],
            'target_stack': target,
            'technology_mapping': {}
        }
    
    def _generate_migration_map_with_ai(self, analysis_data: Dict[str, Any], template: Dict[str, Any], 
                                       source_language: str = None, target_language: str = None) -> Dict[str, Any]:
        """Generate migration map using OpenAI AI"""
        
        # Build prompt for AI
        prompt = self._build_migration_prompt(analysis_data, template, source_language, target_language)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are an expert software migration specialist. Generate detailed migration maps for legacy system modernization."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse AI response
            migration_map = self._parse_ai_response(ai_response, analysis_data, template)
            
            return migration_map
            
        except Exception as e:
            # Fallback to rule-based generation
            return self._generate_rule_based_migration_map(analysis_data, template)
    
    def _generate_technology_suggestions_with_ai(self, analysis_data: Dict[str, Any], use_case: str, 
                                                performance_requirement: str, team_expertise: str, 
                                                budget_constraint: str) -> Dict[str, Any]:
        """Generate technology suggestions using OpenAI AI"""
        
        # Build prompt for technology suggestions
        prompt = self._build_suggestion_prompt(analysis_data, use_case, performance_requirement, team_expertise, budget_constraint)
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": "You are an expert technology consultant specializing in software migration and technology selection. Provide detailed, practical technology recommendations based on project requirements and constraints."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            ai_response = response.choices[0].message.content
            
            # Parse AI response
            suggestions = self._parse_suggestion_response(ai_response, analysis_data)
            
            return suggestions
            
        except Exception as e:
            # Fallback to rule-based suggestions
            return self._generate_rule_based_suggestions(analysis_data, use_case, performance_requirement, team_expertise, budget_constraint)
    
    def _build_migration_prompt(self, analysis_data: Dict[str, Any], template: Dict[str, Any], 
                                source_language: str = None, target_language: str = None) -> str:
        """Build prompt for AI migration map generation"""
        
        language_info = ""
        if source_language and target_language:
            language_info = f"\nLanguage Migration: {source_language.upper()} → {target_language.upper()}"
        elif source_language:
            language_info = f"\nSource Language: {source_language.upper()}"
        
        return f"""Analyze the following legacy system and generate a comprehensive migration map for {template['target_stack']}.{language_info}

System Analysis:
- Project: {analysis_data.get('project_name', 'Unknown')}
- Technology Stack: {analysis_data.get('technology_stack', {})}
- Architecture Patterns: {analysis_data.get('architecture_patterns', [])}
- Dependencies: {analysis_data.get('dependencies', {})}
- Code Metrics: {analysis_data.get('code_metrics', {})}
- Migration Risks: {analysis_data.get('migration_risks', [])}
- Estimated Effort: {analysis_data.get('estimated_effort', 'Unknown')}

Target Technology: {template['target_stack']}
Technology Mapping: {template['technology_mapping']}

Generate a migration map with the following structure:
1. Direct Conversion: Files that can be migrated with minimal changes
2. Rewrite Required: Files that need significant rewriting
3. Special Handling: Files requiring special attention or custom logic
4. Technology Mapping: Specific technology replacements
5. Risks: Migration risks and mitigation strategies
6. Timeline: Estimated migration timeline

Return the response as a JSON object with these fields:
- project_name
- source_stack
- target_stack
- migration_strategy (direct_conversion, rewrite_required, special_handling)
- technology_mapping
- risks
- estimated_effort
"""
    
    def _parse_ai_response(self, ai_response: str, analysis_data: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response into structured migration map"""
        
        try:
            # Try to extract JSON from AI response
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                migration_map = json.loads(json_match.group())
            else:
                # Fallback to rule-based generation
                return self._generate_rule_based_migration_map(analysis_data, template)
            
            # Ensure required fields
            migration_map.setdefault('project_name', analysis_data.get('project_name', 'Unknown'))
            migration_map.setdefault('source_stack', self._detect_source_stack(analysis_data))
            migration_map.setdefault('target_stack', template['target_stack'])
            migration_map.setdefault('migration_strategy', {})
            migration_map.setdefault('technology_mapping', template['technology_mapping'])
            migration_map.setdefault('risks', analysis_data.get('migration_risks', []))
            migration_map.setdefault('estimated_effort', analysis_data.get('estimated_effort', 'Unknown'))
            
            return migration_map
            
        except Exception as e:
            # Fallback to rule-based generation
            return self._generate_rule_based_migration_map(analysis_data, template)
    
    def _generate_rule_based_migration_map(self, analysis_data: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
        """Generate migration map using rule-based approach"""
        
        migration_map = {
            'project_name': analysis_data.get('project_name', 'Unknown'),
            'source_stack': self._detect_source_stack(analysis_data),
            'target_stack': template['target_stack'],
            'migration_strategy': {
                'direct_conversion': [],
                'rewrite_required': [],
                'special_handling': []
            },
            'technology_mapping': template['technology_mapping'],
            'risks': analysis_data.get('migration_risks', []),
            'estimated_effort': analysis_data.get('estimated_effort', 'Unknown')
        }
        
        # Categorize files based on analysis
        code_metrics = analysis_data.get('code_metrics', {})
        file_types = code_metrics.get('file_types', {})
        
        # Simple rule-based categorization
        if 'model' in file_types:
            migration_map['migration_strategy']['direct_conversion'].extend([
                'Models/*.cs',
                'Entities/*.cs'
            ])
        
        if 'controller' in file_types:
            migration_map['migration_strategy']['rewrite_required'].extend([
                'Controllers/*.cs',
                'ApiControllers/*.cs'
            ])
        
        if 'service' in file_types:
            migration_map['migration_strategy']['rewrite_required'].extend([
                'Services/*.cs',
                'BusinessLogic/*.cs'
            ])
        
        # Special handling for configuration files
        migration_map['migration_strategy']['special_handling'].extend([
            'Web.config',
            'Global.asax',
            'packages.config'
        ])
        
        return migration_map
    
    def _detect_source_stack(self, analysis_data: Dict[str, Any]) -> str:
        """Detect source technology stack from analysis"""
        
        tech_stack = analysis_data.get('technology_stack', {})
        
        if 'framework' in tech_stack:
            framework = tech_stack['framework']
            if 'dotnet_framework' in framework:
                return '.NET Framework'
            elif 'dotnet_core' in framework:
                return '.NET Core'
            elif 'java_spring' in framework:
                return 'Spring Framework'
            elif 'python_django' in framework:
                return 'Django'
        
        architecture_patterns = analysis_data.get('architecture_patterns', [])
        if 'microservices' in architecture_patterns:
            return 'Microservices'
        elif 'monolith' in architecture_patterns:
            return 'Monolith'
        
        return 'Unknown' 

    def _detect_source_language(self, analysis_data: Dict[str, Any]) -> str:
        """Detect source programming language from analysis data"""
        
        # Check language distribution in code metrics
        code_metrics = analysis_data.get('code_metrics', {})
        language_distribution = code_metrics.get('language_distribution', {})
        
        if language_distribution:
            # Return the most common language
            return max(language_distribution.items(), key=lambda x: x[1])[0]
        
        # Check technology stack for language hints
        technology_stack = analysis_data.get('technology_stack', {})
        
        if 'dotnet_framework' in str(technology_stack).lower():
            return 'csharp'
        elif 'java' in str(technology_stack).lower():
            return 'java'
        elif 'python' in str(technology_stack).lower():
            return 'python'
        elif 'javascript' in str(technology_stack).lower() or 'node' in str(technology_stack).lower():
            return 'javascript'
        elif 'php' in str(technology_stack).lower():
            return 'php'
        elif 'go' in str(technology_stack).lower():
            return 'go'
        elif 'rust' in str(technology_stack).lower():
            return 'rust'
        
        # Default to unknown
        return 'unknown'
    
    def _update_template_for_language(self, template: Dict[str, Any], source_language: str, target_language: str) -> Dict[str, Any]:
        """Update migration template with language-specific mappings"""
        
        # Language-specific technology mappings
        language_mappings = {
            ('csharp', 'java'): {
                'C#': 'Java',
                'ASP.NET': 'Spring Boot',
                'Entity Framework': 'JPA/Hibernate',
                'LINQ': 'Stream API',
                'async/await': 'CompletableFuture',
                'var': 'var (Java 10+)',
                'null coalescing': 'Optional'
            },
            ('java', 'csharp'): {
                'Java': 'C#',
                'Spring Boot': 'ASP.NET Core',
                'JPA/Hibernate': 'Entity Framework',
                'Stream API': 'LINQ',
                'CompletableFuture': 'async/await',
                'Optional': 'null coalescing',
                'Maven/Gradle': 'NuGet'
            },
            ('python', 'javascript'): {
                'Python': 'JavaScript/Node.js',
                'Django': 'Express.js',
                'Flask': 'Express.js',
                'SQLAlchemy': 'Sequelize/Prisma',
                'pip': 'npm',
                'requirements.txt': 'package.json',
                'async/await': 'async/await'
            },
            ('javascript', 'python'): {
                'JavaScript': 'Python',
                'Node.js': 'Python',
                'Express.js': 'Flask/Django',
                'npm': 'pip',
                'package.json': 'requirements.txt',
                'async/await': 'async/await'
            },
            ('php', 'python'): {
                'PHP': 'Python',
                'Laravel': 'Django/Flask',
                'Composer': 'pip',
                'composer.json': 'requirements.txt',
                'MySQL': 'PostgreSQL/SQLite'
            },
            ('csharp', 'go'): {
                'C#': 'Go',
                'ASP.NET Core': 'Gin/Echo',
                'Entity Framework': 'GORM',
                'LINQ': 'Go slices/maps',
                'async/await': 'goroutines/channels',
                'NuGet': 'Go modules'
            },
            ('java', 'go'): {
                'Java': 'Go',
                'Spring Boot': 'Gin/Echo',
                'JPA': 'GORM',
                'Maven/Gradle': 'Go modules',
                'Stream API': 'Go slices/maps'
            }
        }
        
        # Get language-specific mapping
        language_key = (source_language, target_language)
        if language_key in language_mappings:
            # Update technology mapping with language-specific mappings
            template['technology_mapping'].update(language_mappings[language_key])
        
        return template 

    def _build_suggestion_prompt(self, analysis_data: Dict[str, Any], use_case: str, performance_requirement: str,
                                team_expertise: str, budget_constraint: str) -> str:
        """Build prompt for technology suggestions"""
        
        return f"""Analyze the following legacy system and suggest the best target technologies for migration.

System Analysis:
- Project: {analysis_data.get('project_name', 'Unknown')}
- Technology Stack: {analysis_data.get('technology_stack', {})}
- Architecture Patterns: {analysis_data.get('architecture_patterns', [])}
- Code Metrics: {analysis_data.get('code_metrics', {})}
- Migration Risks: {analysis_data.get('migration_risks', [])}

Requirements:
- Use Case: {use_case}
- Performance Requirement: {performance_requirement}
- Team Expertise: {team_expertise or 'Not specified'}
- Budget Constraint: {budget_constraint}

Based on these factors, suggest the best target technologies with the following considerations:

1. **Primary Recommendations**: Top 3 technology stacks that best fit the requirements
2. **Alternative Options**: Additional options for different scenarios
3. **Technology Mapping**: Specific technology replacements for the current stack
4. **Migration Effort**: Estimated effort for each option
5. **Pros and Cons**: Benefits and challenges of each option
6. **Team Considerations**: How well each option fits the team's expertise
7. **Cost Implications**: Budget considerations for each option

Return the response as a JSON object with these fields:
- primary_recommendations (array of top 3 options)
- alternative_options (array of additional options)
- technology_mapping (object with current to target mappings)
- migration_effort (object with effort estimates)
- pros_cons (object with benefits and challenges)
- team_considerations (object with team fit analysis)
- cost_analysis (object with budget implications)
"""
    
    def _parse_suggestion_response(self, ai_response: str, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse AI response into structured suggestions"""
        
        try:
            # Try to extract JSON from AI response
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                suggestions = json.loads(json_match.group())
            else:
                # Fallback to rule-based suggestions
                return self._generate_rule_based_suggestions(analysis_data, 'web-app', 'medium', None, 'medium')
            
            # Ensure required fields
            suggestions.setdefault('primary_recommendations', [])
            suggestions.setdefault('alternative_options', [])
            suggestions.setdefault('technology_mapping', {})
            suggestions.setdefault('migration_effort', {})
            suggestions.setdefault('pros_cons', {})
            suggestions.setdefault('team_considerations', {})
            suggestions.setdefault('cost_analysis', {})
            
            return suggestions
            
        except Exception as e:
            # Fallback to rule-based suggestions
            return self._generate_rule_based_suggestions(analysis_data, 'web-app', 'medium', None, 'medium')
    
    def _generate_rule_based_suggestions(self, analysis_data: Dict[str, Any], use_case: str, 
                                        performance_requirement: str, team_expertise: str, 
                                        budget_constraint: str) -> Dict[str, Any]:
        """Generate technology suggestions using rule-based approach"""
        
        # Technology recommendations based on use case and requirements
        recommendations = {
            'web-app': {
                'high_performance': ['dotnet-6', 'java-spring-boot', 'go-microservices'],
                'medium_performance': ['node-express', 'python-3', 'php-laravel'],
                'low_budget': ['node-express', 'php-laravel', 'python-3']
            },
            'api-service': {
                'high_performance': ['go-microservices', 'rust-web', 'dotnet-6'],
                'medium_performance': ['java-spring-boot', 'node-express', 'python-3'],
                'low_budget': ['node-express', 'python-3', 'php-laravel']
            },
            'microservices': {
                'high_performance': ['go-microservices', 'rust-web', 'dotnet-6'],
                'medium_performance': ['java-spring-boot', 'node-express', 'python-3'],
                'low_budget': ['node-express', 'python-3']
            },
            'mobile-backend': {
                'high_performance': ['dotnet-6', 'java-spring-boot', 'go-microservices'],
                'medium_performance': ['node-express', 'python-3'],
                'low_budget': ['node-express', 'python-3']
            },
            'data-processing': {
                'high_performance': ['python-3', 'go-microservices', 'rust-web'],
                'medium_performance': ['java-spring-boot', 'python-3'],
                'low_budget': ['python-3', 'node-express']
            },
            'ai-ml': {
                'high_performance': ['python-3', 'go-microservices'],
                'medium_performance': ['python-3', 'java-spring-boot'],
                'low_budget': ['python-3']
            },
            'iot': {
                'high_performance': ['go-microservices', 'rust-web', 'python-3'],
                'medium_performance': ['python-3', 'node-express'],
                'low_budget': ['python-3', 'node-express']
            },
            'gaming': {
                'high_performance': ['go-microservices', 'rust-web', 'dotnet-6'],
                'medium_performance': ['java-spring-boot', 'python-3'],
                'low_budget': ['python-3', 'node-express']
            },
            'enterprise': {
                'high_performance': ['java-spring-boot', 'dotnet-6', 'go-microservices'],
                'medium_performance': ['java-spring-boot', 'dotnet-6'],
                'low_budget': ['java-spring-boot', 'dotnet-6']
            },
            'startup': {
                'high_performance': ['node-express', 'python-3', 'go-microservices'],
                'medium_performance': ['node-express', 'python-3'],
                'low_budget': ['node-express', 'python-3']
            }
        }
        
        # Get recommendations based on use case and performance
        use_case_recs = recommendations.get(use_case, recommendations['web-app'])
        
        if performance_requirement == 'high':
            primary_recs = use_case_recs.get('high_performance', ['dotnet-6', 'java-spring-boot'])
        elif budget_constraint == 'low':
            primary_recs = use_case_recs.get('low_budget', ['node-express', 'python-3'])
        else:
            primary_recs = use_case_recs.get('medium_performance', ['node-express', 'python-3'])
        
        # Generate suggestions structure
        suggestions = {
            'primary_recommendations': primary_recs,
            'alternative_options': ['microservices', 'cloud-native'],
            'technology_mapping': self._get_technology_mapping_for_recommendations(primary_recs),
            'migration_effort': self._estimate_migration_effort(primary_recs),
            'pros_cons': self._get_pros_cons_for_recommendations(primary_recs),
            'team_considerations': self._get_team_considerations(primary_recs, team_expertise),
            'cost_analysis': self._get_cost_analysis(primary_recs, budget_constraint)
        }
        
        return suggestions
    
    def _get_technology_mapping_for_recommendations(self, recommendations: List[str]) -> Dict[str, Any]:
        """Get technology mapping for recommended targets"""
        mapping = {}
        for rec in recommendations:
            if rec in self.migration_templates:
                mapping[rec] = self.migration_templates[rec]['technology_mapping']
        return mapping
    
    def _estimate_migration_effort(self, recommendations: List[str]) -> Dict[str, str]:
        """Estimate migration effort for recommendations"""
        effort_map = {
            'dotnet-6': 'Medium (2-4 weeks)',
            'java-spring-boot': 'Medium (3-5 weeks)',
            'go-microservices': 'High (4-6 weeks)',
            'rust-web': 'Very High (6-8 weeks)',
            'node-express': 'Low (1-3 weeks)',
            'python-3': 'Low (1-2 weeks)',
            'php-laravel': 'Low (1-3 weeks)'
        }
        
        return {rec: effort_map.get(rec, 'Medium (2-4 weeks)') for rec in recommendations}
    
    def _get_pros_cons_for_recommendations(self, recommendations: List[str]) -> Dict[str, Dict[str, List[str]]]:
        """Get pros and cons for recommendations"""
        pros_cons = {
            'dotnet-6': {
                'pros': ['Excellent performance', 'Strong enterprise support', 'Great tooling'],
                'cons': ['Windows-centric', 'Higher licensing costs', 'Steeper learning curve']
            },
            'java-spring-boot': {
                'pros': ['Mature ecosystem', 'Excellent enterprise features', 'Strong community'],
                'cons': ['Verbose syntax', 'Higher memory usage', 'Slower startup time']
            },
            'go-microservices': {
                'pros': ['Excellent performance', 'Simple syntax', 'Great for microservices'],
                'cons': ['Limited ecosystem', 'Less mature web frameworks', 'Steeper learning curve']
            },
            'rust-web': {
                'pros': ['Best performance', 'Memory safety', 'Zero-cost abstractions'],
                'cons': ['Very steep learning curve', 'Limited ecosystem', 'Longer development time']
            },
            'node-express': {
                'pros': ['Fast development', 'Large ecosystem', 'JavaScript everywhere'],
                'cons': ['Single-threaded', 'Callback hell', 'Less type safety']
            },
            'python-3': {
                'pros': ['Easy to learn', 'Rich ecosystem', 'Great for AI/ML'],
                'cons': ['Slower performance', 'GIL limitations', 'Less type safety']
            },
            'php-laravel': {
                'pros': ['Fast development', 'Great for web apps', 'Easy deployment'],
                'cons': ['Performance limitations', 'Less suitable for complex apps', 'Security concerns']
            }
        }
        
        return {rec: pros_cons.get(rec, {'pros': [], 'cons': []}) for rec in recommendations}
    
    def _get_team_considerations(self, recommendations: List[str], team_expertise: str) -> Dict[str, str]:
        """Get team considerations for recommendations"""
        if not team_expertise:
            return {rec: 'Consider team training needs' for rec in recommendations}
        
        expertise_map = {
            'csharp': {'dotnet-6': 'Excellent fit', 'java-spring-boot': 'Good fit', 'go-microservices': 'Needs training'},
            'java': {'java-spring-boot': 'Excellent fit', 'dotnet-6': 'Good fit', 'go-microservices': 'Needs training'},
            'python': {'python-3': 'Excellent fit', 'node-express': 'Good fit', 'go-microservices': 'Needs training'},
            'javascript': {'node-express': 'Excellent fit', 'python-3': 'Good fit', 'go-microservices': 'Needs training'},
            'go': {'go-microservices': 'Excellent fit', 'rust-web': 'Good fit', 'dotnet-6': 'Needs training'},
            'rust': {'rust-web': 'Excellent fit', 'go-microservices': 'Good fit', 'dotnet-6': 'Needs training'}
        }
        
        team_map = expertise_map.get(team_expertise, {})
        return {rec: team_map.get(rec, 'Consider team training needs') for rec in recommendations}
    
    def _get_cost_analysis(self, recommendations: List[str], budget_constraint: str) -> Dict[str, str]:
        """Get cost analysis for recommendations"""
        cost_map = {
            'dotnet-6': 'Medium-High (licensing + hosting)',
            'java-spring-boot': 'Medium (hosting + tools)',
            'go-microservices': 'Low (open source + efficient)',
            'rust-web': 'Low (open source + very efficient)',
            'node-express': 'Low (open source + efficient)',
            'python-3': 'Low (open source + efficient)',
            'php-laravel': 'Low (open source + efficient)'
        }
        
        return {rec: cost_map.get(rec, 'Medium') for rec in recommendations} 