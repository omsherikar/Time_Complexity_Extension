// Background service worker for TimeComplexity Analyzer
// Handles messaging between popup, content scripts, and background tasks

chrome.runtime.onInstalled.addListener(() => {
    console.log('TimeComplexity Analyzer extension installed');
    
    // Set default settings
    chrome.storage.local.set({
        'apiUrl': 'http://localhost:8000',
        'autoExtract': true,
        'showFloatingButton': true
    });
});

// Handle messages from popup and content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'extractCode') {
        // Forward to content script
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs[0]) {
                chrome.tabs.sendMessage(tabs[0].id, { action: 'extractCode' }, (response) => {
                    sendResponse(response);
                });
            }
        });
        return true; // Keep message channel open for async response
    }
    
    if (request.action === 'getSettings') {
        chrome.storage.local.get(['apiUrl', 'autoExtract', 'showFloatingButton'], (result) => {
            sendResponse(result);
        });
        return true;
    }
    
    if (request.action === 'updateSettings') {
        chrome.storage.local.set(request.settings, () => {
            sendResponse({ success: true });
        });
        return true;
    }
});

// Handle tab updates to inject content scripts when needed
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status === 'complete' && tab.url) {
        const supportedPlatforms = [
            'leetcode.com',
            'codeforces.com',
            'geeksforgeeks.org',
            'hackerrank.com'
        ];
        
        const isSupported = supportedPlatforms.some(platform => tab.url.includes(platform));
        
        if (isSupported) {
            // Content script will be automatically injected via manifest
            console.log('Supported platform detected:', tab.url);
        }
    }
});

// Handle extension icon click
chrome.action.onClicked.addListener((tab) => {
    // This will open the popup automatically due to manifest configuration
    console.log('Extension icon clicked on tab:', tab.id);
});

// Handle errors gracefully
chrome.runtime.onSuspend.addListener(() => {
    console.log('TimeComplexity Analyzer extension suspended');
});

// Optional: Add keyboard shortcuts
chrome.commands.onCommand.addListener((command) => {
    if (command === 'analyze-code') {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            if (tabs[0]) {
                chrome.tabs.sendMessage(tabs[0].id, { action: 'analyzeCurrentCode' });
            }
        });
    }
}); 