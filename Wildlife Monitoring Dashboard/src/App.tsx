import { useState } from 'react';
import { AnalysisResults } from './components/AnalysisResults';
import { UploadZone } from './components/UploadZone';
import { analyzeImageFromAPI } from './utils/analyze';
import type { AnalysisResult } from './types';

export default function App() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageUpload = async (file: File) => {
    const imageUrl = URL.createObjectURL(file);
    setUploadedImage(imageUrl);
    setResult(null);
    setError(null);
    setIsAnalyzing(true);

    try {
      // Call the real API
      const analysisResult = await analyzeImageFromAPI(file);
      setResult(analysisResult);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Analysis failed');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    if (uploadedImage) {
      URL.revokeObjectURL(uploadedImage);
    }
    setUploadedImage(null);
    setResult(null);
    setError(null);
    setIsAnalyzing(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-emerald-100 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-emerald-600 to-teal-600 rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-semibold text-gray-900">ECO Q‑Net</h1>
              <p className="text-sm text-gray-600">Wildlife Monitoring System</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-12">
        <div className="mb-8 text-center">
          <p className="text-lg text-gray-700 max-w-2xl mx-auto">
            Upload camera trap images to receive instant analysis and monitoring recommendations
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-red-700 font-medium">⚠️ Error: {error}</p>
            <p className="text-red-600 text-sm mt-1">Make sure the backend API is running on localhost:8000</p>
          </div>
        )}

        {/* Upload Section */}
        {!uploadedImage && !isAnalyzing && !result && (
          <UploadZone onImageUpload={handleImageUpload} />
        )}

        {/* Analysis Section */}
        {uploadedImage && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden border border-gray-100">
              <div className="relative">
                <img 
                  src={uploadedImage} 
                  alt="Uploaded camera trap" 
                  className="w-full h-96 object-contain bg-gray-50"
                />
                {isAnalyzing && (
                  <div className="absolute inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center">
                    <div className="bg-white rounded-xl p-6 shadow-xl">
                      <div className="flex items-center gap-4">
                        <div className="w-8 h-8 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin" />
                        <div>
                          <p className="font-medium text-gray-900">Analyzing image...</p>
                          <p className="text-sm text-gray-600">Processing wildlife data</p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Results Section */}
            {result && (
              <AnalysisResults result={result} onReset={handleReset} />
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-16 pb-8 text-center text-sm text-gray-500">
        <p>ECO Q‑Net • Supporting conservation through intelligent monitoring</p>
      </footer>
    </div>
  );
}
