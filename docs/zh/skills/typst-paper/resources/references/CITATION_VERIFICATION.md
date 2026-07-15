# 引文验证指南

## 目录
- [AI引文错误率警告](#ai-citation-error-rate-warning)
- [6步验证工作流程](#6-step-verification-workflow)
- [基于API的验证](#api-based-verification)
- [Exa MCP 集成](#exa-mcp-integration)
- [引文规则快速参考](#citation-rules-quick-reference)
- [特定打字员：Hayagriva 格式](#typst-specific-hayagriva-format)

## AI引文错误率警告

**警告：人工智能生成的引文错误率约为 40%。** 幻觉参考文献——不存在的论文、错误的作者、不正确的年份、捏造的 DOI——是一种严重的学术不端行为。

**黄金法则**：永远不要从内存中生成 BibTeX 条目。始终以编程方式获取。

|行动|正确的|错误的|
|--------|---------|-------|
|添加引用|搜索 API → 验证 → 获取 BibTeX|从内存中编写 BibTeX|
|对论文不确定|标记为`[CITATION NEEDED]` |猜猜参考|
|找不到准确的论文|注：“占位符——验证”|发明类似的纸|

## 6 步验证工作流程

- [ ] **第 1 步**：使用 Exa MCP 或 Semantic Sc​​holar API 进行搜索
- [ ] **第 2 步**：验证论文存在于 2 个以上来源（语义学者 + arXiv/CrossRef）
- [ ] **步骤 3**：通过 DOI 检索 BibTeX（以编程方式，而不是从内存中）
- [ ] **第 4 步**：验证您引用的主张是否确实出现在论文中
- [ ] **步骤 5**：将经过验证的 BibTeX 添加到参考书目中
- [ ] **步骤 6**：如果任何步骤失败 → 标记为占位符，通知用户

## 基于API的验证

### 使用语义学者搜索

```python
from semanticscholar import SemanticScholar

sch = SemanticScholar()
results = sch.search_paper("attention mechanism transformers", limit=5)
for paper in results:
    print(f"{paper.title} - {paper.paperId}")
    print(f"  DOI: {paper.externalIds.get('DOI', 'N/A')}")
```

### 通过 DOI 检索 BibTeX

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

### 通过 arXiv 验证

```python
import requests
import xml.etree.ElementTree as ET

def search_arxiv(query: str, max_results: int = 5):
    """Search arXiv for papers."""
    url = f"https://export.arxiv.org/api/query?search_query=all:{query}&max_results={max_results}"
    response = requests.get(url)
    root = ET.fromstring(response.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        arxiv_id = entry.find("atom:id", ns).text.strip().split("/")[-1]
        print(f"{title} [arXiv:{arxiv_id}]")
```

## Exa MCP 集成

为了获得最佳论文搜索体验，请安装 Exa MCP：

```bash
# Claude Code
claude mcp add exa -- npx -y mcp-remote "https://mcp.exa.ai/mcp"
```

Exa 支持以下搜索：
- “查找 2023 年后发表的语言模型的 RLHF 论文”
- “搜索 Vaswani 的变压器架构论文”

然后使用 Semantic Sc​​holar API 验证结果并通过 DOI 获取 BibTeX。

## 引文规则快速参考

|情况|行动|
|-----------|--------|
|找到论文，获取 DOI，获取 BibTeX|使用引文|
|找到论文，没有 DOI|使用 arXiv BibTeX 或从纸上手动输入|
|论文存在但无法获取 BibTeX|标记占位符，通知用户|
|不确定论文是否存在|标记`[CITATION NEEDED]`，通知用户|
|“我认为有一篇关于 X 的论文”|**切勿引用** — 首先搜索或标记占位符|

## 占位符格式

当您无法验证引文时：

```typst
// EXPLICIT PLACEHOLDER - requires human verification
@PLACEHOLDER_author2024_verify_this  // TODO: Verify this citation exists
```

**始终告诉用户**：“我已将 [X] 引文标记为需要验证的占位符。”

## 特定类型：Hayagriva 格式

Typst 本身支持 Hayagriva YAML 格式以及 BibTeX：

```yaml
# references.yml (Hayagriva format)
vaswani2017:
  type: article
  title: "Attention Is All You Need"
  author:
    - Vaswani, Ashish
    - Shazeer, Noam
  date: 2017
  parent:
    type: proceedings
    title: "Advances in Neural Information Processing Systems"
  serial-number:
    doi: "10.48550/arXiv.1706.03762"
```

```typst
// Use in Typst
#bibliography("references.yml", style: "ieee")
```

验证 Typst 的引文时，适用相同的 6 步工作流程。唯一的区别是参考书目格式（`.yml`与`.bib`).

## API 参考

- [语义学者 API](https://api.semanticscholar.org/api-docs/)
- [交叉引用 API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [arXiv API](https://info.arxiv.org/help/api/basics.html)
- [马头明王格式](https://github.com/typst/hayagriva/blob/main/docs/file-format.md)

