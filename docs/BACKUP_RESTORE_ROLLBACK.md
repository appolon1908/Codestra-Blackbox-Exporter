# Recovery and rollback design

Blackbox Exporter is stateless. Recover the signed configuration bundle, exact image digest, private-network identity and Prometheus-owned target inventory; never infer targets from runtime traffic.

Before change, record source/image/config digests, checksum, module inventory, network membership and current private health. Restore in an isolated network with synthetic allowlisted endpoints. Prove `/-/healthy`, positive and negative probes, TLS verification, redirect bounds, target rejection by the controlling Prometheus policy, and no public reachability. Rollback requires real previous pullable image/config digests and checksum. Repository tests are not production rollback evidence.
