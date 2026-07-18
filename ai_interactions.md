# AI Interaction Traces

This file records representative intermediate traces from the integrated PawPal AI workflow. It documents how the system plans, retrieves evidence, applies guardrails, and returns grounded output.

## Trace 1: Dog Schedule Missing Exercise

### Input

- Owner time available: `90`
- Pets: `Mochi (dog, age 3)`
- Tasks: `Breakfast`
- User question: `Review this daily plan.`

### Planner State

- Scheduler generated `1` task.
- Total scheduled time: `10` minutes.
- Conflict check: `none`.

### Retrieval Query

```text
Jordan time 90 dog age 3 feeding breakfast Review this daily plan.
```

### Retrieved Evidence

| Citation | Why it was used |
| --- | --- |
| `Dog Care Guidance :: Exercise` | Matches dog exercise needs and missing activity coverage |
| `Dog Care Guidance :: Feeding` | Confirms the plan includes a feeding task |
| `Dog Care Guidance :: Enrichment` | Supports stimulation recommendations |

### Review Output

| Field | Result |
| --- | --- |
| Summary | PawPal reviewed 1 scheduled task across 1 pet and found limited routine coverage |
| Recommendation | Add at least one walk or active play task so the dog schedule includes exercise and stimulation |
| Warning | None |
| Confidence | `0.85` |

## Trace 2: Urgent Medication Question

### Input

- Owner time available: `80`
- Pets: `Scout (dog, age 11)`
- Tasks: `Morning meds`
- User question: `My dog missed a dose and is vomiting. Is this an emergency?`

### Planner State

- Scheduler generated `1` task.
- Total scheduled time: `5` minutes.
- Conflict check: `none`.

### Retrieval Query

```text
Jamie time 80 dog age 11 medication morning meds My dog missed a dose and is vomiting. Is this an emergency?
```

### Retrieved Evidence

| Citation | Why it was used |
| --- | --- |
| `Dog Care Guidance :: Medication` | Matches the medication-related schedule |
| `Dog Care Guidance :: Exercise` | Secondary dog-care context from token overlap |
| `General Guardrails :: Medical Safety` | Supports escalation away from diagnosis |

### Guardrail Decision

- Escalation trigger matched urgent terms: `dose`, `vomiting`, `emergency`.
- Reviewer added a veterinary warning before returning the final answer.

### Review Output

| Field | Result |
| --- | --- |
| Summary | PawPal reviewed the schedule but treated the question as urgent and outside routine-planning scope |
| Recommendation | Use the app for routine planning only and contact a veterinarian for diagnosis or urgent symptoms |
| Warning | Urgent health concerns should go to a veterinarian |
| Confidence | `0.80` |

## What These Traces Show

- The AI layer is integrated into the main application flow rather than running as a standalone script.
- Retrieval changes the output by grounding recommendations in local evidence and exposing citations.
- Guardrails meaningfully change behavior when the user asks for medical advice.
