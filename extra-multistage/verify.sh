#!/usr/bin/env bash
set -euo pipefail

TARGET_MB=300

echo "==> 1. Checking images exist..."
docker image inspect registry:naive > /dev/null 2>&1 || { echo "GREEN CHECK: FAIL (registry:naive missing)"; exit 1; }
docker image inspect registry:multistage > /dev/null 2>&1 || { echo "GREEN CHECK: FAIL (registry:multistage missing)"; exit 1; }

echo "==> 2. Checking size against target..."
multi_bytes=$(docker image inspect registry:multistage --format '{{.Size}}')
multi_mb=$(awk "BEGIN {printf \"%.1f\", $multi_bytes/1024/1024}")

echo "Multi-stage size: ${multi_mb} MB"
if (( $(awk "BEGIN {print ($multi_mb > $TARGET_MB)}") )); then
    echo "GREEN CHECK: FAIL (image size ${multi_mb}MB exceeds target ${TARGET_MB}MB)"
    exit 1
fi

echo "==> 3. Testing runtime container..."
docker rm -f test-registry > /dev/null 2>&1 || true
docker run -d --name test-registry -p 8000:8000 registry:multistage > /dev/null

sleep 2

health_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health || echo "000")
list_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/registry || echo "000")
model_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/registry/Qwen2.5-1.5B-Instruct || echo "000")
notfound_code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/registry/nonexistent || echo "000")

docker rm -f test-registry > /dev/null 2>&1 || true

if [ "$health_code" -eq 200 ] && [ "$list_code" -eq 200 ] && [ "$model_code" -eq 200 ] && [ "$notfound_code" -eq 404 ]; then
    echo "GREEN CHECK: PASS"
else
    echo "GREEN CHECK: FAIL (routes check failed: health=$health_code, list=$list_code, model=$model_code, 404=$notfound_code)"
    exit 1
fi
