#!/usr/bin/env python3
"""
AI Code Migrator CLI - Python Version
Command-line interface with human validation and OpenAI integration
"""

import click
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.syntax import Syntax
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .migrator import CodeMigrator
from .validator import HumanValidator
from .config import Config

console = Console()

@click.group()
@click.version_option(version="1.0.0", prog_name="AI Code Migrator")
def cli():
    """🚀 AI-powered code migration tool with human validation"""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-t', '--target', required=True, 
              type=click.Choice(['javascript', 'python', 'typescript', 'java', 'csharp', 'go', 'rust']),
              help='Target programming language')
@click.option('-s', '--source', 
              type=click.Choice(['javascript', 'python', 'typescript', 'java', 'csharp', 'go', 'rust']),
              help='Source language (auto-detected if not specified)')
@click.option('-o', '--output', type=click.Path(), help='Output file path')
@click.option('--skip-validation', is_flag=True, help='Skip human validation step')
@click.option('--model', default='gpt-4', help='OpenAI model to use')
@click.option('--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
def migrate(input_file, target, source, output, skip_validation, model, api_key):
    """🔄 Migrate code between programming languages"""
    
    try:
        # Initialize configuration
        config = Config(api_key=api_key, model=model)
        
        if not config.api_key:
            console.print("❌ [red]OpenAI API key required![/red]")
            console.print("💡 Set OPENAI_API_KEY environment variable or use --api-key option")
            sys.exit(1)
        
        # Initialize migrator and validator
        migrator = CodeMigrator(config)
        validator = HumanValidator(console)
        
        console.print(f"🚀 [bold blue]Starting migration from {source or 'auto-detected'} to {target}[/bold blue]")
        console.print(f"📁 Input: {input_file}")
        
        # Read source code
        source_code = Path(input_file).read_text(encoding='utf-8')
        console.print(f"📄 Source code ({len(source_code)} characters)")
        
        # Display source code
        if source:
            syntax = Syntax(source_code, source, theme="monokai", line_numbers=True)
        else:
            syntax = Syntax(source_code, "text", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="[bold green]Source Code[/bold green]"))
        
        # Migrate with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("🤖 Migrating with AI...", total=None)
            
            migrated_code = migrator.migrate(
                source_code=source_code,
                source_lang=source,
                target_lang=target,
                input_file=input_file
            )
            
            progress.update(task, description="✅ Migration completed!")
        
        # Display migrated code
        migrated_syntax = Syntax(migrated_code, target, theme="monokai", line_numbers=True)
        console.print(Panel(migrated_syntax, title=f"[bold cyan]Migrated {target.title()} Code[/bold cyan]"))
        
        # Human validation step
        if not skip_validation:
            migrated_code = validator.validate(
                original_code=source_code,
                migrated_code=migrated_code,
                source_lang=source or 'auto-detected',
                target_lang=target,
                migrator=migrator
            )
        else:
            console.print("⚡ [yellow]Skipping human validation (auto-approved)[/yellow]")
        
        # Determine output path
        if not output:
            input_path = Path(input_file)
            output = input_path.parent / f"{input_path.stem}_migrated.{get_extension(target)}"
        
        # Create output directory if needed
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write output
        output_path.write_text(migrated_code, encoding='utf-8')
        
        console.print(f"✅ [bold green]Migration completed successfully![/bold green]")
        console.print(f"📁 Output: {output_path.absolute()}")
        
    except Exception as e:
        console.print(f"❌ [red]Error: {str(e)}[/red]")
        sys.exit(1)

@cli.command()
@click.argument('directory', type=click.Path(exists=True, file_okay=False))
@click.option('-t', '--target', required=True,
              type=click.Choice(['javascript', 'python', 'typescript', 'java', 'csharp', 'go', 'rust']),
              help='Target programming language')
@click.option('-s', '--source',
              type=click.Choice(['javascript', 'python', 'typescript', 'java', 'csharp', 'go', 'rust']),
              help='Source language filter')
@click.option('--pattern', default='**/*', help='File pattern to match (glob)')
@click.option('--skip-validation', is_flag=True, help='Skip human validation for all files')
def batch(directory, target, source, pattern, skip_validation):
    """📦 Batch migrate multiple files in a directory"""
    
    console.print(f"🚀 [bold blue]Starting batch migration to {target}[/bold blue]")
    console.print(f"📁 Directory: {directory}")
    console.print(f"🔍 Pattern: {pattern}")
    
    # Find files to migrate
    base_path = Path(directory)
    files_to_migrate = []
    
    for file_path in base_path.glob(pattern):
        if file_path.is_file() and should_migrate_file(file_path, source):
            files_to_migrate.append(file_path)
    
    if not files_to_migrate:
        console.print("❌ [red]No files found matching the criteria[/red]")
        return
    
    console.print(f"📋 Found {len(files_to_migrate)} files to migrate:")
    for f in files_to_migrate:
        console.print(f"  • {f.relative_to(base_path)}")
    
    if not skip_validation:
        if not Confirm.ask("\n🤔 Proceed with batch migration?"):
            console.print("❌ Batch migration cancelled")
            return
    
    # TODO: Implement batch migration logic
    console.print("🚧 [yellow]Batch migration feature coming soon![/yellow]")

@cli.command()
def demo():
    """🎯 Show demo and usage examples"""
    
    console.print(Panel.fit(
        """[bold blue]🚀 AI Code Migrator - Python Edition[/bold blue]

[green]✨ Features:[/green]
• AI-powered code migration using OpenAI GPT-4
• Interactive human validation with fix suggestions
• Support for 7+ programming languages
• Batch processing capabilities
• Rich terminal interface

[cyan]📖 Usage Examples:[/cyan]

[bold]Basic migration:[/bold]
ai-migrator migrate app.py -t javascript

[bold]Specify source language:[/bold]
ai-migrator migrate script.js -s javascript -t python

[bold]Skip validation (automated):[/bold]
ai-migrator migrate code.py -t java --skip-validation

[bold]Custom output location:[/bold]
ai-migrator migrate app.py -t typescript -o converted/app.ts

[bold]Batch migration:[/bold]
ai-migrator batch ./src -t javascript --pattern "*.py"

[yellow]💡 Set your OpenAI API key:[/yellow]
export OPENAI_API_KEY="your-api-key-here"
""",
        title="[bold green]Demo & Usage Guide[/bold green]"
    ))

def get_extension(language):
    """Get file extension for a programming language"""
    extensions = {
        'javascript': 'js',
        'python': 'py',
        'typescript': 'ts',
        'java': 'java',
        'csharp': 'cs',
        'go': 'go',
        'rust': 'rs'
    }
    return extensions.get(language, 'txt')

def should_migrate_file(file_path, source_filter):
    """Check if a file should be migrated based on extension"""
    if source_filter:
        expected_ext = get_extension(source_filter)
        return file_path.suffix.lstrip('.') == expected_ext
    
    # Auto-detect based on common extensions
    code_extensions = {'.py', '.js', '.ts', '.java', '.cs', '.go', '.rs', '.cpp', '.c', '.php'}
    return file_path.suffix.lower() in code_extensions

def main():
    """Main entry point for the CLI"""
    cli()

if __name__ == '__main__':
    main()
