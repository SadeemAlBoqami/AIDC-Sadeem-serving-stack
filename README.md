# Lab W4D2: Make it Self-Healing

## Overview

Moving from an unmanaged, single container (bare Pod) to a production-grade, self-healing model-serving architecture on Kubernetes (k3s). The system demonstrates zero-downtime rolling updates and automatic fault recovery under continuous traffic.

---

## Core Concepts Implemented

* **Deployment Controller**: Manages state, handles pod replication, and guarantees auto-recovery upon pod termination.
* **Service Abstraction**: Exposes a stable DNS name (`serving:8000`) and decouples traffic routing from ephemeral pod IPs using label selectors (`app: serving`).


* **Readiness Probe**: Gates incoming client traffic to ensure no requests hit an uninitialized model still returning 503.


* **Liveness Probe**: Restarts unhealthy or hanging containers while avoiding startup boot loops via `initialDelaySeconds: 20`.


* **Zero-Downtime Guarantee**: Combined `maxUnavailable: 0` with a 5-second `preStop` hook to eliminate connection drops during endpoint deregistration races.



---

## Architecture Specification

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: serving
spec:
  replicas: 2
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 0
      maxSurge: 1
  template:
    metadata:
      labels:
        app: serving
    spec:
      containers:
        - name: serving
          image: <user>/aidc-serving:cpu-v1
          ports:
            - containerPort: 8000
          lifecycle:
            preStop:
              sleep:
                seconds: 5
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            periodSeconds: 2
            failureThreshold: 2
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 20
            periodSeconds: 5

```

---

## Verification & Key Findings

| Test Scenario | Condition | Traffic Load | Observed Result | Target |
| --- | --- | --- | --- | --- |
| **Fault Recovery (Kill Demo)** | Delete 1 active Pod | 10 req/s (every 100 ms) | `ok=877, bad=0` | Zero dropped requests |
| **Rolling Update** | Environment update (`APP_VERSION=v2`) | 10 req/s (every 100 ms) | `ok=877, bad=0` | Zero dropped requests |
| **Automated Harness (`verify.sh`)**<br> | Full rollout with spec inspection | Continuous probes | `ok=439, bad=0`<br> | `GREEN CHECK: PASS`<br> |

