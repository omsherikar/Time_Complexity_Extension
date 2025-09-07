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
from typing import Dict, Any, List, Tuple
import json
import re

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
        
        # Phase-1 toggle: soft guardrails (no hard overrides when disabled)
        # Default off: ML-first without pattern forcing
        self.STRICT_GUARDRAILS: bool = bool(
            os.environ.get("STRICT_GUARDRAILS", "0").strip() in ("1", "true", "True")
        )
    
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
        
        # Combine results (ML-first policy)
        final_result = self._combine_analyses(rule_based_result, ml_result, code, language)
        
        return final_result
    
    def _combine_analyses(self, rule_result: Dict, ml_result: Dict, code: str, language: str) -> Dict[str, Any]:
        """Intelligently combine rule-based and ML analysis results"""
        
        # If ML is not available, return rule-based result (with safe guardrail corrections if strong signals)
        if not ml_result:
            comp = self._composite_signals(code, language)
            corrected_time, corrected_space = self._guardrail_corrections(comp)
            final_time = corrected_time or rule_result.get('time_complexity', 'Unknown')
            final_space = corrected_space or rule_result.get('space_complexity', 'Unknown')
            method = 'rule_plus_guardrail' if (corrected_time or corrected_space) else 'rule_based'
            ensemble_conf = max(rule_result.get('confidence', 0.0), 0.55 if (corrected_time or corrected_space) else 0.0)
            return {
                **rule_result,
                'time_complexity': final_time,
                'space_complexity': final_space,
                'analysis_method': method,
                'ml_confidence': 0.0,
                'ensemble_confidence': ensemble_conf
            }
        
        # Extract complexities
        rule_time = rule_result.get('time_complexity', 'Unknown')
        rule_space = rule_result.get('space_complexity', 'Unknown')
        rule_confidence = rule_result.get('confidence', 0.0)
        
        ml_time = ml_result.get('time_complexity', 'Unknown')
        ml_space = ml_result.get('space_complexity', 'Unknown')
        ml_time_confidence = ml_result.get('time_confidence', 0.0)
        ml_space_confidence = ml_result.get('space_confidence', 0.0)

        # Phase-1: compute language-specific composite signals (C++/Java priority)
        composite = self._composite_signals(code, language)

        # Soft guardrails: nudge ML confidence based on strong patterns (never hard override here)
        ml_avg_conf = (ml_time_confidence + ml_space_confidence) / 2
        if self.STRICT_GUARDRAILS:
            # Boost confidence slightly if ML matches a strong signature
            if composite.get('binary_search') and ml_time in ('O(log n)', 'O(log n)'):
                ml_time_confidence = min(1.0, ml_time_confidence + 0.1)
            if composite.get('merge_sort') and ml_time in ('O(n log n)', 'O(n log n)'):
                ml_time_confidence = min(1.0, ml_time_confidence + 0.1)
            if composite.get('dp_triply_nested') and ml_time in ('O(n³)', 'O(n^3)', 'O(n3)'):
                ml_time_confidence = min(1.0, ml_time_confidence + 0.12)
            if composite.get('bubble_triangular') and ml_time in ('O(n²)', 'O(n^2)'):
                ml_time_confidence = min(1.0, ml_time_confidence + 0.08)
            ml_avg_conf = (ml_time_confidence + ml_space_confidence) / 2
        
        # Determine final complexity based on confidence and agreement (ML-first)
        final_time, final_space, method, confidence = self._determine_final_complexity(
            rule_time, rule_space, rule_confidence,
            ml_time, ml_space, ml_time_confidence, ml_space_confidence
        )

        # If ML confidence is low and we have very strong composite evidence, provide safe correction
        # We only apply this when ML confidence is clearly low (< 0.5) to avoid fighting ML.
        if ml_result and confidence < 0.5:
            corrected_time, corrected_space = self._guardrail_corrections(composite)
            if corrected_time or corrected_space:
                if corrected_time:
                    final_time = corrected_time
                if corrected_space:
                    final_space = corrected_space
                method = 'guardrail_cpp'
                confidence = max(confidence, 0.55)

        # Stronger guardrails when STRICT_GUARDRAILS enabled: enforce well-known signatures
        if self.STRICT_GUARDRAILS:
            hard_time, hard_space = self._guardrail_corrections(composite)
            if hard_time:
                # Enforce time correction when signature is strong and ML disagrees
                if hard_time != final_time:
                    final_time = hard_time
                    method = 'guardrail_enforced'
                    confidence = max(confidence, 0.6)
            if hard_space:
                if hard_space != final_space:
                    final_space = hard_space
                    method = 'guardrail_enforced'
                    confidence = max(confidence, 0.6)
        
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
        
        # ML-first policy
        ml_avg = (ml_time_conf + ml_space_conf) / 2
        # High-confidence ML → take ML
        if ml_avg >= 0.8:
            return ml_time, ml_space, 'ml_high_confidence', ml_avg
        # Low-confidence ML and decent rule confidence → allow rule fallback
        if ml_avg < 0.45 and rule_conf >= 0.6:
            return rule_time, rule_space, 'rule_based_fallback', rule_conf
        # If both are low → Unknown (avoid confident wrong answers)
        if ml_avg < 0.45 and rule_conf < 0.6:
            return 'Unknown', 'Unknown', 'uncertain', 0.4
        # Otherwise prefer ML (even if moderate)
        return ml_time, ml_space, 'ml_higher_confidence', ml_avg

    def _guardrail_corrections(self, comp: Dict[str, bool]) -> Tuple[str, str]:
        """Provide safe corrections when we have very strong composite evidence and low ML confidence.
        Returns (time_override, space_override) with None when no change.
        """
        t = None
        s = None
        if comp.get('binary_search'):
            t = 'O(log n)'
            s = s or 'O(1)'
        if comp.get('merge_sort'):
            t = 'O(n log n)'
            s = 'O(n)'
        if comp.get('dp_triply_nested'):
            t = 'O(n³)'
            s = s or 'O(n²)'
        if comp.get('bubble_triangular'):
            t = 'O(n²)'
            s = s or 'O(1)'
        if comp.get('dp_2d_table'):
            s = 'O(n²)'
        if comp.get('permutations'):
            t = 'O(n!)'
            s = s or 'O(n)'
        if comp.get('balanced_tree_loop'):
            t = 'O(n log n)'
            s = s or 'O(n)'
        if comp.get('linear_scan'):
            t = 'O(n)'
            s = s or 'O(1)'
        if comp.get('exp_recursive'):
            t = 'O(2ⁿ)'
            s = 'O(n)'
        if comp.get('dp_1d_array'):
            t = 'O(n)'
            s = 'O(n)'
        if comp.get('triple_nested_loops'):
            t = 'O(n³)'
            s = s or 'O(1)'
        return t, s

    def _composite_signals(self, code: str, language: str) -> Dict[str, bool]:
        """Detect strong language-aware patterns (C++/Java prioritized)."""
        comp: Dict[str, bool] = {
            'binary_search': False,
            'merge_sort': False,
            'dp_triply_nested': False,
            'bubble_triangular': False,
            'dp_2d_table': False,
            'permutations': False,
            'balanced_tree_loop': False,
            'linear_scan': False,
            'exp_recursive': False,
            'dp_1d_array': False,
            'triple_nested_loops': False,
        }
        try:
            src = code
            if language in ('cpp', 'java'):
                # Binary search: while (l<=r) + mid + adjust bounds (support l + (r-l)/2 or (l+r)/2)
                if re.search(r'while\s*\(\s*\w+\s*<=\s*\w+\s*\)', src) and \
                   (re.search(r'mid\s*=\s*\(\s*\w+\s*\+\s*\w+\s*\)\s*/\s*2', src) or \
                    re.search(r'mid\s*=\s*\w+\s*\+\s*\(\s*\w+\s*-\s*\w+\s*\)\s*/\s*2', src)) and \
                   (re.search(r'\w+\s*=\s*mid\s*\+\s*1', src) or re.search(r'\w+\s*=\s*mid\s*-\s*1', src)):
                    comp['binary_search'] = True

                # Merge sort: recursive split + merge with temp buffers (vector or stack arrays)
                if (re.search(r'mergeSort\s*\(', src) and re.search(r'merge\s*\(', src)) and \
                   (re.search(r'\bint\s+L\s*\[\s*\w+\s*\]\s*,\s*R\s*\[\s*\w+\s*\]\s*;', src) or \
                    re.search(r'vector\s*<[^>]+>\s*[LR]\s*\(', src) or \
                    ('int[] L' in src and 'int[] R' in src)):
                    comp['merge_sort'] = True

                # DP 2D table: C++ vector<vector<..>> or C/Java 2D arrays like int m[n][n] / new int[n][n]
                if re.search(r'vector\s*<\s*vector<[^>]+>\s*>\s*\w+\s*\(', src) or \
                   re.search(r'\bint\s+\w+\s*\[\s*\w+\s*\]\s*\[\s*\w+\s*\]', src) or \
                   re.search(r'new\s+\w+\s*\[\s*\w+\s*\]\s*\[\s*\w+\s*\]', src):
                    comp['dp_2d_table'] = True

                # Triply nested loops (very rough but effective for DP like MCM)
                # Look for three for-loops with indices i,j,k in proximity
                if re.search(r'for\s*\(.*len.*\)', src) and re.search(r'for\s*\(.*i\s*<', src) and re.search(r'for\s*\(.*k\s*<', src):
                    comp['dp_triply_nested'] = True
                # Generic triple nested loops (C++)
                if len(re.findall(r'for\s*\(', src)) >= 3 and re.search(r'for[\s\S]*for[\s\S]*for', src):
                    comp['triple_nested_loops'] = True

                # Bubble sort triangular bound (j < n - i - 1)
                if re.search(r'for\s*\(\s*int\s+j\s*=\s*0\s*;\s*j\s*<\s*\w+\s*-\s*i\s*-\s*1\s*;', src):
                    comp['bubble_triangular'] = True

                # Exponential recursion: return f(n-1) + f(n-2) or two recursive calls
                if re.search(r'return\s+([A-Za-z_]\w*)\s*\(\s*\w+\s*-\s*1\s*\)\s*\+\s*\1\s*\(\s*\w+\s*-\s*2\s*\)', src):
                    comp['exp_recursive'] = True

                # Permutations/backtracking: swap + recurse on next index or next_permutation loop
                if ('next_permutation' in src) or \
                   (re.search(r'swap\s*\(\s*\w+\s*\[\s*\w+\s*\]\s*,\s*\w+\s*\[\s*\w+\s*\]\s*\)', src) and \
                    re.search(r'\w+\s*\(\s*\w+\s*,\s*\w+\s*[+\-]\s*1\s*\)', src)) or \
                   (re.search(r'int\s+\w+\s*=\s*\w+\s*\[\s*\w+\s*\]\s*;', src) and \
                    re.search(r'\w+\s*\[\s*\w+\s*\]\s*=\s*\w+\s*\[\s*\w+\s*\]\s*;', src) and \
                    re.search(r'\w+\s*\(\s*\w+\s*,\s*\w+\s*\+\s*1\s*\)', src)):
                    comp['permutations'] = True

                # Balanced tree ops in loop: Java TreeMap/TreeSet with puts in a for/foreach
                if ('TreeMap<' in src or 'TreeSet<' in src) and re.search(r'for\s*\(', src) and \
                   ('.put(' in src or '.add(' in src):
                    comp['balanced_tree_loop'] = True

                # Linear scan: single for loop over container size without nested/binary cues
                if re.search(r'for\s*\(\s*int\s+\w+\s*=\s*0\s*;\s*\w+\s*<\s*\w+\.size\s*\(\s*\)\s*;\s*\w+\+\+\s*\)', src) and \
                   not comp['binary_search'] and not comp['bubble_triangular'] and 'while' not in src:
                    comp['linear_scan'] = True

                # DP 1D array: vector<int> dp(n + 1, 0)
                if re.search(r'vector\s*<\s*int\s*>\s*dp\s*\(\s*\w+\s*\+\s*1\s*,\s*0\s*\)', src):
                    comp['dp_1d_array'] = True
            else:
                # Lightweight generic cues for Python/JS
                if 'while left <= right' in src and 'mid' in src:
                    comp['binary_search'] = True
                if ('def merge' in src and 'while i <' in src and 'while j <' in src) or ('merge_sort' in src):
                    comp['merge_sort'] = True
                if re.search(r'dp\s*\[\s*\w+\s*\]\s*\[\s*\w+\s*\]', src):
                    comp['dp_2d_table'] = True
                if re.search(r'for j in range\(.*n.*-.*i.*-.*1\)', src):
                    comp['bubble_triangular'] = True
                if re.search(r'swap\(', src) and re.search(r'backtrack\(', src):
                    comp['permutations'] = True
                # Python triple nested loops
                if re.search(r'for\s+\w+\s+in\s+range\(.*\):[\s\S]*for\s+\w+\s+in\s+range\(.*\):[\s\S]*for\s+\w+\s+in\s+range\(.*\):', src):
                    comp['triple_nested_loops'] = True
        except Exception:
            pass
        return comp
    
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