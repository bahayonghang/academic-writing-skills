# Defense Question Preparation

This file lists the common question categories of a doctoral thesis defense and specifies how to prepare the answers. For the format of the “可能提问” (possible questions) field in the speaker notes, see [Speaker Notes Format](speaker-notes.md).

## Question Categories

| Category                                    | Typical question                                                                      | Preparation points                                                                                                                         |
| ------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Topic significance and innovation scope     | How are the innovations of this thesis different from existing work?                  | Map each innovation to one chapter, and state the existing methods in the comparison and the differences                                   |
| Reason for the method choice                | Why did you select this model or algorithm?                                           | Explain how the problem features match the method assumptions, and give the thesis section that supports the choice                        |
| Experiment validity and comparison fairness | How did you set the parameters of the comparison methods? How did you split the data? | State the dataset, the split method, the evaluation metrics, and the settings of the comparison methods, and cite the thesis table numbers |
| Generalization and scope limits             | Is the method effective on other data or in other scenarios?                          | State the range that the thesis experiments cover and the conditions that the experiments do not cover                                     |
| Engineering application and deployment      | What are the computation time and the deployment conditions of the method?            | Cite the time or complexity results in the thesis and the deployment status in the application chapter                                     |
| Logic between chapters                      | How are the research chapters related?                                                | Use the mapping “问题 k → 研究内容 k → 创新点 k” (problem k → research content k → innovation k) to explain the role of each chapter       |
| Mapping of publications to chapters         | How are the published papers related to the chapters?                                 | Explain each item by the chapter mapping marks in the publication list                                                                     |
| Limitations and outlook                     | What are the main limitations of the method in this thesis?                           | Cite the outlook items of the conclusion chapter, and state the limitations and the future work                                            |

## Preparation Method

1. Prepare 3–5 questions for each research chapter. The questions cover at least three categories from the table above.
2. For each question, write an answer outline: one conclusion sentence, the thesis evidence (section, figure, table, and equation numbers), and one sentence on the scope limit or the limitation.
3. The numbers in the answers come only from the thesis. Give the position of each number in the thesis.
4. For a question that needs a figure or a table in the answer, prepare a backup page (`backup`) after the thanks page. Backup pages use only figures and tables that are in the thesis.
5. Write the 1–2 most likely questions of each page in the “可能提问” (possible questions) field of the notes for that page.

## Stage Differences

- Predefense: the committee usually checks whether the workload, the innovations, and the results meet the requirements for submission to review.
- Formal defense: the committee usually also checks the revisions made for the predefense comments and the blind review comments. This version does not generate a revision description page. When the user needs a revision description page, the user prepares the page separately.

## Answer Outline Example

```text
问题：为什么选用示例方法一，而不直接使用基线方法？
结论：示例数据存在分布差异，基线方法假设数据同分布。
依据：3.2 节问题描述；表3-1 的对比结果。
边界：论文只在两个合成数据集上验证，更大规模数据未做实验。
备用页：图3-2 的完整对比子图。
```
