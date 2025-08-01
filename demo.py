#!/usr/bin/env python3
"""
Demo script for TimeComplexity Analyzer
Shows the complete functionality of the Chrome extension and backend
"""

import requests
import json
import time

def test_api_endpoint():
    """Test the API endpoint with various code examples"""
    
    print("🚀 TimeComplexity Analyzer Demo")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        {
            "name": "Simple Loop",
            "language": "python",
            "code": """
def simple_loop(n):
    for i in range(n):
        print(i)
""",
            "expected": "O(n)"
        },
        {
            "name": "Nested Loops",
            "language": "python", 
            "code": """
def nested_loops(n):
    for i in range(n):
        for j in range(n):
            print(i, j)
""",
            "expected": "O(n²)"
        },
        {
            "name": "Fibonacci Recursion",
            "language": "python",
            "code": """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
""",
            "expected": "O(2ⁿ)"
        },
        {
            "name": "C++ For Loop",
            "language": "cpp",
            "code": """
#include <iostream>
using namespace std;

int main() {
    int n = 10;
    for(int i = 0; i < n; i++) {
        cout << i << endl;
    }
    return 0;
}
""",
            "expected": "O(n)"
        }
    ]
    
    print("📊 Testing API Endpoint")
    print("-" * 30)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Expected: {test_case['expected']}")
        
        try:
            response = requests.post(
                "http://localhost:8000/analyze",
                headers={"Content-Type": "application/json"},
                json={
                    "code": test_case["code"],
                    "language": test_case["language"]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Actual: {result['time_complexity']}")
                print(f"   📈 Confidence: {result['confidence']:.2f}")
                
                if result['breakdown']:
                    print(f"   📝 Breakdown:")
                    for item in result['breakdown']:
                        print(f"      • {item}")
                
                if result['suggestions']:
                    print(f"   💡 Suggestions:")
                    for suggestion in result['suggestions']:
                        print(f"      • {suggestion}")
                
                # Check if prediction matches expected
                if test_case['expected'] in result['time_complexity']:
                    print(f"   🎯 Prediction: CORRECT")
                else:
                    print(f"   ⚠️  Prediction: {result['time_complexity']} (expected {test_case['expected']})")
                    
            else:
                print(f"   ❌ Error: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Connection error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
        
        print()

def show_extension_features():
    """Show the Chrome extension features"""
    
    print("🔧 Chrome Extension Features")
    print("-" * 30)
    
    features = [
        "✅ Modern popup interface with gradient design",
        "✅ Multi-platform code extraction (LeetCode, Codeforces, etc.)",
        "✅ Floating analysis button on coding platforms",
        "✅ Automatic language detection",
        "✅ Real-time analysis without page navigation",
        "✅ Detailed breakdown and optimization suggestions",
        "✅ Context menu integration",
        "✅ Background service worker for state management"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print("\n🎯 Supported Platforms:")
    platforms = ["LeetCode", "Codeforces", "GeeksforGeeks", "HackerRank"]
    for platform in platforms:
        print(f"   • {platform}")
    
    print("\n🔤 Supported Languages:")
    languages = ["Python (AST parsing)", "C++ (Pattern matching)", "Java (Pattern matching)", "JavaScript (Pattern matching)"]
    for lang in languages:
        print(f"   • {lang}")

def show_usage_instructions():
    """Show usage instructions"""
    
    print("\n📖 Usage Instructions")
    print("-" * 30)
    
    print("1. 🚀 Start the Backend Server:")
    print("   python start_server.py")
    print("   # Server runs on http://localhost:8000")
    
    print("\n2. 🔧 Load Chrome Extension:")
    print("   - Open Chrome → chrome://extensions/")
    print("   - Enable 'Developer mode'")
    print("   - Click 'Load unpacked' → Select this directory")
    
    print("\n3. 🧪 Test the Extension:")
    print("   Method 1 - Popup Interface:")
    print("   - Click extension icon in toolbar")
    print("   - Select language and paste code")
    print("   - Click 'Analyze Complexity'")
    
    print("\n   Method 2 - Floating Button:")
    print("   - Visit a supported coding platform")
    print("   - Look for '⏱️ Analyze TC' button")
    print("   - Click for instant analysis")
    
    print("\n   Method 3 - Context Menu:")
    print("   - Select code on any webpage")
    print("   - Right-click → 'Analyze Time Complexity'")

def main():
    """Main demo function"""
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print("❌ Backend server is not responding properly")
            return
    except requests.exceptions.RequestException:
        print("❌ Backend server is not running")
        print("   Please start it with: python start_server.py")
        return
    
    # Run demo
    test_api_endpoint()
    show_extension_features()
    show_usage_instructions()
    
    print("\n🎉 Demo completed!")
    print("\n💡 Next steps:")
    print("   1. Load the extension in Chrome")
    print("   2. Visit a coding platform")
    print("   3. Try the floating analysis button")
    print("   4. Test with your own code")

if __name__ == "__main__":
    main() 