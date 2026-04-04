# Undergraduate Research Anti-Distill Classifier

Classify each paragraph, bullet, example, and behavior rule into exactly one tag:

- `[SAFE]`
- `[DILUTE]`
- `[REMOVE]`
- `[MASK]`

## Core Principle

Keep public academic knowledge and visible structure.

Remove or weaken:

- tacit know-how
- unpublished direction
- advisor-specific preference
- lab-specific workflow context
- collaboration-sensitive details

Do not fabricate results. Do not turn guesses into facts.

## High-Value Signals

Prefer `[DILUTE]` or `[REMOVE]` when the content includes:

- hard-won troubleshooting memory
- repeated experiment failure lessons
- parameter tuning shortcuts
- advisor review preference
- “what really matters in group meeting” type heuristics
- hidden next-step plans
- local scripts, devices, or dataset-specific tricks
- real collaboration map or power structure

## Tag Rules

### `[SAFE]`

Use when the content is generic, public, and expected in a normal research document.

Examples:

- record seeds and metrics
- compare against a baseline
- state limitations clearly

### `[DILUTE]`

Use when the content is useful but can be rewritten into a broader professional principle.

Examples:

- “导师先看问题是否讲清楚，再看数字”
- “结果不稳时先看数据处理链路”

### `[REMOVE]`

Use when the content exposes irreplaceable know-how, unpublished plans, or group-internal operating logic.

Examples:

- exact bug signatures
- unpublished experiment direction
- local environment failure triggers
- highly specific mentor tactics

### `[MASK]`

Use when the content contains names, private systems, internal paths, unpublished identifiers, collaborators, or submission-sensitive references.

## Output Format

For each item, produce:

```text
[TAG] original text
Reason: one short sentence
Replacement direction: one short sentence if not SAFE
```
