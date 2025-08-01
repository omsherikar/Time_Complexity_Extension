// Content script for TimeComplexity Analyzer
// This script runs on coding platforms to extract code and provide additional features

class ContentScript {
    constructor() {
        this.init();
    }

    init() {
        this.setupMessageListener();
        this.injectAnalysisButton();
        this.observePageChanges();
    }

    setupMessageListener() {
        chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
            if (request.action === 'extractCode') {
                const result = this.extractCode();
                sendResponse(result);
            } else if (request.action === 'getSelectedCode') {
                const result = this.getSelectedCode();
                sendResponse(result);
            }
        });
    }

    injectAnalysisButton() {
        // Add a floating analysis button to coding platforms
        const button = document.createElement('button');
        button.id = 'tc-analyzer-btn';
        button.innerHTML = '⏱️ Analyze TC';
        button.title = 'Click to analyze selected code or current page code';
        button.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
        `;

        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-2px)';
            button.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.2)';
        });

        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0)';
            button.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
        });

        button.addEventListener('click', () => {
            // First try to get selected code, then fall back to page extraction
            const selectedCode = this.getSelectedCode();
            if (selectedCode && selectedCode.code) {
                // Show language detection feedback
                this.showNotification(`Detected language: ${selectedCode.language.toUpperCase()}`, 'info');
                this.analyzeSelectedCode(selectedCode.code);
            } else {
                this.analyzeCurrentCode();
            }
        });

        document.body.appendChild(button);
    }

    observePageChanges() {
        // Watch for dynamic content changes (common in SPAs)
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    // Check if code editor elements were added
                    const hasCodeEditor = document.querySelector('.monaco-editor, .ace_editor, .CodeMirror');
                    if (hasCodeEditor && !document.getElementById('tc-analyzer-btn')) {
                        this.injectAnalysisButton();
                    }
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    extractCode() {
        const url = window.location.href;
        let code = '';
        let language = '';

        // LeetCode
        if (url.includes('leetcode.com')) {
            code = this.extractFromLeetCode();
            language = this.detectLeetCodeLanguage();
        }
        // Codeforces
        else if (url.includes('codeforces.com')) {
            code = this.extractFromCodeforces();
        }
        // GeeksforGeeks
        else if (url.includes('geeksforgeeks.org')) {
            code = this.extractFromGeeksforGeeks();
        }
        // HackerRank
        else if (url.includes('hackerrank.com')) {
            code = this.extractFromHackerRank();
        }

        return code ? { code: code.trim(), language } : null;
    }

    extractFromLeetCode() {
        // Try multiple selectors for LeetCode
        const selectors = [
            '.monaco-editor textarea',
            '.ace_editor textarea',
            '.CodeMirror textarea',
            '[data-cy="code-editor"] textarea',
            '.editor-content pre',
            'pre code',
            '.monaco-editor .view-lines',
            '.ace_content',
            '.CodeMirror-code'
        ];

        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element) {
                if (element.value) {
                    return element.value;
                } else if (element.textContent) {
                    return element.textContent;
                }
            }
        }

        // Try to get from Monaco editor instance
        if (window.monaco && window.monaco.editor) {
            const editors = window.monaco.editor.getModels();
            if (editors.length > 0) {
                return editors[0].getValue();
            }
        }

        // Try to get from Ace editor instance
        if (window.ace && window.ace.edit) {
            const editor = window.ace.edit(document.querySelector('.ace_editor'));
            if (editor) {
                return editor.getValue();
            }
        }

        // Try to get from CodeMirror instance
        if (window.CodeMirror) {
            const editor = document.querySelector('.CodeMirror');
            if (editor && editor.CodeMirror) {
                return editor.CodeMirror.getValue();
            }
        }

        return '';
    }

    detectLeetCodeLanguage() {
        const langSelectors = {
            'python': '.language-python, [data-lang="python"], [data-mode="python"]',
            'cpp': '.language-cpp, [data-lang="cpp"], [data-mode="cpp"]',
            'java': '.language-java, [data-lang="java"], [data-mode="java"]',
            'javascript': '.language-javascript, [data-lang="javascript"], [data-mode="javascript"]'
        };

        for (const [lang, selector] of Object.entries(langSelectors)) {
            if (document.querySelector(selector)) {
                return lang;
            }
        }

        // Try to detect from URL or page content
        const url = window.location.href;
        if (url.includes('python')) return 'python';
        if (url.includes('cpp') || url.includes('c++')) return 'cpp';
        if (url.includes('java')) return 'java';
        if (url.includes('javascript') || url.includes('js')) return 'javascript';

        // Try to detect from editor mode
        const editor = document.querySelector('.monaco-editor, .ace_editor, .CodeMirror');
        if (editor) {
            const mode = editor.getAttribute('data-mode') || editor.className;
            if (mode.includes('python')) return 'python';
            if (mode.includes('cpp') || mode.includes('c++')) return 'cpp';
            if (mode.includes('java')) return 'java';
            if (mode.includes('javascript') || mode.includes('js')) return 'javascript';
        }

        return '';
    }

    extractFromCodeforces() {
        const selectors = [
            '.program-source',
            '.source',
            'pre code',
            '.code pre',
            '.prettyprint',
            '.brush',
            '.programming-source'
        ];

        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element) {
                return element.textContent || element.innerText;
            }
        }

        // Try to find any code block
        const codeBlocks = document.querySelectorAll('pre, code');
        for (const block of codeBlocks) {
            if (block.textContent && block.textContent.length > 50) {
                return block.textContent;
            }
        }

        return '';
    }

    extractFromGeeksforGeeks() {
        const selectors = [
            '.code-container pre',
            '.program-source',
            'pre code',
            '.code pre',
            '.prettyprint',
            '.brush',
            '.programming-source',
            '.code-box'
        ];

        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element) {
                return element.textContent || element.innerText;
            }
        }

        // Try to find any code block
        const codeBlocks = document.querySelectorAll('pre, code');
        for (const block of codeBlocks) {
            if (block.textContent && block.textContent.length > 50) {
                return block.textContent;
            }
        }

        return '';
    }

    extractFromHackerRank() {
        const selectors = [
            '.monaco-editor textarea',
            '.ace_editor textarea',
            'pre code',
            '.editor-content pre'
        ];

        for (const selector of selectors) {
            const element = document.querySelector(selector);
            if (element && element.value) {
                return element.value;
            }
        }

        return '';
    }

    async analyzeCurrentCode() {
        const result = this.extractCode();
        
        if (!result || !result.code) {
            this.showNotification('No code found on this page', 'error');
            return;
        }

        try {
            // Use background script to make API call
            const response = await new Promise((resolve, reject) => {
                chrome.runtime.sendMessage({
                    action: 'analyzeCode',
                    code: result.code,
                    language: result.language || 'python',
                    useML: false
                }, (response) => {
                    if (chrome.runtime.lastError) {
                        reject(new Error(chrome.runtime.lastError.message));
                    } else if (response && response.success) {
                        resolve(response.data);
                    } else {
                        reject(new Error(response?.error || 'Analysis failed'));
                    }
                });
            });

            this.showAnalysisResults(response);
        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification('Analysis failed. Make sure the backend server is running.', 'error');
        }
    }

    showAnalysisResults(analysis) {
        // Create enhanced modal with modern design
        const modal = document.createElement('div');
        modal.id = 'tc-analysis-modal';
        modal.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            z-index: 10001;
            display: flex;
            align-items: center;
            justify-content: center;
            animation: modalFadeIn 0.3s ease-out;
        `;

        const content = document.createElement('div');
        content.style.cssText = `
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9));
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 0;
            max-width: 600px;
            width: 90%;
            max-height: 85vh;
            overflow: hidden;
            box-shadow: 
                0 25px 50px rgba(0, 0, 0, 0.25),
                0 0 0 1px rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            animation: modalSlideIn 0.4s ease-out;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        `;

        // Enhanced header with gradient
        const header = document.createElement('div');
        header.style.cssText = `
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 24px 30px;
            position: relative;
            overflow: hidden;
        `;

        header.innerHTML = `
            <div style="position: relative; z-index: 2;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h2 style="margin: 0; font-size: 22px; font-weight: 700; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">
                        ⏱️ Time Complexity Analysis
                    </h2>
                    <button onclick="this.closest('#tc-analysis-modal').remove()" 
                            style="background: rgba(255, 255, 255, 0.2); border: none; font-size: 18px; cursor: pointer; 
                                   color: white; width: 32px; height: 32px; border-radius: 50%; 
                                   display: flex; align-items: center; justify-content: center;
                                   transition: all 0.3s ease; backdrop-filter: blur(10px);">
                        ×
                    </button>
                </div>
                <p style="margin: 0; opacity: 0.9; font-size: 14px; font-weight: 500;">
                    AI-powered algorithm analysis with detailed insights
                </p>
            </div>
            <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; 
                        background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
                        animation: shimmer 3s ease-in-out infinite; z-index: 1;">
            </div>
        `;

        // Enhanced complexity cards
        const complexitySection = document.createElement('div');
        complexitySection.style.cssText = `
            padding: 30px;
            background: rgba(255, 255, 255, 0.5);
        `;

        const complexityGrid = document.createElement('div');
        complexityGrid.style.cssText = `
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        `;

        const timeCard = document.createElement('div');
        timeCard.style.cssText = `
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(102, 126, 234, 0.05));
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        `;
        timeCard.innerHTML = `
            <div style="font-size: 14px; color: #667eea; font-weight: 600; margin-bottom: 8px;">⏱️ Time Complexity</div>
            <div style="font-size: 20px; font-weight: 700; color: #667eea; background: rgba(102, 126, 234, 0.1); 
                        padding: 8px 16px; border-radius: 12px; display: inline-block;">
                ${analysis.time_complexity || 'Unknown'}
            </div>
        `;

        const spaceCard = document.createElement('div');
        spaceCard.style.cssText = `
            background: linear-gradient(135deg, rgba(118, 75, 162, 0.1), rgba(118, 75, 162, 0.05));
            border: 1px solid rgba(118, 75, 162, 0.2);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        `;
        spaceCard.innerHTML = `
            <div style="font-size: 14px; color: #764ba2; font-weight: 600; margin-bottom: 8px;">💾 Space Complexity</div>
            <div style="font-size: 20px; font-weight: 700; color: #764ba2; background: rgba(118, 75, 162, 0.1); 
                        padding: 8px 16px; border-radius: 12px; display: inline-block;">
                ${analysis.space_complexity || 'Unknown'}
            </div>
        `;

        complexityGrid.appendChild(timeCard);
        complexityGrid.appendChild(spaceCard);
        complexitySection.appendChild(complexityGrid);

        // Enhanced content sections
        const contentSection = document.createElement('div');
        contentSection.style.cssText = `
            padding: 0 30px 30px;
            max-height: 400px;
            overflow-y: auto;
        `;

        let contentHTML = '';

        if (analysis.breakdown && analysis.breakdown.length > 0) {
            contentHTML += `
                <div style="margin-bottom: 30px;">
                    <div style="display: flex; align-items: center; margin-bottom: 16px;">
                        <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; 
                                   width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; 
                                   justify-content: center; margin-right: 12px; font-size: 16px;">
                            🧠
                        </div>
                        <h3 style="margin: 0; color: #333; font-size: 18px; font-weight: 600;">Analysis Breakdown</h3>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.8); border-radius: 16px; padding: 20px; 
                               border: 1px solid rgba(225, 229, 233, 0.6); backdrop-filter: blur(10px);">
                        <ul style="margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.6; color: #555;">
                            ${analysis.breakdown.map(item => `<li style="margin-bottom: 8px;">${item}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `;
        }

        if (analysis.suggestions && analysis.suggestions.length > 0) {
            contentHTML += `
                <div>
                    <div style="display: flex; align-items: center; margin-bottom: 16px;">
                        <div style="background: linear-gradient(135deg, #4caf50, #45a049); color: white; 
                                   width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; 
                                   justify-content: center; margin-right: 12px; font-size: 16px;">
                            💡
                        </div>
                        <h3 style="margin: 0; color: #333; font-size: 18px; font-weight: 600;">Optimization Suggestions</h3>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.8); border-radius: 16px; padding: 20px; 
                               border: 1px solid rgba(225, 229, 233, 0.6); backdrop-filter: blur(10px);">
                        <ul style="margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.6; color: #555;">
                            ${analysis.suggestions.map(suggestion => `<li style="margin-bottom: 8px;">${suggestion}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `;
        }

        contentSection.innerHTML = contentHTML;

        // Add CSS animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes modalFadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes modalSlideIn {
                from { 
                    opacity: 0;
                    transform: translateY(30px) scale(0.95);
                }
                to { 
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }
            }
            @keyframes shimmer {
                0%, 100% { transform: translateX(-100%); }
                50% { transform: translateX(100%); }
            }
            #tc-analysis-modal button:hover {
                background: rgba(255, 255, 255, 0.3) !important;
                transform: scale(1.1);
            }
            #tc-analysis-modal .complexity-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            }
        `;
        document.head.appendChild(style);

        // Assemble modal
        content.appendChild(header);
        content.appendChild(complexitySection);
        content.appendChild(contentSection);
        modal.appendChild(content);
        document.body.appendChild(modal);

        // Enhanced close functionality
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.animation = 'modalFadeIn 0.3s ease-out reverse';
                content.style.animation = 'modalSlideIn 0.3s ease-out reverse';
                setTimeout(() => modal.remove(), 300);
            }
        });

        // Add hover effects
        [timeCard, spaceCard].forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-2px)';
                card.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.15)';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = 'none';
            });
        });
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 16px 20px;
            border-radius: 16px;
            color: white;
            font-size: 14px;
            font-weight: 500;
            z-index: 10002;
            animation: notificationSlideIn 0.4s ease-out;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            max-width: 400px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            ${type === 'error' 
                ? 'background: linear-gradient(135deg, rgba(220, 53, 69, 0.9), rgba(220, 53, 69, 0.8));' 
                : 'background: linear-gradient(135deg, rgba(76, 175, 80, 0.9), rgba(76, 175, 80, 0.8));'
            }
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        // Add enhanced animation styles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes notificationSlideIn {
                from { 
                    opacity: 0;
                    transform: translateX(100%) translateY(-10px);
                }
                to { 
                    opacity: 1;
                    transform: translateX(0) translateY(0);
                }
            }
            @keyframes notificationSlideOut {
                from { 
                    opacity: 1;
                    transform: translateX(0) translateY(0);
                }
                to { 
                    opacity: 0;
                    transform: translateX(100%) translateY(-10px);
                }
            }
        `;
        document.head.appendChild(style);

        setTimeout(() => {
            notification.style.animation = 'notificationSlideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    }



    getSelectedCode() {
        const selection = window.getSelection();
        if (selection && selection.toString().trim()) {
            const selectedText = selection.toString().trim();
            const language = this.detectLanguageFromSelection(selectedText);
            return {
                code: selectedText,
                language: language
            };
        }
        return null;
    }

    detectLanguageFromSelection(code) {
        // Enhanced language detection based on code patterns
        const lines = code.split('\n');
        const codeLower = code.toLowerCase();
        
        // Python patterns (high confidence)
        if (code.includes('def ') || code.includes('import ') || 
            code.includes('print(') || code.includes('if __name__') ||
            code.includes('class ') && code.includes(':') ||
            lines.some(line => line.includes('def ') && line.includes(':')) ||
            code.includes('lambda ') || code.includes('list(') ||
            code.includes('dict(') || code.includes('set(') ||
            code.includes('try:') || code.includes('except:') ||
            code.includes('with ') && code.includes(':')) {
            return 'python';
        }
        
        // C++ patterns (high confidence)
        if (code.includes('#include') || code.includes('std::') || 
            code.includes('int main') || code.includes('cout') ||
            code.includes('vector<') || code.includes('string ') ||
            code.includes('namespace ') || code.includes('template<') ||
            code.includes('class ') && code.includes('{') ||
            code.includes('public:') || code.includes('private:') ||
            code.includes('cin >>') || code.includes('endl') ||
            code.includes('auto ') || code.includes('const ')) {
            return 'cpp';
        }
        
        // Java patterns (high confidence)
        if (code.includes('public class') || code.includes('public static void main') ||
            code.includes('System.out.println') || code.includes('import java') ||
            code.includes('String[]') || code.includes('ArrayList<') ||
            code.includes('public ') && code.includes('class ') ||
            code.includes('private ') || code.includes('protected ') ||
            code.includes('interface ') || code.includes('extends ') ||
            code.includes('implements ') || code.includes('new ')) {
            return 'java';
        }
        
        // JavaScript patterns (high confidence)
        if (code.includes('function ') || code.includes('const ') || 
            code.includes('let ') || code.includes('console.log') ||
            code.includes('=>') || code.includes('var ') ||
            code.includes('export ') || code.includes('import ') ||
            code.includes('async ') || code.includes('await ') ||
            code.includes('Promise') || code.includes('fetch(') ||
            code.includes('document.') || code.includes('window.')) {
            return 'javascript';
        }
        
        // C patterns
        if (code.includes('#include <stdio.h>') || code.includes('printf(') ||
            code.includes('scanf(') || code.includes('malloc(') ||
            code.includes('free(') || code.includes('struct ')) {
            return 'c';
        }
        
        // Go patterns
        if (code.includes('package ') || code.includes('import ') ||
            code.includes('func ') || code.includes('fmt.') ||
            code.includes('var ') || code.includes('type ')) {
            return 'go';
        }
        
        // Rust patterns
        if (code.includes('fn ') || code.includes('let ') ||
            code.includes('println!') || code.includes('use ') ||
            code.includes('struct ') || code.includes('impl ')) {
            return 'rust';
        }
        
        // Default to Python if no clear pattern
        return 'python';
    }

    async analyzeSelectedCode(code) {
        try {
            const language = this.detectLanguageFromSelection(code);
            
            // Use background script to make API call
            const response = await new Promise((resolve, reject) => {
                chrome.runtime.sendMessage({
                    action: 'analyzeCode',
                    code: code,
                    language: language,
                    useML: true
                }, (response) => {
                    if (chrome.runtime.lastError) {
                        reject(new Error(chrome.runtime.lastError.message));
                    } else if (response && response.success) {
                        resolve(response.data);
                    } else {
                        reject(new Error(response?.error || 'Analysis failed'));
                    }
                });
            });

            this.showAnalysisResults(response);
        } catch (error) {
            console.error('Analysis error:', error);
            this.showNotification('Analysis failed. Please try again.', 'error');
        }
    }
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
`;
document.head.appendChild(style);

// Initialize content script
new ContentScript(); 