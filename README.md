# AI PHP-to-React Migrator

An AI-powered web application that automatically migrates PHP projects to React JavaScript using OpenAI's GPT models.

## Features

- **AI-Powered Analysis**: Uses OpenAI GPT models to analyze PHP project structure
- **Smart Migration**: Converts PHP code to modern React components with proper dependencies
- **Custom Instructions**: Allows users to provide specific migration requirements
- **File Upload**: Supports both individual files and entire folder structures
- **Test Generation**: Automatically generates comprehensive test cases
- **Complete Package**: Downloads a ready-to-run React project with documentation
- **PDF Reports**: Generates detailed migration and testing documentation

## Tech Stack

- **Frontend**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Routing**: React Router DOM
- **File Handling**: React Dropzone
- **AI Integration**: OpenAI API (GPT-4o, GPT-4 Turbo, GPT-4, GPT-3.5 Turbo)
- **File Generation**: JSZip, file-saver, jsPDF

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd php-to-react-migrator
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Usage

### Step 1: Configure AI Settings
- Enter your OpenAI API key
- Select your preferred AI model (GPT-4o recommended)
- Test the API connection

### Step 2: Upload PHP Project
- Drag and drop PHP files or upload an entire folder
- Supported formats: PHP, JS, CSS, HTML, JSON, TXT, MD

### Step 3: AI Analysis
- The AI analyzes your PHP project structure
- Generates a comprehensive migration guide
- Identifies key patterns and dependencies

### Step 4: Code Migration
- Add optional custom instructions for the AI
- Convert PHP code to React components
- Generate proper package.json with dependencies

### Step 5: Test Generation
- Create comprehensive test cases
- Generate testing instructions and examples

### Step 6: Download Results
- Download complete React project as ZIP
- Includes migration report and test guide PDFs
- Ready-to-run with npm install and npm start

## AI Integration

The application uses OpenAI's API to:

- **Analyze PHP Projects**: Understand code structure, patterns, and dependencies
- **Generate React Code**: Convert PHP logic to modern React components
- **Create Test Cases**: Generate comprehensive testing documentation
- **Handle Large Projects**: Automatically chunk large codebases to avoid token limits

### Supported Models

- **GPT-4o**: Most capable model (128K context) - Recommended
- **GPT-4 Turbo**: Fast and efficient (128K context)
- **GPT-4**: High quality (8K context)
- **GPT-3.5 Turbo**: Fast and cost-effective (4K context)

## Project Structure

```
src/
├── components/          # Reusable UI components
├── pages/              # Main application pages
│   ├── Home.tsx        # API configuration
│   ├── Upload.tsx      # File upload interface
│   ├── Analysis.tsx    # AI analysis results
│   ├── Migration.tsx   # Code migration with custom prompts
│   ├── TestGeneration.tsx # Test case generation
│   └── Download.tsx    # Download results
├── services/           # Business logic
│   ├── aiService.ts    # OpenAI API integration
│   └── downloadService.ts # File generation and download
├── types/              # TypeScript type definitions
└── App.tsx             # Main application component
```

## Customization

### Adding Custom Instructions

In Step 4 (Migration), you can provide specific instructions to the AI:

- "Use TypeScript instead of JavaScript"
- "Include Material-UI for styling"
- "Focus on accessibility features"
- "Use Redux for state management"
- "Implement specific authentication patterns"

### Model Selection

Choose the AI model based on your needs:

- **For complex projects**: Use GPT-4o (highest quality)
- **For speed**: Use GPT-4 Turbo
- **For cost efficiency**: Use GPT-3.5 Turbo

## Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits
2. **Large Projects**: The app automatically handles large projects by chunking them
3. **Token Limits**: Use GPT-4o for projects with many files
4. **Download Issues**: Check browser download settings and available disk space

### Error Messages

- **"API connection failed"**: Check your API key and internet connection
- **"Analysis failed"**: Try with a smaller project or different model
- **"Migration failed"**: Check the custom prompt and try again

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check the troubleshooting section
- Review the console for error messages
- Ensure your OpenAI API key is valid
- Try with a smaller test project first 