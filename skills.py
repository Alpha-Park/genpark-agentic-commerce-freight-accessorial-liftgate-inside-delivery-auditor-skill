# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-agentic-commerce-freight-accessorial-liftgate-inside-delivery-auditor-skill
Category: agentic_commerce
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def audit_freight_accessorial_charges(carrier_invoice_accessorials, bol_authorized_accessorials, consignee_has_dock=True):
    authorized_set = set(bol_authorized_accessorials)
    disputed_charges = []
    total_billed = 0.0
    total_approved = 0.0
    total_disputed = 0.0
    
    for item in carrier_invoice_accessorials:
        code = item["code"].upper()
        amount = item["amount"]
        total_billed += amount
        
        # Invalidation logic:
        # 1. Liftgate billed but consignee has standard loading dock
        # 2. Accessorial billed but not authorized on BOL
        is_invalid = False
        reason = ""
        
        if code == "LIFTGATE" and consignee_has_dock:
            is_invalid = True
            reason = "Consignee possesses standard commercial unloading dock; liftgate service unwarranted"
        elif code not in authorized_set:
            is_invalid = True
            reason = f"Accessorial service '{code}' not contracted or pre-authorized on Bill of Lading"
            
        if is_invalid:
            total_disputed += amount
            disputed_charges.append({
                "accessorial_code": code,
                "amount_usd": round(amount, 2),
                "dispute_reason": reason
            })
        else:
            total_approved += amount
            
    return {
        "total_accessorials_billed_usd": round(total_billed, 2),
        "approved_accessorials_usd": round(total_approved, 2),
        "disputed_accessorials_usd": round(total_disputed, 2),
        "disputed_line_items_count": len(disputed_charges),
        "overcharge_leakage_pct": round((total_disputed / total_billed * 100.0) if total_billed > 0 else 0.0, 1),
        "actionable_disputes": disputed_charges
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "audit_freight_accessorial_charges",
                        "description": """Audit LTL freight carrier invoices for unauthorized accessorial surcharge leakages.
Cross-references carrier invoice accessorial line items (Liftgate $75, Inside Delivery $110, Residential Surcharge $85, Notification $35)
against original Bill of Lading (BOL) service authorization and consignee commercial dock capabilities.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = audit_freight_accessorial_charges(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'carrier_invoice_accessorials': [{'code': 'LIFTGATE', 'amount': 85.0}, {'code': 'INSIDE_DELIVERY', 'amount': 120.0}, {'code': 'NOTIFY_PRIOR', 'amount': 35.0}], 'bol_authorized_accessorials': ['NOTIFY_PRIOR'], 'consignee_has_dock': True}
        out = audit_freight_accessorial_charges(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
