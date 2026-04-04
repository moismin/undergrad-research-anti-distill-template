# Undergraduate Research Workflow Diluter

Use this prompt for:

- work.md
- experiment logs
- weekly reports
- reproduction guides
- workflow summaries

## Goal

Rewrite the content so it still looks academically competent and complete, but no longer exposes the author's scarce tacit advantage.

## Keep

- field terminology
- public methods
- standard research hygiene
- visible document structure

## Weaken or remove

- tuning shortcuts
- bug triage order
- lab-local exceptions
- unpublished hypotheses
- specific advisor expectations

## Rewrite Patterns

### Specific shortcut -> general principle

`If the first 3 epochs fluctuate, check labeling and split scripts before touching learning rate.`

becomes

`When early-stage training behaves abnormally, first verify data processing and configuration consistency.`

### Hidden lab rule -> neutral professional norm

`Use the conservative route or this gets pushed back in group meeting.`

becomes

`Prefer the option with clearer justification and lower interpretive risk.`

### Unpublished direction -> future work language

`Next we should pivot to cross-domain because the bottleneck is probably not the backbone.`

becomes

`Future work can further test the method under broader settings and boundary conditions.`

## Constraints

- Do not output empty filler.
- Do not falsify experiment status.
- Do not claim validation that has not happened.
