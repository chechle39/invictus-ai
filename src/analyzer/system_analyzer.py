"""
System Analyzer - Main analysis coordinator
Analyzes legacy systems to understand architecture, dependencies, and migration requirements
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from config import Config
from code_analyzer import CodeAnalyzer
from architecture_analyzer import ArchitectureAnalyzer
from dependency_analyzer import DependencyAnalyzer


@dataclass
class AnalysisResult:
    """Result of system analysis"""
    project_name: str
    project_path: str
    technology_stack: Dict[str, Any]
    architecture_patterns: List[str]
    dependencies: Dict[str, List[str]]
    code_metrics: Dict[str, Any]
    migration_risks: List[str]
    estimated_effort: str
    analysis_timestamp: str


class SystemAnalyzer:
    """Main system analyzer that coordinates the analysis process"""
    
    def __init__(self, config: Config):
        self.config = config
        self.console = Console()
        self.code_analyzer = CodeAnalyzer(config)
        self.architecture_analyzer = ArchitectureAnalyzer(config)
        self.dependency_analyzer = DependencyAnalyzer(config)
    
    def analyze_system(self, project_path: str, output_file: Optional[str] = None) -> AnalysisResult:
        """
        Analyze a legacy system and generate comprehensive analysis report
        
        Args:
            project_path: Path to the legacy system
            output_file: Optional output file for analysis results
            
        Returns:
            AnalysisResult containing comprehensive analysis
        """
        project_path = Path(project_path)
        
        if not project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")
        
        self.console.print(f"🔍 [bold blue]Analyzing system: {project_path.name}[/bold blue]")
        
        # Initialize analysis components
        analysis_result = AnalysisResult(
            project_name=project_path.name,
            project_path=str(project_path),
            technology_stack={},
            architecture_patterns=[],
            dependencies={},
            code_metrics={},
            migration_risks=[],
            estimated_effort="Unknown",
            analysis_timestamp=""
        )
        
        # Perform analysis with progress tracking
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            
            # Step 1: Code Analysis
            task1 = progress.add_task("📊 Analyzing code structure...", total=None)
            code_analysis = self.code_analyzer.analyze_codebase(project_path)
            analysis_result.code_metrics = code_analysis
            progress.update(task1, description="✅ Code analysis completed")
            
            # Step 2: Architecture Analysis
            task2 = progress.add_task("🏗️  Analyzing architecture patterns...", total=None)
            arch_analysis = self.architecture_analyzer.analyze_architecture(project_path)
            analysis_result.architecture_patterns = arch_analysis.get('patterns', [])
            analysis_result.technology_stack = arch_analysis.get('technology_stack', {})
            progress.update(task2, description="✅ Architecture analysis completed")
            
            # Step 3: Dependency Analysis
            task3 = progress.add_task("🔗 Analyzing dependencies...", total=None)
            dep_analysis = self.dependency_analyzer.analyze_dependencies(project_path)
            analysis_result.dependencies = dep_analysis
            progress.update(task3, description="✅ Dependency analysis completed")
            
            # Step 4: Risk Assessment
            task4 = progress.add_task("⚠️  Assessing migration risks...", total=None)
            risks = self._assess_migration_risks(analysis_result)
            analysis_result.migration_risks = risks
            progress.update(task4, description="✅ Risk assessment completed")
            
            # Step 5: Effort Estimation
            task5 = progress.add_task("⏱️  Estimating migration effort...", total=None)
            effort = self._estimate_migration_effort(analysis_result)
            analysis_result.estimated_effort = effort
            progress.update(task5, description="✅ Effort estimation completed")
        
        # Save results if output file specified
        if output_file:
            self._save_analysis_results(analysis_result, output_file)
        
        # Display summary
        self._display_analysis_summary(analysis_result)
        
        return analysis_result
    
    def _assess_migration_risks(self, analysis_result: AnalysisResult) -> List[str]:
        """Assess migration risks based on analysis results"""
        risks = []
        
        # Check for legacy technologies
        tech_stack = analysis_result.technology_stack
        if 'framework' in tech_stack:
            framework = tech_stack['framework']
            if 'framework' in framework.lower() and 'core' not in framework.lower():
                risks.append(f"Legacy framework detected: {framework}")
        
        # Check for complex dependencies
        if len(analysis_result.dependencies.get('external', [])) > 20:
            risks.append("High number of external dependencies may complicate migration")
        
        # Check for custom authentication
        if any('auth' in pattern.lower() for pattern in analysis_result.architecture_patterns):
            risks.append("Custom authentication system may require significant refactoring")
        
        # Check for database dependencies
        if 'database' in tech_stack:
            db_type = tech_stack['database']
            if 'sql' in db_type.lower() and 'entity' in tech_stack:
                risks.append("Database migration may require data transformation")
        
        # Check for session state dependencies
        if any('session' in pattern.lower() for pattern in analysis_result.architecture_patterns):
            risks.append("Session state management may need architectural changes")
        
        return risks
    
    def _estimate_migration_effort(self, analysis_result: AnalysisResult) -> str:
        """Estimate migration effort based on analysis results"""
        effort_score = 0
        
        # Base effort from code metrics
        loc = analysis_result.code_metrics.get('total_lines', 0)
        if loc < 10000:
            effort_score += 1
        elif loc < 50000:
            effort_score += 2
        else:
            effort_score += 3
        
        # Effort from architecture complexity
        patterns = analysis_result.architecture_patterns
        if 'microservices' in patterns:
            effort_score += 2
        if 'monolith' in patterns:
            effort_score += 1
        
        # Effort from technology stack
        tech_stack = analysis_result.technology_stack
        if 'framework' in tech_stack:
            framework = tech_stack['framework']
            if 'framework' in framework.lower():
                effort_score += 2
        
        # Effort from risks
        effort_score += len(analysis_result.migration_risks)
        
        # Convert to timeline
        if effort_score <= 3:
            return "1-2 weeks"
        elif effort_score <= 6:
            return "2-4 weeks"
        elif effort_score <= 9:
            return "1-2 months"
        else:
            return "2-3 months"
    
    def _save_analysis_results(self, analysis_result: AnalysisResult, output_file: str):
        """Save analysis results to file"""
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to JSON-serializable format
        result_dict = asdict(analysis_result)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result_dict, f, indent=2, ensure_ascii=False)
        
        self.console.print(f"💾 Analysis results saved to: {output_path}")
    
    def _display_analysis_summary(self, analysis_result: AnalysisResult):
        """Display analysis summary"""
        self.console.print("\n📋 [bold green]Analysis Summary[/bold green]")
        self.console.print("=" * 50)
        
        # Project info
        self.console.print(f"📁 Project: {analysis_result.project_name}")
        self.console.print(f"📊 Total Lines: {analysis_result.code_metrics.get('total_lines', 0):,}")
        self.console.print(f"📁 Files Analyzed: {analysis_result.code_metrics.get('total_files', 0)}")
        
        # Technology stack
        if analysis_result.technology_stack:
            self.console.print("\n🔧 [bold]Technology Stack:[/bold]")
            for tech, version in analysis_result.technology_stack.items():
                self.console.print(f"  • {tech}: {version}")
        
        # Architecture patterns
        if analysis_result.architecture_patterns:
            self.console.print("\n🏗️  [bold]Architecture Patterns:[/bold]")
            for pattern in analysis_result.architecture_patterns:
                self.console.print(f"  • {pattern}")
        
        # Dependencies
        if analysis_result.dependencies:
            self.console.print("\n🔗 [bold]Dependencies:[/bold]")
            for dep_type, deps in analysis_result.dependencies.items():
                self.console.print(f"  • {dep_type}: {len(deps)} packages")
        
        # Risks
        if analysis_result.migration_risks:
            self.console.print("\n⚠️  [bold red]Migration Risks:[/bold red]")
            for risk in analysis_result.migration_risks:
                self.console.print(f"  • {risk}")
        
        # Effort estimation
        self.console.print(f"\n⏱️  [bold]Estimated Effort:[/bold] {analysis_result.estimated_effort}")
        
        self.console.print("\n" + "=" * 50) 