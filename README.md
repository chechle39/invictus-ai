# 🚀 AI Code Migrator

A powerful Python-based AI code migration tool that helps developers migrate code between different programming languages using OpenAI GPT models with human validation.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🤖 **AI-Powered Migration** - Uses OpenAI GPT-4o-mini for cost-effective, high-quality code translation
- 🎯 **Multiple Language Support** - JavaScript, Python, Java, C++, Rust, Go, and more
- �️ **Human Validation** - Interactive validation with approve/reject/fix/show/suggest options
- � **Beautiful Terminal UI** - Rich syntax highlighting and progress indicators
- ⚡ **Skip Validation Mode** - Perfect for automated CI/CD workflows
- 🔍 **Auto-Detection** - Automatically detects source language
- � **Batch Processing** - Migrate entire directories (coming soon)
- 🌍 **Global CLI Tool** - Available system-wide after installation

## 💰 Cost Optimization

This tool uses **GPT-4o-mini** by default, which is significantly more cost-effective than GPT-4:

| Model | Cost per 1M Input Tokens | Cost per 1M Output Tokens |
|-------|---------------------------|----------------------------|
| GPT-4 | $30.00 | $60.00 |
| GPT-4o-mini | $0.15 | $0.60 |

**Savings: ~99% cost reduction** while maintaining excellent code quality!

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd AiPyMigrate

# Install dependencies
pip install -r requirements.txt

# Install globally (optional)
pip install -e .
```

### 2. Configuration

Create a `.env` file in the project root:

```properties
# Environment variables for AI Code Migrator
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.1
OPENAI_TIMEOUT=60
```

### 3. Basic Usage

```bash
# Migrate with human validation
ai-migrator migrate samples/calculator.py -t javascript

# Skip validation for automation
ai-migrator migrate samples/user_manager.js -t python --skip-validation

# Use specific API key
ai-migrator migrate app.py -t rust --api-key your_key_here
```

## 🧪 Testing the Sample Files

### Prerequisites

Make sure you have the required dependencies for testing:

```bash
# For Python samples
pip install -r requirements.txt

# For JavaScript samples
npm install mathjs
```

### Test Sample 1: User Manager (JavaScript → Python)

```bash
# 1. Run original JavaScript
node samples/user_manager.js

# 2. Migrate to Python
ai-migrator migrate samples/user_manager.js -t python

# 3. Run migrated Python
python samples/user_manager_migrated.py

# 4. Compare outputs - they should be identical!
```

**Expected Output:**
- ✅ User creation and greeting
- ✅ Statistics calculation (total users, average age)
- ✅ Adult filtering (25+ years old)
- ✅ Identical functional behavior

### Test Sample 2: Calculator (Python → JavaScript)

```bash
# 1. Run original Python
python samples/calculator.py

# 2. Migrate to JavaScript
ai-migrator migrate samples/calculator.py -t javascript

# 3. Run migrated JavaScript
node samples/calculator_migrated.js

# 4. Compare outputs - functionality should match!
```

**Expected Output:**
- ✅ Basic arithmetic operations (add, multiply, power)
- ✅ Statistics processing (count, sum, average, min, max)
- ✅ Fibonacci sequence generation
- ✅ Prime number detection
- ✅ File I/O operations

### Test Sample 3: Interactive Validation Demo

```bash
# Experience the full human validation workflow
ai-migrator migrate samples/calculator.py -t javascript

# Try these validation options:
# - 's' (show) - View side-by-side comparison
# - 'f' (fix) - Request specific improvements
# - 'g' (suggest) - Get AI suggestions for improvements
# - 'a' (approve) - Accept the migration
# - 'r' (reject) - Reject and try again
```

### Test Sample 4: Automated Workflow

```bash
# Perfect for CI/CD pipelines
ai-migrator migrate samples/calculator.py -t javascript --skip-validation

# Batch processing (when available)
ai-migrator batch samples/ -t python --skip-validation
```

## 📊 Migration Quality Validation

### Key Quality Indicators

1. **✅ Naming Conventions**
   - Python `snake_case` ↔ JavaScript `camelCase`
   - Proper variable and function naming

2. **✅ Language-Specific Features**
   - List comprehensions → Array methods
   - Type hints → JSDoc comments
   - Exception handling → Try-catch blocks

3. **✅ Library Mappings**
   - `datetime` → `Date()`
   - `math` → `Math` or `mathjs`
   - `json` → `JSON` or `fs`

4. **✅ Syntax Conversion**
   - Class structures and inheritance
   - Method signatures and return types
   - Control flow and loops

### Testing Checklist

- [ ] Original code runs without errors
- [ ] Migrated code runs without errors
- [ ] Functional output is identical
- [ ] Code style follows target language conventions
- [ ] Dependencies are properly converted
- [ ] Error handling is preserved

## 🛠️ Advanced Usage

### Environment Configuration

```bash
# Use different models
export OPENAI_MODEL="gpt-4"  # Higher quality, higher cost
export OPENAI_MODEL="gpt-3.5-turbo"  # Lower cost option

# Adjust token limits
export OPENAI_MAX_TOKENS=8000  # For larger files

