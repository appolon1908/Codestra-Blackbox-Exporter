# Upgrade and upstream synchronization

Resolve an upstream tag to an exact commit and image index digest, record the platform digest and binary revision, attempt signature verification, scan the exact image, and update all three Compose candidates plus the runtime lock together. Validate every module with the exact binary, SSRF/redirect/TLS rules, `NET_RAW` scope, private network and target allowlist integration. Promote protected commits only and retain a pullable previous digest/config/checksum.
