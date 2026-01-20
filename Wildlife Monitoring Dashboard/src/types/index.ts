export type AnimalCategory = 'deer' | 'predator' | 'other' | 'unknown';

export type PriorityLevel = 'low' | 'medium' | 'high';

export interface AnalysisResult {
  category: AnimalCategory;
  categoryLabel: string;
  confidence: number;
  priority: PriorityLevel;
  requiresEscalation: boolean;
  riskScore?: number;
  timestamp: string;
  recommendations: string[];
}
