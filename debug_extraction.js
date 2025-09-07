// Debug script to help identify code extraction issues
// Run this in the browser console on the coding platform

console.log("🔍 Debugging Code Extraction...");

// Check current URL
console.log("📍 Current URL:", window.location.href);

// Check for common code editor elements
const selectors = [
    '.monaco-editor',
    '.ace_editor', 
    '.CodeMirror',
    'pre code',
    '.program-source',
    '.code-container',
    '[data-cy="code-editor"]',
    '.editor-content',
    'textarea',
    'pre'
];

console.log("🔍 Checking for code elements...");
selectors.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    if (elements.length > 0) {
        console.log(`✅ Found ${elements.length} element(s) with selector: ${selector}`);
        elements.forEach((el, index) => {
            console.log(`  Element ${index}:`, el);
            if (el.value) {
                console.log(`    Has value: ${el.value.substring(0, 100)}...`);
            }
            if (el.textContent) {
                console.log(`    Has textContent: ${el.textContent.substring(0, 100)}...`);
            }
        });
    } else {
        console.log(`❌ No elements found with selector: ${selector}`);
    }
});

// Check for editor instances
console.log("🔍 Checking for editor instances...");
if (window.monaco) {
    console.log("✅ Monaco editor found");
    if (window.monaco.editor) {
        const models = window.monaco.editor.getModels();
        console.log(`Found ${models.length} Monaco models`);
    }
}

if (window.ace) {
    console.log("✅ Ace editor found");
}

if (window.CodeMirror) {
    console.log("✅ CodeMirror found");
}

// Check for language indicators
console.log("🔍 Checking for language indicators...");
const langSelectors = [
    '.language-python',
    '.language-cpp', 
    '.language-java',
    '.language-javascript',
    '[data-lang]',
    '[data-mode]'
];

langSelectors.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    if (elements.length > 0) {
        console.log(`✅ Found language indicator: ${selector}`);
        elements.forEach(el => {
            console.log(`  Language: ${el.getAttribute('data-lang') || el.getAttribute('data-mode') || el.className}`);
        });
    }
});

// Check page title and content
console.log("🔍 Page information:");
console.log("  Title:", document.title);
console.log("  Body classes:", document.body.className);
console.log("  Meta description:", document.querySelector('meta[name="description"]')?.content);

console.log("🎯 Debug complete! Check the console output above."); 