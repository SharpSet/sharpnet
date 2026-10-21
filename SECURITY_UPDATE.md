# Docker security refresh — 2026-10-21

Build locally with `docker build --pull --no-cache -t security-update/IMAGE:20261021 .` (replace IMAGE with this repository's image name). Production Compose uses the dated local tag and preserves its existing container name. Use the existing Compose project name and environment file when recreating services; do not run a blanket `down`, remove volumes, or start unrelated projects.

CircleCI now requires manual approval for a build and neither publishes mutable tags nor calls the legacy SharpCD deployment endpoint. Merge this configuration before resuming automated builds. The older default-branch configuration remains active until this change is merged.

The image uses Python 3.13 on Debian 13, locked Python dependencies, Docker CLI 29.9.2 (Go 1.26.10), and patched certificate trust. The Docker socket remains root-equivalent access and should be replaced with a narrower discovery mechanism in a future architecture change.

The controller now preserves and restores its last working HTTPS configuration on backend, certificate or reload failure; it retries with backoff instead of stopping backends. Certificate domain arguments are deduplicated. The `config` directory persists generated Nginx routes across restarts. For an existing deployment, seed `config/site.conf` from its working proxy configuration before recreation. Keep private keys only in the certificate volume.

Validation: image build, seven regression tests (`python3 -m unittest discover -s tests -v`), all existing HTTPS routes tested with static configuration, actual Python TLS-verifier tests, and a successful production controller/certificate cycle. `NETWORK` optionally overrides the discovery network for isolated testing.
