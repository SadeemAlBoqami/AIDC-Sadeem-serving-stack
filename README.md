# W5D2: Alerting and Service Reports

## Overview
This directory contains the artifacts for the Week 5 Day 2 lab of the AIDC Bootcamp. The lab focuses on configuring Grafana-managed alert rules, routing notifications to a custom webhook receiver, and documenting service-level objective (SLO) compliance.

## Included Artifacts
* **`my-alert.json`**: The exported Grafana alert rule configured to monitor the 95th percentile Time to First Token (TTFT) for the `team-serving` model.
* **`notification-evidence.jsonl`**: Container logs from the `alert-inbox` webhook receiver, demonstrating the successful delivery of both `firing` and `resolved` alert states.
* **`my-service-report.md`**: The SLO measurement report based on simulated API traffic.

## Verification
All configurations and evidence files have been validated using the lab's verification script, resulting in `GREEN CHECK: PASS`.
