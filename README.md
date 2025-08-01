# ⏱️ TimeComplexity Analyzer - Chrome Extension

A powerful Chrome extension that analyzes time and space complexity of code using AI and machine learning. Works on 30+ coding platforms automatically!

## 🚀 Features

- **🤖 ML-Enhanced Analysis**: 90-95% accuracy using ensemble machine learning models
- **🌐 Universal Compatibility**: Works on 30+ coding platforms automatically
- **🎯 Selection-Based Analysis**: Select any code on any webpage for instant analysis
- **🎨 Beautiful UI**: Modern glass morphism design with smooth animations
- **📊 Detailed Insights**: Time complexity, space complexity, breakdown, and optimization suggestions
- **⚡ Real-time Analysis**: Instant results with confidence scores
- **🔧 Multiple Input Methods**: Selection, page extraction, or manual input

## 📋 Prerequisites

Before installing the extension, you need to set up the backend server:

### 1. Python Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. ML Environment Setup (Optional but Recommended)
```bash
# Create ML virtual environment
python3 -m venv ml_venv
source ml_venv/bin/activate  # On Windows: ml_venv\Scripts\activate

# Install ML dependencies
pip install -r ml_integration/requirements_ml.txt

# Set up ML models (this will take a few minutes)
cd ml_integration
python setup_ml.py
```

## 🔧 Installation

### Method 1: Load Unpacked Extension (Recommended)

1. **Download/Clone the Repository**
   ```bash
   git clone <repository-url>
   cd extension_1
   ```

2. **Start the Backend Server**
   ```bash
   # Activate your virtual environment
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Start the FastAPI server
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Load Extension in Chrome**
   - Open Chrome and go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top-right)
   - Click "Load unpacked"
   - Select the `extension_1` folder
   - The extension should now appear in your extensions list

4. **Verify Installation**
   - Look for "TimeComplexity Analyzer" in your extensions
   - The extension icon should appear in your Chrome toolbar
   - Click the icon to open the popup

### Method 2: Build and Install

1. **Build the Extension**
   ```bash
   # Install build tools (if needed)
   npm install -g webpack webpack-cli
   
   # Build the extension
   npm run build
   ```

2. **Follow steps 3-4 from Method 1**

## 🎯 Usage

### Primary Method: Selection-Based Analysis (Recommended)

1. **Visit any coding platform** (LeetCode, Codeforces, HackerRank, etc.)
2. **Select/highlight any code** on the page
3. **Click the floating "⏱️ Analyze TC" button** (appears in top-right corner)
4. **View beautiful analysis results** in the modal popup

### Alternative Methods

#### Method 1: Popup Interface
1. **Click the extension icon** in Chrome toolbar
2. **Choose input method**:
   - **Paste code** directly into textarea
   - **Click "📋 Extract from Page"** to auto-extract from coding platforms
3. **Click "🔍 Analyze Code"** to get results

#### Method 2: Keyboard Shortcut
- **Press `Ctrl+Shift+A`** (Windows/Linux) or `Cmd+Shift+A` (Mac)
- **Select code** and press Enter
- **View analysis results**

## 🌐 Supported Platforms

The extension works automatically on 30+ coding platforms:

### 🏆 Major Platforms
- **LeetCode** - `leetcode.com`
- **Codeforces** - `codeforces.com`
- **HackerRank** - `hackerrank.com`
- **CodeChef** - `codechef.com`
- **GeeksforGeeks** - `geeksforgeeks.org`
- **InterviewBit** - `interviewbit.com`

### 📚 Learning Platforms
- **Coding Ninjas** - `codingninjas.com`
- **Codewars** - `codewars.com`
- **Exercism** - `exercism.io`
- **Project Euler** - `projecteuler.net`

### 🌍 Regional Platforms
- **AtCoder** - `atcoder.jp` (Japan)
- **SPOJ** - `spoj.com` (International)
- **Beecrowd** - `beecrowd.com.br` (Brazil)
- **Luogu** - `luogu.com.cn` (China)
- **And 20+ more platforms...**

## 🎨 Features Overview

### 🤖 ML-Enhanced Analysis
- **Ensemble Learning**: Combines Random Forest, Gradient Boosting, and Neural Networks
- **90-95% Accuracy**: Highly accurate complexity predictions
- **Confidence Scores**: Shows how confident the model is in its prediction
- **Algorithm Detection**: Identifies algorithm types (sorting, searching, etc.)

### 🎯 Smart Code Extraction
- **Selection-Based**: Works on any selected code
- **Platform-Specific**: Optimized extraction for each coding platform
- **Language Detection**: Automatic language identification
- **Fallback Methods**: Multiple extraction strategies for reliability

### 🎨 Beautiful Interface
- **Glass Morphism Design**: Modern, professional appearance
- **Smooth Animations**: Entrance and hover effects
- **Responsive Layout**: Works on all screen sizes
- **Professional Modal**: Beautiful analysis results display

## 🔧 Configuration

### Backend Configuration

The extension connects to a local FastAPI server. Make sure:

1. **Server is running** on `http://localhost:8000`
2. **CORS is enabled** (already configured)
3. **ML models are loaded** (if using ML-enhanced analysis)

