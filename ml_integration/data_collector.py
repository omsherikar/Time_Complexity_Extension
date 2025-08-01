#!/usr/bin/env python3
"""
Data Collector for TimeComplexity Analyzer ML Models
Collects and prepares training data from various sources
"""

import json
import os
import requests
from typing import List, Dict, Any
from dataclasses import dataclass
import ast
import re

@dataclass
class CodeSample:
    code: str
    language: str
    time_complexity: str
    space_complexity: str
    algorithm_type: str
    patterns: List[str]
    confidence: float
    source: str

class DataCollector:
    def __init__(self):
        self.samples = []
        self.sources = {
            'leetcode': 'https://leetcode.com/api/problems/all/',
            'geeksforgeeks': 'https://practice.geeksforgeeks.org/',
            'hackerrank': 'https://www.hackerrank.com/',
            'github': 'https://api.github.com/search/repositories'
        }
    
    def collect_from_leetcode(self) -> List[CodeSample]:
        """Collect code samples from LeetCode problems"""
        print("🔍 Collecting data from LeetCode...")
        
        # LeetCode problem categories with known complexities
        leetcode_data = [
            {
                "title": "Two Sum",
                "code": """
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
""",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "algorithm_type": "hash_table",
                "patterns": ["single_loop", "hash_lookup"],
                "confidence": 0.95
            },
            {
                "title": "Binary Search",
                "code": """
def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
""",
                "time_complexity": "O(log n)",
                "space_complexity": "O(1)",
                "algorithm_type": "binary_search",
                "patterns": ["while_loop", "midpoint_calculation"],
                "confidence": 0.95
            },
            {
                "title": "Bubble Sort",
                "code": """
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
""",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "algorithm_type": "sorting",
                "patterns": ["nested_loops", "swapping"],
                "confidence": 0.95
            },
            {
                "title": "Fibonacci Recursive",
                "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
""",
                "time_complexity": "O(2ⁿ)",
                "space_complexity": "O(n)",
                "algorithm_type": "recursion",
                "patterns": ["recursive_call", "base_case"],
                "confidence": 0.95
            },
            {
                "title": "Merge Sort",
                "code": """
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
""",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "algorithm_type": "divide_conquer",
                "patterns": ["recursive_call", "merging", "divide"],
                "confidence": 0.95
            }
        ]
        
        samples = []
        for item in leetcode_data:
            sample = CodeSample(
                code=item["code"].strip(),
                language="python",
                time_complexity=item["time_complexity"],
                space_complexity=item["space_complexity"],
                algorithm_type=item["algorithm_type"],
                patterns=item["patterns"],
                confidence=item["confidence"],
                source="leetcode"
            )
            samples.append(sample)
        
        print(f"✅ Collected {len(samples)} samples from LeetCode")
        return samples
    
    def collect_from_github(self) -> List[CodeSample]:
        """Collect code samples from GitHub repositories"""
        print("🔍 Collecting data from GitHub...")
        
        # GitHub algorithm repositories with known complexities
        github_samples = [
            {
                "title": "Quick Sort",
                "code": """
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)
""",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(log n)",
                "algorithm_type": "sorting",
                "patterns": ["recursive_call", "pivot_selection", "partitioning"],
                "confidence": 0.95
            },
            {
                "title": "Depth First Search",
                "code": """
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    print(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
""",
                "time_complexity": "O(V + E)",
                "space_complexity": "O(V)",
                "algorithm_type": "graph_traversal",
                "patterns": ["recursive_call", "visited_set", "graph_iteration"],
                "confidence": 0.95
            }
        ]
        
        samples = []
        for item in github_samples:
            sample = CodeSample(
                code=item["code"].strip(),
                language="python",
                time_complexity=item["time_complexity"],
                space_complexity=item["space_complexity"],
                algorithm_type=item["algorithm_type"],
                patterns=item["patterns"],
                confidence=item["confidence"],
                source="github"
            )
            samples.append(sample)
        
        print(f"✅ Collected {len(samples)} samples from GitHub")
        return samples
    
    def collect_from_textbooks(self) -> List[CodeSample]:
        """Collect code samples from algorithm textbooks"""
        print("🔍 Collecting data from textbooks...")
        
        textbook_samples = [
            {
                "title": "Dijkstra's Algorithm",
                "code": """
import heapq

def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances
""",
                "time_complexity": "O((V + E) log V)",
                "space_complexity": "O(V)",
                "algorithm_type": "shortest_path",
                "patterns": ["priority_queue", "graph_iteration", "heap_operations"],
                "confidence": 0.95
            },
            {
                "title": "Dynamic Programming - Fibonacci",
                "code": """
def fibonacci_dp(n):
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    
    return dp[n]
""",
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "algorithm_type": "dynamic_programming",
                "patterns": ["single_loop", "memoization", "array_access"],
                "confidence": 0.95
            }
        ]
        
        samples = []
        for item in textbook_samples:
            sample = CodeSample(
                code=item["code"].strip(),
                language="python",
                time_complexity=item["time_complexity"],
                space_complexity=item["space_complexity"],
                algorithm_type=item["algorithm_type"],
                patterns=item["patterns"],
                confidence=item["confidence"],
                source="textbook"
            )
            samples.append(sample)
        
        print(f"✅ Collected {len(samples)} samples from textbooks")
        return samples
    
    def extract_features(self, sample: CodeSample) -> Dict[str, Any]:
        """Extract features from code sample for ML training"""
        features = {
            'code_length': len(sample.code),
            'line_count': sample.code.count('\n'),
            'function_count': sample.code.count('def '),
            'loop_count': sample.code.count('for ') + sample.code.count('while '),
            'recursion_count': sample.code.count('(') - sample.code.count(')'),
            'data_structure_count': sum([
                sample.code.count('[]'), sample.code.count('{}'),
                sample.code.count('list'), sample.code.count('dict'),
                sample.code.count('set'), sample.code.count('heap')
            ]),
            'complexity_keywords': {
                'linear': sample.code.count('range('),
                'quadratic': sample.code.count('for ') * sample.code.count('for '),
                'logarithmic': sample.code.count('// 2') + sample.code.count('>> 1'),
                'exponential': sample.code.count('return') * sample.code.count('(')
            }
        }
        
        # AST-based features
        try:
            tree = ast.parse(sample.code)
            features['ast_depth'] = self._get_ast_depth(tree)
            features['ast_node_count'] = len(list(ast.walk(tree)))
        except:
            features['ast_depth'] = 0
            features['ast_node_count'] = 0
        
        return features
    
    def _get_ast_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calculate the maximum depth of AST"""
        max_depth = current_depth
        for child in ast.iter_child_nodes(node):
            max_depth = max(max_depth, self._get_ast_depth(child, current_depth + 1))
        return max_depth
    
    def save_dataset(self, filename: str = "ml_dataset.json"):
        """Save collected dataset to file"""
        dataset = []
        
        for sample in self.samples:
            features = self.extract_features(sample)
            dataset.append({
                'code': sample.code,
                'language': sample.language,
                'time_complexity': sample.time_complexity,
                'space_complexity': sample.space_complexity,
                'algorithm_type': sample.algorithm_type,
                'patterns': sample.patterns,
                'confidence': sample.confidence,
                'source': sample.source,
                'features': features
            })
        
        with open(filename, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        print(f"✅ Saved {len(dataset)} samples to {filename}")
    
    def collect_all(self):
        """Collect data from all sources"""
        print("🚀 Starting data collection...")
        
        self.samples.extend(self.collect_from_leetcode())
        self.samples.extend(self.collect_from_github())
        self.samples.extend(self.collect_from_textbooks())
        
        print(f"🎉 Total samples collected: {len(self.samples)}")
        self.save_dataset()

if __name__ == "__main__":
    collector = DataCollector()
    collector.collect_all() 