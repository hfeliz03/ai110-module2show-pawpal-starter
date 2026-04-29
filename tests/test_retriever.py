from datetime import datetime

from ai_reviewer import PawPalAIReviewer
from pawpal_system import Owner, Pet, Scheduler, Task, TaskCategory
from retriever import SimpleRetriever


def test_retriever_returns_dog_exercise_guidance():
    retriever = SimpleRetriever()
    results = retriever.retrieve("dog walking play exercise schedule", top_k=3)

    assert results
    assert any("Dog Care Guidance" in result.citation for result in results)
    assert any(result.section == "Exercise" for result in results)


def test_ai_review_adds_guardrail_for_urgent_question():
    owner = Owner("Jamie", daily_time_available=80)
    dog = Pet("Scout", "dog", 11)
    dog.add_task(Task("Morning meds", 5, 5, TaskCategory.MEDICATION, due_date=datetime(2026, 4, 1, 9, 0)))
    owner.add_pet(dog)

    reviewer = PawPalAIReviewer()
    result = reviewer.review_schedule(owner, Scheduler(owner), "My dog is vomiting after missing a dose. Is this an emergency?")

    assert any("veterinarian" in warning.lower() for warning in result.warnings)
    assert result.citations


def test_ai_review_reduces_confidence_when_no_retrieval_match():
    owner = Owner("Pat", daily_time_available=60)
    pet = Pet("Bean", "other", 1)
    pet.add_task(Task("Custom ritual", 10, 3, TaskCategory.OTHER, due_date=datetime(2026, 4, 1, 10, 0)))
    owner.add_pet(pet)

    reviewer = PawPalAIReviewer()
    result = reviewer.review_schedule(owner, Scheduler(owner), "Assess this unusual ritual with obscure constraints.")

    assert result.confidence <= 0.6
    assert any("limited guidance" in warning.lower() for warning in result.warnings)
