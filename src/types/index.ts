export interface MigrationStep {
  id: number;
  title: string;
  description: string;
  path: string;
}

export interface ProjectAnalysis {
  architecture: string;
  dataFlow: string;
  integrationPoints: string[];
  migrationGuide?: string;
}

export interface MigrationResult {
  jsFiles: string[];
  reactCode?: string;
  testGuide?: string;
}

export interface ApiKeyConfig {
  apiKey: string;
  model: string;
}

export interface UploadedFile {
  name: string;
  size: number;
  type: string;
  content?: string;
  path?: string;
} 