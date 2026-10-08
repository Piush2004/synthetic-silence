import { AnalyzeResponse, ClaimResult } from './models/types.js';

document.addEventListener('DOMContentLoaded', () => {
  const analyzeBtn = document.getElementById('analyzeBtn') as HTMLButtonElement;
  const inputText = document.getElementById('inputText') as HTMLTextAreaElement;
  const resultsDiv = document.getElementById('results') as HTMLDivElement;

  analyzeBtn.addEventListener('click', () => {
    const text = inputText.value.trim();
    if (!text) return;

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';
    resultsDiv.innerHTML = '<p>Querying backend pipeline...</p>';

    chrome.runtime.sendMessage({ action: 'analyze_text', text }, (response) => {
      analyzeBtn.disabled = false;
      analyzeBtn.textContent = 'Analyze with SyntheticSilence2.0';
      
      if (chrome.runtime.lastError || !response || !response.success) {
        resultsDiv.innerHTML = `<p style="color:red">Error: ${response?.error || 'Failed to connect to background script'}</p>`;
        return;
      }

      renderResults(response.data, resultsDiv);
    });
  });
});

function renderResults(data: AnalyzeResponse, container: HTMLDivElement) {
  if (!data.results || data.results.length === 0) {
    container.innerHTML = '<p>No claims extracted or analyzed.</p>';
    return;
  }

  container.innerHTML = '';
  data.results.forEach((result: ClaimResult) => {
    const card = document.createElement('div');
    card.className = 'claim-card';
    
    // Simplistic threshold for visual demo
    const isInsufficient = result.signal.insufficiency_signal > 0.5; 
    const badgeClass = isInsufficient ? 'badge insufficient' : 'badge';
    const statusText = result.signal.construction_family_estimate || 'Unknown';

    card.innerHTML = `
      <span class="${badgeClass}">${statusText.replace('_', ' ').toUpperCase()}</span>
      <p><strong>Claim:</strong> ${result.claim.original_text}</p>
      <p><strong>Explanation:</strong> ${result.explanation}</p>
      <details>
        <summary>Raw Signal Data</summary>
        <pre style="font-size:10px; overflow-x:auto;">${JSON.stringify(result.signal, null, 2)}</pre>
      </details>
    `;
    container.appendChild(card);
  });
}
