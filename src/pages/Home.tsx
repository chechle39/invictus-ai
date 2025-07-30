import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MigrationStep } from '../types';
import { AIService } from '../services/aiService';
import ProgressStepper from '../components/ProgressStepper';

interface HomeProps {
  steps: MigrationStep[];
  currentStep: number;
  setCurrentStep: (step: number) => void;
  apiKey: string;
  setApiKey: (key: string) => void;
  model: string;
  setModel: (model: string) => void;
}

const Home: React.FC<HomeProps> = ({ 
  steps, 
  currentStep, 
  setCurrentStep, 
  apiKey, 
  setApiKey, 
  model, 
  setModel 
}) => {
  const navigate = useNavigate();
  const [isTesting, setIsTesting] = useState(false);
  const [testResult, setTestResult] = useState<string>('');

  const handleStartMigration = () => {
    if (apiKey.trim()) {
      setCurrentStep(2);
      navigate('/upload');
    }
  };

  const testApiConnection = async () => {
    if (!apiKey.trim()) {
      setTestResult('Please enter your API key first');
      return;
    }

    setIsTesting(true);
    setTestResult('Testing connection...');

    try {
      const aiService = new AIService(apiKey, model);
      const isConnected = await aiService.testConnection();
      
      if (isConnected) {
        setTestResult('✅ API connection successful!');
      } else {
        setTestResult('❌ API connection failed. Please check your key.');
      }
    } catch (error) {
      setTestResult(`❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">AI PHP-to-React Migrator</h1>
          <p className="text-xl text-gray-600">Automate PHP to React migration: analyze, convert, test, download.</p>
        </div>

        {/* Progress Stepper */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6 text-center">Migration Progress</h2>
          <ProgressStepper 
            steps={steps} 
            currentStep={currentStep}
            allowNavigation={false}
          />
        </div>

        {/* API Configuration */}
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Configure Your AI Settings</h2>
          
          {/* API Key Input */}
          <div className="mb-6">
            <label htmlFor="apiKey" className="block text-sm font-medium text-gray-700 mb-2">
              OpenAI API Key
            </label>
            <input
              type="password"
              id="apiKey"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-..."
              className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <p className="text-sm text-gray-500 mt-1">
              Your API key is stored locally and never sent to our servers.
            </p>
          </div>

          {/* Model Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Select AI Model
            </label>
            <div className="space-y-2">
              {[
                { id: 'gpt-4o', name: 'GPT-4o', description: 'Most capable model (128K context) - Best for small projects' },
                { id: 'gpt-4-turbo', name: 'GPT-4 Turbo', description: 'Fast and efficient (128K context) - Good balance' },
                { id: 'gpt-4', name: 'GPT-4', description: 'High quality (8K context) - For medium projects' },
                { id: 'gpt-3.5-turbo', name: 'GPT-3.5 Turbo', description: 'Fast and cost-effective (4K context) - Recommended for large projects' }
              ].map((modelOption) => (
                <label key={modelOption.id} className="flex items-center p-3 border border-gray-300 rounded-lg hover:bg-gray-50 cursor-pointer">
                  <input
                    type="radio"
                    name="model"
                    value={modelOption.id}
                    checked={model === modelOption.id}
                    onChange={(e) => setModel(e.target.value)}
                    className="mr-3"
                  />
                  <div>
                    <div className="font-medium text-gray-900">{modelOption.name}</div>
                    <div className="text-sm text-gray-500">{modelOption.description}</div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Test Connection */}
          <div className="mb-6">
            <button
              onClick={testApiConnection}
              disabled={isTesting || !apiKey.trim()}
              className="inline-flex items-center px-4 py-2 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isTesting ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Testing...
                </>
              ) : (
                'Test API Connection'
              )}
            </button>
            {testResult && (
              <p className={`mt-2 text-sm ${testResult.includes('✅') ? 'text-green-600' : 'text-red-600'}`}>
                {testResult}
              </p>
            )}
          </div>

          {/* Start Button */}
          <div className="text-center">
            <button
              onClick={handleStartMigration}
              disabled={!apiKey.trim()}
              className="inline-flex items-center px-8 py-4 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-lg"
            >
              🚀 Start Migration with {model.toUpperCase()}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home; 