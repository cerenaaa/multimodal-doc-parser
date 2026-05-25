"""Batch document processor with retry and structured output collection."""
from __future__ import annotations
import time
import json
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class ParseResult:
    file_path: str
    doc_type: str
    success: bool
    data: dict = field(default_factory=dict)
    error: str = ""
    latency_ms: float = 0.0


class BatchProcessor:
    def __init__(self, parser, max_retries: int = 2, retry_delay: float = 1.0):
        self.parser = parser
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def process_file(self, file_path: str, doc_type: str = "document") -> ParseResult:
        t0 = time.perf_counter()
        for attempt in range(self.max_retries + 1):
            try:
                data = self.parser.parse_image(file_path)
                return ParseResult(
                    file_path=file_path, doc_type=doc_type, success=True,
                    data=data, latency_ms=(time.perf_counter() - t0) * 1000
                )
            except Exception as e:
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    return ParseResult(file_path=file_path, doc_type=doc_type,
                                       success=False, error=str(e),
                                       latency_ms=(time.perf_counter() - t0) * 1000)

    def process_batch(self, files: list[tuple[str, str]], output_dir: str = "results") -> list[ParseResult]:
        Path(output_dir).mkdir(exist_ok=True)
        results = []
        for file_path, doc_type in files:
            print(f"Processing {file_path}...")
            result = self.process_file(file_path, doc_type)
            results.append(result)
            if result.success:
                out = Path(output_dir) / (Path(file_path).stem + ".json")
                out.write_text(json.dumps(result.data, indent=2))
                print(f"  ✓ {out} ({result.latency_ms:.0f}ms)")
            else:
                print(f"  ✗ {result.error}")
        success_rate = sum(r.success for r in results) / len(results) if results else 0
        print(f"\nBatch complete: {sum(r.success for r in results)}/{len(results)} successful ({success_rate:.0%})")
        return results
