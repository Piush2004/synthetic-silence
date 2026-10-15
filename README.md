# SyntheticSilence2.0

**Project Purpose:** Investigating whether representation-space density serves as a reliable, construction-invariant signal for evidence insufficiency.
**Research Question:** Do density-based evidence-sufficiency signals generalize across different constructions?
**Final Findings:** No. Under evaluated conditions, kNN density demonstrated significant construction and reference-manifold dependence. The modest signal on FEVER (AUROC=0.5463) inverted on AVeriTeC (AUROC=0.2754), and cross-manifold evaluation collapsed the signal to chance. 
**Reproducibility:** See `results/FINAL_PAPER_PACKAGE/reproducibility/`.
**Limitations:** Domain gaps, differing manifold sizes, limited matched samples, lack of temporal/NLI baselines.
**Future Work:** Temporal conditions, full NLI baselines, and richer structural control populations.

## Chrome extension

The extension (`extension/`) sends text to the local backend (`backend/`), which extracts claims,
searches Wikipedia and OpenAlex for sources, and returns a verdict per claim plus the experimental density signal.

What you can do in it:

| Action | How |
|---|---|
| Check selected text | Select text, right-click, **Check evidence for "..."**, or press `Alt+Shift+S` (rebind at `chrome://extensions/shortcuts`) |
| Check pasted text | Open the popup or side panel, paste, **Check evidence** (or `Ctrl/Cmd+Enter`) |
| Mark claims on the page | After a check, **Highlight on page**; **Show on page** scrolls to a claim |
| Keep or share a result | **Copy as Markdown** / **Copy JSON**; past checks are in **History** (kept locally) |
| See the research signals | Settings, **Research mode** |

The toolbar badge shows the claim count after a check (teal: all backed up, rose: something refuted, grey otherwise,
`!` when a check failed). Highlighting only finds claims that appear on the page word for word; reworded claims are
reported as "not found on this page".

The verdict shown for each claim ("Sources back this up", "Sources push against this", ...) comes from what the
retrieved sources say, not from the density composite. Consistent with the findings above, the density/entropy
"gap score" is hidden unless Research mode is on, and is reported as `NOT_CALIBRATED`.

Results stream in claim by claim; a claim that fails (for example a spent search budget) shows an explicit
error row with a retry, never an empty "no sources" result. Measured verdict accuracy and the open comparison
between the two verdict modes are in [`docs/VERDICT_EVALUATION.md`](docs/VERDICT_EVALUATION.md).

### Run it

1. **Backend** (Python 3.11+)
   ```bash
   python -m venv .venv
   .venv/Scripts/pip install -r backend/requirements-dev.txt   # Windows; use .venv/bin/pip elsewhere
   cp backend/.env.example backend/.env                         # then set OPENROUTER_API_KEY
   .venv/Scripts/python -m uvicorn app.main:app --app-dir backend --port 8000
   ```
   `GET /health` reports `pipeline_ready` once the embedding model and the reference manifold
   (`data/manifolds/fever_train_v1.npy`) are loaded.
2. **Extension** (Node 20+)
   ```bash
   cd extension
   npm install
   npm run build
   ```
   Open `chrome://extensions`, enable Developer mode, choose **Load unpacked**, and select the `extension/` folder.
   Select text on a page and open the popup (or open it in the side panel with the button in its header).

### Test it

```bash
cd extension && npm test              # API-type drift check, build, unit tests
cd extension && npm run e2e           # real Chrome + stub backend + a real page: selection, highlight,
                                      # history, export, hand-off, theme, error states (no network, no cost)
cd extension && npm run e2e -- --live # real Chrome against the running backend (needs LLM credit)
cd backend && ../.venv/Scripts/python -m pytest tests
```

After changing a backend response model, run `cd extension && npm run gen:api` to regenerate
`src/models/api.d.ts`; `npm test` fails if it is stale.

### Measure verdict accuracy

```bash
python scripts/eval_verdict.py --variant pooled_wiki --n 150 --budget-usd 2
```

Variants and the current results are described in `docs/VERDICT_EVALUATION.md`.

### Configuration (`backend/.env`, never committed)

| Variable | Default | Purpose |
|---|---|---|
| `OPENROUTER_API_KEY` | none, required | LLM for claim extraction, stance / NLI and explanations |
| `OPENROUTER_MODEL` | `openai/gpt-4o-mini` | Any OpenRouter model id that supports JSON mode |
| `OPENALEX_API_KEY` | none | Free key; without it OpenAlex uses a small daily budget shared per IP |
| `SS_RETRIEVERS` | `wikipedia,openalex` | Which sources to query (`wikipedia`, `openalex`) |
| `SS_VERDICT_MODE` | `pooled` | `pooled` (one NLI score) or `stance` (per-source stance with quotes; opt-in until evaluated) |
| `SS_REFERENCE_MANIFOLD` | `data/manifolds/fever_train_v1.npy` | Reference embeddings for the density signal |
| `SS_MAX_CLAIMS` | `6` | Claims analysed per request |
| `SS_CACHE` | `on` | Cache finished claim results on disk (`backend/.cache`); only successes are cached |
