#!/usr/bin/env python3
"""
ML-Enhanced TimeComplexity Analyzer Demo
Demonstrates the power of ML-enhanced complexity analysis
"""

import requests
import json
import time

def test_ml_analysis():
    """Test ML-enhanced analysis with various algorithms"""
    
    # Test cases with known complexities
    test_cases = [
        {
            "name": "Two Sum (Hash Table)",
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
            "expected_time": "O(n)",
            "expected_space": "O(n)"
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
            "expected_time": "O(log n)",
            "expected_space": "O(1)"
        },
        {
            "name": "Merge Sort",
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
            "expected_time": "O(n log n)",
            "expected_space": "O(n)"
        },
        {
            "name": "Fibonacci Recursive",
            "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
""",
            "expected_time": "O(2ⁿ)",
            "expected_space": "O(n)"
        }
    ]
    
    print("🚀 ML-Enhanced TimeComplexity Analyzer Demo")
    print("=" * 60)
    
    # Test regular analysis
    print("\n📊 Testing Regular Analysis:")
    print("-" * 30)
    
    for test_case in test_cases:
        print(f"\n🔍 {test_case['name']}")
        
        # Regular analysis
        try:
            response = requests.post(
                "http://localhost:8000/analyze",
                json={
                    "code": test_case["code"],
                    "language": "python"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ⏱️ Time: {result['time_complexity']} (Expected: {test_case['expected_time']})")
                print(f"  💾 Space: {result['space_complexity']} (Expected: {test_case['expected_space']})")
                print(f"  📊 Confidence: {result.get('confidence', 'N/A')}")
            else:
                print(f"  ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Failed: {e}")
    
    # Test ML-enhanced analysis
    print("\n🤖 Testing ML-Enhanced Analysis:")
    print("-" * 30)
    
    for test_case in test_cases:
        print(f"\n🔍 {test_case['name']}")
        
        # ML-enhanced analysis
        try:
            response = requests.post(
                "http://localhost:8000/analyze-ml",
                json={
                    "code": test_case["code"],
                    "language": "python"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ⏱️ Time: {result['time_complexity']} (Expected: {test_case['expected_time']})")
                print(f"  💾 Space: {result['space_complexity']} (Expected: {test_case['expected_space']})")
                print(f"  🎯 Method: {result.get('analysis_method', 'N/A')}")
                print(f"  📊 Confidence: {result.get('ensemble_confidence', 'N/A')}")
                
                # Show ML insights
                if 'model_agreement' in result:
                    agreement = result['model_agreement']
                    if agreement.get('time_predictions'):
                        print(f"  🤖 ML Time Predictions: {agreement['time_predictions']}")
                    if agreement.get('space_predictions'):
                        print(f"  🤖 ML Space Predictions: {agreement['space_predictions']}")
            else:
                print(f"  ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Failed: {e}")
    
    print("\n🎉 Demo completed!")

if __name__ == "__main__":
    test_ml_analysis()
