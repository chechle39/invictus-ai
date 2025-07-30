# PHP-to-React-Migrator

An AI-powered tool that automatically converts PHP projects to React JS applications with comprehensive analysis, migration mapping, and test generation.

## Features

- **Project Upload**: Drag & drop PHP project files (ZIP or folder)
- **AI Analysis**: Automatic codebase analysis with architecture diagrams
- **Migration Mapping**: Detailed breakdown of convertible vs. rewrite-required code
- **Code Migration**: Convert PHP to React JS with OpenAI integration
- **Test Generation**: Auto-generate Jest tests for migrated code
- **Documentation**: Generate comprehensive migration reports

## Tech Stack

- **Frontend**: React 18, React Router, Styled Components
- **File Handling**: React Dropzone, JSZip, FileSaver
- **Diagrams**: Mermaid.js for architecture and data flow diagrams
- **AI Integration**: OpenAI API for code analysis and migration
- **UI/UX**: Framer Motion, React Icons

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone git@github.com:chechle39/invictus-ai.git
cd invictus-ai
git checkout php-sample-project
```

2. Install dependencies:
```bash
npm install
```

3. Set up your OpenAI API key:
   - Create a `.env` file in the root directory
   - Add: `REACT_APP_OPENAI_API_KEY=your_api_key_here`

4. Start the development server:
```bash
npm start
```

## Usage

1. **Home Page**: Click "Start Migration" to begin
2. **Upload**: Drag & drop your PHP project files
3. **Analysis**: Review the generated architecture and data flow diagrams
4. **Migration Map**: See what code can be converted vs. rewritten
5. **Migration**: Watch the AI convert your PHP code to React
6. **Tests**: Generate and review test cases
7. **Download**: Get your complete React project with documentation

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Main application pages
├── services/      # API and business logic
├── utils/         # Helper functions
└── styles/        # Global styles and themes

public/            # Static assets
data/              # Generated migration data
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License 