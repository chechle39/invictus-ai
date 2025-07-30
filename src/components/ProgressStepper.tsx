import React from 'react';
import { MigrationStep } from '../types';

interface ProgressStepperProps {
  steps: MigrationStep[];
  currentStep: number;
  onStepClick?: (step: number) => void;
  allowNavigation?: boolean;
}

const ProgressStepper: React.FC<ProgressStepperProps> = ({ 
  steps, 
  currentStep, 
  onStepClick,
  allowNavigation = false 
}) => {
  return (
    <div className="w-full py-6">
      <div className="flex items-center justify-between">
        {steps.map((step, index) => {
          const isCompleted = index < currentStep;
          const isCurrent = index === currentStep - 1;
          const isUpcoming = index > currentStep - 1;
          
          return (
            <React.Fragment key={step.id}>
              {/* Step Circle and Label */}
              <div className="flex flex-col items-center">
                {/* Circle */}
                <div 
                  onClick={() => allowNavigation && onStepClick && onStepClick(step.id)}
                  className={`w-10 h-10 rounded-full border-2 flex items-center justify-center transition-all duration-300 ${
                    isCompleted
                      ? 'bg-blue-600 border-blue-600 text-white'
                      : isCurrent
                      ? 'bg-blue-50 border-blue-600 text-blue-600'
                      : 'bg-white border-gray-300 text-gray-400'
                  } ${allowNavigation && !isUpcoming ? 'cursor-pointer hover:border-blue-400' : 'cursor-default'}`}
                >
                  {isCompleted ? (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <span className="text-sm font-semibold">{step.id}</span>
                  )}
                </div>
                
                {/* Label */}
                <div className="mt-2 text-center max-w-20">
                  <div className={`text-xs font-medium ${
                    isCompleted ? 'text-blue-600' : isCurrent ? 'text-blue-600' : 'text-gray-500'
                  }`}>
                    {step.title}
                  </div>
                </div>
              </div>
              
              {/* Connector Line */}
              {index < steps.length - 1 && (
                <div className="flex-1 mx-3 flex items-center">
                  <div className={`h-0.5 w-full transition-all duration-500 ${
                    isCompleted ? 'bg-blue-600' : 'bg-gray-300'
                  }`}></div>
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};

export default ProgressStepper; 