"""
Migration Generator - Generates migration plans and documentation
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from config import Config


class MigrationGenerator:
    """Generates migration plans and documentation from migration maps"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def generate_migration_plan(self, migration_map_file: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate detailed migration plan and documentation
        
        Args:
            migration_map_file: Path to migration map JSON file
            output_dir: Optional output directory for generated files
            
        Returns:
            Dictionary containing generation results
        """
        # Load migration map
        with open(migration_map_file, 'r', encoding='utf-8') as f:
            migration_map = json.load(f)
        
        # Set output directory
        if not output_dir:
            output_dir = f"migration-plan-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate different types of documentation
        results = {
            'migration_guide': self._generate_migration_guide(migration_map, output_path),
            'test_plan': self._generate_test_plan(migration_map, output_path),
            'timeline': self._generate_timeline(migration_map, output_path),
            'risk_assessment': self._generate_risk_assessment(migration_map, output_path),
            'technology_mapping': self._generate_technology_mapping(migration_map, output_path)
        }
        
        return results
    
    def _generate_migration_guide(self, migration_map: Dict[str, Any], output_path: Path) -> str:
        """Generate step-by-step migration guide"""
        
        guide_content = f"""# Migration Guide: {migration_map.get('project_name', 'Unknown')}

## Overview
- **Source Stack**: {migration_map.get('source_stack', 'Unknown')}
- **Target Stack**: {migration_map.get('target_stack', 'Unknown')}
- **Estimated Effort**: {migration_map.get('estimated_effort', 'Unknown')}

## Migration Strategy

### Phase 1: Direct Conversions
Files that can be migrated with minimal changes:

"""
        
        strategy = migration_map.get('migration_strategy', {})
        direct_conversion = strategy.get('direct_conversion', [])
        
        for file_pattern in direct_conversion:
            guide_content += f"- [ ] {file_pattern}\n"
        
        guide_content += f"""
### Phase 2: Rewrites Required
Files that need significant rewriting:

"""
        
        rewrite_required = strategy.get('rewrite_required', [])
        for file_pattern in rewrite_required:
            guide_content += f"- [ ] {file_pattern}\n"
        
        guide_content += f"""
### Phase 3: Special Handling
Files requiring special attention:

"""
        
        special_handling = strategy.get('special_handling', [])
        for file_pattern in special_handling:
            guide_content += f"- [ ] {file_pattern}\n"
        
        guide_content += f"""
## Technology Mapping

"""
        
        tech_mapping = migration_map.get('technology_mapping', {})
        for old_tech, new_tech in tech_mapping.items():
            guide_content += f"- **{old_tech}** → **{new_tech}**\n"
        
        guide_content += f"""
## Migration Steps

1. **Preparation**
   - Backup current system
   - Set up development environment
   - Install required tools and dependencies

2. **Direct Conversions**
   - Migrate models and entities
   - Update package references
   - Convert configuration files

3. **Rewrites**
   - Rewrite controllers and services
   - Implement new authentication system
   - Update database access layer

4. **Special Handling**
   - Handle custom middleware
   - Migrate session state management
   - Update deployment configuration

5. **Testing**
   - Unit tests for migrated components
   - Integration tests for API endpoints
   - Performance testing

6. **Deployment**
   - Deploy to staging environment
   - Run smoke tests
   - Deploy to production

## Post-Migration Checklist

- [ ] All functionality working correctly
- [ ] Performance meets requirements
- [ ] Security measures in place
- [ ] Monitoring and logging configured
- [ ] Documentation updated
- [ ] Team training completed
"""
        
        guide_file = output_path / "migration-guide.md"
        with open(guide_file, 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        return str(guide_file)
    
    def _generate_test_plan(self, migration_map: Dict[str, Any], output_path: Path) -> str:
        """Generate test plan for migration"""
        
        test_plan_content = f"""# Test Plan: {migration_map.get('project_name', 'Unknown')} Migration

## Test Strategy

### Unit Tests
- [ ] Model validation tests
- [ ] Service layer tests
- [ ] Controller action tests
- [ ] Repository pattern tests

### Integration Tests
- [ ] API endpoint tests
- [ ] Database integration tests
- [ ] Authentication flow tests
- [ ] External service integration tests

### Performance Tests
- [ ] Load testing
- [ ] Stress testing
- [ ] Database performance tests
- [ ] Memory usage monitoring

### Security Tests
- [ ] Authentication tests
- [ ] Authorization tests
- [ ] Input validation tests
- [ ] SQL injection tests

## Test Environment Setup

### Prerequisites
- Test database with sample data
- Mock external services
- Test user accounts
- Performance monitoring tools

### Test Data
- Sample user data
- Test transactions
- Edge case scenarios
- Error conditions

## Test Execution

### Phase 1: Unit Testing
1. Run unit tests for migrated components
2. Verify all tests pass
3. Check code coverage (target: >80%)

### Phase 2: Integration Testing
1. Test API endpoints
2. Verify database operations
3. Test authentication flows
4. Validate error handling

### Phase 3: Performance Testing
1. Load test with realistic data
2. Monitor response times
3. Check resource usage
4. Validate scalability

### Phase 4: Security Testing
1. Penetration testing
2. Vulnerability scanning
3. Security audit
4. Compliance verification

## Test Results Tracking

| Test Category | Status | Issues | Resolution |
|---------------|--------|--------|------------|
| Unit Tests    |        |        |            |
| Integration   |        |        |            |
| Performance   |        |        |            |
| Security      |        |        |            |

## Rollback Plan

