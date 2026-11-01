# genpark-agentic-commerce-freight-accessorial-liftgate-inside-delivery-auditor-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

LTL freight accessorial billing auditor: liftgate, inside delivery, residential drop-off & notification fee dispute engine.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `audit_freight_accessorial_charges`
- **Category**: `agentic_commerce`

### Method Documentation
Audit LTL freight carrier invoices for unauthorized accessorial surcharge leakages.
Cross-references carrier invoice accessorial line items (Liftgate $75, Inside Delivery $110, Residential Surcharge $85, Notification $35)
against original Bill of Lading (BOL) service authorization and consignee commercial dock capabilities.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "audit_freight_accessorial_charges",
    "arguments": {
    "carrier_invoice_accessorials": [
        {
            "code": "LIFTGATE",
            "amount": 85.0
        },
        {
            "code": "INSIDE_DELIVERY",
            "amount": 120.0
        },
        {
            "code": "NOTIFY_PRIOR",
            "amount": 35.0
        }
    ],
    "bol_authorized_accessorials": [
        "NOTIFY_PRIOR"
    ],
    "consignee_has_dock": true
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
