import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MigrationStep, ProjectAnalysis, MigrationResult } from '../types';
import { DownloadService } from '../services/downloadService';
import ProgressStepper from '../components/ProgressStepper';

interface DownloadProps {
  steps: MigrationStep[];
  currentStep: number;
  setCurrentStep: (step: number) => void;
  analysis: ProjectAnalysis | null;
  migrationResult: MigrationResult | null;
  resetMigration: () => void;
}

const Download: React.FC<DownloadProps> = ({ 
  steps, 
  currentStep, 
  setCurrentStep, 
  analysis,
  migrationResult,
  resetMigration
}) => {
  const navigate = useNavigate();
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownload = async () => {
    if (!migrationResult || !analysis) return;

    setIsDownloading(true);
    try {
      await DownloadService.downloadProject(migrationResult, analysis);
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      setIsDownloading(false);
    }
  };

  const handleRestart = () => {
    resetMigration();
    navigate('/');
  };

  const handleBack = () => {
    setCurrentStep(5);
    navigate('/test-generation');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Step 6: Download Results</h1>
          <p className="text-gray-600">Download your complete migrated React project with documentation.</p>
        </div>

        {/* Progress Stepper */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <ProgressStepper 
            steps={steps} 
            currentStep={currentStep}
            allowNavigation={true}
            onStepClick={(step) => {
              setCurrentStep(step);
              if (step === 1) navigate('/');
              if (step === 2) navigate('/upload');
              if (step === 3) navigate('/analysis');
              if (step === 4) navigate('/migration');
              if (step === 5) navigate('/test-generation');
              if (step === 6) navigate('/download');
            }}
          />
        </div>

        {migrationResult && analysis ? (
          <div className="space-y-8">
            {/* Download Summary */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Migration Complete! 🎉</h3>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{migrationResult.jsFiles.length}</div>
                  <div className="text-green-700">React Files</div>
                </div>
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">📋</div>
                  <div className="text-blue-700">Migration Report</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">🧪</div>
                  <div className="text-purple-700">Test Guide</div>
                </div>
              </div>
            </div>

            {/* Download Package */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Download Package</h3>
              <p className="text-gray-600 mb-6">
                Your download includes a complete React project with all necessary files, dependencies, and documentation.
              </p>
              
              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <h4 className="font-semibold text-gray-900 mb-3">Package Contents:</h4>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li className="flex items-center">
                    <span className="text-green-600 mr-2">✓</span>
                    Complete React project structure
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-600 mr-2">✓</span>
                    All migrated components and utilities
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-600 mr-2">✓</span>
                    Package.json with dependencies
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-600 mr-2">✓</span>
                    Migration analysis report (PDF)
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-600 mr-2">✓</span>
                    Test cases and instructions (PDF)
                  </li>
                  <li className="flex items-center">
                    <span className="text-green-600 mr-2">✓</span>
                    Setup and usage instructions
                  </li>
                </ul>
              </div>

              <div className="text-center">
                <button
                  onClick={handleDownload}
                  disabled={isDownloading}
                  className="inline-flex items-center px-8 py-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-lg"
                >
                  {isDownloading ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                      Preparing Download...
                    </>
                  ) : (
                    <>
                      📦 Download Complete Project
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Next Steps */}
            <div className="bg-white rounded-2xl shadow-xl p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Next Steps</h3>
              <div className="space-y-4 text-sm text-gray-700">
                <div className="flex items-start">
                  <span className="text-blue-600 mr-3 mt-1">1.</span>
                  <div>Extract the downloaded ZIP file to your desired location</div>
                </div>
                <div className="flex items-start">
                  <span className="text-blue-600 mr-3 mt-1">2.</span>
                  <div>Open a terminal in the project directory</div>
                </div>
                <div className="flex items-start">
                  <span className="text-blue-600 mr-3 mt-1">3.</span>
                  <div>Run <code className="bg-gray-100 px-2 py-1 rounded">npm install</code> to install dependencies</div>
                </div>
                <div className="flex items-start">
                  <span className="text-blue-600 mr-3 mt-1">4.</span>
                  <div>Run <code className="bg-gray-100 px-2 py-1 rounded">npm start</code> to start the development server</div>
                </div>
                <div className="flex items-start">
                  <span className="text-blue-600 mr-3 mt-1">5.</span>
                  <div>Review the PDF reports for detailed migration information and test instructions</div>
                </div>
                <div className="flex items-start">
                  <span className="text-blue-600 mr-3 mt-1">6.</span>
                  <div>Test the application thoroughly before deploying to production</div>
                </div>
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
                onClick={handleRestart}
                className="inline-flex items-center px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors"
              >
                🚀 Start New Migration
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
            <div className="text-blue-600 text-6xl mb-4">📋</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Migration Required</h3>
            <p className="text-gray-600 mb-4">Please complete the migration process first to download results.</p>
            <button
              onClick={handleBack}
              className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              Go Back to Migration
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Download; 