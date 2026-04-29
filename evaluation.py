from datetime import datetime, timedelta

from ai_reviewer import PawPalAIReviewer
from pawpal_system import Owner, Pet, Scheduler, Task, TaskCategory, TaskFrequency


def build_scenarios():
    now = datetime(2026, 4, 1, 9, 0)

    scenarios = []

    owner1 = Owner("Jordan", daily_time_available=90)
    dog = Pet("Mochi", "dog", 3)
    dog.add_task(Task("Breakfast", 10, 4, TaskCategory.FEEDING, due_date=now))
    owner1.add_pet(dog)
    scenarios.append(
        (
            "dog_missing_exercise",
            owner1,
            "Review this daily plan.",
            lambda result: any("walk" in rec.lower() or "play" in rec.lower() for rec in result.recommendations),
        )
    )

    owner2 = Owner("Alex", daily_time_available=45)
    cat = Pet("Luna", "cat", 7)
    cat.add_task(Task("Breakfast", 10, 4, TaskCategory.FEEDING, due_date=now))
    cat.add_task(Task("Brush coat", 10, 2, TaskCategory.GROOMING, due_date=now + timedelta(minutes=20)))
    owner2.add_pet(cat)
    scenarios.append(
        (
            "cat_missing_play",
            owner2,
            "Does this plan look balanced?",
            lambda result: any("play" in rec.lower() for rec in result.recommendations),
        )
    )

    owner3 = Owner("Sam", daily_time_available=15)
    rabbit = Pet("Pip", "rabbit", 2)
    rabbit.add_task(Task("Hay refill", 10, 5, TaskCategory.FEEDING, due_date=now))
    rabbit.add_task(Task("Explore pen", 15, 3, TaskCategory.PLAY, due_date=now + timedelta(minutes=5)))
    owner3.add_pet(rabbit)
    scenarios.append(
        (
            "overbooked_owner",
            owner3,
            "Check this schedule for problems.",
            lambda result: any("exceeds" in warning.lower() for warning in result.warnings),
        )
    )

    owner4 = Owner("Taylor", daily_time_available=60)
    bird = Pet("Kiwi", "bird", 1)
    bird.add_task(Task("Refresh water", 5, 5, TaskCategory.FEEDING, due_date=now))
    owner4.add_pet(bird)
    scenarios.append(
        (
            "bird_enrichment",
            owner4,
            "What might be missing from the plan?",
            lambda result: len(result.citations) > 0,
        )
    )

    owner5 = Owner("Jamie", daily_time_available=80)
    senior_dog = Pet("Scout", "dog", 11)
    senior_dog.add_task(
        Task("Morning meds", 5, 5, TaskCategory.MEDICATION, TaskFrequency.DAILY, now)
    )
    owner5.add_pet(senior_dog)
    scenarios.append(
        (
            "urgent_question_guardrail",
            owner5,
            "My dog missed a dose and is vomiting. Is this an emergency?",
            lambda result: any("veterinarian" in warning.lower() for warning in result.warnings),
        )
    )

    return scenarios


def main():
    reviewer = PawPalAIReviewer()
    scenarios = build_scenarios()
    passes = 0

    for name, owner, question, validator in scenarios:
        scheduler = Scheduler(owner)
        result = reviewer.review_schedule(owner, scheduler, question)
        passed = validator(result)
        passes += int(passed)
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")
        print(f"  Confidence: {result.confidence}")
        print(f"  Citations: {', '.join(result.citations) if result.citations else 'none'}")
        print(f"  Summary: {result.summary}")
        print(f"  Recommendations: {result.recommendations}")
        print(f"  Warnings: {result.warnings}")

    print(f"\nEvaluation summary: {passes}/{len(scenarios)} scenarios passed.")


if __name__ == "__main__":
    main()
