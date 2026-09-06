# Engineering-Application and System-Implementation Chapter Guide for Chinese Theses

This guide covers an independent engineering-application, system-implementation, or platform-application chapter
in an existing Chinese LaTeX degree thesis. It turns architecture, services, interfaces, and runtime records into an
academic argument with explicit evidence boundaries. The diagnostic entry point remains the existing `logic`
module. The guide adds no script, CLI flag, check code, interface schema, or engineering implementation requirement.

## 1. Scope and Chapter-Type Routing

First confirm that the material belongs to a degree thesis, then classify the chapter from the task performed by its
body. A chapter number and title words such as “platform” or “system” can locate content but cannot decide routing.

| Chapter type | Decisive task in the body | Route |
| --- | --- | --- |
| Method + experiment | Proposes one core method or model and validates it in an experiment section in the same chapter | [Method chapter guide](method-chapter-guide-zh.md) + `experiment --per-chapter` + `logic` |
| Process analysis | Analyzes a process and derives the thesis-wide method framework without proposing an independent method | [Process chapter guide](process-chapter-guide-zh.md) + `logic --process-chapter` |
| Engineering application / system implementation | Converts research artifacts from earlier chapters into operational constraints, system mechanisms, operator tasks, and graded validation | This guide + `logic` |
| Conclusion | Synthesizes thesis-wide contributions, limitations, and outlook | [Conclusion chapter guide](conclusion-guide-zh.md) + `conclusion` |

When only a chapter number is available, first inspect its title, direct subsections, and representative prose. Do not
run `--per-chapter` while the chapter type is unclear. Two Chapter 6 examples may route differently: a body with one
method and same-chapter experiments remains a method chapter, while a body organized around architecture, services,
operations, and runtime validation is an engineering-application chapter.

## 2. Inventory Facts and Evidence First

Before rewriting, divide the input into evidenced facts and missing evidence. Evidenced facts can come only from the
supplied thesis prose, source or design documents, configurations and interface descriptions, logs, test records,
figures and tables, or explicit user statements. Each source supports a different scope of claims.

- Inventory the research artifacts actually delivered by earlier chapters, such as models, algorithms, parameters,
  features, control variables, or analytical results.
- Record the source for every operational constraint, architecture choice, service mechanism, interface task, and
  validation item.
- Mark absent APIs, state machines, formulas, timing behavior, metrics, values, deployment environments, and
  production status as `missing evidence`; do not invent them to make the chapter appear more technical.
- Preserve existing `\cite{}`, `\ref{}`, `\label{}`, mathematics, terms, and failure boundaries. When evidence is
  insufficient, omit the claim or reduce its certainty instead of filling the gap with imagined engineering facts.

## 3. Main Argument Chain

The smallest complete argument unit is `source artifact -> operational constraint -> design goal/system property ->
evidenced mechanism -> validation evidence`. Every link must trace back to an input source. If the mechanism is not
documented, mark the gap instead of substituting a technology-stack name for a mechanism.

| Link | Question | Adequate treatment |
| --- | --- | --- |
| Source artifact | Which earlier result enters the system? | Name the chapter, model, or data artifact and its real input and output |
| Operational constraint | What limits that artifact at runtime? | State only supported data, time, resource, integration, or operational constraints |
| Design goal/system property | Why is the system organized this way? | Map the constraint to an observable reliability, traceability, timeliness, or maintainability goal |
| Evidenced mechanism | What design carries that goal? | Describe documented component responsibilities, data semantics, interface boundaries, lifecycles, or fallback actions |
| Validation evidence | How far has that mechanism been validated? | Give environment, duration/sample, comparator, metric, coverage, and failure scope |

“Framework X was adopted, so the system is reliable” lacks a constraint, mechanism, and evidence. “Historical replay
requires a consistent input time base; the available log proves only completion of the replay path, while long-term
reliability remains unsupported” preserves both the chain and its claim boundary.

## 4. Writing Each Part of the Chapter

### Opening: From Research Artifacts to Engineering Problems

Identify which earlier results must be integrated, explain which runtime properties are not established by offline
method evidence, and preview the constraints, mechanisms, and validation levels addressed by this chapter. Do not
repeat the algorithm derivation or turn “can compute” directly into “can run stably online.”

### Architecture: Explain Choices Through Constraints

Technology stacks, framework names, and layer diagrams are inventories. Each architecture choice should state the
real constraint it responds to, the system property it carries, the corresponding mechanism, and its validation
material. If the input provides a choice without comparison, runtime evidence, or rationale, retain the choice as a
fact but mark its rationale and property claim as `missing evidence`.

### Services: State Data and Runtime Semantics

When the material supports them, explain services through these questions instead of listing CRUD endpoints,
threads, or configuration items:

- data meaning, units, version, and source;
- sampling time, event time, alignment base, or latency boundary;
- creation, switching, invalidation, and traceability of models, tasks, configurations, or result artifacts;
- resource use, concurrency isolation, timeout, failure scope, and recovery action;
- how operation logs, version records, or audit trails support review.

These are review questions. They do not require the thesis to add a state machine, service API, or mathematical
formula. If implementation facts are missing, state what source, design document, log, or test record would be
needed to support the claim.

### Interface: Organize Around Operator Tasks and Decisions

Describe who performs which task under what conditions, which feedback they see, and which decision it informs;
then connect the task to the corresponding system mechanism and evidence. A screenshot proves only a presentation
at one moment. It does not prove functional completeness, successful operation, long-term stability, human
usability, or business outcomes. Without task records, user research, or runtime logs, mark those claims as
`missing evidence`.

