import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import BillingSpendAnomalyGuardClient

def main():
    client = BillingSpendAnomalyGuardClient()
    res = client.audit_spend_anomalies()
    print("=== Billing Spend Anomaly Guard Output ===")
    print(f"Customer: {res['customer_id']} | Current Hour Spend: ${res['current_hour_spend_usd']:,.2f}")
    print(f"Baseline Mean: ${res['baseline_mean_hourly_usd']} | Spike: {res['spend_spike_multiplier']} (Z-Score: {res['anomaly_z_score']})")
    print(f"Anomaly Detected: {res['anomaly_detected']} | Severity: {res['severity_level']}")
    print(f"Budget Consumed: {res['budget_consumed_percentage']} of ${res['monthly_budget_usd']:,.2f}")
    print(f"Guard Action: {res['recommended_guard_action']}")

if __name__ == '__main__':
    main()
