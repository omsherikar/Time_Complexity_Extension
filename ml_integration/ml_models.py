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
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    print("⚠️ XGBoost not available, using alternative models")
    XGBOOST_AVAILABLE = False
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
        self._calibration = {'time_temp': 1.0, 'space_temp': 1.0}
        self.meta_models = {}
        
    def _normalize_label(self, label: str, kind: str) -> str:
        """Map variant labels to canonical forms supported by the classifier."""
        if not isinstance(label, str):
            return label
        s = label.strip()
        # Canonical time classes
        time_map = {
            'O((V + E) log V)': 'O(n log n)',
            'O(V + E)': 'O(n)',
            'O(n^2)': 'O(n²)',
            'O(n^3)': 'O(n³)',
            'O(2^n)': 'O(2ⁿ)',
            'O(n^2 log n)': 'O(n log n)',
        }
        space_map = {
            'O(V)': 'O(n)',
            'O(E)': 'O(n)',
            'O(n^2)': 'O(n²)',
        }
        if kind == 'time':
            return time_map.get(s, s)
        else:
            return space_map.get(s, s)
    
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
        
        # Composite, language-aware detectors (C++/Java prioritized)
        comp = self._composite_signals(code, language)
        # Encode as integers (0/1) for ML compatibility
        for key, val in comp.items():
            features[f"comp_{key}"] = 1 if val else 0
        
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
    
    def _composite_signals(self, code: str, language: str) -> Dict[str, bool]:
        """Detect strong composite signals for canonical patterns.
        Returns a dict of boolean flags.
        """
        flags: Dict[str, bool] = {
            'binary_search_signature': False,
            'sort_present': False,
            'dp_2d_table': False,
            'dp_triply_nested': False,
            'divide_and_conquer_linear_merge': False,
            'triangular_nested': False,
            'heap_ops': False,
            'balanced_tree_ops': False,
            'permutation_backtracking': False,
            'memoization_present': False,
        }
        try:
            src = code
            # Common memoization cues
            if re.search(r'memo\\s*\\[', src) or re.search(r'cache\\s*\\[', src) or '@lru_cache' in src:
                flags['memoization_present'] = True
            if language == 'cpp':
                # Binary search signature
                if re.search(r'while\\s*\\(\\s*\\w+\\s*<=\\s*\\w+\\s*\\)', src) and \
                   re.search(r'mid\\s*=\\s*\\(\\s*\\w+\\s*\\+\\s*\\w+\\s*\\)\\s*/\\s*2', src) and \
                   (re.search(r'\\w+\\s*=\\s*mid\\s*\\+\\s*1', src) or re.search(r'\\w+\\s*=\\s*mid\\s*-\\s*1', src)):
                    flags['binary_search_signature'] = True
                # Sort presence
                if 'std::sort' in src or re.search(r'sort\\s*\\(', src):
                    flags['sort_present'] = True
                # DP 2D table
                if re.search(r'vector\\s*<\\s*vector<[^>]+>\\s*>\\s*\\w+\\s*\\(\\s*\\w+\\s*,\\s*vector<[^>]+>\\s*\\(\\s*\\w+\\s*\\)\\s*\\)', src):
                    flags['dp_2d_table'] = True
                # Triply nested loops
                if re.search(r'for\\s*\\(.*len.*\\)', src) and re.search(r'for\\s*\\(.*i\\s*<', src) and re.search(r'for\\s*\\(.*k\\s*<', src):
                    flags['dp_triply_nested'] = True
                # Divide and conquer linear merge (merge sort style)
                if ('merge' in src and re.search(r'for\\s*\\(\\s*int\\s+i', src) and (src.count('L[') + src.count('R[') > 0)) or \
                   (re.search(r'mergeSort\\s*\\(', src) and ('vector' in src)):
                    flags['divide_and_conquer_linear_merge'] = True
                # Triangular nested j < n - i - 1
                if re.search(r'for\\s*\\(\\s*int\\s+j\\s*=\\s*0\\s*;\\s*j\\s*<\\s*\\w+\\s*-\\s*i\\s*-\\s*1\\s*;', src):
                    flags['triangular_nested'] = True
                # Heap ops / balanced tree
                if 'priority_queue<' in src:
                    flags['heap_ops'] = True
                if 'std::map<' in src or 'std::set<' in src:
                    flags['balanced_tree_ops'] = True
            elif language == 'java':
                # Binary search signature (indexes)
                if re.search(r'while\\s*\\(\\s*\\w+\\s*<=\\s*\\w+\\s*\\)', src) and \
                   re.search(r'int\\s+mid\\s*=\\s*\\(\\s*\\w+\\s*\\+\\s*\\w+\\s*\\)\\s*/\\s*2', src) and \
                   (re.search(r'\\w+\\s*=\\s*mid\\s*\\+\\s*1', src) or re.search(r'\\w+\\s*=\\s*mid\\s*-\\s*1', src)):
                    flags['binary_search_signature'] = True
                # Sort presence
                if 'Arrays.sort' in src or 'Collections.sort' in src:
                    flags['sort_present'] = True
                # DP 2D table (array allocation)
                if re.search(r'int\\s*\\[\\s*\\]\\s*\\[\\s*\\]\\s*\\w+\\s*=\\s*new\\s+int\\s*\\[\\s*\\w+\\s*\\]\\s*\\[\\s*\\w+\\s*\\]', src):
                    flags['dp_2d_table'] = True
                # Triangular nested
                if re.search(r'for\\s*\\(\\s*int\\s+j\\s*=\\s*0\\s*;\\s*j\\s*<\\s*\\w+\\s*-\\s*i\\s*-\\s*1\\s*;', src):
                    flags['triangular_nested'] = True
                # Divide and conquer merge sort signals
                if ('merge' in src and 'int[] L' in src and 'int[] R' in src) or ('mergeSort(' in src and ('int[]' in src or 'List<' in src)):
                    flags['divide_and_conquer_linear_merge'] = True
                # Heap ops / balanced tree
                if 'PriorityQueue<' in src:
                    flags['heap_ops'] = True
                if 'TreeMap<' in src or 'TreeSet<' in src:
                    flags['balanced_tree_ops'] = True
            else:
                # Lightweight generic cues for Python/JS
                if 'while left <= right' in src and 'mid =' in src:
                    flags['binary_search_signature'] = True
                if 'sorted(' in src or '.sort(' in src:
                    flags['sort_present'] = True
                if re.search(r'dp\\s*\\[\\s*\\w+\\s*\\]\\s*\\[\\s*\\w+\\s*\\]', src):
                    flags['dp_2d_table'] = True
                if re.search(r'for .* in range\\(.*\\):[\\s\\S]*for .* in range\\(', src):
                    flags['dp_triply_nested'] = True
                if ('def merge' in src and 'while i <' in src and 'while j <' in src) or ('merge_sort' in src):
                    flags['divide_and_conquer_linear_merge'] = True
                if re.search(r'for j in range\\(.*n.*-.*i.*-.*1\\)', src):
                    flags['triangular_nested'] = True
        except Exception:
            # Be resilient to any regex/encoding issues
            pass
        return flags
    
    def prepare_training_data(self, dataset_file: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Prepare training data from dataset"""
        print("📊 Preparing training data...")
        
        with open(dataset_file, 'r') as f:
            data = json.load(f)
        
        X = []
        y_time = []
        y_space = []
        
        self.feature_names = []
        first_features = None
        for idx, item in enumerate(data):
            features = self.extract_advanced_features(item['code'], item['language'])
            if first_features is None:
                # Freeze feature order for scaler and models
                first_features = features
                self.feature_names = list(first_features.keys())
            # Align each sample to the frozen feature order
            X.append([features.get(name, 0) for name in self.feature_names])
            y_time.append(self._normalize_label(item['time_complexity'], 'time'))
            y_space.append(self._normalize_label(item['space_complexity'], 'space'))
        
        X = np.array(X)
        y_time = np.array(y_time)
        y_space = np.array(y_space)
        
        print(f"✅ Prepared {len(X)} samples with {len(self.feature_names)} features")
        return X, y_time, y_space
    
    def train_models(self, X: np.ndarray, y_time: np.ndarray, y_space: np.ndarray):
        """Train ensemble of ML models"""
        print("🤖 Training ML models...")
        
        # Fit encoders on full label sets to avoid unseen labels after split
        time_encoder = LabelEncoder()
        space_encoder = LabelEncoder()
        y_time_encoded_full = time_encoder.fit_transform(y_time)
        y_space_encoded_full = space_encoder.fit_transform(y_space)
        self.label_encoders['time_complexity'] = time_encoder
        self.label_encoders['space_complexity'] = space_encoder
        
        # Split data
        X_train, X_val, y_time_train_enc, y_time_val_enc, y_space_train_enc, y_space_val_enc = train_test_split(
            X, y_time_encoded_full, y_space_encoded_full, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        self.scalers['feature_scaler'] = scaler
        
        # Train models for time complexity
        print("⏱️ Training time complexity models...")
        self.models['time_complexity'] = {
            'random_forest': RandomForestClassifier(n_estimators=200, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=200, random_state=42),
            'neural_network': MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=800, random_state=42)
        }
        
        for name, model in self.models['time_complexity'].items():
            print(f"  Training {name}...")
            model.fit(X_train_scaled, y_time_train_enc)
            y_pred = model.predict(X_val_scaled)
            acc = accuracy_score(time_encoder.inverse_transform(y_time_val_enc), time_encoder.inverse_transform(y_pred))
            print(f"    {name} accuracy: {acc:.3f}")
        
        # Train models for space complexity
        print("💾 Training space complexity models...")
        self.models['space_complexity'] = {
            'random_forest': RandomForestClassifier(n_estimators=200, random_state=42),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=200, random_state=42),
            'neural_network': MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=800, random_state=42)
        }
        
        for name, model in self.models['space_complexity'].items():
            print(f"  Training {name}...")
            model.fit(X_train_scaled, y_space_train_enc)
            y_pred = model.predict(X_val_scaled)
            acc = accuracy_score(space_encoder.inverse_transform(y_space_val_enc), space_encoder.inverse_transform(y_pred))
            print(f"    {name} accuracy: {acc:.3f}")
        
        # Simple temperature scaling calibration using validation split
        self._calibration = {}
        self._calibration['time_temp'] = self._fit_temperature(self.models['time_complexity'], X_val_scaled, y_time_val_enc)
        self._calibration['space_temp'] = self._fit_temperature(self.models['space_complexity'], X_val_scaled, y_space_val_enc)
        
        # Meta-combiner for time complexity: averaged probs + composite flags
        from sklearn.linear_model import LogisticRegression
        time_classes = list(time_encoder.classes_)
        # Build validation averaged probs
        val_probs = []
        for i in range(X_val_scaled.shape[0]):
            x_row = X_val_scaled[i:i+1]
            probs_sum = None
            count = 0
            for m in self.models['time_complexity'].values():
                if hasattr(m, 'predict_proba'):
                    p = m.predict_proba(x_row)[0]
                    probs_sum = p if probs_sum is None else (probs_sum + p)
                    count += 1
                else:
                    pred = m.predict(x_row)[0]
                    p = np.zeros(len(time_classes))
                    p[pred] = 1.0
                    probs_sum = p if probs_sum is None else (probs_sum + p)
                    count += 1
            avg_probs = probs_sum / max(count, 1)
            val_probs.append(avg_probs)
        val_probs = np.array(val_probs)
        # Extract composite flags from raw (unscaled) X_val using feature names prefixed with 'comp_'
        comp_indices = [idx for idx, name in enumerate(self.feature_names) if name.startswith('comp_')]
        comp_val = X_val[:, comp_indices] if comp_indices else np.zeros((X_val.shape[0], 0))
        meta_X = np.hstack([val_probs, comp_val])
        meta_y = y_time_val_enc
        if meta_X.shape[0] > 5:
            meta = LogisticRegression(max_iter=1000, random_state=42)
            meta.fit(meta_X, meta_y)
            self.meta_models['time_meta'] = meta
            self.meta_models['time_meta_classes'] = time_classes
            print("✅ Trained time meta-combiner")
        else:
            self.meta_models['time_meta'] = None
            self.meta_models['time_meta_classes'] = time_classes
        
        self.is_trained = True
        print("✅ All models trained successfully!")
    
    def _fit_temperature(self, models: Dict[str, Any], X_val: np.ndarray, y_val: np.ndarray) -> float:
        """Fit a single temperature for averaging softmax-like probabilities from models with predict_proba.
        Returns a scalar temperature T >= 0.5 and <= 5.0.
        """
        import numpy as _np
        if X_val.shape[0] == 0:
            return 1.0
        # Determine global class count from any model (max classes)
        max_classes = 0
        global_labels = None
        for m in models.values():
            if hasattr(m, 'classes_'):
                max_classes = max(max_classes, len(m.classes_))
                global_labels = m.classes_ if global_labels is None else global_labels
        if max_classes == 0:
            return 1.0
        # Aggregate probs aligned to global label indices (encoded labels)
        probs = None
        count = 0
        for m in models.values():
            if hasattr(m, 'predict_proba'):
                p = m.predict_proba(X_val)
                # Align columns to global label set size
                aligned = _np.zeros((p.shape[0], max_classes), dtype=float)
                # Map each model class label to its column index
                for col, lab in enumerate(m.classes_):
                    if lab < max_classes:
                        aligned[:, lab] = p[:, col]
                probs = aligned if probs is None else probs + aligned
                count += 1
        if count == 0:
            return 1.0
        probs = probs / count
        # Temperature search simple grid
        best_T = 1.0
        best_nll = 1e9
        for T in [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 5.0]:
            pT = _np.clip(probs ** (1.0 / T), 1e-9, 1.0)
            pT = pT / pT.sum(axis=1, keepdims=True)
            n = _np.arange(len(y_val))
            # Guard against label indices outside current column range
            y_clipped = _np.clip(y_val, 0, pT.shape[1]-1)
            nll = -_np.log(pT[n, y_clipped]).mean()
            if nll < best_nll:
                best_nll = nll
                best_T = T
        return float(best_T)
    
    def predict_complexity(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Predict time and space complexity using ensemble"""
        if not self.is_trained:
            raise ValueError("Models not trained. Call train_models() first.")
        
        # Extract features
        features = self.extract_advanced_features(code, language)
        
        # Align features to the model's expected order/size
        if self.feature_names:
            aligned = [features.get(name, 0) for name in self.feature_names]
            X = np.array([aligned])
        else:
            X = np.array([list(features.values())])
        
        # Scale features
        X_scaled = self.scalers['feature_scaler'].transform(X)
        
        # Probability-averaged ensemble
        # Build stable class lists from encoders
        time_classes = list(self.label_encoders['time_complexity'].classes_)
        space_classes = list(self.label_encoders['space_complexity'].classes_)
        time_index = {c: i for i, c in enumerate(time_classes)}
        space_index = {c: i for i, c in enumerate(space_classes)}
        
        time_probs = np.zeros(len(time_classes), dtype=float)
        space_probs = np.zeros(len(space_classes), dtype=float)
        time_models_count = 0
        space_models_count = 0
        
        for name, model in self.models['time_complexity'].items():
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X_scaled)[0]
                # Align to global time classes using encoded labels
                for col, enc_lab in enumerate(getattr(model, 'classes_', [])):
                    cls = self.label_encoders['time_complexity'].inverse_transform([enc_lab])[0]
                    time_probs[time_index[cls]] += float(proba[col])
                time_models_count += 1
            else:
                pred = model.predict(X_scaled)[0]
                cls = self.label_encoders['time_complexity'].inverse_transform([pred])[0]
                time_probs[time_index[cls]] += 1.0
                time_models_count += 1
        
        for name, model in self.models['space_complexity'].items():
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X_scaled)[0]
                for col, enc_lab in enumerate(getattr(model, 'classes_', [])):
                    cls = self.label_encoders['space_complexity'].inverse_transform([enc_lab])[0]
                    space_probs[space_index[cls]] += float(proba[col])
                space_models_count += 1
            else:
                pred = model.predict(X_scaled)[0]
                cls = self.label_encoders['space_complexity'].inverse_transform([pred])[0]
                space_probs[space_index[cls]] += 1.0
                space_models_count += 1
        
        if time_models_count > 0:
            time_probs /= time_models_count
        if space_models_count > 0:
            space_probs /= space_models_count
        
        # Apply temperature scaling
        Tt = (self._calibration or {}).get('time_temp', 1.0)
        Ts = (self._calibration or {}).get('space_temp', 1.0)
        time_probs = np.clip(time_probs ** (1.0 / Tt), 1e-9, 1.0)
        space_probs = np.clip(space_probs ** (1.0 / Ts), 1e-9, 1.0)
        time_probs = time_probs / time_probs.sum()
        space_probs = space_probs / space_probs.sum()
        
        # Meta combiner (time): combine averaged probs + composite flags
        if self.meta_models.get('time_meta') is not None:
            comp_indices = [idx for idx, name in enumerate(self.feature_names) if name.startswith('comp_')]
            comp_vec = X[0, comp_indices] if comp_indices else np.zeros((0,), dtype=float)
            meta_input = np.concatenate([time_probs, comp_vec])
            meta = self.meta_models['time_meta']
            meta_proba = meta.predict_proba(meta_input.reshape(1, -1))[0]
            # Blend: average base probs with meta probs (mapped to class order)
            # meta classes already align with encoder indices used during training
            meta_classes = self.meta_models.get('time_meta_classes', time_classes)
            # Map meta proba order to time_classes index order
            # Assume encoders stable; average directly if lengths match
            if len(meta_proba) == len(time_probs):
                time_probs = (time_probs + meta_proba) / 2.0
                time_probs = time_probs / time_probs.sum()
        
        time_top_idx = int(np.argmax(time_probs))
        space_top_idx = int(np.argmax(space_probs))
        time_complexity = time_classes[time_top_idx]
        space_complexity = space_classes[space_top_idx]
        time_confidence = float(time_probs[time_top_idx])
        space_confidence = float(space_probs[space_top_idx])
        
        return {
            'time_complexity': time_complexity,
            'space_complexity': space_complexity,
            'time_confidence': time_confidence,
            'space_confidence': space_confidence,
            'time_probabilities': {cls: float(time_probs[i]) for i, cls in enumerate(time_classes)},
            'space_probabilities': {cls: float(space_probs[i]) for i, cls in enumerate(space_classes)}
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
            'is_trained': self.is_trained,
            'calibration': self._calibration,
            'meta_models': self.meta_models,
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
        self._calibration = model_data.get('calibration', {'time_temp': 1.0, 'space_temp': 1.0})
        self.meta_models = model_data.get('meta_models', {})
        
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