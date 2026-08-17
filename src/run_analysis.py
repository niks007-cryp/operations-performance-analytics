from pathlib import Path
from analytics import generate_operations_data, add_metrics, bottleneck_summary, channel_summary

root = Path(__file__).resolve().parents[1]
out = root / "outputs"
out.mkdir(exist_ok=True)
df = generate_operations_data()
d = add_metrics(df)
d.to_csv(out / "operations_cases.csv", index=False)
bottleneck_summary(d).to_csv(out / "process_summary.csv", index=False)
channel_summary(d).to_csv(out / "channel_summary.csv", index=False)
print(bottleneck_summary(d).to_string(index=False))
