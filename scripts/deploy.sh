#!/usr/bin/env bash
# ── deploy.sh ────────────────────────────────────────────────────────
# Build, test, and deploy Admin Meta-Agents.
#
# Usage:
#   ./scripts/deploy.sh              # deploy to production
#   ./scripts/deploy.sh staging      # deploy to staging
#   DRY_RUN=1 ./scripts/deploy.sh    # preview without deploying
# ─────────────────────────────────────────────────────────────────────
set -euo pipefail

ENVIRONMENT="${1:-production}"
IMAGE_NAME="admin-meta-agents"
TAG="$(git describe --tags --always --dirty 2>/dev/null || echo 'latest')"
DRY_RUN="${DRY_RUN:-0}"

log()  { printf '\033[36m[deploy]\033[0m %s\n' "$*"; }
err()  { printf '\033[31m[deploy]\033[0m %s\n' "$*" >&2; }
fail() { err "$@"; exit 1; }

# ── Pre-flight checks ───────────────────────────────────────────────
log "Environment : $ENVIRONMENT"
log "Image       : $IMAGE_NAME:$TAG"

if [ ! -f ".env" ] && [ "$ENVIRONMENT" = "production" ]; then
    fail ".env file not found — copy .env.example and configure before deploying."
fi

# ── Run tests ────────────────────────────────────────────────────────
log "Running test suite…"
python -m pytest tests/ -v --tb=short || fail "Tests failed — aborting deploy."

# ── Build ────────────────────────────────────────────────────────────
log "Building Docker image…"
docker build -t "${IMAGE_NAME}:${TAG}" -t "${IMAGE_NAME}:latest" .

# ── Deploy ───────────────────────────────────────────────────────────
if [ "$DRY_RUN" = "1" ]; then
    log "Dry-run complete — skipping deploy."
    exit 0
fi

log "Deploying ($ENVIRONMENT)…"
docker compose down --remove-orphans 2>/dev/null || true
docker compose up -d

# ── Post-deploy health check ────────────────────────────────────────
log "Waiting for health check…"
sleep 5
if docker compose ps | grep -q "healthy\|running"; then
    log "✅ Deploy successful — $IMAGE_NAME:$TAG is running."
else
    err "⚠️  Container may not be healthy. Check: docker compose logs"
    exit 1
fi
