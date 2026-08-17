import pandas as pd
import numpy as np

PROCESSES = ["Order Fulfillment", "Customer Support", "Loan Processing"]
CHANNELS = ["Digital", "Branch", "Partner"]


def generate_operations_data(n=1200, seed=42):
    rng = np.random.default_rng(seed)
    process = rng.choice(PROCESSES, n, p=[0.45, 0.30, 0.25])
    channel = rng.choice(CHANNELS, n, p=[0.55, 0.25, 0.20])
    dates = pd.Timestamp("2026-01-01") + pd.to_timedelta(rng.integers(0, 180, n), unit="D")
    base = np.where(process == "Order Fulfillment", rng.normal(22, 8, n), np.where(process == "Customer Support", rng.normal(14, 6, n), rng.normal(38, 15, n)))
    backlog = rng.poisson(8, n)
    rework = rng.binomial(2, np.where(channel == "Digital", 0.10, 0.20), n)
    duration = np.maximum(1, base + backlog * 1.2 + rework * 5 + rng.normal(0, 3, n))
    sla = np.where(process == "Order Fulfillment", 30, np.where(process == "Customer Support", 20, 50))
    revenue_impact = np.maximum(0, duration - sla) * rng.uniform(5, 25, n)
    return pd.DataFrame({"case_id": np.arange(1, n + 1), "date": dates, "process": process, "channel": channel,
                         "duration_hours": duration.round(2), "sla_hours": sla, "backlog": backlog,
                         "rework_count": rework, "revenue_impact": revenue_impact.round(2)})


def add_metrics(df):
    out = df.copy()
    out["sla_breach"] = (out.duration_hours > out.sla_hours).astype(int)
    out["delay_hours"] = np.maximum(0, out.duration_hours - out.sla_hours).round(2)
    return out


def bottleneck_summary(df):
    d = add_metrics(df)
    s = d.groupby("process").agg(cases=("case_id", "count"), avg_duration_hours=("duration_hours", "mean"),
        sla_breach_rate=("sla_breach", "mean"), avg_backlog=("backlog", "mean"),
        rework_rate=("rework_count", lambda x: (x > 0).mean()), revenue_impact=("revenue_impact", "sum")).reset_index()
    s["efficiency_score"] = (100 * (1 - s.sla_breach_rate) * (1 / (1 + s.rework_rate))).round(1)
    return s.sort_values(["sla_breach_rate", "revenue_impact"], ascending=False).reset_index(drop=True)


def channel_summary(df):
    d = add_metrics(df)
    return d.groupby("channel").agg(cases=("case_id", "count"), avg_duration_hours=("duration_hours", "mean"),
        sla_breach_rate=("sla_breach", "mean"), rework_rate=("rework_count", lambda x: (x > 0).mean())).reset_index()


def top_bottleneck(df):
    return bottleneck_summary(df).iloc[0]["process"]
