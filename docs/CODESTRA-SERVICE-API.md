# Codestra service API contract: Blackbox Exporter

This repository owns the **synthetic-availability-dns-tls-authority** for the Codestra observability, analytics, telemetry, and secrets suite.

## Communication rule

Blackbox Exporter keeps its native API and protocol. The shared Codestra control plane in `appolon1908-hue/Codestra-Telemetry` performs only sanitized health, readiness, contract, topology, and immutable-release read-back. It never proxies native probe output, permits caller-selected targets, changes modules, mutates endpoints, reads secret values, or issues credentials.

Canonical hostname: `blac.codestra.media`
Native exposure: `internal_private`
Deployment class: `central`
Contract: `codestra/api/service-contract.v1.json`

## Native operations

| Method | Path | Category | Access | Control-plane rule |
|---|---|---|---|---|
| `GET` | `/-/healthy` | health | read_only | never proxied by the Codestra control API |
| `GET` | `/-/healthy` | readiness | read_only | never proxied by the Codestra control API |
| `GET` | `/metrics` | metrics | read_only | never proxied by the Codestra control API |
| `GET` | `/probe` | synthetic_probe | query | never proxied by the Codestra control API |

## Suite integrations

| Peer | Direction | Signal | Protocol | Purpose |
|---|---|---|---|---|
| `prometheus` | outbound | `metrics` | `prometheus-scrape` | publish approved side-effect-free probe evidence |

Probe targets and modules must be reviewed, repository-controlled, allowlisted, and side-effect-free. The shared control API cannot accept a target, module, hostname, URL, TCP endpoint, or DNS name from its caller.

## Identity and correlation

Every private request should propagate `X-Correlation-ID` and W3C `traceparent` when the native protocol supports them. `request_id`, `trace_id`, and `tenant_id` remain structured, protected, non-indexed fields. Metrics use only the bounded dimensions `codestra_business`, `application`, `service`, `environment`, `server`, `region`, and `deployment`.

Business identity is deployment-controlled. Caller-supplied business identity, cross-business defaults, anonymous management access, insecure TLS verification, and inline credentials are prohibited.

## Release and runtime boundary

The control plane reads source revision and image digest only from deployment environment variables. A valid release requires a 40-character Git SHA and `sha256:<64 lowercase hex>` image digest. This source change does not deploy the exporter, activate probes or scrapes, add targets, expose the native endpoint, issue credentials, or enable any business mutation.


## Contract authority handoff

- Canonical schema repository: `appolon1908-hue/Codestra-Telemetry`
- Canonical merged Telemetry SHA: `c35d880a730ca5206d445e8a9a688cb465ae2ad4`
- Contract version: `1.0.0`
- Downstream exact head: this PR branch commit; the authoritative literal SHA is the GitHub PR `headRefOid` recorded after this handoff commit.
- Deployment authorization: unauthorized until staging certification and protected production promotion are complete.
