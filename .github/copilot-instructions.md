<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# AI Code Migrator - Copilot Instructions

This is a Python-based AI code migration tool that helps developers migrate code between different programming languages using OpenAI GPT-4 with human validation.

## Project Structure
- `ai_migrator/` - Main package directory
- `ai_migrator/cli.py` - Command-line interface using Click and Rich
- `ai_migrator/migrator.py` - Core migration logic with OpenAI integration
- `ai_migrator/validator.py` - Human validation system with interactive prompts
- `ai_migrator/config.py` - Configuration management for API keys and settings

## Key Technologies
- **OpenAI API** - For AI-powered code migration
- **Click** - For command-line interface
- **Rich** - For beautiful terminal UI with syntax highlighting
- **pathlib** - For cross-platform file operations

## Code Style Guidelines
- Follow PEP 8 Python style guide
- Use type hints for all function parameters and return values
- Use dataclasses for configuration objects
- Handle exceptions gracefully with informative error messages
- Use pathlib.Path for all file operations
- Use f-strings for string formatting

## Interactive Features
- Human validation with multiple options (approve, reject, fix, show, suggest)
- Real-time syntax highlighting in terminal
- Progress indicators for long-running operations
- Interactive prompts with default values

## Error Handling
- Always wrap OpenAI API calls in try-catch blocks
- Provide fallback migration options when AI fails
- Show user-friendly error messages with suggested solutions
- Log detailed errors for debugging

## Testing Considerations
- Create simple test files for migration demonstrations
- Support multiple programming languages as source and target
- Handle file encoding properly (UTF-8)
- Validate API key before making requests
