export class AIService {
  private apiKey: string;
  private model: string;

  constructor(apiKey: string, model: string) {
    this.apiKey = apiKey;
    this.model = model;
  }

  private async callOpenAI(messages: any[]): Promise<string> {
    try {
      console.log('Calling OpenAI API with model:', this.model);
      console.log('Messages length:', messages.length);
      
      // Add delay to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.apiKey}`
        },
        body: JSON.stringify({
          model: this.model,
          messages,
          temperature: 0.7,
          max_tokens: this.model.includes('gpt-4o') ? 2000 : 1000
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error('OpenAI API error:', errorData);
        throw new Error(`OpenAI API error: ${response.status} - ${JSON.stringify(errorData)}`);
      }

      const data = await response.json();
      console.log('OpenAI API response received');
      return data.choices[0].message.content;
    } catch (error) {
      console.error('Error calling OpenAI API:', error);
      throw error;
    }
  }

  private async readFileContent(file: File): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => resolve(e.target?.result as string);
      reader.onerror = reject;
      reader.readAsText(file);
    });
  }

  private estimateTokens(text: string): number {
    // Rough estimation: 1 token ≈ 4 characters
    return Math.ceil(text.length / 4);
  }

  private chunkFiles(files: File[], maxTokens: number = 2000): File[][] {
    const chunks: File[][] = [];
    let currentChunk: File[] = [];
    let currentTokens = 0;

    for (const file of files) {
      // More conservative token estimation
      const estimatedTokens = this.estimateTokens(file.name) + 200;
      
      if (currentTokens + estimatedTokens > maxTokens && currentChunk.length > 0) {
        chunks.push(currentChunk);
        currentChunk = [file];
        currentTokens = estimatedTokens;
      } else {
        currentChunk.push(file);
        currentTokens += estimatedTokens;
      }
    }

    if (currentChunk.length > 0) {
      chunks.push(currentChunk);
    }

    return chunks;
  }

  async testConnection(): Promise<boolean> {
    try {
      await this.callOpenAI([
        { role: 'user', content: 'Hello, this is a test message. Please respond with "Test successful."' }
      ]);
      return true;
    } catch (error) {
      console.error('API connection test failed:', error);
      return false;
    }
  }

  async analyzeProject(files: File[]): Promise<{ migrationGuide: string; analyzedFiles: string[] }> {
    console.log('Starting project analysis...');
    
    const systemPrompt = `You are an expert PHP to React migration specialist. Analyze the provided PHP project and create a comprehensive migration guide.

CRITICAL RULES:
- Focus on the actual code structure and functionality
- Identify PHP-specific patterns that need React equivalents
- Suggest modern React patterns and best practices
- Be specific about dependencies needed
- Provide clear migration steps
- Avoid assumptions about databases or frameworks unless explicitly present in the code

Your response should include:
1. Project Overview
2. Key PHP Patterns Identified
3. React Migration Strategy
4. Required Dependencies
5. Migration Steps
6. Potential Challenges and Solutions

Format your response as a clear, structured migration guide.`;

    const fileContents = await Promise.all(
      files.map(async (file) => {
        const content = await this.readFileContent(file);
        return `File: ${file.name}\nContent:\n${content}\n---\n`;
      })
    );

    const totalContent = fileContents.join('\n');
    const estimatedTokens = this.estimateTokens(totalContent);

    console.log(`Estimated tokens: ${estimatedTokens}`);

    if (estimatedTokens > 2000) {
      console.log('Large project detected, using chunked analysis...');
      return this.analyzeProjectChunked(files);
    }

    const userPrompt = `Please analyze this PHP project and create a migration guide:

${totalContent}

Provide a comprehensive migration guide following the system instructions.`;

    const response = await this.callOpenAI([
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ]);

    const analyzedFiles = files.map(f => f.name);
    
    return {
      migrationGuide: response,
      analyzedFiles
    };
  }

  private async analyzeProjectChunked(files: File[]): Promise<{ migrationGuide: string; analyzedFiles: string[] }> {
    console.log('Using chunked analysis...');
    
    const chunks = this.chunkFiles(files);
    const analysisResults: string[] = [];
    
    for (let i = 0; i < chunks.length; i++) {
      console.log(`Analyzing chunk ${i + 1}/${chunks.length}...`);
      
      const chunkFiles = chunks[i];
      const fileContents = await Promise.all(
        chunkFiles.map(async (file) => {
          const content = await this.readFileContent(file);
          return `File: ${file.name}\nContent:\n${content}\n---\n`;
        })
      );

      const userPrompt = `Analyze this part of the PHP project (chunk ${i + 1}/${chunks.length}):

${fileContents.join('\n')}

Provide a brief analysis of this section.`;

      const response = await this.callOpenAI([
        { role: 'system', content: 'You are analyzing a PHP project section for migration to React. Provide a concise analysis.' },
        { role: 'user', content: userPrompt }
      ]);

      analysisResults.push(response);
    }

    // Combine all analyses
    const combinedAnalysis = analysisResults.join('\n\n---\n\n');
    
    const finalPrompt = `Based on the following analyses of different parts of the PHP project, create a comprehensive migration guide:

${combinedAnalysis}

Provide a complete migration guide that covers the entire project.`;

    const finalResponse = await this.callOpenAI([
      { role: 'system', content: 'Create a comprehensive migration guide based on the project analysis.' },
      { role: 'user', content: finalPrompt }
    ]);

    const analyzedFiles = files.map(f => f.name);
    
    return {
      migrationGuide: finalResponse,
      analyzedFiles
    };
  }

  async migrateCode(
    files: File[], 
    analysis: any, 
    customPrompt: string = ''
  ): Promise<{ reactCode: string; jsFiles: string[] }> {
    console.log('Starting code migration...');
    
    const systemPrompt = `You are an expert PHP to React migration specialist. Convert the provided PHP code to modern React JavaScript.

CRITICAL RULES:
- Generate VALID, RUNNABLE React code
- Use modern React patterns (hooks, functional components)
- Include ALL necessary imports and exports
- Carefully analyze PHP code to determine ALL required dependencies
- NEVER skip essential dependencies (react-router-dom, axios, etc.)
- Generate complete, working components
- Use proper file structure and naming conventions
- Include error handling and proper state management

CRITICAL REQUIREMENTS:
1. Analyze PHP code to identify:
   - Form handling → React form libraries or controlled components
   - Database queries → API calls with axios/fetch
   - Session management → React state or context
   - Routing → react-router-dom
   - File uploads → FormData or file handling
   - Authentication → JWT or session management
   - Any other PHP-specific functionality

2. Generate package.json with EXACT dependencies:
\`\`\`json
{
  "name": "migrated-react-app",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    // ADD ALL NECESSARY DEPENDENCIES HERE
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }
}
\`\`\`

3. Generate React components in this format:
\`\`\`javascript
// ComponentName.js
import React, { useState, useEffect } from 'react';
// Add all necessary imports

const ComponentName = () => {
  // Component logic here
  return (
    // JSX here
  );
};

export default ComponentName;
\`\`\`

4. Generate utility files for API calls, authentication, etc.

${customPrompt ? `CUSTOM USER INSTRUCTIONS: ${customPrompt}` : ''}

Provide the complete React project structure and code.`;

    const fileContents = await Promise.all(
      files.map(async (file) => {
        const content = await this.readFileContent(file);
        return `File: ${file.name}\nContent:\n${content}\n---\n`;
      })
    );

    const totalContent = fileContents.join('\n');
    const estimatedTokens = this.estimateTokens(totalContent);

    console.log(`Estimated tokens: ${estimatedTokens}`);

    if (estimatedTokens > 2000) {
      console.log('Large project detected, using chunked migration...');
      return this.migrateCodeChunked(files, analysis, customPrompt);
    }

    const userPrompt = `Migrate this PHP project to React:

${totalContent}

Analysis: ${JSON.stringify(analysis)}

${customPrompt ? `Custom Instructions: ${customPrompt}` : ''}

Generate the complete React project following the system instructions.`;

    const response = await this.callOpenAI([
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ]);

    const jsFiles = this.extractGeneratedFiles(response);
    
    return {
      reactCode: response,
      jsFiles
    };
  }

  private async migrateCodeChunked(
    files: File[], 
    analysis: any, 
    customPrompt: string
  ): Promise<{ reactCode: string; jsFiles: string[] }> {
    console.log('Using chunked migration...');
    
    const chunks = this.chunkFiles(files);
    const migrationResults: string[] = [];
    
    for (let i = 0; i < chunks.length; i++) {
      console.log(`Migrating chunk ${i + 1}/${chunks.length}...`);
      
      const chunkFiles = chunks[i];
      const fileContents = await Promise.all(
        chunkFiles.map(async (file) => {
          const content = await this.readFileContent(file);
          return `File: ${file.name}\nContent:\n${content}\n---\n`;
        })
      );

      const userPrompt = `Migrate this part of the PHP project (chunk ${i + 1}/${chunks.length}):

${fileContents.join('\n')}

Analysis: ${JSON.stringify(analysis)}

${customPrompt ? `Custom Instructions: ${customPrompt}` : ''}

Generate React code for this section.`;

      const response = await this.callOpenAI([
        { role: 'system', content: 'Migrate PHP code to React components and utilities.' },
        { role: 'user', content: userPrompt }
      ]);

      migrationResults.push(response);
    }

    // Combine all migrations
    const combinedMigration = migrationResults.join('\n\n---\n\n');
    
    const finalPrompt = `Combine these React migrations into a complete project:

${combinedMigration}

Create a unified React project structure with proper package.json and all components.`;

    const finalResponse = await this.callOpenAI([
      { role: 'system', content: 'Create a complete React project from the migration results.' },
      { role: 'user', content: finalPrompt }
    ]);

    const jsFiles = this.extractGeneratedFiles(finalResponse);
    
    return {
      reactCode: finalResponse,
      jsFiles
    };
  }

  async generateTests(
    files: File[], 
    migrationResult: any
  ): Promise<{ testGuide: string }> {
    console.log('Generating test cases...');
    
    const systemPrompt = `You are an expert in React testing. Generate comprehensive test cases for the migrated React project.

Generate:
1. Jest test files for each component
2. Unit tests for utility functions
3. Integration test examples
4. Testing instructions and commands
5. Test coverage recommendations

Use modern testing practices with React Testing Library and Jest.`;

    const userPrompt = `Generate test cases for this React project:

Migration Result: ${JSON.stringify(migrationResult)}

Generate comprehensive test cases and testing instructions.`;

    const response = await this.callOpenAI([
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt }
    ]);

    return {
      testGuide: response
    };
  }

  private extractGeneratedFiles(aiResponse: string): string[] {
    const files: string[] = [];
    
    // Extract file names from markdown headers
    const headerMatches = aiResponse.match(/###\s+(.+\.(js|jsx|ts|tsx|json))/gi);
    if (headerMatches) {
      files.push(...headerMatches.map(match => match.replace(/###\s+/, '')));
    }
    
    // Extract file names from code block headers
    const codeBlockMatches = aiResponse.match(/```(?:javascript|jsx|typescript|tsx|json)\s*(.+\.(js|jsx|ts|tsx|json))/gi);
    if (codeBlockMatches) {
      files.push(...codeBlockMatches.map(match => match.replace(/```(?:javascript|jsx|typescript|tsx|json)\s*/, '')));
    }
    
    // Extract component names from export statements
    const exportMatches = aiResponse.match(/export\s+(?:default\s+)?(\w+)/gi);
    if (exportMatches) {
      files.push(...exportMatches.map(match => {
        const componentName = match.replace(/export\s+(?:default\s+)?/, '');
        return `${componentName}.js`;
      }));
    }
    
    // Remove duplicates and filter
    const uniqueFiles = Array.from(new Set(files)).filter(file => 
      file.endsWith('.js') || file.endsWith('.jsx') || file.endsWith('.ts') || file.endsWith('.tsx') || file.endsWith('.json')
    );
    
    return uniqueFiles.length > 0 ? uniqueFiles : ['App.js', 'index.js', 'package.json'];
  }
} 