"""Minimal LangChain agent stub."""

from __future__ import annotations

from typing import Optional

from langchain.llms.base import LLM


class DummyLLM(LLM):
    """LLM stub used when no real model is provided."""

    @property
    def _llm_type(self) -> str:  # pragma: no cover - simple property
        return "dummy"

    def _call(self, prompt: str, stop: Optional[list[str]] = None) -> str:
        return "stub"


def run_agent(query: str, llm: Optional[LLM] = None) -> str:
    """Run the LangChain agent with ``query`` using ``llm``."""
    llm = llm or DummyLLM()
    return llm(query)
