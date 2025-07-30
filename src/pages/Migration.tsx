import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { MigrationStep, ProjectAnalysis, MigrationResult } from '../types';
import { AIService } from '../services/aiService';
import ProgressStepper from '../components/ProgressStepper';

interface MigrationProps {
  steps: MigrationStep[];
  currentStep: number;
  setCurrentStep: (step: number) => void;
  analysis: ProjectAnalysis | null;
  uploadedFiles: File[];
  migrationResult: MigrationResult | null;
  setMigrationResult: (result: MigrationResult) => void;
  apiKey: string;
  model: string;
  customPrompt: string;
  setCustomPrompt: (prompt: string) => void;
}

const Migration: React.FC<MigrationProps> = ({ 
  steps, 
  currentStep, 
  setCurrentStep, 
  analysis,
  uploadedFiles,
  migrationResult, 
  setMigrationResult, 
  apiKey,
  model,
  customPrompt,
  setCustomPrompt
}) => {
  const navigate = useNavigate();
  const [isMigrating, setIsMigrating] = useState(false);
  const [error, setError] = useState<string>('');
  const [progress, setProgress] = useState(0);
  const [currentFile, setCurrentFile] = useState('');

  const performMigration = useCallback(async () => {
    if (!analysis || !uploadedFiles.length) return;

    setIsMigrating(true);
    setError('');
    setProgress(0);
    setCurrentFile('Starting migration...');

    try {
      const aiService = new AIService(apiKey, model);
      
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 5;
        });
      }, 300);

      const result = await aiService.migrateCode(uploadedFiles, analysis, customPrompt);
      
      clearInterval(progressInterval);
      setProgress(100);
      setCurrentFile('Migration complete!');

      setMigrationResult({
        jsFiles: result.jsFiles,
        reactCode: result.reactCode
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Migration failed');
    } finally {
      setIsMigrating(false);
    }
  }, [analysis, uploadedFiles, setMigrationResult, apiKey, model, customPrompt]);

  // Remove automatic migration - let user start manually after entering custom prompt
  // useEffect(() => {
  //   if (!migrationResult && analysis) {
  //     performMigration();
  //   }
  // }, [migrationResult, analysis, performMigration]);

  const handleContinue = () => {
    setCurrentStep(5);
    navigate('/test-generation');
  };

  const handleBack = () => {
    setCurrentStep(3);
    navigate('/analysis');
  };

  const handleRetry = () => {
    setMigrationResult(null as any);
    performMigration();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Step 4: Migrate Code</h1>
          <p className="text-gray-600">Converting your PHP code to React JavaScript using {model}.</p>
        </div>

        {/* Progress Stepper */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <ProgressStepper 
            steps={steps} 
            currentStep={currentStep}
            allowNavigation={true}
            onStepClick={(step) => {
              if (step <= 4) {
                setCurrentStep(step);
                if (step === 1) navigate('/');
                if (step === 2) navigate('/upload');
                if (step === 3) navigate('/analysis');
                if (step === 4) navigate('/migration');
              }
            }}
          />
        </div>

        {/* Custom Prompt Input */}
        {!isMigrating && !migrationResult && analysis && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Custom Migration Instructions (Optional)</h3>
            <p className="text-gray-600 mb-4">
              Add specific instructions to improve migration accuracy. For example:
              "Use TypeScript instead of JavaScript", "Include specific styling library", "Focus on accessibility", etc.
            </p>
            <textarea
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
              placeholder="Enter custom instructions for the AI migration..."
              className="w-full h-32 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
            <div className="mt-2 text-sm text-gray-500">
              {customPrompt.length}/1000 characters
            </div>
            
            {/* Start Migration Button */}
            <div className="mt-6 text-center">
              <button
                onClick={performMigration}
                disabled={isMigrating}
                className="inline-flex items-center px-8 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isMigrating ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Starting Migration...
                  </>
                ) : (
                  <>
                    🚀 Start Migration with {model}
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {isMigrating ? (
          <div className="bg-white rounded-2xl shadow-xl p-12">
            <div className="text-center mb-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Migrating Code...</h3>
              <p className="text-gray-600 mb-4">{currentFile}</p>
              
              {/* Progress Bar */}
              <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-500" 
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-gray-500">{progress}% Complete</p>
            </div>
          </div>
        ) : error ? (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="text-red-600 text-6xl mb-4">⚠️</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Migration Failed</h3>
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={handleRetry}
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Retry Migration
            </button>
          </div>
        ) : !analysis ? (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="text-blue-600 text-6xl mb-4">📋</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Analysis Required</h3>
            <p className="text-gray-600 mb-4">Please complete the analysis step first to proceed with migration.</p>
            <button
              onClick={handleBack}
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Go Back to Analysis
            </button>
          </div>
        ) : migrationResult ? (
          <div className="space-y-8">
            {/* Migration Results */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Migration Complete!</h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{migrationResult.jsFiles.length}</div>
                  <div className="text-green-700">React Files Generated</div>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{model}</div>
                  <div className="text-blue-700">AI Model Used</div>
                </div>
              </div>
            </div>

            {/* Generated React Code */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Generated React Code</h3>
              <div className="bg-gray-50 rounded-lg p-6 max-h-96 overflow-y-auto">
                <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono">
                  {migrationResult.reactCode}
                </pre>
              </div>
            </div>

            {/* Generated React Files */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Generated React Files</h3>
              <div className="grid gap-2">
                {migrationResult.jsFiles.map((file, index) => (
                  <div key={index} className="flex items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-2xl mr-3">📄</span>
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900">{file}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Navigation */}
            <div className="flex justify-between">
              <button
                onClick={handleBack}
                className="inline-flex items-center px-6 py-3 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition-colors"
              >
                ← Back
              </button>
              
              <button
                onClick={handleContinue}
                className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
              >
                Continue to Test Generation →
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <p className="text-gray-600">No analysis data available for migration.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Migration; 