# PawPal AI Care Coach Model Card

## System Purpose

PawPal AI Care Coach extends the original PawPal+ scheduler into a retrieval-grounded planning assistant for routine pet care. It reviews the user's generated schedule, retrieves relevant local guidance, and returns recommendations, warnings, confidence, and citations.

## Base Project

The original project was **PawPal+ from Module 2**, a Streamlit app for tracking pet-care tasks, generating a daily schedule, managing recurrence, and detecting overlaps. Its goal was to help a pet owner stay organized and consistent with feeding, walks, medication, grooming, and play tasks.

## AI Feature

Primary AI feature: **Retrieval-Augmented Generation (RAG)**.

How it works:
- build a query from pet species, age, tasks, owner constraints, and optional user question
- retrieve relevant snippets from the local `knowledge/` documents
- generate a grounded schedule review
- cite the retrieved guidance in the output

The app uses an optional OpenAI model if `OPENAI_API_KEY` is available. Otherwise it falls back to a deterministic grounded reviewer so the project remains reproducible.

## Reliability Summary

- Automated tests cover the scheduler, recurrence logic, retriever behavior, and AI guardrails.
- The evaluation harness runs fixed scenarios and checks for expected grounded behavior.
- The system logs retrieval activity, fallback usage, and failures to `pawpal_ai.log`.

## Testing Results

Current local reliability summary:
- Existing scheduler tests pass.
- Retrieval and AI review tests verify citation generation, missing-context handling, and urgent-question guardrails.
- Evaluation script reports pass/fail status across predefined scenarios.

## Limitations and Biases

- The knowledge base is small and manually written, so coverage is limited.
- Guidance is general and may reflect common-care assumptions more strongly for cats and dogs than for less common pets.
- Confidence is heuristic in fallback mode and should not be treated as a clinical certainty signal.
- The system can suggest routine care improvements, but it does not diagnose illness.

## Misuse Risks and Mitigations

Potential misuse:
- treating the app as veterinary advice
- using schedule suggestions as medication instructions
- assuming silence means no health risk

Mitigations:
- explicit guardrails in the prompt and fallback reviewer
- warnings for urgent or medical questions
- clear reminder that the system is for planning support, not diagnosis
- reduced confidence when retrieval evidence is weak

## Reflection and Ethics

### What surprised me while testing reliability?

The most fragile part was not the scheduler. It was making sure the AI stayed cautious when evidence was weak. The retrieval layer made it much easier to see when the app had enough context and when it should hold back.

### Collaboration with AI

Helpful suggestion:
- AI helped identify that the best extension was not a generic chatbot, but a retrieval-grounded review step that builds on the existing scheduler and creates measurable behavior.

Flawed or incorrect suggestion:
- One early suggestion pushed toward giving stronger health-specific medication guidance. That would have violated the safety boundary of the project, so I constrained the system to routine planning and explicit veterinary escalation instead.

### What this project taught me

A practical AI system is stronger when it combines deterministic logic with grounded generation and visible evaluation. The scheduler handles structure well, while the retrieval-based review adds useful reasoning without pretending to be a veterinarian.
