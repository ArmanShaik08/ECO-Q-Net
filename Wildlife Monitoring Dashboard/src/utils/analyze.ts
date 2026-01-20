import type { AnalysisResult, AnimalCategory, PriorityLevel } from '../types';

const API_URL = 'http://localhost:8000';

// Map backend predictions to categories
const categoryMap: Record<string, { category: AnimalCategory; label: string }> = {
  'predator': { category: 'predator', label: 'Predator' },
  'deer': { category: 'deer', label: 'Deer' },
  'other': { category: 'other', label: 'Other Wildlife' }
};

// Priority level mapping
const priorityMap: Record<string, PriorityLevel> = {
  'HIGH': 'high',
  'MEDIUM': 'medium',
  'LOW': 'low'
};

// Real API analysis function
export async function analyzeImageFromAPI(file: File): Promise<AnalysisResult> {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    const data = await response.json();
    
    const mapping = categoryMap[data.prediction] || { category: 'other' as AnimalCategory, label: 'Unknown' };
    const priority = priorityMap[data.priority] || 'low';
    const requiresEscalation = data['Conditional Quantumn Usage'];

    // Generate recommendations based on prediction
    const recommendations = generateRecommendations(mapping.category, data.confidence, requiresEscalation);

    return {
      category: mapping.category,
      categoryLabel: mapping.label,
      confidence: data.confidence,
      priority,
      requiresEscalation,
      riskScore: data.risk_score,
      timestamp: new Date().toISOString(),
      recommendations
    };
  } catch (error) {
    console.error('API Analysis failed:', error);
    // Fallback to mock analysis
    return analyzeImage(file.name);
  }
}

// Generate contextual recommendations
function generateRecommendations(category: AnimalCategory, confidence: number, escalated: boolean): string[] {
  const recommendations: string[] = [];

  if (escalated) {
    recommendations.push('⚠️ QUANTUM ANALYSIS REQUIRED - High-risk prediction with low confidence');
    recommendations.push('Alert supervisor for manual verification');
    recommendations.push('Escalate to quantum-enhanced processing');
  }

  if (confidence < 0.75) {
    recommendations.push('⚠️ Low confidence detection - verify manually');
  }

  switch (category) {
    case 'predator':
      recommendations.push('Alert field team immediately');
      recommendations.push('Monitor area for increased predator activity');
      recommendations.push('Review nearby camera footage for patterns');
      break;
    case 'deer':
      recommendations.push('Continue routine monitoring');
      recommendations.push('Log sighting in database');
      break;
    case 'other':
      recommendations.push('Document wildlife observation');
      break;
  }

  if (confidence > 0.95) {
    recommendations.push('✅ High confidence detection - proceed with standard protocols');
  }

  return recommendations;
}

// Mock analysis function that simulates AI processing (fallback)
export function analyzeImage(filename: string): AnalysisResult {
  // Simulate different scenarios based on filename or random selection
  const scenarios: AnalysisResult[] = [
    {
      category: 'predator',
      categoryLabel: 'Large Predator',
      confidence: 0.94,
      priority: 'high',
      requiresEscalation: true,
      riskScore: 1.45,
      timestamp: new Date().toISOString(),
      recommendations: [
        'Alert field team immediately',
        'Monitor area for increased predator activity',
        'Review recent footage from nearby cameras'
      ]
    },
    {
      category: 'deer',
      categoryLabel: 'Deer',
      confidence: 0.88,
      priority: 'low',
      requiresEscalation: false,
      riskScore: 0.24,
      timestamp: new Date().toISOString(),
      recommendations: [
        'Continue routine monitoring',
        'Log sighting in database',
        'No immediate action required'
      ]
    },
    {
      category: 'predator',
      categoryLabel: 'Medium Carnivore',
      confidence: 0.76,
      priority: 'medium',
      requiresEscalation: false,
      timestamp: new Date().toISOString(),
      recommendations: [
        'Schedule follow-up check within 48 hours',
        'Compare with historical data for this location',
        'Note in weekly report'
      ]
    },
    {
      category: 'bird',
      categoryLabel: 'Large Bird',
      confidence: 0.91,
      priority: 'low',
      requiresEscalation: false,
      timestamp: new Date().toISOString(),
      recommendations: [
        'Continue routine monitoring',
        'Log sighting for biodiversity records',
        'No immediate action required'
      ]
    },
    {
      category: 'small_mammal',
      categoryLabel: 'Small Mammal',
      confidence: 0.82,
      priority: 'low',
      requiresEscalation: false,
      timestamp: new Date().toISOString(),
      recommendations: [
        'Continue routine monitoring',
        'Update species inventory',
        'No immediate action required'
      ]
    },
    {
      category: 'unknown',
      categoryLabel: 'Unidentified',
      confidence: 0.42,
      priority: 'medium',
      requiresEscalation: true,
      timestamp: new Date().toISOString(),
      recommendations: [
        'Manual review required',
        'Check camera positioning and image quality',
        'Consider expert consultation if pattern continues'
      ]
    }
  ];

  // Randomly select a scenario for demonstration
  const randomIndex = Math.floor(Math.random() * scenarios.length);
  return scenarios[randomIndex];
}
