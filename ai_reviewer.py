from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
import json
import logging
import os

from pawpal_system import Owner, Scheduler, TaskCategory
from retriever import KnowledgeSnippet, SimpleRetriever


LOGGER = logging.getLogger(__name__)


def configure_logging() -> None:
    logging.basicConfig(
        filename="pawpal_ai.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )


@dataclass
class AIReviewResult:
    summary: str
    recommendations: List[str]
    warnings: List[str]
    confidence: float
    citations: List[str]
    used_fallback: bool


class PawPalAIReviewer:
    def __init__(self, retriever: Optional[SimpleRetriever] = None):
        self.retriever = retriever or SimpleRetriever()

    def build_query(self, owner: Owner, user_question: str = "") -> str:
        parts = [owner.name, f"time {owner.daily_time_available}"]
        for pet in owner.pets:
            categories = " ".join(task.category.value.lower() for task in pet.tasks)
            task_names = " ".join(task.name.lower() for task in pet.tasks)
            parts.append(f"{pet.species} age {pet.age} {categories} {task_names}")
        if user_question:
            parts.append(user_question)
        return " ".join(parts)

    def review_schedule(self, owner: Owner, scheduler: Scheduler, user_question: str = "") -> AIReviewResult:
        configure_logging()
        scheduler.generate_plan()
        query = self.build_query(owner, user_question)
        snippets = self.retriever.retrieve(query)
        citations = [snippet.citation for snippet in snippets]

        if self._should_escalate(user_question):
            warnings = [
                "This question sounds medical or urgent. PawPal can help with planning, but urgent health concerns should go to a veterinarian."
            ]
        else:
            warnings = []

        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                result = self._review_with_openai(owner, scheduler, snippets, user_question, api_key)
                LOGGER.info("Generated AI review with OpenAI, citations=%s", citations)
                if warnings:
                    result.warnings = warnings + result.warnings
                return result
            except Exception as exc:
                LOGGER.exception("OpenAI review failed, falling back: %s", exc)

        result = self._review_with_fallback(owner, scheduler, snippets, user_question)
        if warnings:
            result.warnings = warnings + result.warnings
        LOGGER.info("Generated fallback AI review, citations=%s", citations)
        return result

    def _review_with_openai(
        self,
        owner: Owner,
        scheduler: Scheduler,
        snippets: List[KnowledgeSnippet],
        user_question: str,
        api_key: str,
    ) -> AIReviewResult:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        prompt = self._build_prompt(owner, scheduler, snippets, user_question)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=prompt,
        )
        text = response.output_text
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = {
                "summary": text,
                "recommendations": [],
                "warnings": ["Model response was not valid JSON; raw output shown."],
                "confidence": 0.55,
            }

        return AIReviewResult(
            summary=payload.get("summary", "No summary returned."),
            recommendations=payload.get("recommendations", []),
            warnings=payload.get("warnings", []),
            confidence=float(payload.get("confidence", 0.55)),
            citations=[snippet.citation for snippet in snippets],
            used_fallback=False,
        )

    def _build_prompt(
        self,
        owner: Owner,
        scheduler: Scheduler,
        snippets: List[KnowledgeSnippet],
        user_question: str,
    ) -> str:
        task_lines = []
        for task in scheduler.daily_plan:
            task_lines.append(
                f"- {task.name} | {task.category.value} | {task.duration} min | priority {task.priority} | {task.due_date.isoformat()}"
            )

        evidence_lines = []
        for snippet in snippets:
            evidence_lines.append(f"{snippet.citation}: {snippet.text}")

        return (
            "You are PawPal AI Care Coach. Use only the retrieved evidence. "
            "Do not diagnose or change medication. "
            "Return strict JSON with keys summary, recommendations, warnings, confidence.\n"
            f"Owner time available: {owner.daily_time_available}\n"
            f"User question: {user_question or 'Review this schedule'}\n"
            "Schedule:\n"
            + "\n".join(task_lines)
            + "\nRetrieved evidence:\n"
            + "\n".join(evidence_lines)
        )

    def _review_with_fallback(
        self,
        owner: Owner,
        scheduler: Scheduler,
        snippets: List[KnowledgeSnippet],
        user_question: str,
    ) -> AIReviewResult:
        recommendations: List[str] = []
        warnings: List[str] = []
        citations = [snippet.citation for snippet in snippets]

        categories = {task.category for task in scheduler.daily_plan}
        species = {pet.species.lower() for pet in owner.pets}
        total_time = sum(task.duration for task in scheduler.daily_plan)

        if total_time > owner.daily_time_available:
            warnings.append(
                f"The current plan needs {total_time} minutes, which exceeds the owner's available {owner.daily_time_available} minutes."
            )

        if "dog" in species and TaskCategory.WALKING not in categories and TaskCategory.PLAY not in categories:
            recommendations.append(
                "Add at least one walk or active play task so the dog schedule includes exercise and stimulation."
            )

        if "cat" in species and TaskCategory.PLAY not in categories:
            recommendations.append(
                "Add a short interactive play session to support daily enrichment for the cat."
            )

        if not snippets:
            warnings.append("The retriever found limited guidance for this exact schedule, so the review confidence is reduced.")

        if any("Medication" in task.category.value for task in scheduler.daily_plan):
            warnings.append("Medication reminders are scheduling aids only and should not replace veterinary instructions.")

        if not recommendations:
            recommendations.append("The plan covers the main scheduled tasks. Keep monitoring appetite, behavior, and consistency over time.")

        if user_question and self._should_escalate(user_question):
            recommendations.append("Use this app for routine planning only and contact a veterinarian for diagnosis or urgent symptoms.")

        summary = (
            f"PawPal reviewed {len(scheduler.daily_plan)} scheduled task(s) across {len(owner.pets)} pet(s). "
            "The feedback is grounded in retrieved pet-care notes and focuses on routine planning coverage."
        )

        confidence = self._estimate_confidence(snippets, recommendations, warnings)
        return AIReviewResult(
            summary=summary,
            recommendations=recommendations,
            warnings=warnings,
            confidence=confidence,
            citations=citations,
            used_fallback=True,
        )

    def _estimate_confidence(
        self,
        snippets: List[KnowledgeSnippet],
        recommendations: List[str],
        warnings: List[str],
    ) -> float:
        confidence = 0.45 + min(len(snippets), 4) * 0.1
        if warnings:
            confidence -= 0.05
        if not recommendations:
            confidence -= 0.05
        return max(0.2, min(round(confidence, 2), 0.95))

    def _should_escalate(self, user_question: str) -> bool:
        lowered = user_question.lower()
        urgent_terms = ["emergency", "seizure", "vomit", "bleeding", "not breathing", "dose", "poison"]
        return any(term in lowered for term in urgent_terms)
