import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { MigrationStep, MigrationResult } from '../types';
import { AIService } from '../services/aiService';
import ProgressStepper from '../components/ProgressStepper';

interface TestGenerationProps {
  steps: MigrationStep[];
  currentStep: number;
  setCurrentStep: (step: number) => void;
  uploadedFiles: File[];
  migrationResult: MigrationResult | null;
  setMigrationResult: (result: MigrationResult) => void;
  apiKey: string;
  model: string;
}

const TestGeneration: React.FC<TestGenerationProps> = ({ 
  steps, 
  currentStep, 
  setCurrentStep, 
  uploadedFiles,
  migrationResult, 
  setMigrationResult, 
  apiKey,
  model
}) => {
  const navigate = useNavigate();
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string>('');
  const [progress, setProgress] = useState(0);
  const [currentTest, setCurrentTest] = useState('');

  const performTestGeneration = useCallback(async () => {
    if (!migrationResult) return;

    setIsGenerating(true);
    setError('');
    setProgress(0);
    setCurrentTest('Generating test cases...');

    try {
      const aiService = new AIService(apiKey, model);
      
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 400);

      const result = await aiService.generateTests(uploadedFiles, migrationResult);
      
      clearInterval(progressInterval);
      setProgress(100);
      setCurrentTest('Test generation complete!');

      setMigrationResult({
        ...migrationResult,
        testGuide: result.testGuide
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Test generation failed');
    } finally {
      setIsGenerating(false);
    }
  }, [migrationResult, uploadedFiles, setMigrationResult, apiKey, model]);

  useEffect(() => {
    if (migrationResult && !migrationResult.testGuide) {
      performTestGeneration();
    }
  }, [migrationResult, performTestGeneration]);

  const handleContinue = () => {
    setCurrentStep(6);
    navigate('/download');
  };

  const handleBack = () => {
    setCurrentStep(4);
    navigate('/migration');
  };

  const handleRetry = () => {
    if (migrationResult) {
      const resultWithoutTests = { ...migrationResult };
      delete resultWithoutTests.testGuide;
      setMigrationResult(resultWithoutTests);
    }
    performTestGeneration();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Step 5: Generate Test Cases</h1>
          <p className="text-gray-600">Creating comprehensive test cases for your migrated React code using {model}.</p>
        </div>

        {/* Progress Stepper */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <ProgressStepper 
            steps={steps} 
            currentStep={currentStep}
            allowNavigation={true}
            onStepClick={(step) => {
              if (step <= 5) {
                setCurrentStep(step);
                if (step === 1) navigate('/');
                if (step === 2) navigate('/upload');
                if (step === 3) navigate('/analysis');
                if (step === 4) navigate('/migration');
                if (step === 5) navigate('/test-generation');
              }
            }}
          />
        </div>

        {isGenerating ? (
          <div className="bg-white rounded-2xl shadow-xl p-12">
            <div className="text-center mb-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Generating Test Cases...</h3>
              <p className="text-gray-600 mb-4">{currentTest}</p>
              
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
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Test Generation Failed</h3>
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={handleRetry}
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Retry Test Generation
            </button>
          </div>
        ) : migrationResult?.testGuide ? (
          <div className="space-y-8">
            {/* Test Generation Results */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Test Generation Complete!</h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">✅</div>
                  <div className="text-green-700">Test Cases Generated</div>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{model}</div>
                  <div className="text-blue-700">AI Model Used</div>
                </div>
              </div>
            </div>

            {/* Test Cases & Instructions */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Test Cases & Instructions</h3>
              <div className="bg-gray-50 rounded-lg p-6 max-h-96 overflow-y-auto">
                <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono">
                  {migrationResult.testGuide}
                </pre>
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
                Continue to Download →
              </button>
            </div>
          </div>
        ) : !migrationResult ? (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="text-blue-600 text-6xl mb-4">📋</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Migration Required</h3>
            <p className="text-gray-600 mb-4">Please complete the migration step first to generate test cases.</p>
            <button
              onClick={handleBack}
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Go Back to Migration
            </button>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <p className="text-gray-600">No migration result available for test generation.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default TestGeneration; 