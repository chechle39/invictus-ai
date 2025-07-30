import React, { useCallback, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDropzone } from 'react-dropzone';
import { MigrationStep } from '../types';
import ProgressStepper from '../components/ProgressStepper';

type FileWithPath = File & { webkitRelativePath?: string; };

interface UploadProps {
  steps: MigrationStep[];
  currentStep: number;
  setCurrentStep: (step: number) => void;
  uploadedFiles: File[];
  setUploadedFiles: (files: File[]) => void;
}

const Upload: React.FC<UploadProps> = ({ 
  steps, 
  currentStep, 
  setCurrentStep, 
  uploadedFiles, 
  setUploadedFiles 
}) => {
  const navigate = useNavigate();
  const folderInputRef = useRef<HTMLInputElement>(null);
  const [originalFileCount, setOriginalFileCount] = useState<number>(0);
  const [showAllFiles, setShowAllFiles] = useState<boolean>(false);
  const [allFiles, setAllFiles] = useState<FileWithPath[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setUploadedFiles(acceptedFiles);
  }, [setUploadedFiles]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/php': ['.php'],
      'text/javascript': ['.js'],
      'text/css': ['.css'],
      'text/html': ['.html', '.htm'],
      'application/json': ['.json'],
      'text/plain': ['.txt', '.md']
    },
    multiple: true
  });

  const filterRelevantFiles = (files: FileWithPath[]): FileWithPath[] => {
    return files.filter(file => {
      const fileName = file.name.toLowerCase();
      const filePath = file.webkitRelativePath?.toLowerCase() || '';
      
      // Skip hidden files and system files
      if (fileName.startsWith('.') || fileName.startsWith('_')) return false;
      
      // Skip common system directories
      if (filePath.includes('/.git/') || 
          filePath.includes('/node_modules/') || 
          filePath.includes('/vendor/') ||
          filePath.includes('/.vscode/') ||
          filePath.includes('/.idea/') ||
          filePath.includes('/.DS_Store') ||
          filePath.includes('/Thumbs.db')) return false;
      
      // Only include relevant file types
      const relevantExtensions = ['.php', '.js', '.css', '.html', '.htm', '.json', '.txt', '.md', '.xml', '.yml', '.yaml'];
      const hasRelevantExtension = relevantExtensions.some(ext => fileName.endsWith(ext));
      
      return hasRelevantExtension;
    });
  };

  const handleFolderUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      const fileArray = Array.from(files) as FileWithPath[];
      const filteredFiles = filterRelevantFiles(fileArray);
      console.log(`Original files: ${fileArray.length}, Filtered files: ${filteredFiles.length}`);
      setOriginalFileCount(fileArray.length);
      setAllFiles(fileArray);
      setUploadedFiles(filteredFiles as File[]);
    }
  };

  const handleContinue = () => {
    if (uploadedFiles.length > 0) {
      setCurrentStep(3);
      navigate('/analysis');
    }
  };

  const handleBack = () => {
    setCurrentStep(1);
    navigate('/');
  };

  const getFileIcon = (fileName: string) => {
    if (fileName.endsWith('.php')) return '🐘';
    if (fileName.endsWith('.js')) return '📜';
    if (fileName.endsWith('.css')) return '🎨';
    if (fileName.endsWith('.html') || fileName.endsWith('.htm')) return '🌐';
    if (fileName.endsWith('.json')) return '📋';
    if (fileName.endsWith('.txt') || fileName.endsWith('.md')) return '📝';
    if (fileName.includes('/') || fileName.includes('\\')) return '📁';
    return '📄';
  };

  const getFileStats = () => {
    const total = uploadedFiles.length;
    const php = uploadedFiles.filter(f => f.name.endsWith('.php')).length;
    const js = uploadedFiles.filter(f => f.name.endsWith('.js')).length;
    const css = uploadedFiles.filter(f => f.name.endsWith('.css')).length;
    return { total, php, js, css };
  };

  const stats = getFileStats();

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Step 2: Upload PHP Project</h1>
          <p className="text-gray-600">Upload your PHP project files for analysis and migration.</p>
        </div>

        {/* Progress Stepper */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
          <ProgressStepper 
            steps={steps} 
            currentStep={currentStep}
            allowNavigation={true}
            onStepClick={(step) => {
              if (step <= 2) {
                setCurrentStep(step);
                if (step === 1) navigate('/');
                if (step === 2) navigate('/upload');
              }
            }}
          />
        </div>

        {/* Upload Options */}
        <div className="grid md:grid-cols-2 gap-8 mb-8">
          {/* Drag & Drop Upload */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Upload Files</h3>
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
                isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'
              }`}
            >
              <input {...getInputProps()} />
              <div className="text-4xl mb-4">📁</div>
              {isDragActive ? (
                <p className="text-blue-600">Drop the files here...</p>
              ) : (
                <div>
                  <p className="text-gray-600 mb-2">Drag & drop files here, or click to select</p>
                  <p className="text-sm text-gray-500">Supports: PHP, JS, CSS, HTML, JSON, TXT, MD</p>
                </div>
              )}
            </div>
          </div>

          {/* Folder Upload */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Upload Folder</h3>
            <div className="text-center">
              <div className="text-4xl mb-4">📦</div>
              <p className="text-gray-600 mb-4">Upload an entire folder structure</p>
              <div className="mb-4 p-3 bg-yellow-50 rounded-lg">
                <p className="text-sm text-yellow-700">
                  <strong>Note:</strong> The browser may show many files in the selection dialog, but only relevant files will be processed.
                </p>
              </div>
              <button
                onClick={() => folderInputRef.current?.click()}
                className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
              >
                Select Folder
              </button>
              <input
                ref={folderInputRef}
                type="file"
                {...{ webkitdirectory: '', directory: '' }}
                onChange={handleFolderUpload}
                className="hidden"
                multiple
              />
            </div>
          </div>
        </div>

        {/* File List */}
        {uploadedFiles.length > 0 && (
          <div className="bg-white rounded-2xl shadow-xl p-8 mb-8">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-semibold text-gray-900">Uploaded Files (Filtered)</h3>
              <div className="text-sm text-gray-500">
                Total: {stats.total} | PHP: {stats.php} | JS: {stats.js} | CSS: {stats.css}
              </div>
            </div>
            
            <div className="mb-4 p-3 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-700">
                <strong>Note:</strong> Only relevant files are shown. Hidden files, system files, and files from node_modules/.git/vendor directories are automatically filtered out.
                {originalFileCount > 0 && originalFileCount !== uploadedFiles.length && (
                  <span className="block mt-1">
                    <strong>Filtering:</strong> {originalFileCount} total files → {uploadedFiles.length} relevant files
                  </span>
                )}
              </p>
              {originalFileCount > 0 && originalFileCount !== uploadedFiles.length && (
                <div className="mt-3">
                  <button
                    onClick={() => setShowAllFiles(!showAllFiles)}
                    className="text-sm text-blue-600 hover:text-blue-800 underline"
                  >
                    {showAllFiles ? 'Hide' : 'Show'} all {originalFileCount} files
                  </button>
                </div>
              )}
            </div>
            
            <div className="max-h-96 overflow-y-auto">
              <div className="grid gap-2">
                {(showAllFiles ? allFiles : uploadedFiles).map((file, index) => (
                  <div key={index} className={`flex items-center p-3 rounded-lg ${
                    showAllFiles && !uploadedFiles.includes(file) 
                      ? 'bg-red-50 border border-red-200' 
                      : 'bg-gray-50'
                  }`}>
                    <span className="text-2xl mr-3">{getFileIcon(file.name)}</span>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-gray-900 truncate">
                        {file.name}
                        {showAllFiles && !uploadedFiles.includes(file) && (
                          <span className="ml-2 text-xs text-red-600">(filtered out)</span>
                        )}
                      </div>
                      {file.webkitRelativePath && (
                        <div className="text-xs text-gray-500 truncate">
                          {file.webkitRelativePath}
                        </div>
                      )}
                    </div>
                    <div className="text-sm text-gray-500">
                      {(file.size / 1024).toFixed(1)} KB
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

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
            disabled={uploadedFiles.length === 0}
            className="inline-flex items-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Continue to Analysis →
          </button>
        </div>
      </div>
    </div>
  );
};

export default Upload; 