#\!/bin/bash
NAMESPACE="${1:-codebase_b39_app}"
shift 2>/dev/null || true

DETACH=""
RM_FLAG="--rm"

for arg in "$@"; do
    case "$arg" in
        -d|--detach) DETACH="-d" ;;
        -k|--keep) RM_FLAG="" ;;
    esac
done

# Run with X11 forwarding support for pygame GUI
docker run $DETACH -it $RM_FLAG \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    "$NAMESPACE"