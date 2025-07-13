"""
Migration Validator - Validates migration maps and performs quality checks
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from openai import OpenAI

from config import Config


class MigrationValidator:
    """Validates migration maps and performs quality checks"""
    
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(**config.get_openai_config())
    
    def validate_migration_map(self, migration_map_file: str) -> Dict[str, Any]:
        """
        Validate migration map and perform quality checks
        
        Args:
            migration_map_file: Path to migration map JSON file
            
        Returns:
            Dictionary containing validation results
        """
        # Load migration map
        with open(migration_map_file, 'r', encoding='utf-8') as f:
            migration_map = json.load(f)
        
        # Perform validation checks
        validation_result = {
            'quality_score': 0.0,
            'issues': [],
            'recommendations': [],
            'validation_details': {}
        }
        
        # Check completeness
        completeness_score = self._check_completeness(migration_map)
        validation_result['validation_details']['completeness'] = completeness_score
        
        # Check consistency
        consistency_score = self._check_consistency(migration_map)
        validation_result['validation_details']['consistency'] = consistency_score
        
        # Check feasibility
        feasibility_score = self._check_feasibility(migration_map)
        validation_result['validation_details']['feasibility'] = feasibility_score
        
        # Check risks
        risk_assessment = self._assess_risks(migration_map)
        validation_result['validation_details']['risk_assessment'] = risk_assessment
        
        # Calculate overall quality score
        validation_result['quality_score'] = (
            completeness_score * 0.3 +
            consistency_score * 0.3 +
            feasibility_score * 0.4
        )
        
        # Generate recommendations using AI
        ai_recommendations = self._generate_ai_recommendations(migration_map)
        validation_result['recommendations'].extend(ai_recommendations)
        
        return validation_result
    
    def _check_completeness(self, migration_map: Dict[str, Any]) -> float:
        """Check if migration map is complete"""
        score = 1.0
        issues = []
        
        required_fields = [
            'project_name', 'source_stack', 'target_stack',
            'migration_strategy', 'technology_mapping', 'risks'
        ]
        
        for field in required_fields:
            if field not in migration_map:
                score -= 0.15
                issues.append(f"Missing required field: {field}")
        
        # Check migration strategy completeness
        strategy = migration_map.get('migration_strategy', {})
        strategy_fields = ['direct_conversion', 'rewrite_required', 'special_handling']
        
        for field in strategy_fields:
            if field not in strategy:
                score -= 0.1
                issues.append(f"Missing strategy field: {field}")
        
        # Check if any files are categorized
        total_files = 0
        for field in strategy_fields:
            if field in strategy:
                total_files += len(strategy[field])
        
        if total_files == 0:
            score -= 0.2
            issues.append("No files categorized in migration strategy")
        
        return max(0.0, score)
    
    def _check_consistency(self, migration_map: Dict[str, Any]) -> float:
        """Check if migration map is consistent"""
        score = 1.0
        issues = []
        
        # Check technology mapping consistency
        tech_mapping = migration_map.get('technology_mapping', {})
        source_stack = migration_map.get('source_stack', '')
        target_stack = migration_map.get('target_stack', '')
        
        # Basic consistency checks
        if source_stack == target_stack:
            score -= 0.3
            issues.append("Source and target stacks are identical")
        
        if not tech_mapping:
            score -= 0.2
            issues.append("No technology mappings defined")
        
        # Check for conflicting mappings
        mapped_technologies = set()
        for old_tech, new_tech in tech_mapping.items():
            if new_tech in mapped_technologies:
                score -= 0.1
                issues.append(f"Multiple technologies mapping to: {new_tech}")
            mapped_technologies.add(new_tech)
        
        return max(0.0, score)
    
    def _check_feasibility(self, migration_map: Dict[str, Any]) -> float:
        """Check if migration plan is feasible"""
        score = 1.0
        issues = []
        
        # Check effort estimation
        effort = migration_map.get('estimated_effort', '')
        if not effort or effort == 'Unknown':
            score -= 0.2
            issues.append("No effort estimation provided")
        
        # Check risk assessment
        risks = migration_map.get('risks', [])
        if not risks:
            score -= 0.1
            issues.append("No risks identified")
        
        # Check technology mapping feasibility
        tech_mapping = migration_map.get('technology_mapping', {})
        source_stack = migration_map.get('source_stack', '')
        
        # Check for common migration patterns
        if 'dotnet_framework' in source_stack.lower():
            expected_mappings = ['System.Web.Http', 'Entity Framework 6', 'Web.config']
            missing_mappings = [tech for tech in expected_mappings if tech not in tech_mapping]
            if missing_mappings:
                score -= 0.1
                issues.append(f"Missing common .NET Framework mappings: {missing_mappings}")
        
        return max(0.0, score)
    
    def _assess_risks(self, migration_map: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks in migration plan"""
        risks = migration_map.get('risks', [])
        
        risk_assessment = {
            'total_risks': len(risks),
            'high_risk_count': 0,
            'medium_risk_count': 0,
            'low_risk_count': 0,
            'risk_categories': {}
        }
        
        # Categorize risks
        for risk in risks:
            risk_lower = risk.lower()
            
            if any(keyword in risk_lower for keyword in ['authentication', 'security', 'data loss']):
                risk_assessment['high_risk_count'] += 1
                risk_assessment['risk_categories']['security'] = risk_assessment['risk_categories'].get('security', 0) + 1
            elif any(keyword in risk_lower for keyword in ['performance', 'database', 'session']):
                risk_assessment['medium_risk_count'] += 1
                risk_assessment['risk_categories']['performance'] = risk_assessment['risk_categories'].get('performance', 0) + 1
            else:
                risk_assessment['low_risk_count'] += 1
                risk_assessment['risk_categories']['general'] = risk_assessment['risk_categories'].get('general', 0) + 1
        
        return risk_assessment
    
    def _generate_ai_recommendations(self, migration_map: Dict[str, Any]) -> List[str]:
        """Generate AI-powered recommendations for migration map improvement"""
        
        try:
            # Prepare prompt for AI
            prompt = self._build_validation_prompt(migration_map)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software migration consultant. Analyze migration maps and provide specific, actionable recommendations for improvement. Focus on practical advice that can be implemented."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=self.config.max_tokens // 2,  # Shorter response for recommendations
                temperature=self.config.temperature,
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            
            # Extract recommendations
            recommendations = []
            for line in ai_response.split('\n'):
                line = line.strip()
                if line.startswith('- ') or line.startswith('• '):
                    recommendations.append(line[2:])
                elif line and not line.startswith('#'):
                    recommendations.append(line)
            
            return recommendations[:5]  # Limit to top 5 recommendations
            
        except Exception as e:
            # Fallback recommendations
            return [
                "Consider adding more detailed technology mappings",
                "Include specific file paths in migration strategy",
                "Add timeline estimates for each migration phase",
                "Define rollback procedures for critical components",
                "Include testing requirements for each migration step"
            ]
    
    def _build_validation_prompt(self, migration_map: Dict[str, Any]) -> str:
        """Build prompt for AI validation"""
        
        return f"""Analyze this migration map and provide specific recommendations for improvement:

Migration Map:
- Project: {migration_map.get('project_name', 'Unknown')}
- Source: {migration_map.get('source_stack', 'Unknown')}
- Target: {migration_map.get('target_stack', 'Unknown')}
- Strategy: {migration_map.get('migration_strategy', {})}
- Technology Mapping: {migration_map.get('technology_mapping', {})}
- Risks: {migration_map.get('risks', [])}

Provide 3-5 specific, actionable recommendations to improve this migration plan. Focus on:
1. Completeness and detail
2. Risk mitigation
3. Implementation feasibility
4. Testing strategy
5. Timeline optimization

Format as bullet points with specific suggestions.
""" 