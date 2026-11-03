# Security policy

Report vulnerabilities through GitHub Security Advisories without credentials or production targets. `/probe` is an SSRF-sensitive private control surface. It must remain reachable only from authoritative Prometheus on the dedicated network.

Targets and modules are repository-controlled and side-effect free. Public host ports/routes, insecure TLS, arbitrary headers, unrestricted redirects, broad internal probing and mutation endpoints are forbidden. The container drops all capabilities and restores only `NET_RAW` for reviewed ICMP probes. Source changes do not run a probe or deploy the service.
