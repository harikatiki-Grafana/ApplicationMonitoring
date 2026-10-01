# Teamcenter Application Monitoring with Prometheus and Grafana

Reference implementation for application monitoring of Siemens Teamcenter.

## Architecture

Teamcenter -> Teamcenter monitoring adapter -> Prometheus -> Grafana
                                   \
                                    -> Alertmanager
JVMs -> JMX Exporter
Linux -> Node Exporter
Windows -> Windows Exporter

## Quick start

1. Copy .env.example to .env and set Teamcenter endpoints.
2. Run: docker compose up -d --build
3. Open Grafana at http://localhost:3000
4. Open Prometheus at http://localhost:9090
5. Open Alertmanager at http://localhost:9093

The adapter deliberately isolates Teamcenter-release-specific APIs. Replace the example health/statistics paths with supported interfaces for the deployed Teamcenter version.

Metric names in this repository are application contract examples, not claims of a universal native Teamcenter Prometheus endpoint.
