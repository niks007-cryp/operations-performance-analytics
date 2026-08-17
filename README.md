# Operations Performance Analytics

A business analytics system that turns operational case data into measurable SLA, bottleneck, rework and revenue-impact insights.

## Business problem
Operations teams often know that work is slow but cannot quickly identify **where** the delay is concentrated, which channels create rework, or which bottleneck has the largest financial impact.

## What it does
- Generates a reproducible operational case dataset
- Calculates SLA-breach and delay metrics
- Compares processes and channels
- Quantifies rework and revenue impact
- Produces an efficiency score for prioritisation
- Exports analyst-ready CSV summaries

## Run
```bash
pip install -r requirements.txt
PYTHONPATH=src python src/run_analysis.py
pytest -q
```

## Outputs
- `outputs/operations_cases.csv` — case-level enriched data
- `outputs/process_summary.csv` — process bottleneck view
- `outputs/channel_summary.csv` — channel comparison

## Verified run
Using seed `42` and 1,200 synthetic cases, the test suite completed **3/3 tests passed**. The generated process summary identified Customer Support as the highest SLA-breach process at **71.92%**, followed by Order Fulfillment at **62.41%** and Loan Processing at **50.48%**. Order Fulfillment had the largest estimated delay-related revenue impact at **46,724.86** units.

## Decision use case
The output can support weekly operations reviews: prioritise the process with the highest combination of SLA breaches and revenue impact, then investigate backlog/rework drivers before changing staffing or workflow rules.

## Scope
The included dataset is synthetic and is intended to demonstrate analytics engineering and decision logic. It does not represent a real company's operating performance.
