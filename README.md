# Multimodal Document Parser

[![CI](https://github.com/cerenaaa/multimodal-doc-parser/actions/workflows/ci.yml/badge.svg)](https://github.com/cerenaaa/multimodal-doc-parser/actions)

Extract structured data from PDFs, invoices, contracts, and images using Claude's vision capabilities. Converts unstructured documents into clean JSON for downstream ML pipelines.

## Capabilities

| Document type | Extracted fields |
|---|---|
| Invoices | vendor, date, line items, totals, tax |
| Contracts | parties, dates, obligations, termination clauses |
| Tables | headers, rows, data types, notes |
| Forms | field names, values, checkboxes, signatures |
| Charts | chart type, axes, data series, trends |

## Structure

```
multimodal-doc-parser/
├── parsers/
│   ├── base_parser.py        # Base class with Claude vision API
│   ├── invoice_parser.py     # Invoice structured extraction
│   ├── table_parser.py       # Table → DataFrame extraction
│   └── contract_parser.py    # Contract clause extraction
├── pipeline/
│   └── batch_processor.py    # Batch document processing with retry
├── schemas/
│   └── output_schemas.py     # Pydantic output schemas
└── parse.py                  # CLI entrypoint
```

## Quickstart

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python parse.py --file invoice.pdf --type invoice
```
