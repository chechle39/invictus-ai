import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import jsPDF from 'jspdf';
import { MigrationResult, ProjectAnalysis } from '../types';

export class DownloadService {
  static async generateReactProjectFiles(migrationResult: MigrationResult): Promise<{ [key: string]: string }> {
    const files: { [key: string]: string } = {};
    
    if (!migrationResult.reactCode) {
      // Fallback to placeholder files if no AI code
      files['package.json'] = JSON.stringify({
        name: "migrated-react-app",
        version: "1.0.0",
        private: true,
        dependencies: {
          "react": "^18.2.0",
          "react-dom": "^18.2.0",
          "react-scripts": "5.0.1"
        },
        scripts: {
          "start": "react-scripts start",
          "build": "react-scripts build",
          "test": "react-scripts test",
          "eject": "react-scripts eject"
        },
        browserslist: {
          production: [">0.2%", "not dead", "not op_mini all"],
          development: ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
        }
      }, null, 2);
      
      files['src/App.js'] = `import React from 'react';

function App() {
  return (
    <div className="App">
      <h1>Migrated React App</h1>
      <p>Your PHP project has been migrated to React!</p>
    </div>
  );
}

export default App;`;
      
      files['src/index.js'] = `import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);`;
      
      files['public/index.html'] = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Migrated React App</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>`;
      
      return files;
    }

    // Parse AI-generated code to extract actual files
    const aiCode = migrationResult.reactCode;
    
    // Extract package.json
    const packageJsonMatch = aiCode.match(/```json\s*(\{[\s\S]*?\})\s*```/);
    if (packageJsonMatch) {
      try {
        const packageJson = JSON.parse(packageJsonMatch[1]);
        files['package.json'] = JSON.stringify(packageJson, null, 2);
      } catch (e) {
        console.error('Failed to parse package.json from AI response');
      }
    }
    
    // Extract React components and files
    const codeBlockMatches = aiCode.match(/```(?:javascript|jsx|typescript|tsx)\s*([\s\S]*?)```/g);
    if (codeBlockMatches) {
      codeBlockMatches.forEach((match, index) => {
        const codeContent = match.replace(/```(?:javascript|jsx|typescript|tsx)\s*/, '').replace(/```$/, '');
        
        // Try to determine file name from context
        let fileName = `component${index + 1}.js`;
        
        // Look for component names in the code
        const componentMatch = codeContent.match(/const\s+(\w+)\s*=/);
        if (componentMatch) {
          fileName = `${componentMatch[1]}.js`;
        }
        
        // Look for export statements
        const exportMatch = codeContent.match(/export\s+(?:default\s+)?(\w+)/);
        if (exportMatch) {
          fileName = `${exportMatch[1]}.js`;
        }
        
        // Determine file path based on component type
        let filePath = fileName;
        if (fileName.toLowerCase().includes('app')) {
          filePath = `src/${fileName}`;
        } else if (fileName.toLowerCase().includes('form') || fileName.toLowerCase().includes('component')) {
          filePath = `src/components/${fileName}`;
        } else if (fileName.toLowerCase().includes('util') || fileName.toLowerCase().includes('api') || fileName.toLowerCase().includes('auth')) {
          filePath = `src/utils/${fileName}`;
        } else {
          filePath = `src/${fileName}`;
        }
        
        files[filePath] = codeContent;
      });
    }
    
    // Add essential files if not present
    if (!files['src/index.js']) {
      files['src/index.js'] = `import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);`;
    }
    
    if (!files['public/index.html']) {
      files['public/index.html'] = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Migrated React App</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>`;
    }
    
    return files;
  }

  static generateMigrationReportPDF(analysis: ProjectAnalysis): jsPDF {
    const doc = new jsPDF();
    
    // Title
    doc.setFontSize(20);
    doc.text('PHP to React Migration Report', 20, 20);
    
    // Analysis Summary
    doc.setFontSize(14);
    doc.text('Migration Analysis Summary', 20, 40);
    
    doc.setFontSize(10);
    doc.text('This report contains the analysis and migration guide for your PHP project.', 20, 50);
    
    if (analysis.migrationGuide) {
      const lines = doc.splitTextToSize(analysis.migrationGuide, 170);
      let yPosition = 70;
      lines.forEach((line: string) => {
        doc.text(line, 20, yPosition);
        yPosition += 7; // Move down for next line
      });
    }
    
    return doc;
  }

  static generateTestReportPDF(migrationResult: MigrationResult): jsPDF {
    const doc = new jsPDF();
    
    // Title
    doc.setFontSize(20);
    doc.text('React Migration Test Guide', 20, 20);
    
    // Test Instructions
    doc.setFontSize(14);
    doc.text('Testing Instructions', 20, 40);
    
    doc.setFontSize(10);
    doc.text('Follow these instructions to test your migrated React application:', 20, 50);
    
    if (migrationResult.testGuide) {
      const lines = doc.splitTextToSize(migrationResult.testGuide, 170);
      let yPosition = 70;
      lines.forEach((line: string) => {
        doc.text(line, 20, yPosition);
        yPosition += 7; // Move down for next line
      });
    }
    
    return doc;
  }

  static async downloadProject(
    migrationResult: MigrationResult,
    analysis: ProjectAnalysis
  ): Promise<void> {
    const zip = new JSZip();
    
    // Generate React project files
    const reactFiles = await this.generateReactProjectFiles(migrationResult);
    
    // Add React project files to ZIP
    Object.entries(reactFiles).forEach(([path, content]) => {
      zip.file(path, content);
    });
    
    // Generate and add PDF reports
    const migrationReport = this.generateMigrationReportPDF(analysis);
    const testReport = this.generateTestReportPDF(migrationResult);
    
    zip.file('Migration_Report.pdf', migrationReport.output('blob'));
    zip.file('Test_Guide.pdf', testReport.output('blob'));
    
    // Add README
    const readme = `# Migrated React Application

This React application was automatically generated from your PHP project using AI-powered migration.

## Getting Started

1. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

2. Start the development server:
   \`\`\`bash
   npm start
   \`\`\`

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

## Project Structure

- \`src/\` - React components and application code
- \`public/\` - Static assets
- \`Migration_Report.pdf\` - Detailed migration analysis
- \`Test_Guide.pdf\` - Testing instructions and test cases

## Migration Details

This project was migrated using AI analysis of your original PHP code. Please review the generated code and test thoroughly before deploying to production.

## Support

If you encounter any issues with the migrated code, please refer to the PDF reports for detailed information about the migration process.
`;
    
    zip.file('README.md', readme);
    
    // Generate and download ZIP
    const zipBlob = await zip.generateAsync({ type: 'blob' });
    saveAs(zipBlob, 'migrated-react-project.zip');
  }
} 