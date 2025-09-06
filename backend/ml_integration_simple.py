#!/usr/bin/env python3
"""
Simplified ML Integration for TimeComplexity Analyzer Backend
Lightweight version that works reliably on free hosting platforms
"""

import os
import sys
from pathlib import Path

# Add ML integration to path
ml_path = Path(__file__).parent.parent / "ml_integration"
sys.path.append(str(ml_path))

try:
    # Try to import basic ML libraries first
    import pandas as pd
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_extraction.text import TfidfVectorizer
    import joblib
    
    print("✅ Basic ML libraries loaded successfully")
    
    # Simple ML-based complexity analyzer
    class SimpleMLAnalyzer:
        def __init__(self):
            self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            self.model = None
            self.is_trained = False
            
        def train_simple_model(self):
            """Train a simple model with basic patterns"""
            # Simple training data based on code patterns
            training_data = [
                ("for i in range(n):", "O(n)"),
                ("for i in range(n): for j in range(n):", "O(n²)"),
                ("while left <= right:", "O(log n)"),
                ("if x in list:", "O(n)"),
                ("if x in set:", "O(1)"),
                ("def recursive_function(n):", "O(2ⁿ)"),
                ("return recursive_function(n-1)", "O(2ⁿ)"),
                ("arr.sort()", "O(n log n)"),
                ("return arr[0]", "O(1)"),
                ("return len(arr)", "O(1)"),
            ]
            
            # Extract features and labels
            X = [item[0] for item in training_data]
            y = [item[1] for item in training_data]
            
            # Vectorize the code snippets
            X_vectorized = self.vectorizer.fit_transform(X)
            
            # Train a simple classifier
            self.model = RandomForestClassifier(n_estimators=10, random_state=42)
            self.model.fit(X_vectorized, y)
            self.is_trained = True
            
            print("✅ Simple ML model trained successfully")
            
        def predict_complexity(self, code):
            """Predict time complexity using simple ML"""
            if not self.is_trained:
                self.train_simple_model()
            
            # Vectorize the input code
            code_vectorized = self.vectorizer.transform([code])
            
            # Predict complexity
            prediction = self.model.predict(code_vectorized)[0]
            confidence = max(self.model.predict_proba(code_vectorized)[0])
            
            return prediction, confidence
    
    # Initialize the simple ML analyzer
    ml_analyzer = SimpleMLAnalyzer()
    
    def analyze_with_ml(code, language):
        """Analyze code using simple ML approach"""
        try:
            # Extract key lines from code
            lines = code.split('\n')
            key_lines = []
            
            for line in lines:
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['for', 'while', 'if', 'def', 'return', 'sort', 'in ']):
                    key_lines.append(line)
            
            # Combine key lines for analysis
            code_sample = ' '.join(key_lines[:5])  # Use first 5 key lines
            
            if not code_sample.strip():
                return {
                    "time_complexity": "Unknown",
                    "space_complexity": "Unknown", 
                    "breakdown": ["No analyzable patterns found"],
                    "suggestions": ["Try adding more code structure"],
                    "confidence": 0.0
                }
            
            # Get ML prediction
            prediction, confidence = ml_analyzer.predict_complexity(code_sample)
            
            # Map prediction to full response
            complexity_map = {
                "O(1)": {"time": "O(1)", "space": "O(1)"},
                "O(n)": {"time": "O(n)", "space": "O(1)"},
                "O(n²)": {"time": "O(n²)", "space": "O(1)"},
                "O(log n)": {"time": "O(log n)", "space": "O(1)"},
                "O(2ⁿ)": {"time": "O(2ⁿ)", "space": "O(n)"},
                "O(n log n)": {"time": "O(n log n)", "space": "O(1)"}
            }
            
            result = complexity_map.get(prediction, {"time": "Unknown", "space": "Unknown"})
            
            return {
                "time_complexity": result["time"],
                "space_complexity": result["space"],
                "breakdown": [f"ML prediction: {prediction} (confidence: {confidence:.2f})"],
                "suggestions": [
                    "This analysis is based on machine learning patterns",
                    "For more accuracy, consider the full algorithm structure"
                ],
                "confidence": confidence
            }
            
        except Exception as e:
            print(f"ML analysis error: {e}")
            return {
                "time_complexity": "Unknown",
                "space_complexity": "Unknown",
                "breakdown": [f"ML analysis failed: {str(e)}"],
                "suggestions": ["Falling back to pattern-based analysis"],
                "confidence": 0.0
            }
    
    print("✅ Simple ML integration loaded successfully")
    ML_AVAILABLE = True
    
except ImportError as e:
    print(f"⚠️ Simple ML integration not available: {e}")
    ML_AVAILABLE = False
    
    def analyze_with_ml(code, language):
        return {
            "time_complexity": "Unknown",
            "space_complexity": "Unknown",
            "breakdown": ["ML integration not available"],
            "suggestions": ["Using basic pattern analysis"],
            "confidence": 0.0
        }
