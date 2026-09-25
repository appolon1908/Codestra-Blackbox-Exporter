# Codestra Blackbox Exporter Corporate Features

## Mission

Blackbox Exporter provides synthetic reachability evidence for Codestra applications, APIs and infrastructure dependencies. It verifies that a user/system can actually reach an endpoint rather than relying only on container/process health.

## Corporate probe classes

- public HTTPS availability;
- private HTTPS availability;
- TCP connectivity;
- DNS resolution;
- TLS certificate validity/expiry.

## Corporate features

- expected HTTP status validation;
- safe expected-content checks;
- DNS lookup failures and latency;
- TLS handshake/certificate expiry visibility;
- TCP reachability for approved infrastructure services;
- endpoint latency trends;
- business/service/environment ownership metadata;
- dependency-health scorecards in Grafana;
- distinction between public-customer probes and private-service probes.

## Safety

Synthetic probes must be side-effect free. Do not place PSTN calls, send email/SMS, trigger business workflows, submit financial/trading operations or execute authenticated write transactions merely to test availability.

Where authentication health must be tested, prefer discovery/health endpoints or dedicated read-only synthetic identities and endpoints.

## Security

`blac.codestra.media` is internal/private. The Blackbox Exporter native interface is not publicly exposed. Prometheus requests probes over an approved internal path.

## Release rule

Probe definitions are reviewed in Git and grouped by business/service ownership. Merge does not activate probes or publish ports.
