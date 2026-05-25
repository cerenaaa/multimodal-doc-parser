"""
Base document parser using Claude vision API.
Handles image encoding, prompt construction, and JSON extraction.
"""
from __future__ import annotations
import base64
import json
import re
from pathlib import Path
from typing import Any
import anthropic


def encode_image(path: str) -> tuple[str, str]:
    """Encode image file to base64 and detect media type."""
    suffix = Path(path).suffix.lower()
    media_types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                   ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"}
    media_type = media_types.get(suffix, "image/jpeg")
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode(), media_type


class BaseDocumentParser:
    """
    Base class for vision-powered document parsers.
    Subclasses define the extraction prompt and output schema.
    """
    SYSTEM_PROMPT = (
        "You are a precise document parser. Extract information exactly as it appears. "
        "Return ONLY valid JSON matching the requested schema. No explanations, no markdown."
    )

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.Anthropic()
        self.model = model

    def _extraction_prompt(self) -> str:
        raise NotImplementedError

    def _parse_json(self, text: str) -> dict:
        text = text.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\n?", "", text)
            text = re.sub(r"\n?```$", "", text)
        return json.loads(text)

    def parse_image(self, image_path: str) -> dict[str, Any]:
        data, media_type = encode_image(image_path)
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}},
                    {"type": "text", "text": self._extraction_prompt()},
                ],
            }],
        )
        return self._parse_json(response.content[0].text)

    def parse_text(self, document_text: str) -> dict[str, Any]:
        """Parse from plain text (no image) — useful for OCR-pre-processed docs."""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"{self._extraction_prompt()}\n\nDocument:\n{document_text}"}],
        )
        return self._parse_json(response.content[0].text)
