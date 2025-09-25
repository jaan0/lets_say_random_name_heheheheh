import fs from 'fs';
import path from 'path';

class AnalysisStorage {
  constructor() {
    this.storageDir = '/tmp/analysis_results';
    this.ensureStorageDir();
  }

  ensureStorageDir() {
    if (!fs.existsSync(this.storageDir)) {
      fs.mkdirSync(this.storageDir, { recursive: true });
    }
  }

  getStoragePath(analysisId) {
    return path.join(this.storageDir, `${analysisId}.json`);
  }

  saveAnalysisResult(analysisId, result) {
    try {
      const filePath = this.getStoragePath(analysisId);
      fs.writeFileSync(filePath, JSON.stringify(result, null, 2));
      return true;
    } catch (error) {
      console.error('Error saving analysis result:', error);
      return false;
    }
  }

  getAnalysisResult(analysisId) {
    try {
      const filePath = this.getStoragePath(analysisId);
      if (fs.existsSync(filePath)) {
        const data = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(data);
      }
      return null;
    } catch (error) {
      console.error('Error reading analysis result:', error);
      return null;
    }
  }

  getAllAnalysisResults() {
    try {
      const files = fs.readdirSync(this.storageDir);
      const results = {};
      
      files.forEach(file => {
        if (file.endsWith('.json')) {
          const analysisId = file.replace('.json', '');
          const result = this.getAnalysisResult(analysisId);
          if (result) {
            results[analysisId] = result;
          }
        }
      });
      
      return results;
    } catch (error) {
      console.error('Error reading all analysis results:', error);
      return {};
    }
  }

  deleteAnalysisResult(analysisId) {
    try {
      const filePath = this.getStoragePath(analysisId);
      if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error deleting analysis result:', error);
      return false;
    }
  }
}

export default AnalysisStorage;
