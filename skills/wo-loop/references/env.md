# Environment names only — never values
SSE_TOKEN        device + VM ingest bearer (hq-core)
WEBDAV_USER/PASS vault-webdav basic auth (VM /srv/secrets/vault/webdav/env)
GH token         VM /srv/secrets/vault/tokens/github-tokens/*
Value files are outside git and chmod 600. Skills reference names, never values.
