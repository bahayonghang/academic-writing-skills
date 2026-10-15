# 示例：预评审意见的逐条回复

本示例用合成评阅书 `evals/fixtures/rebuttal/reviews/` 与合成论文 `evals/fixtures/mini-thesis/` 演示从读取评阅书到交付粘贴文本的全过程。完成后的台账为 `evals/fixtures/rebuttal/concerns-done.yaml`。题目、意见与页码均为虚构。

场景：论文仓库为 `$THESIS`，送审版本已提交到 git。用户把两份评阅书放在 `$THESIS/rebuttal/pre-review/review_results/`，需要填写「博士生修改说明」。

## 用户请求

> 预评审的两份评阅书回来了，在 rebuttal/pre-review/review_results 里。帮我逐条整理意见、定处理方式，改完论文后生成可以直接粘贴到 Word 修改说明里的回复。

## 1. 读取评阅书

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_intake.py --reviews $THESIS/rebuttal/pre-review/review_results --thesis $THESIS --main document.tex --stage pre-review --json
```

输出摘要：

```json
{
  "reviewers": [
    {
      "id": "R1",
      "file": "评阅书1.txt",
      "grade": "A",
      "total_score": 88,
      "items": 3,
      "anchors": 6
    },
    {
      "id": "R2",
      "file": "评阅书2.txt",
      "grade": "B",
      "total_score": 85,
      "items": 2,
      "anchors": 6
    }
  ],
  "warnings": [
    {
      "code": "W-ANCHOR-MISSING",
      "message": "第3章至第5章（chapter 4） 在论文 aux 中找不到对应标签",
      "source": "评阅书2.txt"
    },
    {
      "code": "W-ANCHOR-MISSING",
      "message": "第3章至第5章（chapter 5） 在论文 aux 中找不到对应标签",
      "source": "评阅书2.txt"
    }
  ],
  "ledger_written": true
}
```

脚本在 `$THESIS/rebuttal/pre-review/` 下创建 `responses/`（空）与 `workspace/`（`rebuttal_state.json`、`reviews/R1.md`、`reviews/R2.md`、`concerns.yaml`）。水印行、页脚与页码行已删除，跨行意见已合并。

**检查点 R1**：

> 评阅人1：总分 88，等级 A，同意答辩，意见 3 条；评阅人2：总分 85，等级 B，同意答辩，意见 2 条。两条 W-ANCHOR-MISSING 是「第3章至第5章」中间的第4、5章在合成论文中没有章标签，不影响后续步骤。
> 请确认：R1、R2 的顺序与评阅书原件编号一致；基线提交是送审版本。

用户确认。

## 2. 拆分意见并定处理方式

评阅人1第3条含四个独立要求，按 [回复流程](../references/rebuttal-workflow.md) 的拆分规则拆为 `R1-3a`（缩写）、`R1-3b`（图2-1）、`R1-3c`（文献[3]）、`R1-3d`（章间衔接），每个 `quote` 为原文逐字子串。`R1-3a` 与 `R2-2` 都涉及第2.3节，用 `shared_with` 互指。

| 条目             | 处理方式    | 理由                         |
| ---------------- | ----------- | ---------------------------- |
| R1-1 跨路网迁移  | future_work | 没有第二个同类路网的数据     |
| R1-2 式(2-1)符号 | add         | 补充符号定义                 |
| R1-3a 缩写       | revise      | 精简缩写，首次出现给全称     |
| R1-3b 图2-1      | revise      | 重绘该图                     |
| R1-3c 文献[3]    | revise      | 补全著录信息                 |
| R1-3d 章间衔接   | clarify     | 第3章引言已有承接说明        |
| R2-1 复杂度      | decline     | 硬件平台开销评测超出问题范围 |
| R2-2 数据切分    | add         | 补充与对比文献切分方式的差异 |

全部条目写好 `action`、`owner`、`plan` 后改为 `status: planned`：

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_build.py --workspace $THESIS/rebuttal/pre-review/workspace --thesis $THESIS --plan-only
```

`workspace/revision_plan.md` 按负责方分组（drawio、latex-thesis-zh、manual、none），`R1-3a` 与 `R2-2` 合并为一行。

**检查点 R2**：把修改计划交给用户，逐条说明 `R1-1`（future_work）与 `R2-1`（decline）的理由。用户批准。

## 3. 修改论文

用户用 `latex-thesis-zh` 修改第2章正文，重绘图并在该图之前新增一幅检测器布设图，补全 `references.bib`，完整编译并提交。新增图使原图2-1变为图2-2，页码顺延一页。

LLM 按 [回复写法](../references/rebuttal-writing.md) 写每条 `response`、`locations` 与 `evidence`，改为 `status: done`（结果即 `evals/fixtures/rebuttal/concerns-done.yaml`）。

## 4. 生成与检查

```bash
uv run python -B $SKILL_DIR/scripts/rebuttal_build.py --workspace $THESIS/rebuttal/pre-review/workspace --thesis $THESIS
uv run python -B $SKILL_DIR/scripts/rebuttal_check.py --workspace $THESIS/rebuttal/pre-review/workspace --thesis $THESIS
```

```text
锚点：已解析 6 个，未解析 0 个
% 汇总：Critical 0，Major 0，Minor 0，Info 0；skipped：无
```

`responses/response-all.md` 节选：

```text
意见3：写作规范方面：自定义缩写较多，影响可读性；图2-1文字过于密集；文献[3]著录信息不完整；第2章与第3章衔接不足。

（1）回复：已删除不常用的自定义缩写，其余缩写在首次出现处给出中文全称。（与评阅人2意见2一并修改）

（1）修改位置：第2.3节

（2）回复：已重绘该图，删去图中重复的说明文字并放大坐标轴标注。

（2）修改位置：原图2-1，现图2-2（第13页）

（3）回复：已补全该文献的卷号、期号与起止页码。

（3）修改位置：参考文献[3]
```

`responses/review-result.md`：

```text
总体评价 1（A）；总体评价 2（B）
```

## 5. 交付

**检查点 R3**：

> 已生成 `responses/review-result.md`、`responses/response-all.md`、`responses/response-R1.md`、`responses/response-R2.md`。质量门 Critical 0、Major 0、Minor 0、Info 0。
> 粘贴方式：`response-all.md` 整体复制到「博士生修改说明」栏；表格按评阅人分栏时，分别复制 `response-R1.md` 与 `response-R2.md`。页码指修改后论文；论文再次编译后，重新运行 build 与 check。
