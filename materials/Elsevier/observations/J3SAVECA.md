---
key: J3SAVECA
title: "From prompt design to iterative generation: Leveraging LLMs in PSE applications"
venue: "Computers & Chemical Engineering"
doi: "10.1016/j.compchemeng.2025.109282"
item_type: journalArticle
has_pdf: true
status: complete
pages_read: "1-18"
date_observed: 2026-09-11
story_pattern: SP-ELS-002
---

## Structure

数字节：`1. Introduction` → `2. Common problems and solutions for using LLM in process systems engineering (PSE)` → `3. Application: process system decomposition` → `4. Application: flowsheet ordering` → `5. Application: Visualization of process flowsheet` → `6. Application: process simulation` → `7. Application: Heat exchanger network synthesis` → `8. Conclusion`。前置 `ABSTRACT` / `Keywords`。无独立 Related Work。`related_work=inlined`（Introduction 中段 AIGC/LLM、PSE 历史、FATE-LLM、SFILES、PEOA 等）。Introduction 末有节序路标。Method 为第 2 节框架（standardized prompt、task chaining、iterative generation）。Applications 3–7 充当 experiments。

## Openers

- abstract: `Large Language Models` — "Large Language Models (LLMs) have demonstrated significant potential in coding, mathematical problem-solving, complex reasoning, etc."
- introduction: `Artificial Intelligence Generated` — "Artificial Intelligence Generated Content (AIGC) has recently emerged as a significant focus in academia and industry, driven by the advancements in large language models (LLMs) like ChatGPT-4."
- method: `Incorporating Large Language` — "Incorporating Large Language Models (LLMs) into Process Systems Engineering (PSE) offers promising opportunities for solving complex problems."
- experiments: `In industrial practice` — "In industrial practice, a chemical process could be very complex."
- conclusion: `Using Large Language` — "Using Large Language Models (LLMs) for Process Systems Engineering (PSE) mission presents a powerful opportunity to address complex industrial challenges through automated, data-driven solutions."

## Gap transitions

- however (abstract): "However, their application in PSE remains limited due to several practical challenges, such as ambiguous and underspecified prompts, managing tasks with intricate logical dependencies, and uncertainties in task complexity."
- despite (introduction): "Despite this, the process systems view remains a fundamental element in integrating modern chemical engineering components into a cohesive framework (Stephanopoulos and Reklaitis, 2011)."
- despite (introduction): "Despite the positive signs of progress, the applications of LLM in the industrial practice of PSE are still limited and face obstacles."
- though (introduction): "Though LLMs could bring new possibilities to PSE, applying LLMs in PSE industrial practice presents several common challenges."
- however (conclusion): "However, the practical use of LLMs in PSE has been constrained by issues such as vague or ambiguous prompts, the complexity of logical relationships in engineering tasks, and uncertainties surrounding the scope and depth of tasks."

## Hedge verbs

- is proposed / causal / abstract: "A systematic framework consisting of three key strategies is proposed in this paper to deal with these challenges."
- demonstrate / associative / abstract: "The results demonstrate how LLMs, when guided with structured methodologies, can enhance problem-solving in PSE, ultimately streamlining engineering workflows and decision-making processes."
- we proposed / causal / conclusion: "In this paper, we proposed a comprehensive framework consisting of standardized prompt design, task decomposition, and iterative generation for these challenges."
- demonstrate / associative / conclusion: "The case studies—focused on system decomposition, flowsheet ordering, and process visualization—demonstrate the efficacy of this framework in guiding LLMs through complex engineering problems."
- could / hedge / conclusion: "LLMs could implement the code design conceptualized by engineers from totally scratch."
- anticipate / hedge / conclusion: "As advancements in Artificial Intelligence Generated Content (AIGC) continue, we anticipate that the framework we have outlined will further lower the entry barriers for engineers, enabling broader applications of LLMs in PSE."

## Cross-section linkers

- introduction → method: "In Section 2, we identify and discuss these common issues with multiple examples. We then introduce a framework designed to address these challenges."
- method → applications: "Sections 3 to 5 present case studies with increasing complexity, demonstrating the application of the proposed framework."
- applications → later cases: "The applications in Sections 3 to 6 provide a more detailed demonstration of this point."
- applications → conclusion: `8. Conclusion`

## Candidate rules

- R002 Related Work 并入 Introduction。
- R003 节序路标：`In Section 2, we identify and discuss these common issues` / `Sections 3 to 5 present case studies`
- R009 自称：`is proposed in this paper` / `In this paper, we proposed`

## Candidate phrases

- `A systematic framework consisting of three key strategies is proposed in this paper to deal with these challenges.` (abstract)
- `In this paper, we will explore these common problems in detail, provide illustrative examples, and propose solutions to address them effectively.` (introduction)
- `Sections 3 to 5 present case studies with increasing complexity, demonstrating the application of the proposed framework.` (introduction)
- `In this paper, we proposed a comprehensive framework consisting of standardized prompt design, task decomposition, and iterative generation for these challenges.` (conclusion)
- `This work represents a step toward a more seamless integration of LLMs into industrial workflows` (conclusion)

## House style

自称 `is proposed in this paper` / `we proposed` / `In this paper, we proposed`。第一人称复数与 `this paper` 并用。进 phrase_bank，不进 anti_ai_patterns。

## Quotes

- abstract: Large Language Models (LLMs) have demonstrated significant potential in coding, mathematical problem-solving, complex reasoning, etc.
- abstract: A systematic framework consisting of three key strategies is proposed in this paper to deal with these challenges.
- abstract: The results demonstrate how LLMs, when guided with structured methodologies, can enhance problem-solving in PSE, ultimately streamlining engineering workflows and decision-making processes.
- introduction: Artificial Intelligence Generated Content (AIGC) has recently emerged as a significant focus in academia and industry, driven by the advancements in large language models (LLMs) like ChatGPT-4.
- introduction: Despite the positive signs of progress, the applications of LLM in the industrial practice of PSE are still limited and face obstacles.
- introduction: In Section 2, we identify and discuss these common issues with multiple examples.
- method: Incorporating Large Language Models (LLMs) into Process Systems Engineering (PSE) offers promising opportunities for solving complex problems.
- experiments: This section demonstrates an example of system decomposition to illustrate how standardizing prompt structure can be effectively applied to PSE issues.
- conclusion: Using Large Language Models (LLMs) for Process Systems Engineering (PSE) mission presents a powerful opportunity to address complex industrial challenges through automated, data-driven solutions.
- conclusion: In this paper, we proposed a comprehensive framework consisting of standardized prompt design, task decomposition, and iterative generation for these challenges.
- conclusion: This work represents a step toward a more seamless integration of LLMs into industrial workflows, fostering innovation and enhancing decision-making in the chemical and process industries.
