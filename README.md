# Codestra Blackbox Exporter

This repository is the service authority for governed HTTP, HTTPS, TCP, DNS, ICMP, and approved synthetic probes. `appolon1908-hue/Codestra-Prometheus` owns the target allowlist, target labels, recording rules, alerts, SLO evaluation, and retention.

## Security boundary

The accepted source candidate is upstream v0.28.0 at commit `5a059bee8d8ffa4e75947c5055fb0abeefc582e6`, pinned as `quay.io/prometheus/blackbox-exporter@sha256:e753ff9f3fc458d02cca5eddab5a77e1c175eee484a8925ac7d524f04366c2fc`. Selection does not activate it.

Blackbox Exporter can initiate network connections to a caller-selected target, so `/probe` is a sensitive internal control surface. It runs only on the dedicated external `codestra-prometheus-blackbox` network, whose only members are the authoritative Prometheus service and Blackbox Exporter. It has no host port and must not receive a public Caddy/Kong route. `blac.codestra.media` is an ownership/DNS identifier, not permission for public access. Operators reach probe results through Prometheus rather than joining arbitrary workloads to this network.

The container runs as UID/GID 65534 with a read-only filesystem, drops every capability, adds back only `NET_RAW` for ICMP, and enables `no-new-privileges`. HTTPS probes require TLS and verify certificates. IPv4 fallback is disabled so results do not silently change address families.

## Module and target policy

Approved source-controlled modules are:

- `https_2xx`: public HTTPS health with certificate verification and bounded redirects;
- `http_2xx_internal`: private HTTP health with only 200/204 and no redirects;
- `tcp_connect`: bounded TCP reachability;
- `dns_codestra_a`: `codestra.co` A-record resolution through an approved DNS target;
- `icmp_private`: private-host ICMP reachability.

New modules require a PR, explicit timeout, SSRF/threat review, side-effect analysis, and staging evidence. Credentials, arbitrary sensitive headers, insecure TLS, unrestricted internal redirects, and target addresses do not belong in this repository. Targets remain in Prometheus-controlled discovery and must be allowlisted. Probes must never send email/SMS, place calls, mutate Odoo or provider systems, submit financial/trading actions, or trigger business transactions.

The corporate profile adds business/service ownership, customer-path/dependency health, TLS-expiry, DNS, latency, and status/content expectations while preserving the side-effect-free boundary. See `codestra/enterprise-profile.v1.json` and `codestra/docs/CORPORATE-FEATURES.md`.

## Validation

Repository CI renders the hardened compose candidate, validates approved modules and bounded timeouts, verifies certificate safety, private networking, non-root/read-only operation, capability limits, immutable-image enforcement, and absence of public port publication.

A future approved deployment may use:

```bash
cp .env.example .env
python3 scripts/validate_deployment_inputs.py --env-file .env
docker compose -f deploy/compose.yaml config
docker compose -f deploy/compose.yaml up -d
# From Prometheus/private observability network only:
curl --fail 'http://blackbox-exporter:9115/probe?module=https_2xx&target=https://codestra.co/'
```

Those commands are documentation only during the repository-first phase. Before target activation, later evidence must prove public denial, approved target inventory, positive and negative `probe_success` behavior, TLS-expiry metrics, limited ICMP capability, required labels, and rollback.

`deploy/compose.yaml` with `config/blackbox.yml` is canonical. The files under `codestra/runtime-v1/` are compatibility candidates for the central suite and may not diverge from the canonical image, private network, module safety or narrowly bounded `NET_RAW` requirement.

## Promotion and safety

Promotion is `feature/* -> development -> test -> staging -> production -> main`. Merging changes source authority only and does not deploy. `DEPLOYMENT_ENABLED=NO` remains binding until the 14-repository release manifest is accepted.

Automated upstream synchronization requires the repository Actions secret `CODESTRA_AUTOMATION_TOKEN`, backed by an approved GitHub App or fine-grained token with contents and pull-request permissions. The non-default token is required so generated review PRs trigger normal exact-source validation; absence of the secret fails the sync closed.
