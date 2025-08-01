#!/usr/bin/env python3
"""
ML Models for TimeComplexity Analyzer
Ensemble of models for pattern recognition and complexity prediction
"""

import json
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
# import xgboost as xgb  # Temporarily disabled due to OpenMP dependency
import joblib
import ast
import re

class TimeComplexityMLAnalyzer:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.label_encoders = {}
        self.feature_names = []
        self.is_trained = False
        
    def extract_advanced_features(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Extract advanced features for ML analysis"""
        features = {}
        
        # Basic code metrics
        features['code_length'] = len(code)
        features['line_count'] = code.count('\n') + 1
        features['char_count'] = len(code.replace(' ', '').replace('\n', ''))
        
        # Function and class analysis
        features['function_count'] = code.count('def ')
        features['class_count'] = code.count('class ')
        features['method_count'] = code.count('def ') - code.count('def __')
        
        # Loop analysis
        features['for_loops'] = code.count('for ')
        features['while_loops'] = code.count('while ')
        features['total_loops'] = features['for_loops'] + features['while_loops']
        
        # Recursion analysis
        features['recursive_calls'] = self._count_recursive_calls(code)
        features['base_cases'] = self._count_base_cases(code)
        
        # Data structure usage
        features['arrays'] = code.count('[]') + code.count('list(')
        features['dictionaries'] = code.count('{}') + code.count('dict(')
        features['sets'] = code.count('set(')
        features['stacks'] = code.count('append(') + code.count('pop(')
        features['queues'] = code.count('deque(')
        features['heaps'] = code.count('heapq') + code.count('PriorityQueue')
        
        # Algorithm patterns
        features['binary_search'] = self._detect_binary_search(code)
        features['dynamic_programming'] = self._detect_dp(code)
        features['divide_conquer'] = self._detect_divide_conquer(code)
        features['greedy'] = self._detect_greedy(code)
        features['backtracking'] = self._detect_backtracking(code)
        
        # Complexity indicators
        features['nested_loops'] = self._count_nested_loops(code)
        features['exponential_patterns'] = self._detect_exponential(code)
        features['logarithmic_patterns'] = self._detect_logarithmic(code)
        features['linear_patterns'] = self._detect_linear(code)
        
        # AST-based features
        ast_features = self._extract_ast_features(code)
        features.update(ast_features)
        
        # Language-specific features
        if language == "python":
            features.update(self._extract_python_features(code))
        elif language == "cpp":
            features.update(self._extract_cpp_features(code))
        elif language == "java":
            features.update(self._extract_java_features(code))
        elif language == "javascript":
            features.update(self._extract_javascript_features(code))
        
        return features
    
    def _count_recursive_calls(self, code: str) -> int:
        """Count recursive function calls"""
        try:
            tree = ast.parse(code)
            function_names = set()
            recursive_calls = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_names.add(node.name)
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in function_names:
                        recursive_calls += 1
            
            return recursive_calls
        except:
            return 0
    
    def _count_base_cases(self, code: str) -> int:
        """Count base cases in recursive functions"""
        base_case_patterns = [
            r'if\s+\w+\s*<=\s*1',
            r'if\s+len\s*\(\s*\w+\s*\)\s*<=\s*1',
            r'if\s+not\s+\w+',
            r'if\s+\w+\s*==\s*0'
        ]
        
        count = 0
        for pattern in base_case_patterns:
            count += len(re.findall(pattern, code))
        
        return count
    
    def _detect_binary_search(self, code: str) -> int:
        """Detect binary search patterns"""
        patterns = [
            r'while\s+\w+\s*<=\s*\w+',
            r'mid\s*=\s*\(\s*\w+\s*\+\s*\w+\s*\)\s*//\s*2',
            r'left\s*=\s*mid\s*\+\s*1',
            r'right\s*=\s*mid\s*-\s*1'
        ]
        
        score = 0
        for pattern in patterns:
            if re.search(pattern, code):
                score += 1
        
        return score
    
    def _detect_dp(self, code: str) -> int:
        """Detect dynamic programming patterns"""
        patterns = [
            r'dp\s*\[',
            r'memo\s*\[',
            r'cache\s*\[',
            r'@lru_cache',
            r'@memoize'
        ]
        
        score = 0
        for pattern in patterns:
            if re.search(pattern, code):
                score += 1
        
        return score
    
    def _detect_divide_conquer(self, code: str) -> int:
        """Detect divide and conquer patterns"""
        patterns = [
            r'len\s*\(\s*\w+\s*\)\s*//\s*2',
            r'mid\s*=\s*len\s*\(\s*\w+\s*\)\s*//\s*2',
            r'left\s*=\s*\w+\s*\[\s*:\s*mid\s*\]',
            r'right\s*=\s*\w+\s*\[\s*mid\s*:\s*\]'
        ]
        
        score = 0
        for pattern in patterns:
            if re.search(pattern, code):
                score += 1
        
        return score
    
    def _detect_greedy(self, code: str) -> int:
        """Detect greedy algorithm patterns"""
        patterns = [
            r'sort\s*\(',
            r'sorted\s*\(',
            r'max\s*\(',
            r'min\s*\(',
            r'heapq\.heappop',
            r'heapq\.heappush'
        ]
        
        score = 0
        for pattern in patterns:
            if re.search(pattern, code):
                score += 1
        
        return score
    
    def _detect_backtracking(self, code: str) -> int:
        """Detect backtracking patterns"""
        patterns = [
            r'backtrack\s*\(',
            r'dfs\s*\(',
            r'visited\s*=\s*set\s*\(',
            r'visited\.add\s*\(',
            r'visited\.remove\s*\('
        ]
        
        score = 0
        for pattern in patterns:
            if re.search(pattern, code):
                score += 1
        
        return score
    
    def _count_nested_loops(self, code: str) -> int:
        """Count nested loop patterns"""
        lines = code.split('\n')
        nested_count = 0
        loop_depth = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith(('for ', 'while ')):
                loop_depth += 1
                if loop_depth > 1:
                    nested_count += 1
            elif stripped.startswith(('if ', 'elif ', 'else:')):
                pass  # Don't reset loop depth for conditionals
            elif stripped and not stripped.startswith((' ', '\t')):
                loop_depth = 0
        
        return nested_count
    
    def _detect_exponential(self, code: str) -> int:
        """Detect exponential complexity patterns"""
        patterns = [
            r'return\s+\w+\s*\(\s*\w+\s*-\s*1\s*\)\s*\+\s*\w+\s*\(\s*\w+\s*-\s*2\s*\)',
            r'return\s+\w+\s*\(\s*\w+\s*-\s*1\s*\)\s*\*\s*\w+\s*\(\s*\w+\s*-\s*1\s*\)',
            r'for\s+\w+\s+in\s+itertools\.product',
            r'for\s+\w+\s+in\s+itertools\.combinations'
        ]
        
        score = 0
        for pattern in patterns:
            if re.search(pattern, code):
                score += 1
        
        return score
    
    def _detect_logarithmic(self, code: str) -> int:
        """Detect logarithmic complexity patterns"""
        patterns = [
            r'while\s+\w+\s*<=\s*\w+',
            r'//\s*2',
            r'>>\s*1',
            r'math\.log',
            r'math\.log2'
        ]
        
        score = 0
        for pattern in patterns:
            if re.search(pattern, code):
                score += 1
        
        return score
    
    def _detect_linear(self, code: str) -> int:
        """Detect linear complexity patterns"""
        patterns = [
            r'for\s+\w+\s+in\s+range',
            r'for\s+\w+\s+in\s+\w+',
            r'while\s+\w+\s*<',
            r'while\s+\w+\s*!=\s*\w+'
        ]
        
        score = 0
        for pattern in patterns:
            if re.search(pattern, code):
                score += 1
        
        return score
    
    def _extract_ast_features(self, code: str) -> Dict[str, Any]:
        """Extract AST-based features"""
        try:
            tree = ast.parse(code)
            
            # Count different node types
            node_counts = {}
            for node in ast.walk(tree):
                node_type = type(node).__name__
                node_counts[node_type] = node_counts.get(node_type, 0) + 1
            
            # Calculate AST metrics
            features = {
                'ast_depth': self._get_ast_depth(tree),
                'ast_node_count': len(list(ast.walk(tree))),
                'ast_function_defs': node_counts.get('FunctionDef', 0),
                'ast_for_loops': node_counts.get('For', 0),
                'ast_while_loops': node_counts.get('While', 0),
                'ast_if_statements': node_counts.get('If', 0),
                'ast_calls': node_counts.get('Call', 0),
                'ast_assignments': node_counts.get('Assign', 0),
                'ast_returns': node_counts.get('Return', 0)
            }
            
            return features
        except:
            return {
                'ast_depth': 0,
                'ast_node_count': 0,
                'ast_function_defs': 0,
                'ast_for_loops': 0,
                'ast_while_loops': 0,
                'ast_if_statements': 0,
                'ast_calls': 0,
                'ast_assignments': 0,
                'ast_returns': 0
            }
    
    def _get_ast_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum AST depth"""
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            max_depth = max(max_depth, self._get_ast_depth(child, current_depth + 1))
        return max_depth
    
    def _extract_python_features(self, code: str) -> Dict[str, Any]:
        """Extract Python-specific features"""
        return {
            'list_comprehensions': code.count('[') - code.count('[]'),
            'generator_expressions': code.count('(') - code.count('()'),
            'lambda_functions': code.count('lambda '),
            'decorators': code.count('@'),
            'context_managers': code.count('with '),
            'exceptions': code.count('try:') + code.count('except'),
            'imports': code.count('import ') + code.count('from ')
        }
    
    def _extract_cpp_features(self, code: str) -> Dict[str, Any]:
        """Extract C++-specific features"""
        return {
            'templates': code.count('template'),
            'classes': code.count('class '),
            'namespaces': code.count('namespace'),
            'pointers': code.count('*'),
            'references': code.count('&'),
            'const': code.count('const'),
            'stl_containers': code.count('vector') + code.count('map') + code.count('set')
        }
    
    def _extract_java_features(self, code: str) -> Dict[str, Any]:
        """Extract Java-specific features"""
        return {
            'classes': code.count('class '),
            'interfaces': code.count('interface '),
            'public': code.count('public '),
            'private': code.count('private '),
            'static': code.count('static '),
            'final': code.count('final '),
            'collections': code.count('List') + code.count('Map') + code.count('Set')
        }
    
    def _extract_javascript_features(self, code: str) -> Dict[str, Any]:
        """Extract JavaScript-specific features"""
        return {
            'arrow_functions': code.count('=>'),
            'const_declarations': code.count('const '),
            'let_declarations': code.count('let '),
            'async_functions': code.count('async '),
            'await_keyword': code.count('await '),
            'promises': code.count('Promise'),
            'array_methods': code.count('.map(') + code.count('.filter(') + code.count('.reduce(')
        }
    
    def prepare_training_data(self, dataset_file: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Prepare training data from dataset"""
        print("📊 Preparing training data...")
        
        with open(dataset_file, 'r') as f:
            data = json.load(f)
        
        X = []
        y_time = []
        y_space = []
        
        for item in data:
            features = self.extract_advanced_features(item['code'], item['language'])
            X.append(list(features.values()))
            y_time.append(item['time_complexity'])
            y_space.append(item['space_complexity'])
        
        X = np.array(X)
        y_time = np.array(y_time)
        y_space = np.array(y_space)
        
        # Store feature names
        self.feature_names = list(data[0]['features'].keys())
        
        print(f"✅ Prepared {len(X)} samples with {len(self.feature_names)} features")
        return X, y_time, y_space
    
    def train_models(self, X: np.ndarray, y_time: np.ndarray, y_space: np.ndarray):
        """Train ensemble of ML models"""
        print("🤖 Training ML models...")
        
        # Split data
        X_train, X_test, y_time_train, y_time_test, y_space_train, y_space_test = train_test_split(
            X, y_time, y_space, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        self.scalers['feature_scaler'] = scaler
        
        # Encode labels
        time_encoder = LabelEncoder()
        space_encoder = LabelEncoder()
        
        y_time_train_encoded = time_encoder.fit_transform(y_time_train)
        y_space_train_encoded = space_encoder.fit_transform(y_space_train)
        
        self.label_encoders['time_complexity'] = time_encoder
        self.label_encoders['space_complexity'] = space_encoder
        
        # Train models for time complexity
        print("⏱️ Training time complexity models...")
        self.models['time_complexity'] = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            # 'xgboost': xgb.XGBClassifier(n_estimators=100, random_state=42),  # Temporarily disabled
            'neural_network': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        }
        
        for name, model in self.models['time_complexity'].items():
            print(f"  Training {name}...")
            model.fit(X_train_scaled, y_time_train_encoded)
            
            # Evaluate
            y_pred = model.predict(X_test_scaled)
            accuracy = accuracy_score(y_time_test, time_encoder.inverse_transform(y_pred))
            print(f"    {name} accuracy: {accuracy:.3f}")
        
        # Train models for space complexity
        print("💾 Training space complexity models...")
        self.models['space_complexity'] = {
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            # 'xgboost': xgb.XGBClassifier(n_estimators=100, random_state=42),  # Temporarily disabled
            'neural_network': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        }
        
        for name, model in self.models['space_complexity'].items():
            print(f"  Training {name}...")
            model.fit(X_train_scaled, y_space_train_encoded)
            
            # Evaluate
            y_pred = model.predict(X_test_scaled)
            accuracy = accuracy_score(y_space_test, space_encoder.inverse_transform(y_pred))
            print(f"    {name} accuracy: {accuracy:.3f}")
        
        self.is_trained = True
        print("✅ All models trained successfully!")
    
    def predict_complexity(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Predict time and space complexity using ensemble"""
        if not self.is_trained:
            raise ValueError("Models not trained. Call train_models() first.")
        
        # Extract features
        features = self.extract_advanced_features(code, language)
        X = np.array([list(features.values())])
        
        # Scale features
        X_scaled = self.scalers['feature_scaler'].transform(X)
        
        # Get predictions from all models
        time_predictions = []
        space_predictions = []
        
        for name, model in self.models['time_complexity'].items():
            pred = model.predict(X_scaled)[0]
            time_predictions.append(self.label_encoders['time_complexity'].inverse_transform([pred])[0])
        
        for name, model in self.models['space_complexity'].items():
            pred = model.predict(X_scaled)[0]
            space_predictions.append(self.label_encoders['space_complexity'].inverse_transform([pred])[0])
        
        # Ensemble prediction (majority vote)
        from collections import Counter
        time_complexity = Counter(time_predictions).most_common(1)[0][0]
        space_complexity = Counter(space_predictions).most_common(1)[0][0]
        
        # Calculate confidence
        time_confidence = Counter(time_predictions).most_common(1)[0][1] / len(time_predictions)
        space_confidence = Counter(space_predictions).most_common(1)[0][1] / len(space_predictions)
        
        return {
            'time_complexity': time_complexity,
            'space_complexity': space_complexity,
            'time_confidence': time_confidence,
            'space_confidence': space_confidence,
            'model_agreement': {
                'time_predictions': dict(Counter(time_predictions)),
                'space_predictions': dict(Counter(space_predictions))
            }
        }
    
    def save_models(self, filepath: str):
        """Save trained models"""
        if not self.is_trained:
            raise ValueError("Models not trained. Call train_models() first.")
        
        model_data = {
            'models': self.models,
            'scalers': self.scalers,
            'label_encoders': self.label_encoders,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        joblib.dump(model_data, filepath)
        print(f"✅ Models saved to {filepath}")
    
    def load_models(self, filepath: str):
        """Load trained models"""
        model_data = joblib.load(filepath)
        
        self.models = model_data['models']
        self.scalers = model_data['scalers']
        self.label_encoders = model_data['label_encoders']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']
        
        print(f"✅ Models loaded from {filepath}")

if __name__ == "__main__":
    # Example usage
    analyzer = TimeComplexityMLAnalyzer()
    
    # Train models (if dataset exists)
    try:
        X, y_time, y_space = analyzer.prepare_training_data("ml_dataset.json")
        analyzer.train_models(X, y_time, y_space)
        analyzer.save_models("ml_models.pkl")
    except FileNotFoundError:
        print("Dataset not found. Run data_collector.py first.") 