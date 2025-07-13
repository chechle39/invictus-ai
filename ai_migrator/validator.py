"""
Human validation system for AI Code Migrator
Interactive validation with fix capabilities
"""

from typing import Optional
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.panel import Panel
from rich.syntax import Syntax

class HumanValidator:
    """Interactive human validation system"""
    
    def __init__(self, console: Console):
        self.console = console
    
    def validate(self, original_code: str, migrated_code: str, 
                 source_lang: str, target_lang: str, migrator) -> str:
        """
        Interactive validation of migrated code with fix options
        
        Args:
            original_code: Original source code
            migrated_code: AI-generated migrated code
            source_lang: Source programming language
            target_lang: Target programming language
            migrator: CodeMigrator instance for applying fixes
            
        Returns:
            Final validated/fixed code
        """
        
        self.console.print("\n" + "="*60)
        self.console.print("🔍 [bold yellow]HUMAN VALIDATION STEP[/bold yellow]")
        self.console.print("="*60)
        
        self.console.print(f"📋 Please review the migration from [cyan]{source_lang}[/cyan] to [green]{target_lang}[/green]")
        self.console.print("\n📖 [bold]Available Options:[/bold]")
        self.console.print("  [green]✅ approve[/green] - Code looks good, proceed")
        self.console.print("  [red]❌ reject[/red] - Use fallback migration")
        self.console.print("  [yellow]🔧 fix[/yellow] - Provide custom fix instructions")
        self.console.print("  [blue]📄 show[/blue] - Show original code for comparison")
        self.console.print("  [cyan]💡 suggest[/cyan] - Get AI suggestions for improvements")
        
        while True:
            choice = Prompt.ask(
                "\n🤔 [bold]What would you like to do?[/bold]",
                choices=["approve", "reject", "fix", "show", "suggest"],
                default="approve"
            )
            
            if choice == "approve":
                self.console.print("✅ [bold green]Migration approved![/bold green]")
                return migrated_code
                
            elif choice == "reject":
                self.console.print("❌ [bold red]Migration rejected[/bold red]")
                self.console.print("🔄 Using fallback migration...")
                # Return a basic fallback (could implement simple rule-based migration)
                return self._create_fallback_migration(original_code, target_lang)
                
            elif choice == "fix":
                fixed_code = self._handle_fix_request(
                    migrated_code, source_lang, target_lang, migrator
                )
                if fixed_code:
                    return fixed_code
                # Continue loop if fix failed
                
            elif choice == "show":
                self._show_comparison(original_code, migrated_code, source_lang, target_lang)
                
            elif choice == "suggest":
                self._show_ai_suggestions(migrated_code, target_lang, migrator)
    
    def _handle_fix_request(self, code: str, source_lang: str, 
                           target_lang: str, migrator) -> Optional[str]:
        """Handle user's request to fix the migrated code"""
        
        self.console.print("\n🔧 [bold yellow]CUSTOM FIX MODE[/bold yellow]")
        self.console.print("💭 Describe what needs to be fixed (be specific):")
        self.console.print("   Examples:")
        self.console.print("   - 'Fix the import statements for Node.js'")
        self.console.print("   - 'Use async/await instead of promises'")
        self.console.print("   - 'Add proper error handling'")
        self.console.print("   - 'Convert to use modern Python syntax'")
        
        fix_instructions = Prompt.ask("\n🎯 [bold]Fix instructions[/bold]")
        
        if not fix_instructions.strip():
            self.console.print("❌ [red]No instructions provided[/red]")
            return None
        
        try:
            self.console.print("🤖 [cyan]Applying AI fixes...[/cyan]")
            
            fixed_code = migrator.apply_fix(
                code=code,
                fix_instructions=fix_instructions,
                source_lang=source_lang,
                target_lang=target_lang
            )
            
            # Show the fixed code
            self.console.print("\n📄 [bold green]Fixed Code:[/bold green]")
            syntax = Syntax(fixed_code, target_lang, theme="monokai", line_numbers=True)
            self.console.print(Panel(syntax, title="🔧 AI-Fixed Code"))
            
            # Ask for approval
            if Confirm.ask("\n✅ [bold]Accept this fix?[/bold]", default=True):
                self.console.print("🎉 [bold green]Fixed migration approved![/bold green]")
                return fixed_code
            else:
                self.console.print("🔄 [yellow]Fix rejected, returning to validation menu[/yellow]")
                return None
                
        except Exception as e:
            self.console.print(f"❌ [red]Fix application failed: {str(e)}[/red]")
            self.console.print("🔄 [yellow]Returning to validation menu[/yellow]")
            return None
    
    def _show_comparison(self, original_code: str, migrated_code: str, 
                        source_lang: str, target_lang: str):
        """Show side-by-side comparison of original and migrated code"""
        
        self.console.print("\n📊 [bold blue]CODE COMPARISON[/bold blue]")
        
        # Show original code
        self.console.print(f"\n🔵 [bold]Original ({source_lang.title()}):[/bold]")
        original_syntax = Syntax(original_code, source_lang, theme="monokai", line_numbers=True)
        self.console.print(Panel(original_syntax, title=f"📄 {source_lang.title()} Source"))
        
        # Show migrated code
        self.console.print(f"\n🟢 [bold]Migrated ({target_lang.title()}):[/bold]")
        migrated_syntax = Syntax(migrated_code, target_lang, theme="monokai", line_numbers=True)
        self.console.print(Panel(migrated_syntax, title=f"🔄 {target_lang.title()} Migration"))
    
    def _show_ai_suggestions(self, code: str, target_lang: str, migrator):
        """Get and show AI suggestions for code improvements"""
        
        self.console.print("\n💡 [bold cyan]AI IMPROVEMENT SUGGESTIONS[/bold cyan]")
        
        try:
            suggestions = migrator.apply_fix(
                code=code,
                fix_instructions="Analyze this code and suggest specific improvements for better code quality, performance, and following best practices. List 3-5 specific suggestions.",
                source_lang="analysis",
                target_lang=target_lang
            )
            
            self.console.print(Panel(suggestions, title="🧠 AI Code Analysis & Suggestions"))
            
        except Exception as e:
            self.console.print(f"❌ [red]Failed to get AI suggestions: {str(e)}[/red]")
    
    def _create_fallback_migration(self, original_code: str, target_lang: str) -> str:
        """Create a basic fallback migration when AI migration is rejected"""
        
        # This is a very basic fallback - in practice you might want more sophisticated rules
        fallback_header = f"// FALLBACK MIGRATION TO {target_lang.upper()}\n"
        fallback_header += f"// Original code preserved below - manual conversion needed\n\n"
        
        if target_lang.lower() == 'javascript':
            return fallback_header + f"/* Original code:\n{original_code}\n*/\n\n// TODO: Convert to JavaScript"
        elif target_lang.lower() == 'python':
            return fallback_header + f'"""\nOriginal code:\n{original_code}\n"""\n\n# TODO: Convert to Python'
        else:
            return fallback_header + f"/* Original code:\n{original_code}\n*/\n\n// TODO: Convert to {target_lang}"
