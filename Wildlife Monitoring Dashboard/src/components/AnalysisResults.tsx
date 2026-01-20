import { AlertTriangle, CheckCircle, AlertCircle, TrendingUp, RefreshCw } from 'lucide-react';
import type { AnalysisResult } from '../types';

interface AnalysisResultsProps {
  result: AnalysisResult;
  onReset: () => void;
}

export function AnalysisResults({ result, onReset }: AnalysisResultsProps) {
  const getPriorityConfig = () => {
    switch (result.priority) {
      case 'high':
        return {
          color: 'red',
          bgClass: 'bg-red-50',
          borderClass: 'border-red-200',
          textClass: 'text-red-900',
          badgeClass: 'bg-red-100 text-red-800 border-red-300',
          icon: AlertTriangle,
          iconClass: 'text-red-600',
          label: 'High Priority',
          description: 'Immediate attention required'
        };
      case 'medium':
        return {
          color: 'amber',
          bgClass: 'bg-amber-50',
          borderClass: 'border-amber-200',
          textClass: 'text-amber-900',
          badgeClass: 'bg-amber-100 text-amber-800 border-amber-300',
          icon: AlertCircle,
          iconClass: 'text-amber-600',
          label: 'Medium Priority',
          description: 'Review within 48 hours'
        };
      case 'low':
        return {
          color: 'emerald',
          bgClass: 'bg-emerald-50',
          borderClass: 'border-emerald-200',
          textClass: 'text-emerald-900',
          badgeClass: 'bg-emerald-100 text-emerald-800 border-emerald-300',
          icon: CheckCircle,
          iconClass: 'text-emerald-600',
          label: 'Low Priority',
          description: 'Routine monitoring'
        };
    }
  };

  const config = getPriorityConfig();
  const Icon = config.icon;

  return (
    <div className="space-y-4">
      {/* Priority Alert - Most Prominent */}
      <div className={`${config.bgClass} ${config.borderClass} border-2 rounded-2xl p-8 shadow-lg`}>
        <div className="flex items-start gap-6">
          <div className={`w-16 h-16 ${config.badgeClass} rounded-xl flex items-center justify-center flex-shrink-0 border-2`}>
            <Icon className={`w-8 h-8 ${config.iconClass}`} />
          </div>
          
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <h2 className={`text-3xl font-semibold ${config.textClass}`}>
                {config.label}
              </h2>
              {result.requiresEscalation && (
                <span className="px-3 py-1 bg-red-600 text-white text-sm font-medium rounded-full">
                  Escalation Required
                </span>
              )}
            </div>
            <p className={`text-lg ${config.textClass} opacity-80`}>
              {config.description}
            </p>
          </div>
        </div>
      </div>

      {/* Analysis Details */}
      <div className="grid md:grid-cols-2 gap-4">
        {/* Detection Card */}
        <div className="bg-white rounded-xl p-6 shadow border border-gray-100">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Detection</h3>
          </div>
          
          <div className="space-y-3">
            <div>
              <p className="text-sm text-gray-600 mb-1">Category</p>
              <p className="text-2xl font-semibold text-gray-900">{result.categoryLabel}</p>
            </div>
            
            <div>
              <p className="text-sm text-gray-600 mb-2">Confidence</p>
              <div className="flex items-center gap-3">
                <div className="flex-1 bg-gray-100 rounded-full h-3 overflow-hidden">
                  <div 
                    className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all duration-1000"
                    style={{ width: `${result.confidence * 100}%` }}
                  />
                </div>
                <span className="text-lg font-semibold text-gray-900 w-16 text-right">
                  {Math.round(result.confidence * 100)}%
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Recommendations Card */}
        <div className="bg-white rounded-xl p-6 shadow border border-gray-100">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900">Recommended Actions</h3>
          </div>
          
          <ul className="space-y-2">
            {result.recommendations.map((rec, index) => (
              <li key={index} className="flex items-start gap-2 text-gray-700">
                <span className="text-purple-600 font-medium mt-0.5">•</span>
                <span className="flex-1">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex justify-center pt-4">
        <button
          onClick={onReset}
          className="flex items-center gap-2 px-6 py-3 bg-white hover:bg-gray-50 border-2 border-gray-200 rounded-xl font-medium text-gray-700 transition-colors shadow-sm"
        >
          <RefreshCw className="w-5 h-5" />
          Analyze Another Image
        </button>
      </div>
    </div>
  );
}
