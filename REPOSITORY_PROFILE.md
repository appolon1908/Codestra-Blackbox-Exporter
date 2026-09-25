# Repository profile — Codestra Blackbox Exporter

- Repository: `appolon1908-hue/Codestra-Blackbox-Exporter`
- Component ID: `blackbox-exporter`
- Purpose: side-effect-free, allowlisted HTTP/TLS/DNS/TCP/ICMP probes
- Non-goals: caller-controlled public probing, mutation endpoints, credential use or public native API
- Branch path: `feature/* -> development -> test -> staging -> production -> main`
- Canonical config: `deploy/compose.yaml` and `config/blackbox.yml`; runtime-v1 is compatibility-only
- Upstream: `prometheus/blackbox_exporter` v0.28.0, commit `5a059bee8d8ffa4e75947c5055fb0abeefc582e6`
- Runtime: `quay.io/prometheus/blackbox-exporter@sha256:e753ff9f3fc458d02cca5eddab5a77e1c175eee484a8925ac7d524f04366c2fc`
- Artifact model: verified upstream image plus signed Codestra configuration bundle
- Health/readiness: private `/-/healthy`; probe results through private `/probe` only from Prometheus
- Exposure: dedicated private Prometheus/Blackbox network, no host port or Caddy/Kong route
- Privilege exception: only `NET_RAW` for the reviewed ICMP module; no privileged mode or other capability
- Persistence: none
- Release/rollback: exact image/config digests and checksum with a pullable previous artifact
- Source hygiene: whitespace enforcement applies to Codestra-owned files; `upstream/` is byte-preserved and exempt through `.gitattributes`

Current verdict: `SOURCE_PREPARED_NOT_DEPLOYED`; registry and production evidence remain absent.
