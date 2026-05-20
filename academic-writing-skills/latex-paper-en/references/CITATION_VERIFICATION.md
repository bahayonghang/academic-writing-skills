# Citation Verification Guide

## Table of Contents
- [AI Citation Error Rate Warning](#ai-citation-error-rate-warning)
- [6-Step Verification Workflow](#6-step-verification-workflow)
- [API-Based Verification](#api-based-verification)
- [Exa MCP Integration](#exa-mcp-integration)
- [Citation Rules Quick Reference](#citation-rules-quick-reference)

## AI Citation Error Rate Warning

**WARNING: AI-generated citations have a ~40% error rate.** Hallucinated references — papers that don't exist, wrong authors, incorrect years, fabricated DOIs — are a serious form of academic misconduct.

**The Golden Rule**: NEVER generate BibTeX entries from memory. ALWAYS fetch programmatically.

| Action | Correct | Wrong |
|--------|---------|-------|
| Adding a citation | Search API → verify → fetch BibTeX | Write BibTeX from memory |
| Uncertain about a paper | Mark as `[CITATION NEEDED]` | Guess the reference |
| Can't find exact paper | Note: "placeholder — verify" | Invent similar-sounding paper |

## 6-Step Verification Workflow

- [ ] **Step 1**: Search using Exa MCP or Semantic Scholar API
- [ ] **Step 2**: Verify paper exists in 2+ sources (Semantic Scholar + arXiv/CrossRef)
- [ ] **Step 3**: Retrieve BibTeX via DOI (programmatically, not from memory)
- [ ] **Step 4**: Verify the claim you're citing actually appears in the paper
- [ ] **Step 5**: Add verified BibTeX to bibliography
- [ ] **Step 6**: If ANY step fails → mark as placeholder, inform user

## Verification Layers

Keep these layers separate in user-facing output:

1. **Entry format valid** — the BibTeX/BibLaTeX entry parses and has required
   fields.
2. **Canonical metadata exists** — DOI, arXiv, publisher landing page, or
   trusted index metadata confirms the paper identity.
3. **Claim support verified** — the cited paper actually supports the
   manuscript sentence or paragraph.

A local citation key, `.bib` match, DOI, or metadata hit is not enough to claim
Layer 3. When Layer 3 is not checked, write `CITATION_SUPPORT_NEEDED` or tell
the author that claim-level support remains unverified.

## API-Based Verification

### Search with Semantic Scholar

```python
from semanticscholar import SemanticScholar

sch = SemanticScholar()
results = sch.search_paper("attention mechanism transformers", limit=5)
for paper in results:
    print(f"{paper.title} - {paper.paperId}")
    print(f"  DOI: {paper.externalIds.get('DOI', 'N/A')}")
```

### Retrieve BibTeX via DOI

```python
import requests

def doi_to_bibtex(doi: str) -> str:
    """Get verified BibTeX from DOI via CrossRef."""
    response = requests.get(
        f"https://doi.org/{doi}",
        headers={"Accept": "application/x-bibtex"}
    )
    response.raise_for_status()
    return response.text

# Example
bibtex = doi_to_bibtex("10.48550/arXiv.1706.03762")
print(bibtex)
```

### Verify via arXiv

```python
import requests
import xml.etree.ElementTree as ET

def search_arxiv(query: str, max_results: int = 5):
    """Search arXiv for papers."""
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
    response = requests.get(url)
    root = ET.fromstring(response.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        arxiv_id = entry.find("atom:id", ns).text.strip().split("/")[-1]
        print(f"{title} [arXiv:{arxiv_id}]")
```

## Exa MCP Integration

For the best paper search experience, install Exa MCP:

```bash
# Claude Code
claude mcp add exa -- npx -y mcp-remote "https://mcp.exa.ai/mcp"
```

Exa enables searches like:
- "Find papers on RLHF for language models published after 2023"
- "Search for transformer architecture papers by Vaswani"

Then verify results with Semantic Scholar API and fetch BibTeX via DOI.

## Citation Rules Quick Reference

| Situation | Action |
|-----------|--------|
| Found paper, got DOI, fetched BibTeX | Use the citation |
| Found paper, no DOI | Use arXiv BibTeX or manual entry from paper |
| Paper exists but can't fetch BibTeX | Mark placeholder, inform user |
| Uncertain if paper exists | Mark `[CITATION NEEDED]`, inform user |
| "I think there's a paper about X" | **NEVER cite** — search first or mark placeholder |
| Citation key exists but claim support is unknown | Keep the key, mark `CITATION_SUPPORT_NEEDED` |

## Placeholder Format

When you cannot verify a citation:

```latex
% EXPLICIT PLACEHOLDER - requires human verification
\cite{PLACEHOLDER_author2024_verify_this}  % TODO: Verify this citation exists
```

**Always tell the user**: "I've marked [X] citations as placeholders that need verification."

## API References

- [Semantic Scholar API](https://api.semanticscholar.org/api-docs/)
- [CrossRef API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [arXiv API](https://info.arxiv.org/help/api/basics.html)

