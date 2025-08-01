#!/usr/bin/env python3
"""
ML Setup Script for TimeComplexity Analyzer
Sets up the ML environment, collects data, trains models, and integrates with the main analyzer
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required for ML features")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_virtual_environment():
    """Set up virtual environment for ML dependencies"""
    print("🔧 Setting up ML virtual environment...")
    
    venv_path = Path("../ml_venv")
    if venv_path.exists():
        print("✅ ML virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "../ml_venv"], check=True)
        print("✅ ML virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_ml_dependencies():
    """Install ML-specific dependencies"""
    print("📦 Installing ML dependencies...")
    
    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = "../ml_venv/Scripts/pip"
    else:  # Unix/Linux/macOS
        pip_path = "../ml_venv/bin/pip"
    
    try:
        # Upgrade pip first
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
        
        # Install ML requirements
        subprocess.run([pip_path, "install", "-r", "requirements_ml.txt"], check=True)
        print("✅ ML dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install ML dependencies: {e}")
        return False

def collect_training_data():
    """Collect training data for ML models"""
    print("📊 Collecting training data...")
    
    # Determine python path
    if os.name == 'nt':  # Windows
        python_path = "../ml_venv/Scripts/python"
    else:  # Unix/Linux/macOS
        python_path = "../ml_venv/bin/python"
    
    try:
        subprocess.run([python_path, "data_collector.py"], check=True)
        print("✅ Training data collected successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to collect training data: {e}")
        return False

def train_ml_models():
    """Train ML models"""
    print("🤖 Training ML models...")
    
    # Determine python path
    if os.name == 'nt':  # Windows
        python_path = "../ml_venv/Scripts/python"
    else:  # Unix/Linux/macOS
        python_path = "../ml_venv/bin/python"
    
    try:
        subprocess.run([python_path, "ml_models.py"], check=True)
        print("✅ ML models trained successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to train ML models: {e}")
        return False

def test_hybrid_analyzer():
    """Test the hybrid analyzer"""
    print("🧪 Testing hybrid analyzer...")
    
    # Determine python path
    if os.name == 'nt':  # Windows
        python_path = "../ml_venv/Scripts/python"
    else:  # Unix/Linux/macOS
        python_path = "../ml_venv/bin/python"
    
    try:
        subprocess.run([python_path, "hybrid_analyzer.py"], check=True)
        print("✅ Hybrid analyzer test completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to test hybrid analyzer: {e}")
        return False

def integrate_with_main_analyzer():
    """Integrate ML models with the main analyzer"""
    print("🔗 Integrating ML with main analyzer...")
    
    # Create integration script
    integration_code = '''#!/usr/bin/env python3
"""
ML Integration for TimeComplexity Analyzer Backend
Integrates ML models with the main FastAPI backend
"""

import os
import sys
from pathlib import Path

# Add ML integration to path
ml_path = Path(__file__).parent / "ml_integration"
sys.path.append(str(ml_path))

try:
    from hybrid_analyzer import HybridTimeComplexityAnalyzer
    
    # Initialize hybrid analyzer with ML models
    ml_models_path = "ml_integration/ml_models.pkl"
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
        from backend.analyzer import TimeComplexityAnalyzer
        analyzer = TimeComplexityAnalyzer()
        return analyzer.analyze(code, language)
'''
    
    # Write integration script
    with open("../backend/ml_integration.py", "w") as f:
        f.write(integration_code)
    
    print("✅ ML integration script created")
    return True

def update_main_analyzer():
    """Update the main analyzer to use ML when available"""
    print("🔄 Updating main analyzer...")
    
    # Read current analyzer
    with open("../backend/main.py", "r") as f:
        content = f.read()
    
    # Add ML import and integration
    ml_import = '''
# ML Integration
try:
    from .ml_integration import analyze_with_ml, ML_AVAILABLE
    print(f"🤖 ML Integration: {'Available' if ML_AVAILABLE else 'Not Available'}")
except ImportError:
    print("⚠️ ML Integration not available")
    ML_AVAILABLE = False
    analyze_with_ml = None
'''
    
    # Add ML-enhanced analyze endpoint
    ml_endpoint = '''
@app.post("/analyze-ml")
async def analyze_with_ml_endpoint(request: AnalysisRequest):
    """Analyze code using ML-enhanced approach"""
    try:
        if analyze_with_ml:
            result = analyze_with_ml(request.code, request.language)
            return result
        else:
            # Fallback to regular analysis
            analyzer = TimeComplexityAnalyzer()
            return analyzer.analyze(request.code, request.language)
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}
'''
    
    # Insert ML import after existing imports
    if "ML Integration" not in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('from .analyzer import'):
                lines.insert(i + 1, ml_import)
                break
        content = '\n'.join(lines)
    
    # Add ML endpoint before the last line
    if "analyze-ml" not in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.strip() == 'if __name__ == "__main__":':
                lines.insert(i, ml_endpoint)
                break
        content = '\n'.join(lines)
    
    # Write updated content
    with open("../backend/main.py", "w") as f:
        f.write(content)
    
    print("✅ Main analyzer updated with ML integration")
    return True

def create_ml_demo():
    """Create a demo script for ML features"""
    demo_code = '''#!/usr/bin/env python3
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
    print("\\n📊 Testing Regular Analysis:")
    print("-" * 30)
    
    for test_case in test_cases:
        print(f"\\n🔍 {test_case['name']}")
        
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
    print("\\n🤖 Testing ML-Enhanced Analysis:")
    print("-" * 30)
    
    for test_case in test_cases:
        print(f"\\n🔍 {test_case['name']}")
        
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
    
    print("\\n🎉 Demo completed!")

if __name__ == "__main__":
    test_ml_analysis()
'''
    
    with open("../ml_demo.py", "w") as f:
        f.write(demo_code)
    
    print("✅ ML demo script created")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up ML-Enhanced TimeComplexity Analyzer")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Setup virtual environment
    if not setup_virtual_environment():
        return False
    
    # Install dependencies
    if not install_ml_dependencies():
        return False
    
    # Collect training data
    if not collect_training_data():
        return False
    
    # Train models
    if not train_ml_models():
        return False
    
    # Test hybrid analyzer
    if not test_hybrid_analyzer():
        return False
    
    # Integrate with main analyzer
    if not integrate_with_main_analyzer():
        return False
    
    # Update main analyzer
    if not update_main_analyzer():
        return False
    
    # Create demo
    if not create_ml_demo():
        return False
    
    print("\n🎉 ML setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the backend server: python start_server.py")
    print("2. Run the ML demo: python ml_demo.py")
    print("3. Load the Chrome extension and test ML-enhanced analysis")
    print("4. Visit http://localhost:8000/docs for API documentation")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 