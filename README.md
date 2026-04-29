# PawPal AI Care Coach

PawPal AI Care Coach is a retrieval-grounded pet care planner built on top of the original PawPal+ scheduling app. It combines deterministic scheduling with local pet-care knowledge retrieval so the app can review a user's plan, cite evidence, flag gaps, and stay cautious when evidence is weak.

## Original Project

This project extends **PawPal+ from Module 2**. The original app was a Streamlit-based pet care planner that let an owner create pets, add care tasks, generate a daily schedule, detect overlaps, and manage recurring tasks such as daily walks or weekly grooming.

## Why This Matters

The original scheduler could organize tasks, but it could not judge whether a plan was balanced or missing important care coverage. The new AI layer makes the system more useful by retrieving species-specific guidance before giving feedback, so recommendations are grounded instead of generic.

## AI Feature

Primary feature: **Retrieval-Augmented Generation (RAG)**.

What changed in the main app:
- the scheduler still creates the plan
- a retriever searches local pet-care documents in `knowledge/`
- the AI review step uses those retrieved snippets to generate grounded recommendations
- the app returns citations, warnings, and a confidence score

The project also includes a reliability layer:
- automated tests
- logging to `pawpal_ai.log`
- an evaluation harness in `evaluation.py`
- guardrails for urgent or medical questions

## Architecture Overview

The system has six main pieces:
- Streamlit UI for owner, pet, task, and AI review input
- Scheduler for deterministic task ordering, recurrence, and conflict detection
- Query builder that converts schedule state into a retrieval query
- Retriever that ranks relevant local pet-care guidance
- AI reviewer that produces grounded feedback using either an OpenAI model or a safe fallback reviewer
- Logger and evaluation harness for reliability checks

System diagram:

![PawPal architecture](/Users/vilma/Codepath/AI110%20Project%202/ai110-module2show-pawpal-starter/assets/system_architecture.svg)

Data flow:
- user input -> scheduler -> retriever -> AI reviewer -> cited output
- tests and human review check whether the AI response stays grounded

## Repository Structure

- [app.py](/Users/vilma/Codepath/AI110%20Project%202/ai110-module2show-pawpal-starter/app.py) contains the Streamlit app
- [pawpal_system.py](/Users/vilma/Codepath/AI110%20Project%202/ai110-module2show-pawpal-starter/pawpal_system.py) contains the original scheduling logic
- [retriever.py](/Users/vilma/Codepath/AI110%20Project%202/ai110-module2show-pawpal-starter/retriever.py) loads and ranks local knowledge snippets
- [ai_reviewer.py](/Users/vilma/Codepath/AI110%20Project%202/ai110-module2show-pawpal-starter/ai_reviewer.py) orchestrates the AI schedule review
- [evaluation.py](/Users/vilma/Codepath/AI110%20Project%202/ai110-module2show-pawpal-starter/evaluation.py) runs the reliability scenarios
- [model_card.md](/Users/vilma/Codepath/AI110%20Project%202/ai110-module2show-pawpal-starter/model_card.md) contains reflection, ethics, and AI-collaboration notes
- `knowledge/` stores the local pet-care guidance documents used for retrieval
- `tests/` stores unit tests for scheduling, recurrence, retrieval, and guardrails

## Setup Instructions

1. Create a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Optional: add an OpenAI API key if you want the live model-backed reviewer.

```bash
export OPENAI_API_KEY="your_api_key_here"
export OPENAI_MODEL="gpt-4.1-mini"
```

If no API key is provided, the app still runs with the built-in grounded fallback reviewer. That fallback keeps the project reproducible for grading.

4. Run the Streamlit app.

```bash
streamlit run app.py
```

## How To Use

1. Create an owner profile and set daily available time.
2. Add one or more pets.
3. Add tasks such as feeding, walks, medication, grooming, or play.
4. Generate the daily schedule.
5. Run the AI review to retrieve relevant care guidance and get grounded feedback.

## Product Tour

### Owner Setup

The workflow starts with a simple owner profile where the user sets daily availability, which becomes a hard scheduling constraint for the planner.

![Owner setup](</Users/vilma/Codepath/AI110 Project 2/ai110-module2show-pawpal-starter/assets/Screenshot 2026-04-28 at 8.40.39 p.m..png>)

### Multi-Pet Setup

PawPal supports more than one pet in the same account, which lets the planner combine care tasks across species into a single daily view.

![Pet setup](</Users/vilma/Codepath/AI110 Project 2/ai110-module2show-pawpal-starter/assets/Screenshot 2026-04-28 at 8.40.35 p.m..png>)

### Schedule Generation and Conflict Detection

The scheduling layer generates a chronological task plan and surfaces overlap warnings when tasks collide, making the deterministic planning logic visible to the user.

![Schedule and conflicts](</Users/vilma/Codepath/AI110 Project 2/ai110-module2show-pawpal-starter/assets/Screenshot 2026-04-28 at 8.40.25 p.m..png>)

### AI Schedule Review

After the schedule is built, the AI review stage retrieves pet-care evidence and produces grounded feedback with recommendations, confidence, and cited sources.

