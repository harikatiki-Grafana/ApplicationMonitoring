# Technical Specification (TS)
## Teamcenter Application Monitoring with Prometheus and Grafana

**Status:** Draft for technical review · **Version:** 1.0 · **Date:** 14 October 2026

## 1. Principles
Reference implementation using vendor-supported interfaces, bounded metric labels, explicit monitoring failure states, configuration as code, least privilege and self-monitoring. Validate Teamcenter API details against the deployed release. No universal native Teamcenter /metrics endpoint is assumed.

## 2. Logical architecture
1. Teamcenter supported health/statistics sources, JVMs and hosts.
2. Monitoring adapter translates release-specific APIs into stable metrics.
3. JMX Exporter exposes approved JVM MBean metrics.
4. Node Exporter and Windows Exporter expose OS metrics.
5. Prometheus scrapes targets, stores time series and evaluates rules.
6. Alertmanager groups, deduplicates, inhibits and routes alerts.
7. Grafana provisions datasource and dashboards with production access controls.
Optional: database exporters, synthetic probes, long-term metrics storage, HA Prometheus and authenticated reverse proxy.

## 3. Deployment topology
Docker Compose is a development/reference topology. Production options include enterprise VMs/containers, Kubernetes with persistent volumes/network policies/secrets, or centralized monitoring with remote scrape/federation. Keep monitoring ports private. Document HA, storage, backup, failure domains and alert deduplication.

## 4. Interfaces
| Component | Interface | Purpose | Notes |
|---|---|---|---|
| Adapter | /health | Adapter process health | Independent of Teamcenter |
| Adapter | /metrics | Prometheus exposition | Include collection success/freshness |
| Teamcenter | Configurable health path | Component health | Release-specific placeholder |
| Teamcenter | Configurable stats path | Queue/error/service data | Normalized contract below |
| Prometheus | 9090 | Query/admin UI | Restrict access |
| Alertmanager | 9093 | Alert routing/UI | Configure real receivers |
| Grafana | 3000 | Dashboards | TLS/SSO/RBAC in production |
| Node Exporter | 9100 | Linux metrics | Private network only |
| Windows Exporter | 9182 | Windows metrics | Private network only |

## 5. Adapter contract
Normalized health example:
    {"services":[{"name":"foundation","up":true},{"name":"dispatcher","up":true}]}

Statistics example:
    {"job_queues":{"dispatcher":12},"application_errors":{"soa":{"timeout":2}}}

These are adapter contracts, not native Teamcenter response guarantees. Implement authentication, bounded timeouts, TLS verification, payload validation, bounded retry/backoff and clear timeout/HTTP/malformed-response handling. Do not fabricate zeroes on collection failure; expose collection success and last-success timestamp. Current adapter scaffold requires hardening before production.

## 6. Metric catalogue
| Metric | Type | Labels | Meaning |
|---|---|---|---|
| tc_service_up | Gauge | service | Source-reported availability |
| tc_job_queue_depth | Gauge | queue | Pending jobs |
| tc_http_requests_total | Counter | bounded route/method/status | Requests, only if supported instrumentation exists |
| tc_http_request_duration_seconds | Histogram | bounded route/method | Request latency distribution |
| tc_application_errors_total | Counter | service, bounded error type | Categorized application errors |
| tc_adapter_scrape_success | Gauge | bounded source or none | Latest upstream collection success |
| tc_adapter_last_success_timestamp_seconds | Gauge | none | Timestamp of last successful collection |
| up | Prometheus metric | target labels | Scrape reachability |

Never label by username, item/revision ID, filename, correlation ID, raw URL containing IDs, or exception message. Do not claim request metrics unless a supported source actually provides them.

## 7. Prometheus
Set scrape/evaluation intervals based on system load (30 seconds is only a starting point). Configure actual adapter, JVM, Linux, Windows and optional database targets. Use stable labels such as environment, site, role and service group. Keep secrets out of committed config. Validate with promtool check config and promtool check rules. Set retention/storage from series count and required retention; use external labels for federation/remote write where applicable.

