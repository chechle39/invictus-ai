import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { MigrationStep, ProjectAnalysis, MigrationResult } from './types';
import Home from './pages/Home';
import Upload from './pages/Upload';
import Analysis from './pages/Analysis';
import Migration from './pages/Migration';
import TestGeneration from './pages/TestGeneration'
import Download from './pages/Download'

const steps: MigrationStep[] = [
  { id: 1, title: 'Configure AI', description: 'Enter your OpenAI API key and select model', path: '/' },
  { id: 2, title: 'Upload Project', description: 'Upload your PHP project files', path: '/upload' },
  { id: 3, title: 'Analyze Project', description: 'AI analyzes your PHP project', path: '/analysis' },
  { id: 4, title: 'Migrate Code', description: 'Convert PHP to React JavaScript', path: '/migration' },
  { id: 5, title: 'Generate Tests', description: 'Create test cases for migrated code', path: '/test-generation' },
  { id: 6, title: 'Download Results', description: 'Download your migrated React project', path: '/download' }
];

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('gpt-4o');
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [analysis, setAnalysis] = useState<ProjectAnalysis | null>(null);
  const [migrationResult, setMigrationResult] = useState<MigrationResult | null>(null);
  const [customPrompt, setCustomPrompt] = useState<string>('');

  const resetMigration = () => {
    setCurrentStep(1);
    setUploadedFiles([]);
    setAnalysis(null);
    setMigrationResult(null);
    setCustomPrompt('');
  };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/" 
            element={
              <Home 
                steps={steps}
                currentStep={currentStep}
                setCurrentStep={setCurrentStep}
                apiKey={apiKey}
                setApiKey={setApiKey}
                model={model}
                setModel={setModel}
              />
            } 
          />
          <Route 
            path="/upload" 
            element={
              <Upload 
                steps={steps}
                currentStep={currentStep}
                setCurrentStep={setCurrentStep}
                uploadedFiles={uploadedFiles}
                setUploadedFiles={setUploadedFiles}
              />
            } 
          />
          <Route 
            path="/analysis" 
            element={
              <Analysis 
                steps={steps}
                currentStep={currentStep}
                setCurrentStep={setCurrentStep}
                uploadedFiles={uploadedFiles}
                analysis={analysis}
                setAnalysis={setAnalysis}
                apiKey={apiKey}
                model={model}
              />
            } 
          />
          <Route 
            path="/migration" 
            element={
              <Migration 
                steps={steps}
                currentStep={currentStep}
                setCurrentStep={setCurrentStep}
                analysis={analysis}
                uploadedFiles={uploadedFiles}
                migrationResult={migrationResult}
                setMigrationResult={setMigrationResult}
                apiKey={apiKey}
                model={model}
                customPrompt={customPrompt}
                setCustomPrompt={setCustomPrompt}
              />
            } 
          />
          <Route 
            path="/test-generation" 
            element={
              <TestGeneration 
                steps={steps}
                currentStep={currentStep}
                setCurrentStep={setCurrentStep}
                uploadedFiles={uploadedFiles}
                migrationResult={migrationResult}
                setMigrationResult={setMigrationResult}
                apiKey={apiKey}
                model={model}
              />
            } 
          />
          <Route 
            path="/download" 
            element={
              <Download 
                steps={steps}
                currentStep={currentStep}
                setCurrentStep={setCurrentStep}
                analysis={analysis}
                migrationResult={migrationResult}
                resetMigration={resetMigration}
              />
            } 
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App; 