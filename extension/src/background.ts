import { AnalyzeResponse } from './models/types.js';

chrome.runtime.onInstalled.addListener(() => {
  console.log('SyntheticSilence2.0 Extension Installed');
});

// Listener for messages from the popup or content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyze_text') {
    analyzeTextWithBackend(request.text)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    
    return true; // Indicates asynchronous response
  }
});

async function analyzeTextWithBackend(text: string): Promise<AnalyzeResponse> {
  const backendUrl = "http://127.0.0.1:8000/api/v1/analyze";
  
  try {
    const response = await fetch(backendUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ source_text: text })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data as AnalyzeResponse;
  } catch (error) {
    console.error("Error communicating with backend:", error);
    throw error;
  }
}
