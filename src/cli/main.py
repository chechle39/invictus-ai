"""
Main CLI interface for AI Migration Map Generator
"""

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import Config
from analyzer import SystemAnalyzer
from mapper import MigrationMapper
from generator import MigrationGenerator
from validator import MigrationValidator


console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="AI Migration Map Generator")
def main():
    """🚀 AI-powered system migration tool for FPT Software"""
    pass


@main.command()
@click.argument('project_path', type=click.Path(exists=True, file_okay=False))
@click.option('-o', '--output', type=click.Path(), help='Output file for analysis results')
@click.option('--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
@click.option('--model', default='gpt-4', help='OpenAI model to use')
def analyze(project_path, output, api_key, model):
    """🔍 Analyze a legacy system and generate comprehensive analysis report"""
    
    try:
        # Initialize configuration
        config = Config(api_key=api_key, model=model)
        
        if not config.is_valid:
            console.print("❌ [red]Configuration error![/red]")
            console.print("💡 Set OPENAI_API_KEY environment variable or use --api-key option")
            sys.exit(1)
        
        # Initialize analyzer
        analyzer = SystemAnalyzer(config)
        
        # Perform analysis
        result = analyzer.analyze_system(project_path, output)
        
        console.print(f"\n✅ [bold green]Analysis completed successfully![/bold green]")
        if output:
            console.print(f"📁 Results saved to: {output}")
        
    except Exception as e:
        console.print(f"❌ [red]Error during analysis: {str(e)}[/red]")
        sys.exit(1)


@main.command()
@click.argument('analysis_file', type=click.Path(exists=True))
@click.option('-t', '--target', required=True, 
              type=click.Choice([
                  'dotnet-core', 'dotnet-6', 'microservices', 'cloud-native',
                  'java-17', 'java-spring-boot', 'python-3', 'node-express', 
                  'node-nest', 'go-microservices', 'rust-web', 'php-laravel'
              ]),
              help='Target technology stack')
@click.option('--source-language', 
              type=click.Choice(['csharp', 'java', 'python', 'javascript', 'typescript', 'php', 'go', 'rust']),
              help='Source programming language (auto-detected if not specified)')
@click.option('--target-language',
              type=click.Choice(['csharp', 'java', 'python', 'javascript', 'typescript', 'php', 'go', 'rust']),
              help='Target programming language')
@click.option('--template', help='Custom migration template')
@click.option('--api-key', help='OpenAI API key')
@click.option('--model', default='gpt-4', help='OpenAI model to use')
def generate(analysis_file, target, source_language, target_language, template, api_key, model):
    """🗺️ Generate migration map from analysis results"""
    
    try:
        # Initialize configuration
        config = Config(api_key=api_key, model=model)
        
        if not config.is_valid:
            console.print("❌ [red]Configuration error![/red]")
            console.print("💡 Set OPENAI_API_KEY environment variable or use --api-key option")
            sys.exit(1)
        
        # Initialize mapper
        mapper = MigrationMapper(config)
        
        # Generate migration map
        migration_map = mapper.generate_migration_map(
            analysis_file, target, template, 
            source_language=source_language,
            target_language=target_language
        )
        
        # Display results
        _display_migration_map(migration_map)
        
        console.print(f"\n✅ [bold green]Migration map generated successfully![/bold green]")
        
    except Exception as e:
        console.print(f"❌ [red]Error generating migration map: {str(e)}[/red]")
        sys.exit(1)


@main.command()
@click.argument('migration_map_file', type=click.Path(exists=True))
@click.option('--output-dir', type=click.Path(), help='Output directory for generated files')
@click.option('--api-key', help='OpenAI API key')
@click.option('--model', default='gpt-4', help='OpenAI model to use')
def plan(migration_map_file, output_dir, api_key, model):
    """📋 Generate detailed migration plan and documentation"""
    
    try:
        # Initialize configuration
        config = Config(api_key=api_key, model=model)
        
        if not config.is_valid:
            console.print("❌ [red]Configuration error![/red]")
            console.print("💡 Set OPENAI_API_KEY environment variable or use --api-key option")
            sys.exit(1)
        
        # Initialize generator
        generator = MigrationGenerator(config)
        
        # Generate migration plan
        plan_result = generator.generate_migration_plan(migration_map_file, output_dir)
        
        console.print(f"\n✅ [bold green]Migration plan generated successfully![/bold green]")
        if output_dir:
            console.print(f"📁 Files saved to: {output_dir}")
        
    except Exception as e:
        console.print(f"❌ [red]Error generating migration plan: {str(e)}[/red]")
        sys.exit(1)


@main.command()
@click.argument('migration_map_file', type=click.Path(exists=True))
@click.option('--api-key', help='OpenAI API key')
@click.option('--model', default='gpt-4', help='OpenAI model to use')
def validate(migration_map_file, api_key, model):
    """✅ Validate migration map and perform quality checks"""
    
    try:
        # Initialize configuration
        config = Config(api_key=api_key, model=model)
        
        if not config.is_valid:
            console.print("❌ [red]Configuration error![/red]")
            console.print("💡 Set OPENAI_API_KEY environment variable or use --api-key option")
            sys.exit(1)
        
        # Initialize validator
        validator = MigrationValidator(config)
        
        # Validate migration map
        validation_result = validator.validate_migration_map(migration_map_file)
        
        # Display validation results
        _display_validation_results(validation_result)
        
        console.print(f"\n✅ [bold green]Validation completed![/bold green]")
        
    except Exception as e:
        console.print(f"❌ [red]Error during validation: {str(e)}[/red]")
        sys.exit(1)


@main.command()
def templates():
    """📚 List available migration templates"""
    
    try:
        config = Config()
        templates = config.get_migration_templates()
        
        if not templates:
            console.print("📚 [yellow]No custom templates found.[/yellow]")
            console.print("💡 Create templates in the templates/ directory")
            return
        
        table = Table(title="Available Migration Templates")
        table.add_column("Template Name", style="cyan")
        table.add_column("Description", style="green")
        
        for template in templates:
            table.add_row(template, "Custom migration template")
        
        console.print(table)
        
    except Exception as e:
        console.print(f"❌ [red]Error listing templates: {str(e)}[/red]")
        sys.exit(1)


@main.command()
def demo():
    """🎯 Show demo and usage examples"""
    
    demo_text = """[bold blue]🚀 AI Migration Map Generator - Demo[/bold blue]

[green]✨ Features:[/green]
• AI-powered system analysis
• Migration map generation
• Technology stack mapping
• Risk assessment and effort estimation
• Automated documentation generation

[cyan]📖 Usage Examples:[/cyan]

[bold]Analyze legacy system:[/bold]
ai-migration-map analyze ./legacy-dotnet-app -o analysis.json

[bold]Generate migration map:[/bold]
ai-migration-map generate analysis.json -t dotnet-6

[bold]Create migration plan:[/bold]
ai-migration-map plan migration-map.json --output-dir ./migration-plan

[bold]Validate migration map:[/bold]
ai-migration-map validate migration-map.json

[bold]List templates:[/bold]
ai-migration-map templates

[yellow]💡 Set your OpenAI API key:[/yellow]
export OPENAI_API_KEY="your-api-key-here"

[bold]Supported Migrations:[/bold]
• .NET Framework → .NET Core/6
• Monolith → Microservices
• SQL → NoSQL
• REST → GraphQL
• On-premise → Cloud-native
"""
    
    console.print(Panel(demo_text, title="[bold green]Demo & Usage Guide[/bold green]"))


@main.command()
@click.argument('analysis_file', type=click.Path(exists=True))
@click.option('--use-case', 
              type=click.Choice(['web-app', 'api-service', 'microservices', 'mobile-backend', 'data-processing', 'ai-ml', 'iot', 'gaming', 'enterprise', 'startup']),
              help='Primary use case of the application')
@click.option('--performance-requirement',
              type=click.Choice(['high', 'medium', 'low']),
              default='medium',
              help='Performance requirements')
@click.option('--team-expertise',
              type=click.Choice(['csharp', 'java', 'python', 'javascript', 'go', 'rust', 'mixed']),
              help='Team programming language expertise')
@click.option('--budget-constraint',
              type=click.Choice(['low', 'medium', 'high']),
              default='medium',
              help='Budget constraints for migration')
@click.option('--api-key', help='OpenAI API key')
@click.option('--model', default='gpt-4', help='OpenAI model to use')
def suggest(analysis_file, use_case, performance_requirement, team_expertise, budget_constraint, api_key, model):
    """💡 Suggest target technologies based on project analysis and requirements"""
    
    try:
        # Initialize configuration
        config = Config(api_key=api_key, model=model)
        
        if not config.is_valid:
            console.print("❌ [red]Configuration error![/red]")
            console.print("💡 Set OPENAI_API_KEY environment variable or use --api-key option")
            sys.exit(1)
        
        # Initialize mapper
        mapper = MigrationMapper(config)
        
        # Generate technology suggestions
        suggestions = mapper.suggest_target_technologies(
            analysis_file, use_case, performance_requirement, team_expertise, budget_constraint
        )
        
        # Display suggestions
        _display_technology_suggestions(suggestions)
        
        console.print(f"\n✅ [bold green]Technology suggestions generated![/bold green]")
        
    except Exception as e:
        console.print(f"❌ [red]Error generating suggestions: {str(e)}[/red]")
        sys.exit(1)


def _display_migration_map(migration_map):
    """Display migration map in a formatted table"""
    
    console.print("\n🗺️  [bold blue]Migration Map[/bold blue]")
    console.print("=" * 60)
    
    # Project info
    console.print(f"📁 Project: {migration_map.get('project_name', 'Unknown')}")
    console.print(f"🔧 Source Stack: {migration_map.get('source_stack', 'Unknown')}")
    console.print(f"🎯 Target Stack: {migration_map.get('target_stack', 'Unknown')}")
    console.print(f"⏱️  Estimated Effort: {migration_map.get('estimated_effort', 'Unknown')}")
    
    # Migration strategy
    strategy = migration_map.get('migration_strategy', {})
    
    if 'direct_conversion' in strategy:
        console.print(f"\n✅ [green]Direct Conversion ({len(strategy['direct_conversion'])} files):[/green]")
        for file in strategy['direct_conversion'][:5]:  # Show first 5
            console.print(f"  • {file}")
        if len(strategy['direct_conversion']) > 5:
            console.print(f"  ... and {len(strategy['direct_conversion']) - 5} more")
    
    if 'rewrite_required' in strategy:
        console.print(f"\n🔄 [yellow]Rewrite Required ({len(strategy['rewrite_required'])} files):[/yellow]")
        for file in strategy['rewrite_required'][:5]:
            console.print(f"  • {file}")
        if len(strategy['rewrite_required']) > 5:
            console.print(f"  ... and {len(strategy['rewrite_required']) - 5} more")
    
    if 'special_handling' in strategy:
        console.print(f"\n⚠️  [red]Special Handling ({len(strategy['special_handling'])} files):[/red]")
        for file in strategy['special_handling'][:5]:
            console.print(f"  • {file}")
        if len(strategy['special_handling']) > 5:
            console.print(f"  ... and {len(strategy['special_handling']) - 5} more")
    
    # Technology mapping
    tech_mapping = migration_map.get('technology_mapping', {})
    if tech_mapping:
        console.print(f"\n🔧 [bold]Technology Mapping:[/bold]")
        for old_tech, new_tech in tech_mapping.items():
            console.print(f"  • {old_tech} → {new_tech}")
    
    # Risks
    risks = migration_map.get('risks', [])
    if risks:
        console.print(f"\n⚠️  [bold red]Migration Risks:[/bold red]")
        for risk in risks:
            console.print(f"  • {risk}")


def _display_validation_results(validation_result):
    """Display validation results"""
    
    console.print("\n✅ [bold blue]Validation Results[/bold blue]")
    console.print("=" * 50)
    
    # Quality score
    quality_score = validation_result.get('quality_score', 0)
    console.print(f"📊 Quality Score: {quality_score:.1%}")
    
    # Issues
    issues = validation_result.get('issues', [])
    if issues:
        console.print(f"\n❌ [red]Issues Found ({len(issues)}):[/red]")
        for issue in issues:
            console.print(f"  • {issue}")
    else:
        console.print(f"\n✅ [green]No issues found![/green]")
    
    # Recommendations
    recommendations = validation_result.get('recommendations', [])
    if recommendations:
        console.print(f"\n💡 [yellow]Recommendations ({len(recommendations)}):[/yellow]")
        for rec in recommendations:
            console.print(f"  • {rec}")


def _display_technology_suggestions(suggestions):
    """Display technology suggestions in a formatted table"""
    
    console.print("\n💡 [bold blue]Technology Suggestions[/bold blue]")
    console.print("=" * 60)
    
    # Primary recommendations
    primary_recs = suggestions.get('primary_recommendations', [])
    if primary_recs:
        console.print(f"\n🏆 [bold green]Primary Recommendations:[/bold green]")
        for i, rec in enumerate(primary_recs, 1):
            console.print(f"  {i}. {rec}")
    
    # Alternative options
    alt_options = suggestions.get('alternative_options', [])
    if alt_options:
        console.print(f"\n🔄 [bold yellow]Alternative Options:[/bold yellow]")
        for option in alt_options:
            console.print(f"  • {option}")
    
    # Migration effort
    effort = suggestions.get('migration_effort', {})
    if effort:
        console.print(f"\n⏱️  [bold]Migration Effort:[/bold]")
        for tech, est_effort in effort.items():
            console.print(f"  • {tech}: {est_effort}")
    
    # Pros and cons
    pros_cons = suggestions.get('pros_cons', {})
    if pros_cons:
        console.print(f"\n✅ [bold green]Pros & Cons:[/bold green]")
        for tech, details in pros_cons.items():
            console.print(f"  [bold]{tech}:[/bold]")
            if 'pros' in details and details['pros']:
                console.print(f"    ✅ Pros: {', '.join(details['pros'])}")
            if 'cons' in details and details['cons']:
                console.print(f"    ❌ Cons: {', '.join(details['cons'])}")
    
    # Team considerations
    team_considerations = suggestions.get('team_considerations', {})
    if team_considerations:
        console.print(f"\n👥 [bold]Team Considerations:[/bold]")
        for tech, consideration in team_considerations.items():
            console.print(f"  • {tech}: {consideration}")
    
    # Cost analysis
    cost_analysis = suggestions.get('cost_analysis', {})
    if cost_analysis:
        console.print(f"\n💰 [bold]Cost Analysis:[/bold]")
        for tech, cost in cost_analysis.items():
            console.print(f"  • {tech}: {cost}")
    
    # Technology mapping
    tech_mapping = suggestions.get('technology_mapping', {})
    if tech_mapping:
        console.print(f"\n🔧 [bold]Technology Mapping:[/bold]")
        for tech, mappings in tech_mapping.items():
            console.print(f"  [bold]{tech}:[/bold]")
            for old_tech, new_tech in mappings.items():
                console.print(f"    • {old_tech} → {new_tech}")


if __name__ == '__main__':
    main() 