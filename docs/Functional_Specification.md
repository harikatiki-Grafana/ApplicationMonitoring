# Functional Specification (FS)
## Teamcenter Application Monitoring with Prometheus and Grafana

**Status:** Draft for stakeholder review · **Version:** 1.0 · **Date:** 14 October 2026

## 1. Purpose
Define functional requirements for monitoring Siemens Teamcenter using Prometheus for metrics collection and alert evaluation, Grafana for dashboards, and Alertmanager for notifications. Validate this specification against the deployed Teamcenter release, modules, topology and operating model.

## 2. Goals and success criteria
- Consolidated view of Teamcenter service health, latency, errors, queues, JVM and host resources.
- Distinguish monitoring-path failures from application failures.
- Actionable alerts with severity, ownership and runbook links.
- Reproducible dashboards and data sources provisioned as code.
- No sensitive or high-cardinality metric labels.
- Approved acceptance tests and operational ownership.

## 3. Scope
**In scope:** supported Teamcenter health/statistics interfaces; adapter mapping; request/error/latency metrics where available; JMX Exporter; Node Exporter; Windows Exporter; Prometheus scraping/rules; Alertmanager; Grafana provisioning; security, validation and operations.

**Out of scope unless approved:** changes to vendor-managed binaries/business logic; unapproved database instrumentation; full tracing/log aggregation/SIEM; automatic remediation; assuming a universal native Teamcenter /metrics endpoint.

## 4. Stakeholders
| Role | Responsibility |
|---|---|
| PLM application owner | Critical workflows, service boundaries and thresholds |
| Teamcenter administrator | Supported endpoints, topology and component mapping |
| Observability team | Prometheus, Grafana, exporters and Alertmanager |
| Infrastructure team | Host exporter installation and OS telemetry |
| Database team | Database monitoring and capacity |
| Security/IAM | Credentials, TLS, access and retention |
| Service desk/on-call | Alert response and incident records |

## 5. Personas and use cases
1. Operations engineer identifies which tier is degraded.
2. Teamcenter administrator correlates health, queue backlog and JVM pressure.
3. Service owner reviews trends against SLOs.
4. Incident commander receives grouped notifications and runbooks.
5. Security reviewer validates least privilege, TLS and retention.

## 6. Functional requirements
| ID | Requirement | Priority | Acceptance evidence |
|---|---|---|---|
| FR-001 | Prometheus scrapes the adapter on a configurable interval. | Must | Target status and scrape errors visible |
| FR-002 | Adapter health endpoint is independent of Teamcenter probe. | Must | /health works when adapter is healthy |
| FR-003 | Adapter maps approved Teamcenter interfaces into stable metrics. | Must | Contract tests cover valid and invalid payloads |
| FR-004 | Component availability is a gauge with bounded labels. | Must | Component dashboard and missing-data handling verified |
| FR-005 | Queue depth is reported where source supports it. | Should | Queue panels and threshold test work |
| FR-006 | Request rate, error ratio and latency are exposed only where instrumentation supports them. | Should | PromQL returns expected test values |
| FR-007 | JVM metrics collected via JMX Exporter where applicable. | Should | Exporter up and JVM panels populated |
| FR-008 | Linux/Windows host metrics collected through approved exporters. | Must | All in-scope hosts visible |
| FR-009 | Grafana datasource and dashboard are file-provisioned. | Must | Clean deployment provisions both |
| FR-010 | Prometheus evaluates recording and alerting rules. | Must | promtool checks pass and test alert fires |
| FR-011 | Alertmanager groups/deduplicates/routes alerts. | Must | Test notification reaches receiver |
| FR-012 | Dashboard identifies environment and target. | Must | Labels visible without sensitive identifiers |
| FR-013 | Monitoring stack health is monitored. | Must | Failure injection identifies failed layer |
| FR-014 | Config, dashboards and rules are version-controlled. | Must | Reviewed change exists |
| FR-015 | No unbounded identifiers in metric labels. | Must | Cardinality review passes |
| FR-016 | Troubleshooting and escalation runbooks are approved. | Must | Alert links and runbooks verified |

## 7. Dashboard requirements
Overview dashboard should include adapter/scrape status; Teamcenter component availability; request rate, error ratio and latency when available; queue depth/age where available; JVM heap, threads, GC; host CPU, memory, disk/inodes and network; active alerts and runbook links. Include units, environment, legends and time range. Missing telemetry must not look like a healthy zero.

## 8. Alerting
Initial thresholds are examples to be baselined and approved: adapter down 5 minutes (critical); Teamcenter component unavailable 5 minutes (critical); 5xx ratio above 5% for 10 minutes (warning, only if metric exists); p95 above 2 seconds for 10 minutes (provisional); queue depth above agreed threshold for 15 minutes. Each alert includes name, severity, service/environment, summary, impact and runbook. Configure receivers, maintenance windows and escalation per operations policy.

## 9. Security
Use TLS and certificate validation; read-only least-privilege identities; approved secret manager; restricted network access; SSO/RBAC in production; no sensitive business data in labels/annotations/logs; approved retention, backup, audit and patching.

## 10. Availability and performance
Define availability target, retention, scrape/evaluation intervals, backup/recovery objectives and target counts before production. Local Prometheus storage alone may not satisfy HA/long-term retention requirements. Estimate cardinality and ingestion using representative load tests.

## 11. Dependencies and assumptions
- Supported Teamcenter health/statistics API or approved adapter approach exists.
- Release, topology, authentication, TLS and service names are known.
- Exporters can be installed in an approved manner.
- Network/firewall and service accounts are approved.
- Thresholds are based on baselines and owner approval.

## 12. Acceptance tests
1. Clean deployment provisions Prometheus, Grafana datasource and dashboard.
2. Adapter/exporter targets show correct up/down states.
3. Valid normalized payload maps to expected metrics.
4. Timeout, non-2xx, malformed JSON and auth failure show collection failure—not healthy data.
5. Adapter stop triggers alert after configured duration.
6. Test error/latency/queue metrics trigger and clear alerts.
7. Alertmanager groups and routes notifications.
8. Grafana viewer cannot edit configuration.
9. Sensitive/high-cardinality labels are absent.
10. Recovery from temporary upstream outage does not require restarting monitoring.

## 13. Rollout
Discovery → design/security review → adapter/exporter development → non-production pilot → baseline and threshold tuning → production change → operations handover.

## 14. Risks
Unsupported endpoint assumptions (validate exact release); high cardinality (bounded labels); false positives (baseline and pending durations); blind spots (monitor scrape and freshness); secret exposure (secret manager and scanning); single points of failure (explicit HA/DR design).

## 15. Open decisions
Teamcenter release/topology; supported endpoints/authentication; in-scope components/hosts/JVMs/queues; SLOs and notification channels; HA/retention/DR; SSO/RBAC and secret manager.
