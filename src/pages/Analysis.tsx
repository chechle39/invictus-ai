import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { MigrationStep, ProjectAnalysis } from '../types';
import { AIService } from '../services/aiService';
import ProgressStepper from '../components/ProgressStepper';

interface AnalysisProps {
  steps: MigrationStep[];
  currentStep: number;
  setCurrentStep: (step: number) => void;
  uploadedFiles: File[];
  analysis: ProjectAnalysis | null;
  setAnalysis: (analysis: ProjectAnalysis) => void;
  apiKey: string;
  model: string;
}

const Analysis: React.FC<AnalysisProps> = ({ 
  steps, 
  currentStep, 
  setCurrentStep, 
  uploadedFiles,
  analysis,
  setAnalysis,
  apiKey,
  model
}) => {
  const navigate = useNavigate();
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string>('');
  const [progress, setProgress] = useState(0);
  const [currentFile, setCurrentFile] = useState('');

  const performAnalysis = useCallback(async () => {
    if (!uploadedFiles.length) return;

    setIsAnalyzing(true);
    setError('');
    setProgress(0);
    setCurrentFile('Analyzing project structure...');

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
      }, 500);

      const result = await aiService.analyzeProject(uploadedFiles);
      
      clearInterval(progressInterval);
      setProgress(100);
      setCurrentFile('Analysis complete!');

      const analysisData: ProjectAnalysis = {
        architecture: 'AI-generated architecture analysis',
        dataFlow: 'AI-generated data flow analysis',
        integrationPoints: ['API endpoints', 'Database connections', 'External services'],
        migrationGuide: result.migrationGuide
      };

      setAnalysis(analysisData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  }, [uploadedFiles, apiKey, model, setAnalysis]);

  useEffect(() => {
    if (!analysis && uploadedFiles.length > 0) {
      performAnalysis();
    }
  }, [analysis, uploadedFiles.length, performAnalysis]);

  const handleContinue = () => {
    setCurrentStep(4);
    navigate('/migration');
  };

  const handleBack = () => {
    setCurrentStep(2);
    navigate('/upload');
  };

  const handleRetry = () => {
    setAnalysis(null as any);
    performAnalysis();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Step 3: Analyze Project</h1>
          <p className="text-gray-600">AI analyzes your PHP project using {model}.</p>
        </div>

        {/* Progress Stepper */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <ProgressStepper 
            steps={steps} 
            currentStep={currentStep}
            allowNavigation={true}
            onStepClick={(step) => {
              if (step <= 3) {
                setCurrentStep(step);
                if (step === 1) navigate('/');
                if (step === 2) navigate('/upload');
                if (step === 3) navigate('/analysis');
              }
            }}
          />
        </div>

        {isAnalyzing ? (
          <div className="bg-white rounded-2xl shadow-xl p-12">
            <div className="text-center mb-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Analyzing Project...</h3>
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
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Analysis Failed</h3>
            <p className="text-red-600 mb-4">{error}</p>
            <button
              onClick={handleRetry}
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Retry Analysis
            </button>
          </div>
        ) : analysis ? (
          <div className="space-y-8">
            {/* Analysis Results */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Analysis Complete!</h3>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{uploadedFiles.length}</div>
                  <div className="text-green-700">Files Analyzed</div>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{model}</div>
                  <div className="text-blue-700">AI Model Used</div>
                </div>
              </div>
            </div>

            {/* AI Migration Guide */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">AI Migration Guide</h3>
              <div className="bg-gray-50 rounded-lg p-6 max-h-96 overflow-y-auto">
                <pre className="whitespace-pre-wrap text-sm text-gray-800 font-mono">
                  {analysis.migrationGuide}
                </pre>
              </div>
            </div>

            {/* Analyzed Files */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Analyzed Files</h3>
              <div className="grid gap-2">
                {uploadedFiles.map((file, index) => (
                  <div key={index} className="flex items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-2xl mr-3">📄</span>
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900">{file.name}</div>
                      <div className="text-xs text-gray-500">{(file.size / 1024).toFixed(1)} KB</div>
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
                Continue to Migration →
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <p className="text-gray-600">No files uploaded for analysis.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Analysis; 