import json, sys
from client import BillingSpendAnomalyGuardClient

def handle_mcp_request(payload):
    method = payload.get("method")
    req_id = payload.get("id", 1)
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "billing-spend-anomaly-guard", "version": "1.0.0"}}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [{"name": "audit_spend_anomalies", "description": "Audits real-time usage spend anomalies, detects runaway agent token burns, and triggers automated circuit-breaker throttles."}]}}
    elif method == "tools/call":
        client = BillingSpendAnomalyGuardClient()
        res = client.audit_spend_anomalies()
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "ACTIVE"}}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(handle_mcp_request({"method": "tools/list"})))
    else:
        client = BillingSpendAnomalyGuardClient()
        print(json.dumps(client.audit_spend_anomalies(), indent=2))
