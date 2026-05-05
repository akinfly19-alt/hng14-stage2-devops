#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:?Service name required}"
IMAGE="${2:?Image required}"
HEALTH_TIMEOUT=60
HEALTH_INTERVAL=5
NEW_NAME="${SERVICE}_new"
OLD_NAME="${SERVICE}"

echo "==> Rolling deploy: ${SERVICE} -> ${IMAGE}"

docker pull "${IMAGE}"

docker run -d \
  --name "${NEW_NAME}" \
  --network internal \
  --env-file .env \
  "${IMAGE}"

echo "==> Waiting for health check (max ${HEALTH_TIMEOUT}s)..."

ELAPSED=0
while [ $ELAPSED -lt $HEALTH_TIMEOUT ]; do
  STATUS=$(docker inspect --format='{{.State.Health.Status}}' "${NEW_NAME}" 2>/dev/null || echo "starting")
  echo "    [${ELAPSED}s] Status: ${STATUS}"
  if [ "${STATUS}" = "healthy" ]; then
    echo "==> Health check passed!"
    break
  fi
  if [ "${STATUS}" = "unhealthy" ]; then
    echo "ERROR: New container unhealthy. Aborting."
    docker stop "${NEW_NAME}" && docker rm "${NEW_NAME}"
    exit 1
  fi
  sleep $HEALTH_INTERVAL
  ELAPSED=$((ELAPSED + HEALTH_INTERVAL))
done

if [ $ELAPSED -ge $HEALTH_TIMEOUT ]; then
  echo "ERROR: Timed out. Aborting."
  docker stop "${NEW_NAME}" && docker rm "${NEW_NAME}"
  exit 1
fi

docker stop "${OLD_NAME}" && docker rm "${OLD_NAME}"
docker rename "${NEW_NAME}" "${OLD_NAME}"
echo "==> Deploy complete."