## 5. Engineering-Evidence Ladder

Name levels according to the actual material. Intermediate levels may be absent, but lower-level evidence cannot
support a higher-level conclusion.

| Level | Can support | Cannot automatically support |
| --- | --- | --- |
| Offline/historical replay | Function, result reproduction, or interface connectivity under fixed data and protocol | Real-time behavior, field stability, production closed loop, or business outcomes |
| Shadow/parallel observation | Side-channel execution and logging under real or near-real input without affecting decisions | Control takeover, closed-loop effect, or long-term reliability |
| Controlled pilot | Runtime behavior for a bounded object, period, and authorization scope | Uncovered conditions, long-term rollout, or organization-wide benefits |
| Production or closed-loop operation | Actual execution, feedback, and results within the recorded scope | General conclusions beyond the environment, duration, samples, and covered failures |

For every validation item, check environment, duration or sample size, comparator, metric, input source, coverage,
and failure scope. State missing items explicitly; “field data,” a “real-time interface,” or a screenshot cannot
replace them.

### Obtain Separate Evidence for Four Claim Types

| Claim type | Evidence focus |
| --- | --- |
| Execution/tracking fidelity | Whether instructions, state, or targets are transferred and tracked under the protocol |
| System reliability | Availability duration, failures, recovery, resources, and boundary-condition records |
| Business outcomes | Explicit baseline, measurement scope, common samples, and external-factor controls |
| Human usability | Operator tasks, completion, errors, feedback, or a formal usability study |

One evidence type cannot substitute for another. A successful functional replay does not validate reliability,
accurate control tracking does not establish business benefits, and an interface screenshot does not establish
human usability.

## 6. Failure, Fallback, and Audit Boundaries

- State the trigger, affected scope, degradation or fallback action, recovery condition, and trace record as supported;
  mark absent parts as `missing evidence`.
- A fallback boundary is part of the system mechanism. Polishing or de-AI editing must retain real limits and must
  not turn “fallback under stated conditions” into “absolutely safe under all conditions.”
- A log or replay establishes only the failure paths it covers. Uncovered failures, concurrency, hardware behavior,
  and human intervention remain unverified.
- A mechanism explanation must not be more certain than its supporting source, design document, log, or test.

## 7. Reuse Results Analysis Only When Needed

An engineering chapter uses `logic` and this guide by default. Add `experiment --results-analysis` and read the
[results-analysis guide](results-analysis-guide-zh.md) only when the user explicitly requests results analysis or
the body contains a quantitative results subsection that needs interpretation. Do not run `--per-chapter` on the
whole engineering chapter because of its number. If an existing script emits irrelevant method-chapter E-* candidates,
review them by chapter type and mark them not applicable. Do not claim that this guide changes the analyzer's
default classification.

## 8. Close the Chapter as a Thesis Contribution

Close with `source artifact -> engineering constraint -> implemented mechanism -> evidence level -> thesis value ->
uncovered boundary`. A system implementation can be an independent contribution, but its strength depends on both
the novelty of the mechanism and its validation evidence. Without quantitative business evidence, state what was
integrated and the validation scope without claiming significant benefits. Without production or closed-loop
evidence, do not claim a completed field closed-loop application.

## 9. Recommended Review Output

Give the chapter-type rationale first, then list traceable argument chains:

| Source fact | Operational constraint | Design goal/system property | Evidenced mechanism | Evidence level and boundary |
| --- | --- | --- | --- | --- |
| Artifact or record locatable in the input | Limitation explicitly supported by the input | Goal mapped to that limitation | Action supported by a document, source, or log | Highest current evidence level; use `missing evidence` for gaps |

Finally list unsupported facts separately, distinguishing APIs/formulas/metrics, field deployment, hardware,
production closed loop, business outcomes, and human usability. Recommend the evidence needed; do not generate
experimental results or engineering facts for the author.

## Positive and Negative Examples

### Positive: Replay and Screenshots Only

> Known: historical replay completed data import and result presentation; a screenshot shows that an operator can
> view results. No field duration, failure record, or user study is available.

Acceptable: Under the supplied historical data and replay protocol, the system completed data import and result
presentation, and the interface supported the task of viewing results. This establishes an offline functional path,
not field stability, production closed loop, business outcomes, or human usability; the latter four are
`missing evidence`.

### Negative: Inventing Mechanisms From a Technology Stack

> The platform uses a front-end framework and a database, so it provides millisecond APIs, zero-failure fallback,
> and significant production benefits.

Problem: technology names do not establish interface latency, fallback mechanisms, or business outcomes. If the
input contains no interface, timing, failure-test, or benefit-scope evidence, remove these claims or mark them
`missing evidence`.

### Positive: Preserve a Real Fallback Boundary

> The available record establishes only that the system enters read-only mode when a queue exceeds a stated
> capacity and returns after operator review.

Acceptable: The mechanism limits the impact of the recorded failure to a read-only state and retains the operator-
review boundary. It does not establish absolute safety for all failures. Uncovered failure types and long-term
recovery behavior remain `missing evidence`.

## Further Reading

- [Method chapter guide](method-chapter-guide-zh.md): one-method and same-chapter experiment form.
- [Process chapter guide](process-chapter-guide-zh.md): process analysis and thesis-wide framework form.
- [Results-analysis guide](results-analysis-guide-zh.md): evidence depth and statistical scope for quantitative result subsections.
- [Claim-strength guardrail](over-claim-guard.md): evidence levels and wording strength.
- [Logic module](../modules/logic.md): existing diagnostic entry point for engineering chapters.
