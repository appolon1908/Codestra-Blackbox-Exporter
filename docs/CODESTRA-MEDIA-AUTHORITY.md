# Codestra Blackbox Exporter Authority

Principal repository: `ingtrader21-spec/Codestra-Blackbox-Exporter`
Canonical service host: `blac.codestra.media`
Canonical DNS target: `37.27.128.39`
TTL: `600`

DNS has been externally verified. No alternate authoritative hostname is permitted.

## Ownership
Own Blackbox Exporter probe modules, probe policy, synthetic-check validation and upgrade runbooks. Do not own Prometheus scrape policy, target application configuration, Caddy or secrets.

## Exposure
Private/internal only. DNS may exist, but exporter service ports must be restricted to Prometheus/private monitoring networks.

## Integration
Upstream targets: approved HTTPS/TLS/TCP/internal endpoints. Downstream: Prometheus scrapes and alert rules based on probe metrics.

## Branch policy
Persistent: `main`, `development`, `test`, `staging`, `production`.
Temporary: `feature/*`, `fix/*`, `upgrade/*`, `security/*`, `docs/*`, `hotfix/*`, optional `release/*`, `rollback/*`.
Promotion: work -> development -> test -> staging -> production -> main.
