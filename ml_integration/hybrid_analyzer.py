#!/usr/bin/env python3
"""
Hybrid TimeComplexity Analyzer
Combines rule-based analysis with ML predictions for optimal accuracy
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from backend.analyzer import TimeComplexityAnalyzer
except ImportError:
    # For deployment, try alternative import
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
    from analyzer import TimeComplexityAnalyzer
from .ml_models import TimeComplexityMLAnalyzer
from typing import Dict, Any, List
import json

class HybridTimeComplexityAnalyzer:
    def __init__(self, ml_models_path: str = None):
        """Initialize hybrid analyzer with both rule-based and ML components"""
        self.rule_based_analyzer = TimeComplexityAnalyzer()
        self.ml_analyzer = TimeComplexityMLAnalyzer()
        self.ml_enabled = False
        
        # Load ML models if available
        if ml_models_path and os.path.exists(ml_models_path):
            try:
                self.ml_analyzer.load_models(ml_models_path)
                self.ml_enabled = True
                print("✅ ML models loaded successfully")
            except Exception as e:
                print(f"⚠️ Failed to load ML models: {e}")
                print("🔄 Falling back to rule-based analysis only")
        else:
            print("ℹ️ ML models not found. Using rule-based analysis only")
    
    def analyze(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyze code using hybrid approach
        Combines rule-based and ML analysis for optimal results
        """
        print(f"🔍 Analyzing {language} code with hybrid approach...")
        
        # Get rule-based analysis
        rule_based_result = self.rule_based_analyzer.analyze(code, language)
        
        # Get ML analysis if available
        ml_result = None
        if self.ml_enabled:
            try:
                ml_result = self.ml_analyzer.predict_complexity(code, language)
            except Exception as e:
                print(f"⚠️ ML analysis failed: {e}")
        
        # Combine results
        final_result = self._combine_analyses(rule_based_result, ml_result, code, language)
        
        return final_result
    
    def _combine_analyses(self, rule_result: Dict, ml_result: Dict, code: str, language: str) -> Dict[str, Any]:
        """Intelligently combine rule-based and ML analysis results"""
        
        # If ML is not available, return rule-based result
        if not ml_result:
            return {
                **rule_result,
                'analysis_method': 'rule_based',
                'ml_confidence': 0.0,
                'ensemble_confidence': rule_result.get('confidence', 0.0)
            }
        
        # Extract complexities
        rule_time = rule_result.get('time_complexity', 'Unknown')
        rule_space = rule_result.get('space_complexity', 'Unknown')
        rule_confidence = rule_result.get('confidence', 0.0)
        
        ml_time = ml_result.get('time_complexity', 'Unknown')
        ml_space = ml_result.get('space_complexity', 'Unknown')
        ml_time_confidence = ml_result.get('time_confidence', 0.0)
        ml_space_confidence = ml_result.get('space_confidence', 0.0)
        
        # Determine final complexity based on confidence and agreement
        final_time, final_space, method, confidence = self._determine_final_complexity(
            rule_time, rule_space, rule_confidence,
            ml_time, ml_space, ml_time_confidence, ml_space_confidence
        )
        
        # Combine breakdowns
        breakdown = self._combine_breakdowns(rule_result.get('breakdown', []), ml_result)
        
        # Combine suggestions
        suggestions = self._combine_suggestions(
            rule_result.get('suggestions', []), 
            ml_result, 
            final_time, 
            final_space
        )
        
        return {
            'time_complexity': final_time,
            'space_complexity': final_space,
            'breakdown': breakdown,
            'suggestions': suggestions,
            'analysis_method': method,
            'rule_based_confidence': rule_confidence,
            'ml_confidence': (ml_time_confidence + ml_space_confidence) / 2,
            'ensemble_confidence': confidence,
            'model_agreement': ml_result.get('model_agreement', {}),
            'rule_based_result': rule_result,
            'ml_result': ml_result
        }
    
    def _determine_final_complexity(self, rule_time, rule_space, rule_conf, 
                                  ml_time, ml_space, ml_time_conf, ml_space_conf):
        """Determine final complexity based on confidence and agreement"""
        
        # If rule-based has high confidence and ML agrees, use rule-based
        if rule_conf > 0.8 and rule_time == ml_time and rule_space == ml_space:
            return rule_time, rule_space, 'hybrid_agreement', max(rule_conf, (ml_time_conf + ml_space_conf) / 2)
        
        # If ML has high confidence and rule-based is uncertain
        if (ml_time_conf + ml_space_conf) / 2 > 0.8 and rule_conf < 0.5:
            return ml_time, ml_space, 'ml_high_confidence', (ml_time_conf + ml_space_conf) / 2
        
        # If rule-based has high confidence and ML is uncertain
        if rule_conf > 0.8 and (ml_time_conf + ml_space_conf) / 2 < 0.5:
            return rule_time, rule_space, 'rule_based_high_confidence', rule_conf
        
        # If both are uncertain, use weighted average
        if rule_conf < 0.5 and (ml_time_conf + ml_space_conf) / 2 < 0.5:
            # Prefer rule-based for known patterns, ML for complex patterns
            if rule_time != 'Unknown':
                return rule_time, rule_space, 'rule_based_fallback', rule_conf
            else:
                return ml_time, ml_space, 'ml_fallback', (ml_time_conf + ml_space_conf) / 2
        
        # Default: use the one with higher confidence
        rule_avg_conf = rule_conf
        ml_avg_conf = (ml_time_conf + ml_space_conf) / 2
        
        if rule_avg_conf > ml_avg_conf:
            return rule_time, rule_space, 'rule_based_higher_confidence', rule_avg_conf
        else:
            return ml_time, ml_space, 'ml_higher_confidence', ml_avg_conf
    
    def _combine_breakdowns(self, rule_breakdown: List[str], ml_result: Dict) -> List[str]:
        """Combine breakdown information from both approaches"""
        breakdown = rule_breakdown.copy()
        
        if ml_result:
            # Add ML-specific insights
            model_agreement = ml_result.get('model_agreement', {})
            
            if model_agreement:
                time_predictions = model_agreement.get('time_predictions', {})
                space_predictions = model_agreement.get('space_predictions', {})
                
                if len(time_predictions) > 1:
                    breakdown.append(f"ML models show {len(time_predictions)} different time complexity predictions")
                
                if len(space_predictions) > 1:
                    breakdown.append(f"ML models show {len(space_predictions)} different space complexity predictions")
                
                # Add most confident predictions
                if time_predictions:
                    most_confident_time = max(time_predictions.items(), key=lambda x: x[1])
                    breakdown.append(f"ML most confident time complexity: {most_confident_time[0]} ({most_confident_time[1]} models)")
                
                if space_predictions:
                    most_confident_space = max(space_predictions.items(), key=lambda x: x[1])
                    breakdown.append(f"ML most confident space complexity: {most_confident_space[0]} ({most_confident_space[1]} models)")
        
        return breakdown
    
    def _combine_suggestions(self, rule_suggestions: List[str], ml_result: Dict, 
                           final_time: str, final_space: str) -> List[str]:
        """Combine suggestions from both approaches"""
        suggestions = rule_suggestions.copy()
        
        if ml_result:
            ml_time_conf = ml_result.get('time_confidence', 0.0)
            ml_space_conf = ml_result.get('space_confidence', 0.0)
            
            # Add ML-specific suggestions
            if ml_time_conf < 0.7:
                suggestions.append("ML models show low confidence in time complexity prediction")
                suggestions.append("Consider providing more context or simplifying the algorithm")
            
            if ml_space_conf < 0.7:
                suggestions.append("ML models show low confidence in space complexity prediction")
                suggestions.append("Check for complex data structure usage patterns")
            
            # Add ensemble-specific suggestions
            model_agreement = ml_result.get('model_agreement', {})
            time_predictions = model_agreement.get('time_predictions', {})
            
            if len(time_predictions) > 2:
                suggestions.append("Multiple ML models disagree on time complexity")
                suggestions.append("This suggests the algorithm has complex or ambiguous patterns")
                suggestions.append("Consider breaking down the algorithm into smaller functions")
        
        # Add hybrid-specific suggestions
        if final_time == 'Unknown':
            suggestions.append("Both rule-based and ML analysis are uncertain")
            suggestions.append("Consider adding algorithm comments or using a simpler approach")
        
        return suggestions
    
    def get_analysis_details(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Get detailed analysis with both rule-based and ML breakdowns"""
        result = self.analyze(code, language)
        
        details = {
            'final_result': {
                'time_complexity': result['time_complexity'],
                'space_complexity': result['space_complexity'],
                'confidence': result['ensemble_confidence'],
                'method': result['analysis_method']
            },
            'rule_based_analysis': {
                'time_complexity': result['rule_based_result']['time_complexity'],
                'space_complexity': result['rule_based_result']['space_complexity'],
                'confidence': result['rule_based_confidence'],
                'breakdown': result['rule_based_result']['breakdown'],
                'suggestions': result['rule_based_result']['suggestions']
            },
            'ml_analysis': {
                'enabled': self.ml_enabled,
                'time_complexity': result['ml_result']['time_complexity'] if result['ml_result'] else 'N/A',
                'space_complexity': result['ml_result']['space_complexity'] if result['ml_result'] else 'N/A',
                'time_confidence': result['ml_result']['time_confidence'] if result['ml_result'] else 0.0,
                'space_confidence': result['ml_result']['space_confidence'] if result['ml_result'] else 0.0,
                'model_agreement': result['model_agreement']
            },
            'combined_result': {
                'breakdown': result['breakdown'],
                'suggestions': result['suggestions']
            }
        }
        
        return details

def test_hybrid_analyzer():
    """Test the hybrid analyzer with various code examples"""
    
    # Initialize analyzer (without ML models for testing)
    analyzer = HybridTimeComplexityAnalyzer()
    
    test_cases = [
        {
            "name": "Simple Loop",
            "code": """
def simple_loop(n):
    for i in range(n):
        print(i)
""",
            "language": "python"
        },
        {
            "name": "Binary Search",
            "code": """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
            "language": "python"
        },
        {
            "name": "Complex Algorithm",
            "code": """
def complex_algorithm(data):
    result = []
    for item in data:
        if item > 0:
            processed = []
            for subitem in item:
                if subitem % 2 == 0:
                    processed.append(subitem * 2)
            result.extend(processed)
    return result
""",
            "language": "python"
        }
    ]
    
    print("🧪 Testing Hybrid TimeComplexity Analyzer")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 30)
        
        result = analyzer.analyze(test_case['code'], test_case['language'])
        
        print(f"⏱️ Time Complexity: {result['time_complexity']}")
        print(f"💾 Space Complexity: {result['space_complexity']}")
        print(f"🎯 Method: {result['analysis_method']}")
        print(f"📊 Confidence: {result['ensemble_confidence']:.2f}")
        
        print("📋 Breakdown:")
        for item in result['breakdown']:
            print(f"  • {item}")
        
        print("💡 Suggestions:")
        for suggestion in result['suggestions']:
            print(f"  • {suggestion}")

if __name__ == "__main__":
    test_hybrid_analyzer() 