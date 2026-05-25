"""Invoice structured data extractor."""
from parsers.base_parser import BaseDocumentParser


class InvoiceParser(BaseDocumentParser):
    def _extraction_prompt(self) -> str:
        return """Extract all invoice data and return this JSON schema exactly:
{
  "invoice_number": "string or null",
  "invoice_date": "YYYY-MM-DD or null",
  "due_date": "YYYY-MM-DD or null",
  "vendor": {"name": "string", "address": "string or null", "tax_id": "string or null"},
  "bill_to": {"name": "string", "address": "string or null"},
  "line_items": [{"description": "string", "quantity": number, "unit_price": number, "total": number}],
  "subtotal": number,
  "tax_amount": number,
  "tax_rate_pct": number,
  "total_amount": number,
  "currency": "USD",
  "payment_terms": "string or null",
  "notes": "string or null"
}"""