Example 5xx ratio, only if counter exists:
    sum(rate(tc_http_requests_total{status_class="5xx"}[5m])) / clamp_min(sum(rate(tc_http_requests_total[5m])), 0.001)

Example p95, only if histogram buckets exist:
    histogram_quantile(0.95, sum by (le) (rate(tc_http_request_duration_seconds_bucket[5m])))

## 8. Rules and alerting
Initial candidates: adapter down for 5m; service unavailable for 5m; 5xx ratio >5% for 10m; p95 above agreed SLO for 10m; queue depth above approved threshold; host disk/memory pressure, JVM pressure and exporter down. Tune from baseline. Handle absent series intentionally. Include severity, service, environment, owner, impact and runbook in alert metadata.

## 9. Grafana
Provision Prometheus datasource and dashboard provider from version-controlled files. Panels: adapter/scrape status, service health, request rate, error ratio, latency, queue depth, JVM and host resources, alerts. Include units, environment/instance variables and runbook links. Validate dashboard JSON and test import. Use SSO/RBAC and folder permissions.

## 10. Alertmanager
Configure grouping, wait/interval/repeat behavior, inhibition and actual notification receivers. Store receiver credentials as secrets. Test routing with a synthetic alert and confirm delivery.

## 11. Security
TLS verification; read-only Teamcenter identity; approved secret store; firewall/network policies; Grafana SSO/RBAC; non-root containers where possible; pinned and scanned images/dependencies; redacted logs; backup/retention; monitor the monitoring stack.

## 12. Reliability/performance
Bound HTTP timeouts to scrape budget; consider cached snapshots and explicit freshness to avoid slow upstream calls blocking scrapes; avoid excessive polling; monitor scrape duration, sample ingestion, active series and disk growth. For HA, document redundant Prometheus, alert deduplication, supported storage and recovery procedures.

## 13. Deployment
1. Confirm Teamcenter release, endpoints, authentication, CA chain and component inventory.
2. Create environment-specific secrets securely.
3. Implement supported Teamcenter integration and normalize payloads.
4. Configure real exporter targets and JMX rules.
5. Configure Alertmanager receivers and Grafana access.
6. Validate Compose config, Prometheus rules, JSON and tests.
7. Pilot in non-production and test failure modes.
8. Baseline and tune thresholds; obtain owner approval.
9. Promote via change control and verify access, dashboards and alerts.

## 14. Test strategy
Unit tests for mapping, malformed payloads, metric contracts, label allowlists and timeout behavior; contract tests for each supported release; integration tests for scrape/rules/provisioning/notifications; failure injection for timeout, 401/403, 5xx, bad JSON, DNS/network, exporter down and queue growth; security checks for secrets/TLS/RBAC/ports; load and cardinality tests.

## 15. Troubleshooting
| Symptom | Checks | Action |
|---|---|---|
| Adapter target down | Process, /health, port, logs | Restore adapter and inspect deployment |
| Adapter up, no Teamcenter metrics | Freshness, auth/TLS, endpoint payload | Validate supported API and mapping |
| Exporter down | Process, port, firewall, logs | Restore exporter and verify labels |
| Dashboard missing | Provisioning logs, JSON, mounted path | Correct provisioning config |
| Alert not delivered | Rule state, Alertmanager route/receiver logs | Check match, credentials and network |
| Cardinality growth | TSDB series/labels | Remove unbounded labels |

## 16. Change management and limitations
Version-control adapter/config/dashboards/rules; review and test changes; separate environment config from code; never commit secrets. This repository is a reference scaffold, not a vendor-certified turnkey integration. Teamcenter paths, payloads, authentication, JMX patterns, exporter targets, receivers, TLS/RBAC, HA, backup and retention must be completed before production.

## 17. References
- Prometheus exporters: https://prometheus.io/docs/instrumenting/exporters/
- Alertmanager configuration: https://prometheus.io/docs/alerting/latest/configuration/
- Grafana provisioning: https://grafana.com/tutorials/provision-dashboards-and-data-sources/
- Teamcenter baseline architecture: https://learn.microsoft.com/th-th/azure/architecture/example-scenario/manufacturing/teamcenter-baseline
