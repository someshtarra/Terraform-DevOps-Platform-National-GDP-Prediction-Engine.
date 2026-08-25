# Monitoring & Metrics Guide

## Prometheus Metrics
- `/metrics` endpoint exposes HTTP request rates, status codes, and latency histograms.

## Prometheus Alerts (`monitoring/prometheus-rules.yaml`)
- `HighHTTPErrorRate`: HTTP 5xx > 1% for 3 minutes.
- `HighLatencyP95`: P95 Latency > 500ms for 5 minutes.
- `PodCrashLooping`: Pod restarts > 2 in 15 minutes.

## Grafana Dashboard
Import `monitoring/grafana-dashboard.json` into Grafana for real-time visualization.
