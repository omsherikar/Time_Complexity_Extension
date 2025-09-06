class TimeComplexityAnalyzer {
    constructor() {
        this.apiUrl = 'https://time-complexity-extension-1.onrender.com/analyze';
        this.mlApiUrl = 'https://time-complexity-extension-1.onrender.com/analyze-ml';
        this.useML = true; // Default to ML-enhanced analysis
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadStoredData();
    }

    bindEvents() {
        document.getElementById('analyzeBtn').addEventListener('click', () => this.analyzeCode());
        document.getElementById('extractBtn').addEventListener('click', () => this.extractFromPage());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearAll());
        
        // ML toggle functionality
        const mlToggle = document.getElementById('mlToggle');
        if (mlToggle) {
            mlToggle.addEventListener('change', (e) => {
                this.useML = e.target.checked;
                chrome.storage.local.set({ 'useML': this.useML });
            });
        }
        
        // Auto-save code input
        document.getElementById('codeInput').addEventListener('input', (e) => {
            chrome.storage.local.set({ 'lastCode': e.target.value });
        });
    }

    async loadStoredData() {
        try {
            const result = await chrome.storage.local.get(['lastCode', 'lastLanguage', 'useML']);
            if (result.lastCode) {
                document.getElementById('codeInput').value = result.lastCode;
            }
            if (result.lastLanguage) {
                document.getElementById('language').value = result.lastLanguage;
            }
            if (result.useML !== undefined) {
                this.useML = result.useML;
                const mlToggle = document.getElementById('mlToggle');
                if (mlToggle) {
                    mlToggle.checked = this.useML;
                }
            }
        } catch (error) {
            console.error('Error loading stored data:', error);
        }
    }

    async analyzeCode() {
        const code = document.getElementById('codeInput').value.trim();
        const language = document.getElementById('language').value;

        if (!code) {
            this.showError('Please enter some code to analyze.');
            return;
        }

        this.showLoading();
        this.hideError();
        this.hideResults();

        try {
            // Store current state
            chrome.storage.local.set({ 
                'lastCode': code, 
                'lastLanguage': language 
            });

            // Choose API endpoint based on ML toggle
            const apiUrl = this.useML ? this.mlApiUrl : this.apiUrl;
            const analysisType = this.useML ? 'ML-Enhanced' : 'Regular';

            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: code,
                    language: language
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            this.displayResults(result, analysisType);
        } catch (error) {
            console.error('Analysis error:', error);
            let errorMessage = 'Analysis failed. ';
            
            if (error.message.includes('Failed to fetch')) {
                errorMessage += 'Network error - check your internet connection and try again.';
            } else if (error.message.includes('CORS')) {
                errorMessage += 'CORS error - the API server may be down.';
            } else if (error.message.includes('HTTP error')) {
                errorMessage += `Server error: ${error.message}`;
            } else {
                errorMessage += `${error.message}`;
            }
            
            this.showError(errorMessage);
        } finally {
            this.hideLoading();
        }
    }

    async extractFromPage() {
        try {
            const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
            
            // Try to use the content script's extraction method
            try {
                const response = await chrome.tabs.sendMessage(tab.id, { action: 'extractCode' });
                if (response && response.code) {
                    document.getElementById('codeInput').value = response.code;
                    if (response.language) {
                        document.getElementById('language').value = response.language;
                    }
                    this.showSuccess('Code extracted successfully! Click "Analyze Complexity" to proceed.');
                    return;
                }
            } catch (contentScriptError) {
                console.log('Content script not available, trying fallback extraction...');
            }
            
            // Fallback to popup's extraction method
            const result = await chrome.scripting.executeScript({
                target: { tabId: tab.id },
                function: this.extractCodeFromPage
            });

            if (result[0].result) {
                const { code, language } = result[0].result;
                document.getElementById('codeInput').value = code;
                if (language) {
                    document.getElementById('language').value = language;
                }
                this.showSuccess('Code extracted successfully! Click "Analyze Complexity" to proceed.');
            } else {
                this.showError('No code found on this page. Use the floating "⏱️ Analyze TC" button instead, or make sure you\'re on a supported coding platform.');
            }
        } catch (error) {
            console.error('Extraction error:', error);
            this.showError('Failed to extract code from page. Use the floating "⏱️ Analyze TC" button instead, or make sure you\'re on a supported platform.');
        }
    }



    extractCodeFromPage() {
        const url = window.location.href;
        let code = '';
        let language = '';

        // LeetCode
        if (url.includes('leetcode.com')) {
            const editor = document.querySelector('.monaco-editor');
            if (editor) {
                const textarea = editor.querySelector('textarea');
                if (textarea) {
                    code = textarea.value;
                }
            }
            
            // Try alternative selectors
            if (!code) {
                const codeBlocks = document.querySelectorAll('pre code');
                if (codeBlocks.length > 0) {
                    code = codeBlocks[0].textContent;
                }
            }

            // Detect language from LeetCode
            const langSelectors = {
                'python': '.language-python',
                'cpp': '.language-cpp',
                'java': '.language-java',
                'javascript': '.language-javascript'
            };

            for (const [lang, selector] of Object.entries(langSelectors)) {
                if (document.querySelector(selector)) {
                    language = lang;
                    break;
                }
            }
        }
        
        // Codeforces
        else if (url.includes('codeforces.com')) {
            const codeBlocks = document.querySelectorAll('.program-source');
            if (codeBlocks.length > 0) {
                code = codeBlocks[0].textContent;
            }
        }
        
        // GeeksforGeeks
        else if (url.includes('geeksforgeeks.org')) {
            const codeBlocks = document.querySelectorAll('.code-container pre');
            if (codeBlocks.length > 0) {
                code = codeBlocks[0].textContent;
            }
        }
        
        // HackerRank
        else if (url.includes('hackerrank.com')) {
            const editor = document.querySelector('.monaco-editor');
            if (editor) {
                const textarea = editor.querySelector('textarea');
                if (textarea) {
                    code = textarea.value;
                }
            }
        }

        return code ? { code: code.trim(), language } : null;
    }

    displayResults(result, analysisType = 'Regular') {
        // Update analysis type indicator
        const analysisTypeElement = document.getElementById('analysisType');
        if (analysisTypeElement) {
            analysisTypeElement.textContent = analysisType;
            analysisTypeElement.className = analysisType === 'ML-Enhanced' ? 'ml-enhanced' : 'regular';
        }

        document.getElementById('timeComplexity').textContent = result.time_complexity || 'Unknown';
        document.getElementById('spaceComplexity').textContent = result.space_complexity || 'Unknown';
        
        // Display confidence score
        const confidenceElement = document.getElementById('confidence');
        if (confidenceElement) {
            const confidence = result.ensemble_confidence || result.confidence || 'N/A';
            confidenceElement.textContent = `Confidence: ${confidence}`;
        }

        // Display analysis method
        const methodElement = document.getElementById('analysisMethod');
        if (methodElement && result.analysis_method) {
            methodElement.textContent = `Method: ${result.analysis_method}`;
        }
        
        const breakdown = document.getElementById('analysisBreakdown');
        if (result.breakdown) {
            breakdown.innerHTML = `
                <ul>
                    ${result.breakdown.map(item => `<li>${item}</li>`).join('')}
                </ul>
            `;
        } else {
            breakdown.innerHTML = '<p>No detailed breakdown available.</p>';
        }

        const suggestions = document.getElementById('suggestions');
        if (result.suggestions && result.suggestions.length > 0) {
            suggestions.innerHTML = `
                <ul>
                    ${result.suggestions.map(suggestion => `<li>${suggestion}</li>`).join('')}
                </ul>
            `;
        } else {
            suggestions.innerHTML = '<p>No optimization suggestions available.</p>';
        }

        // Display ML-specific information
        if (analysisType === 'ML-Enhanced' && result.model_agreement) {
            this.displayMLInsights(result.model_agreement);
        }

        this.showResults();
    }

    displayMLInsights(modelAgreement) {
        const mlInsightsElement = document.getElementById('mlInsights');
        if (!mlInsightsElement) return;

        let insightsHTML = '<h4>🤖 ML Model Insights</h4>';
        
        if (modelAgreement.time_predictions) {
            insightsHTML += '<p><strong>Time Complexity Predictions:</strong></p><ul>';
            Object.entries(modelAgreement.time_predictions).forEach(([complexity, count]) => {
                insightsHTML += `<li>${complexity}: ${count} model(s)</li>`;
            });
            insightsHTML += '</ul>';
        }

        if (modelAgreement.space_predictions) {
            insightsHTML += '<p><strong>Space Complexity Predictions:</strong></p><ul>';
            Object.entries(modelAgreement.space_predictions).forEach(([complexity, count]) => {
                insightsHTML += `<li>${complexity}: ${count} model(s)</li>`;
            });
            insightsHTML += '</ul>';
        }

        mlInsightsElement.innerHTML = insightsHTML;
        mlInsightsElement.style.display = 'block';
    }

    clearAll() {
        document.getElementById('codeInput').value = '';
        this.hideResults();
        this.hideError();
        chrome.storage.local.remove(['lastCode', 'lastLanguage']);
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    showResults() {
        document.getElementById('resultsSection').style.display = 'block';
    }

    hideResults() {
        document.getElementById('resultsSection').style.display = 'none';
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('error').style.display = 'block';
    }

    hideError() {
        document.getElementById('error').style.display = 'none';
    }

    showSuccess(message) {
        // Create a temporary success message
        const successDiv = document.createElement('div');
        successDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #d4edda;
            color: #155724;
            padding: 12px 16px;
            border-radius: 6px;
            border: 1px solid #c3e6cb;
            font-size: 12px;
            z-index: 1000;
            animation: slideIn 0.3s ease;
        `;
        successDiv.textContent = message;
        document.body.appendChild(successDiv);

        setTimeout(() => {
            successDiv.remove();
        }, 3000);
    }
}

// Add CSS for success animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
`;
document.head.appendChild(style);

// Initialize the analyzer when the popup loads
document.addEventListener('DOMContentLoaded', () => {
    new TimeComplexityAnalyzer();
}); 