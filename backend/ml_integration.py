#!/usr/bin/env python3
"""
ML Integration for TimeComplexity Analyzer Backend
Integrates ML models with the main FastAPI backend
"""

import os
import sys
from pathlib import Path

# Add ML integration to path
ml_path = Path(__file__).parent.parent / "ml_integration"
sys.path.append(str(ml_path))

try:
    from hybrid_analyzer import HybridTimeComplexityAnalyzer
    
    # Initialize hybrid analyzer with ML models
    ml_models_path = str(ml_path / "ml_models.pkl")
    hybrid_analyzer = HybridTimeComplexityAnalyzer(ml_models_path)
    
    print("✅ ML integration loaded successfully")
    ML_AVAILABLE = True
    
except ImportError as e:
    print(f"⚠️ ML integration not available: {e}")
    ML_AVAILABLE = False
    hybrid_analyzer = None

def analyze_with_ml(code: str, language: str = "python"):
    """Analyze code using ML-enhanced approach"""
    if ML_AVAILABLE and hybrid_analyzer:
        return hybrid_analyzer.analyze(code, language)
    else:
        # Fallback to rule-based analysis
        from analyzer import TimeComplexityAnalyzer
        analyzer = TimeComplexityAnalyzer()
        return analyzer.analyze(code, language)
