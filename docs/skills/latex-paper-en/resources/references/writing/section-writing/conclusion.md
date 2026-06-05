# Conclusion Section Writing

## Objective

Close the paper by answering the Introduction promises with bounded evidence, implications, limitations, and a concrete future direction.

## Required Roles

1. **Solved problem**: restate the target problem and core technical idea.
2. **Evidence recap**: summarize strongest supported findings with setting boundaries.
3. **Implication**: state what the result enables or suggests.
4. **Limitation**: name a real scope boundary without undermining the whole contribution.
5. **Future work**: connect the limitation to a specific next direction.

## Closure Check

Map Introduction promises to Conclusion answers:

```text
Intro claim: ...
Conclusion answer: ...
Evidence anchor: ...
Status: closed / weakly closed / missing
```

If a promise is not answered, add a bounded answer only when evidence exists. Otherwise flag the missing evidence.

## Limitation Guidance

Prefer scope limitations over avoidable implementation excuses:

- data regime, domain, or scenario boundary;
- assumption boundary;
- deployment or sensor/setup boundary;
- scale or resource boundary.

Avoid universal future-work claims such as "we will improve performance" unless the current limitation is specific.

## Safe Wording

- `The presented results indicate ... in the evaluated setting`
- `A current limitation is ...`
- `Extending the method to ... remains an important direction`

Avoid:

- `This solves ...` when only a benchmark subset is tested.
- `The method is universally applicable ...` without cross-domain evidence.
