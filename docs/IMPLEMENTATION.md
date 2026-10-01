# Implementation notes

## Telemetry sources

* Teamcenter application adapter: release-specific health/statistics interfaces.
* JMX Exporter: JVM/MBean metrics where applicable.
* Node Exporter: Linux host metrics.
* Windows Exporter: Windows host metrics.

## Production rules

Keep labels low-cardinality. Do not use user IDs, object IDs, request IDs, filenames, or other unbounded values as Prometheus labels. Prefer symptom-oriented alerts and recording rules for expensive PromQL.

## Teamcenter release validation

The adapter paths are placeholders. Validate the exact supported Teamcenter APIs, authentication method, JVM topology, and component names for the deployed release before production use.
