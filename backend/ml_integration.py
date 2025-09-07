#!/usr/bin/env python3
"""
ML Integration for TimeComplexity Analyzer
Provides ML-enhanced analysis capabilities
"""

import sys
import os
from typing import Dict, Any, List
import json

# Add the parent directory to the path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    # Try absolute imports first
    from analyzer import TimeComplexityAnalyzer
    # Add ml_integration to path
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml_integration'))
    from hybrid_analyzer import HybridTimeComplexityAnalyzer
    from ml_models import TimeComplexityMLAnalyzer
    ML_AVAILABLE = True
    print("✅ ML Integration: All modules loaded successfully")
except ImportError as e:
    print(f"⚠️ ML Integration: Import error - {e}")
    try:
        # Fallback 1: try importing from ml_integration directory
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml_integration'))
        from hybrid_analyzer import HybridTimeComplexityAnalyzer
        from ml_models import TimeComplexityMLAnalyzer
        from analyzer import TimeComplexityAnalyzer
        ML_AVAILABLE = True
        print("✅ ML Integration: Fallback 1 successful")
    except ImportError as e2:
        print(f"⚠️ ML Integration: Fallback 1 failed - {e2}")
        try:
            # Fallback 2: try absolute imports
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from backend.analyzer import TimeComplexityAnalyzer
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'ml_integration'))
            from hybrid_analyzer import HybridTimeComplexityAnalyzer
            from ml_models import TimeComplexityMLAnalyzer
            ML_AVAILABLE = True
            print("✅ ML Integration: Fallback 2 successful")
        except ImportError as e3:
            print(f"❌ ML Integration: All fallbacks failed - {e3}")
            ML_AVAILABLE = False
            HybridTimeComplexityAnalyzer = None
            TimeComplexityMLAnalyzer = None

def analyze_with_ml(code: str, language: str) -> Dict[str, Any]:
    """
    Analyze code using ML-enhanced approach
    
    Args:
        code: Source code to analyze
        language: Programming language
        
    Returns:
        Dictionary containing analysis results
    """
    if not ML_AVAILABLE:
        # Fallback to rule-based analysis
        try:
            from analyzer import TimeComplexityAnalyzer
        except ImportError:
            from backend.analyzer import TimeComplexityAnalyzer
        analyzer = TimeComplexityAnalyzer()
        return analyzer.analyze(code, language)
    
    try:
        # Use hybrid analyzer
        hybrid_analyzer = HybridTimeComplexityAnalyzer()
        result = hybrid_analyzer.analyze(code, language)
        return result
    except Exception as e:
        print(f"⚠️ ML Analysis failed, falling back to rule-based: {e}")
        # Fallback to rule-based analysis
        try:
            from analyzer import TimeComplexityAnalyzer
        except ImportError:
            from backend.analyzer import TimeComplexityAnalyzer
        analyzer = TimeComplexityAnalyzer()
        return analyzer.analyze(code, language)

# Export for main.py
__all__ = ['analyze_with_ml', 'ML_AVAILABLE']