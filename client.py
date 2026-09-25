import json
import statistics
from typing import Dict, Any, List, Optional

class BillingSpendAnomalyGuardClient:
    """
    Production-grade real-time spend clarity and billing anomaly guard engine.
    Inspired by Metronome (metronome.com) and Fly.io spend clarity dashboards.
    Monitors hourly/daily spend spikes, detects runaway agent loops, and auto-generates throttle alerts.
    """
    def __init__(self, z_score_threshold: float = 2.5):
        self.z_score_threshold = z_score_threshold

    def audit_spend_anomalies(
        self,
        customer_id: str = "cust_hubspot_enterprise_04",
        current_hour_spend_usd: float = 845.20,
        historical_hourly_spends: Optional[List[float]] = None,
        monthly_budget_usd: float = 15000.0,
        month_to_date_spend_usd: float = 12430.0
    ) -> Dict[str, Any]:
        if not historical_hourly_spends:
            # Baseline normal hourly spends around $110 - $140
            historical_hourly_spends = [
                112.4, 108.9, 125.0, 131.5, 119.0, 115.8, 128.4,
                122.1, 118.9, 130.0, 126.5, 121.0, 135.3, 129.0,
                118.0, 124.5, 132.3, 129.7, 125.0, 130.1, 128.8, 124.2,
                120.5, 122.8
            ]

        mean = statistics.mean(historical_hourly_spends)
        stdev = statistics.stdev(historical_hourly_spends) if len(historical_hourly_spends) > 1 else 1.0

        z_score = round((current_hour_spend_usd - mean) / max(0.01, stdev), 2)
        spike_multiplier = round(current_hour_spend_usd / max(0.01, mean), 2)
        anomaly_detected = z_score >= self.z_score_threshold

        budget_burn_pct = round((month_to_date_spend_usd + current_hour_spend_usd) / max(1.0, monthly_budget_usd) * 100, 1)
        budget_breach_risk = budget_burn_pct >= 90.0

        if anomaly_detected and spike_multiplier >= 5.0:
            guard_action = "IMMEDIATE_CIRCUIT_BREAKER_THROTTLE_AGENT_CONCURRENCY"
            severity = "CRITICAL"
        elif anomaly_detected:
            guard_action = "DISPATCH_SLACK_WEBHOOK_AND_NOTIFY_REV_OPS"
            severity = "HIGH"
        elif budget_breach_risk:
            guard_action = "NOTIFY_ACCOUNT_EXECUTIVE_FOR_PRE_AUTH_EXPANSION"
            severity = "MEDIUM"
        else:
            guard_action = "NORMAL_SPEND_TRAFFIC_CLEARED"
            severity = "LOW"

        return {
            "anomaly_check_id": "spnd_anom_mtr_9102",
            "customer_id": customer_id,
            "current_hour_spend_usd": current_hour_spend_usd,
            "baseline_mean_hourly_usd": round(mean, 2),
            "spend_spike_multiplier": f"{spike_multiplier}x",
            "anomaly_z_score": z_score,
            "anomaly_detected": anomaly_detected,
            "severity_level": severity,
            "month_to_date_spend_usd": month_to_date_spend_usd,
            "monthly_budget_usd": monthly_budget_usd,
            "budget_consumed_percentage": f"{budget_burn_pct}%",
            "recommended_guard_action": guard_action,
            "powered_by": "metronome.com spend clarity and anomaly guard"
        }