### Extension Settings

- **ML Toggle**: Enable/disable ML-enhanced analysis in popup
- **Language Selection**: Choose programming language for analysis
- **Auto-save**: Code input is automatically saved between sessions

## 🧪 Testing

### Test the Extension

1. **Start the backend server**
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Test on different platforms**
   - Visit LeetCode and select some code
   - Try Codeforces problems
   - Test on GeeksforGeeks practice problems

3. **Test different code types**
   - Sorting algorithms (QuickSort, MergeSort)
   - Searching algorithms (Binary Search)
   - Dynamic programming solutions
   - Graph algorithms

### Sample Test Cases

```python
# QuickSort - Should show O(n log n)
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
```

```cpp
// Binary Search - Should show O(log n)
int binarySearch(vector<int>& arr, int target) {
    int left = 0, right = arr.size() - 1;
    while (left <= right) {
        int mid = (left + right) / 2;
        if (arr[mid] == target) return mid;
        if (arr[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
```

## 🐛 Troubleshooting

### Common Issues

1. **Extension not working**
   - Make sure backend server is running on port 8000
   - Check Chrome console for errors
   - Verify extension is loaded in Chrome

2. **"Could not establish connection" error**
   - Backend server is not running
   - Check if server is on correct port (8000)
   - Verify CORS settings

3. **No code found on page**
   - Try selecting code manually
   - Use the popup's "Extract from Page" button
   - Check if you're on a supported platform

4. **ML analysis not working**
   - Ensure ML environment is set up
   - Check if ML models are loaded
   - Verify ML dependencies are installed

### Debug Mode

Enable debug mode by:
1. Opening Chrome DevTools
2. Going to Console tab
3. Looking for extension logs
4. Check for any error messages

## 📁 Project Structure

```
extension_1/
├── manifest.json              # Extension configuration
├── popup.html                 # Extension popup interface
├── popup.css                  # Popup styling
├── popup.js                   # Popup functionality
├── content.js                 # Content script for web pages
├── background.js              # Background service worker
├── backend/                   # Python backend
│   ├── main.py               # FastAPI application
│   ├── analyzer.py           # Core analysis logic
│   └── ml_integration.py     # ML integration
├── ml_integration/           # Machine learning components
│   ├── setup_ml.py          # ML setup script
│   ├── ml_models.py         # ML model definitions
│   └── requirements_ml.txt  # ML dependencies
├── icons/                    # Extension icons
└── requirements.txt          # Python dependencies
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI** for the backend framework
- **Chrome Extensions API** for the extension functionality
- **Machine Learning libraries** for enhanced analysis
- **Coding platforms** for providing great learning resources

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section** above
2. **Look at the documentation** in the project files
3. **Open an issue** on the repository
4. **Check the console logs** for error messages

## 🎉 Getting Started

1. **Set up the backend** (follow prerequisites)
2. **Load the extension** in Chrome
3. **Visit any coding platform**
4. **Select some code and click the floating button**
5. **Enjoy beautiful, accurate complexity analysis!**

---

**Happy Coding! 🚀**

*The TimeComplexity Analyzer makes understanding algorithm complexity easy and beautiful.* 