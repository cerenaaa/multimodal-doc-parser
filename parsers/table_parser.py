"""Table extractor: converts document tables into structured JSON."""
from parsers.base_parser import BaseDocumentParser


class TableParser(BaseDocumentParser):
    def _extraction_prompt(self) -> str:
        return """Extract all tables from this document. Return JSON:
{
  "tables": [
    {
      "title": "string or null",
      "headers": ["col1", "col2", ...],
      "rows": [["val1", "val2", ...], ...],
      "notes": "string or null",
      "page": number
    }
  ]
}
Preserve all column headers and row values exactly as they appear."""