# Fine-tune creativity
export OPENAI_TEMPERATURE=0.0  # More deterministic
export OPENAI_TEMPERATURE=0.3  # More creative
```

### Custom Prompts and Improvements

The AI migrator supports requesting specific fixes during validation:

```
Fix request examples:
- "Add more detailed comments"
- "Use async/await instead of promises"
- "Add error handling for edge cases"
- "Optimize for performance"
- "Follow language-specific best practices"
```

## 🔧 Development and Contributing

### Project Structure

```
ai_migrator/
├── __init__.py          # Package initialization
├── cli.py              # Command-line interface
├── config.py           # Configuration management
├── migrator.py         # Core migration engine
└── validator.py        # Human validation system

samples/                # Test files for migration
├── calculator.py       # Python → JavaScript test
├── user_manager.js     # JavaScript → Python test
└── ...

requirements.txt        # Python dependencies
setup.py               # Package setup
.env                   # Environment configuration
```

## 📈 Performance and Limitations

### Performance Metrics

- **Small Files (< 100 lines)**: ~10-15 seconds
- **Medium Files (100-500 lines)**: ~30-45 seconds  
- **Large Files (500+ lines)**: ~60-90 seconds

### Current Limitations

- Maximum file size: ~4000 tokens (due to model limits)
- Batch processing: Coming soon
- Some complex library mappings may need manual review
- Context awareness limited to single file scope

### Best Practices

1. **Break down large files** into smaller, logical components
2. **Review migrations** especially for complex algorithms
3. **Test thoroughly** with sample data
4. **Use version control** to track changes
5. **Validate dependencies** in target environment

## 🆘 Troubleshooting

### Common Issues

**Issue**: `OpenAI API key not found`
```bash
# Solution: Set API key in .env file or environment
export OPENAI_API_KEY=your_key_here
```

**Issue**: `Module 'mathjs' not found`
```bash
# Solution: Install JavaScript dependencies
npm install mathjs
```

**Issue**: `Migration takes too long`
```bash
# Solution: Use smaller files or adjust timeout
export OPENAI_TIMEOUT=120
```

**Issue**: `Poor migration quality`
```bash
# Solution: Try different model or use human validation
export OPENAI_MODEL=gpt-4
ai-migrator migrate file.py -t javascript  # Use interactive mode
```

## 📚 Examples and Use Cases

### Use Case 1: Legacy Code Modernization

```bash
# Migrate old JavaScript to modern Python
ai-migrator migrate legacy_app.js -t python
```

### Use Case 2: Cross-Platform Development

```bash
# Port Python ML models to JavaScript for web deployment
ai-migrator migrate ml_model.py -t javascript
```

### Use Case 3: Learning and Exploration

```bash
# See how algorithms look in different languages
ai-migrator migrate algorithm.py -t rust
ai-migrator migrate algorithm.py -t go
```

---

**Happy Code Migration! 🚀**

For support, please open an issue on GitHub or contact the maintainers.

# Or create .env file
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

### 3. Basic Usage

```bash
# Basic migration
ai-migrator migrate app.py -t javascript

# Specify source language
ai-migrator migrate script.js -s javascript -t python

# Skip validation (automated)
ai-migrator migrate code.py -t java --skip-validation

# Custom output location
ai-migrator migrate app.py -t typescript -o converted/app.ts
```

## 📖 Usage Examples

### Interactive Migration with Validation

```bash
ai-migrator migrate calculator.py -t javascript
```

This will:
1. 🤖 Use AI to migrate your Python code to JavaScript
2. 📋 Show you the migrated code with syntax highlighting
3. 🔍 Ask for your validation with options:
   - ✅ **approve** - Code looks good
   - ❌ **reject** - Use fallback migration
   - 🔧 **fix** - Provide custom instructions
   - 📄 **show** - Compare original vs migrated
   - 💡 **suggest** - Get AI improvement suggestions

### Human Validation Features

The interactive validation system provides several powerful options:

#### 🔧 Custom Fix Mode
```bash
# When you choose "fix", you can provide specific instructions:
Fix instructions: "Use async/await instead of promises"
Fix instructions: "Add proper error handling for file operations"  
Fix instructions: "Convert to use modern ES6+ syntax"
```

#### 💡 AI Suggestions
Get intelligent recommendations for code improvements:
- Performance optimizations
- Best practice adherence
- Modern language features
- Error handling improvements

#### 📄 Side-by-Side Comparison
View original and migrated code side-by-side with syntax highlighting.

## 🎯 Why Python is Better for This Tool

### 1. **Simpler Development**
- Less boilerplate code
- Better string manipulation
- Rich ecosystem for AI/text processing

### 2. **Powerful Libraries**
- `click` for robust CLI
- `rich` for beautiful terminal UI
- `openai` for API integration
- `pathlib` for cross-platform paths

### 3. **Easy Distribution**
- pip install works everywhere Python does
- PyInstaller creates standalone executables
- Docker containers for isolated execution

## 📦 Supported Languages

- **Source**: Python, JavaScript, TypeScript, Java, C#, Go, Rust
- **Target**: Python, JavaScript, TypeScript, Java, C#, Go, Rust
- **Auto-detection** based on file extensions and content analysis

## 🔧 Development

```bash
# Setup development environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -e .[dev]

# Run tests
pytest

# Code formatting
black ai_migrator/
```

## 📄 License

MIT License - Made with ❤️ for developers who value simplicity and power
