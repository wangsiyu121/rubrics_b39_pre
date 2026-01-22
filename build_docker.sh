#\!/bin/bash
NAMESPACE="${1:-codebase_b39_app}"
docker build -t "$NAMESPACE" .