If critical issues are found:
1. Stop migration process
2. Revert to previous version
3. Document issues
4. Plan fixes
5. Retest before proceeding
"""
        
        test_plan_file = output_path / "test-plan.md"
        with open(test_plan_file, 'w', encoding='utf-8') as f:
            f.write(test_plan_content)
        
        return str(test_plan_file)
    
    def _generate_timeline(self, migration_map: Dict[str, Any], output_path: Path) -> str:
        """Generate migration timeline"""
        
        timeline_content = f"""# Migration Timeline: {migration_map.get('project_name', 'Unknown')}

## Overall Timeline: {migration_map.get('estimated_effort', 'Unknown')}

### Week 1: Preparation
- [ ] Environment setup
- [ ] Tool installation
- [ ] Team training
- [ ] Backup creation

### Week 2: Direct Conversions
- [ ] Model migrations
- [ ] Configuration updates
- [ ] Package reference updates
- [ ] Basic testing

### Week 3: Rewrites
- [ ] Controller rewrites
- [ ] Service layer updates
- [ ] Authentication migration
- [ ] Integration testing

### Week 4: Special Handling
- [ ] Custom middleware
- [ ] Session management
- [ ] Deployment configuration
- [ ] Performance optimization

### Week 5: Testing & Validation
- [ ] Comprehensive testing
- [ ] Bug fixes
- [ ] Performance tuning
- [ ] Security validation

### Week 6: Deployment
- [ ] Staging deployment
- [ ] User acceptance testing
- [ ] Production deployment
- [ ] Monitoring setup

## Milestones

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Environment Ready | Week 1 | | |
| Direct Conversions | Week 2 | | |
| Rewrites Complete | Week 3 | | |
| Special Handling | Week 4 | | |
| Testing Complete | Week 5 | | |
| Production Ready | Week 6 | | |

## Risk Mitigation

### High Risk Items
- Authentication system migration
- Database schema changes
- Performance impact
- User training requirements

### Mitigation Strategies
- Parallel development approach
- Comprehensive testing
- Gradual rollout
- Rollback procedures
"""
        
        timeline_file = output_path / "timeline.md"
        with open(timeline_file, 'w', encoding='utf-8') as f:
            f.write(timeline_content)
        
        return str(timeline_file)
    
    def _generate_risk_assessment(self, migration_map: Dict[str, Any], output_path: Path) -> str:
        """Generate risk assessment document"""
        
        risks = migration_map.get('risks', [])
        
        risk_content = f"""# Risk Assessment: {migration_map.get('project_name', 'Unknown')} Migration

## Identified Risks

"""
        
        for i, risk in enumerate(risks, 1):
            risk_content += f"### Risk {i}: {risk}\n\n"
            risk_content += f"**Impact**: High/Medium/Low\n"
            risk_content += f"**Probability**: High/Medium/Low\n"
            risk_content += f"**Mitigation**: [Describe mitigation strategy]\n\n"
        
        risk_content += f"""
## Risk Matrix

| Risk Level | Count | Mitigation Priority |
|------------|-------|-------------------|
| High       |       | Immediate         |
| Medium     |       | Within 1 week     |
| Low        |       | Within 2 weeks    |

## Contingency Plans

### Critical Risks
- [ ] Data loss prevention
- [ ] Service downtime minimization
- [ ] Rollback procedures
- [ ] Communication plan

### Medium Risks
- [ ] Performance degradation
- [ ] User experience impact
- [ ] Training requirements
- [ ] Timeline delays

### Low Risks
- [ ] Documentation updates
- [ ] Process changes
- [ ] Tool adoption
- [ ] Knowledge transfer

## Monitoring and Control

### Key Metrics
- Migration progress percentage
- Test pass rate
- Performance benchmarks
- User feedback scores

### Escalation Procedures
1. Identify issue severity
2. Notify stakeholders
3. Implement mitigation
4. Monitor resolution
5. Document lessons learned
"""
        
        risk_file = output_path / "risk-assessment.md"
        with open(risk_file, 'w', encoding='utf-8') as f:
            f.write(risk_content)
        
        return str(risk_file)
    
    def _generate_technology_mapping(self, migration_map: Dict[str, Any], output_path: Path) -> str:
        """Generate detailed technology mapping document"""
        
        tech_mapping = migration_map.get('technology_mapping', {})
        
        mapping_content = f"""# Technology Mapping: {migration_map.get('project_name', 'Unknown')}

## Migration Summary
- **From**: {migration_map.get('source_stack', 'Unknown')}
- **To**: {migration_map.get('target_stack', 'Unknown')}

## Detailed Technology Mappings

"""
        
        for old_tech, new_tech in tech_mapping.items():
            mapping_content += f"""### {old_tech} → {new_tech}

**Purpose**: [Describe what this technology does]

**Migration Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Considerations**:
- [Consideration 1]
- [Consideration 2]
- [Consideration 3]

**Testing Requirements**:
- [Test requirement 1]
- [Test requirement 2]

---

"""
        
        mapping_content += f"""
## Implementation Guidelines

### Best Practices
- Follow target technology conventions
- Maintain backward compatibility where possible
- Implement proper error handling
- Add comprehensive logging
- Write unit tests for all changes

### Common Pitfalls
- Avoid hardcoding configuration values
- Don't skip proper testing
- Ensure proper error handling
- Consider performance implications
- Plan for scalability

### Quality Gates
- [ ] Code review completed
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Performance benchmarks met
- [ ] Security review completed
- [ ] Documentation updated
"""
        
        mapping_file = output_path / "technology-mapping.md"
        with open(mapping_file, 'w', encoding='utf-8') as f:
            f.write(mapping_content)
        
        return str(mapping_file) 