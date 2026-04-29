from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import logging
import re


LOGGER = logging.getLogger(__name__)

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "for",
    "from",
    "has",
    "have",
    "if",
    "in",
    "is",
    "it",
    "no",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "time",
    "to",
    "with",
    "age",
    "other",
}


@dataclass(frozen=True)
class KnowledgeSnippet:
    source: str
    section: str
    text: str

    @property
    def citation(self) -> str:
        return f"{self.source} :: {self.section}"


def _tokenize(text: str) -> List[str]:
    tokens = re.findall(r"[a-zA-Z]+", text.lower())
    return [token for token in tokens if token not in STOP_WORDS]


class KnowledgeBase:
    def __init__(self, knowledge_dir: str = "knowledge"):
        self.knowledge_dir = Path(knowledge_dir)
        self.snippets = self._load_snippets()

    def _load_snippets(self) -> List[KnowledgeSnippet]:
        snippets: List[KnowledgeSnippet] = []
        if not self.knowledge_dir.exists():
            LOGGER.warning("Knowledge directory missing: %s", self.knowledge_dir)
            return snippets

        for path in sorted(self.knowledge_dir.glob("*.md")):
            title = path.stem.replace("_", " ")
            content = path.read_text(encoding="utf-8")
            current_section = "Overview"
            buffer: List[str] = []

            for line in content.splitlines():
                if line.startswith("# "):
                    title = line[2:].strip()
                    continue
                if line.startswith("## "):
                    if buffer:
                        snippets.append(
                            KnowledgeSnippet(
                                source=title,
                                section=current_section,
                                text=" ".join(buffer).strip(),
                            )
                        )
                        buffer = []
                    current_section = line[3:].strip()
                elif line.strip():
                    buffer.append(line.strip())

            if buffer:
                snippets.append(
                    KnowledgeSnippet(
                        source=title,
                        section=current_section,
                        text=" ".join(buffer).strip(),
                    )
                )

        LOGGER.info("Loaded %s knowledge snippets", len(snippets))
        return snippets


class SimpleRetriever:
    def __init__(self, knowledge_base: KnowledgeBase | None = None):
        self.knowledge_base = knowledge_base or KnowledgeBase()

    def retrieve(self, query: str, top_k: int = 4) -> List[KnowledgeSnippet]:
        query_tokens = set(_tokenize(query))
        if not query_tokens:
            return []

        ranked = []
        for snippet in self.knowledge_base.snippets:
            snippet_tokens = set(_tokenize(f"{snippet.source} {snippet.section} {snippet.text}"))
            overlap = query_tokens & snippet_tokens
            if not overlap:
                continue

            score = len(overlap)
            if any(token in snippet.source.lower() for token in query_tokens):
                score += 2
            if any(token in snippet.section.lower() for token in query_tokens):
                score += 1
            ranked.append((score, snippet))

        ranked.sort(key=lambda item: item[0], reverse=True)
        results = [snippet for _, snippet in ranked[:top_k]]
        LOGGER.info("Retriever query=%r top_k=%s matches=%s", query, top_k, len(results))
        return results