![AI review](</Users/vilma/Codepath/AI110 Project 2/ai110-module2show-pawpal-starter/assets/Screenshot 2026-04-28 at 8.40.19 p.m..png>)

### Retrieved Evidence

The UI exposes the evidence used during review so the user can inspect which knowledge snippets informed the final recommendation.

![Retrieved evidence](</Users/vilma/Codepath/AI110 Project 2/ai110-module2show-pawpal-starter/assets/Screenshot 2026-04-28 at 8.40.15 p.m..png>)

### System Architecture

The architecture below shows how the deterministic scheduler, retriever, AI reviewer, and evaluation layer work together as one applied AI system.

![PawPal architecture](/Users/vilma/Codepath/AI110%20Project%202/ai110-module2show-pawpal-starter/assets/system_architecture.svg)

## Sample Interactions

### Example 1: Dog schedule missing exercise

Input:
- Pet: dog, age 3
- Tasks: `Breakfast`
- Question: `Review this daily plan.`

Resulting AI output:
- Summary: the plan covers only a small portion of routine care
- Recommendation: add at least one walk or active play task
- Citation: `Dog Care Guidance :: Exercise`
- Confidence: moderate because the retriever found matching evidence

### Example 2: Cat schedule missing enrichment

Input:
- Pet: cat, age 7
- Tasks: `Breakfast`, `Brush coat`
- Question: `Does this plan look balanced?`

Resulting AI output:
- Recommendation: add a short interactive play session
- Citation: `Cat Care Guidance :: Enrichment`
- Confidence: moderate to high because both species and topic matched the knowledge base

### Example 3: Urgent medication question

Input:
- Pet: senior dog
- Tasks: `Morning meds`
- Question: `My dog missed a dose and is vomiting. Is this an emergency?`

Resulting AI output:
- Warning: urgent or medical concerns should go to a veterinarian
- Recommendation: use the app for routine planning only
- Citation: retrieved care and guardrail guidance
- Confidence: reduced because medical diagnosis is outside scope

## Reliability and Evaluation

This project does not rely on "it looked right." It includes multiple reliability checks.

### Automated tests

Run:

```bash
python -m pytest
```

Covered behaviors:
- recurring task generation
- chronological schedule sorting
- conflict detection
- empty-plan and edge-case handling
- retrieval relevance
- urgent-question guardrails
- reduced confidence when evidence is weak

### Evaluation harness

Run:

```bash
python evaluation.py
```

What it does:
- runs fixed pet-care scenarios
- prints citations, recommendations, warnings, and confidence
- marks each scenario pass or fail based on expected grounded behavior

Current summary:
- baseline scheduler and AI extension tests pass locally
- the evaluation script checks 5 predefined scenarios
- the system is strongest when the user asks routine planning questions that match the knowledge base
- confidence drops when retrieval coverage is weak or the user asks for medical advice

## Guardrails

The app includes explicit safety boundaries:
- it does not diagnose illness
- it does not change medication instructions
- it warns when the user asks an urgent or medical question
- it lowers confidence when evidence is limited
- it falls back safely if model-based generation fails

## Design Decisions and Tradeoffs

- I kept the original scheduler deterministic because task ordering, recurrence, and conflict checks are better handled with explicit logic than with an LLM.
- I used a local knowledge base so the RAG behavior is reproducible during grading and does not depend on external retrieval APIs.
- I added an optional OpenAI path, but the fallback reviewer remains the default-safe path for environments without API access.
- The retriever is intentionally simple and transparent. It uses token overlap rather than embeddings, which is easier to test but less expressive than a production-grade semantic retriever.

## Testing Summary

What worked:
- the original scheduling and recurrence logic remained stable
- retrieval consistently surfaced relevant species guidance for the supported scenarios
- urgent questions triggered guardrails instead of overconfident advice

What did not fully work:
- the local knowledge base is small, so unusual pets and unusual questions can produce weaker retrieval matches
- fallback confidence is heuristic rather than learned

What I learned:
- adding AI value was less about replacing the scheduler and more about adding a grounded review layer on top of it
- evaluation is critical because AI systems can sound reasonable even when their evidence is thin

## Reflection

This project taught me that a useful AI system usually needs both deterministic structure and grounded generation. The scheduler is reliable because it is explicit, while the retrieval-backed reviewer adds flexible reasoning only when it has evidence.

The biggest limitation is knowledge coverage. If the local documents do not contain enough relevant material, the reviewer should stay cautious, and that requirement shaped both the guardrails and the confidence system.

## Project Outcome

PawPal AI Care Coach is a complete applied AI extension of the original PawPal+ planner. The final system combines structured scheduling, local retrieval, grounded recommendations, guardrails, and evaluation into a single user-facing product that is reproducible, testable, and ready to present as a portfolio project.

## Portfolio Reflection

This project shows me as an AI engineer who can take an existing software system, identify where AI adds real value, and integrate it with testing, safety boundaries, and documentation. Instead of adding a generic chatbot, I built an AI feature that is measurable, grounded, and connected to the product's core behavior.
