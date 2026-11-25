#!/usr/bin/env bash
set -euo pipefail

image=${1:?pass the Ombi image to test}
name="ombi-smoke-$$"
tmp=$(mktemp -d)
cleanup() {
    docker rm -f "$name-app" "$name-supervisor" >/dev/null 2>&1 || true
    docker network rm "$name" >/dev/null 2>&1 || true
    rm -rf -- "$tmp"
}
trap cleanup EXIT

# Supply the Supervisor metadata that Bashio reads during app startup.
cat > "$tmp/nginx.conf" <<'NGINX'
events {}
http {
    server {
        listen 80;
        default_type application/json;
        location = /addons/self/options/config {
            return 200 '{"result":"ok","data":{"PUID":1000,"PGID":1000,"env_vars":[]}}';
        }
        location / {
            return 200 '{"result":"ok","data":{"version":"4.60.20","ingress_entry":"/api/hassio_ingress/smoke"}}';
        }
    }
}
NGINX

docker network create "$name" >/dev/null
docker run -d --name "$name-supervisor" --network "$name" \
    --network-alias supervisor --entrypoint nginx \
    --mount "type=bind,source=$tmp/nginx.conf,target=/tmp/supervisor.conf,readonly" \
    "$image" -c /tmp/supervisor.conf -g 'daemon off;' >/dev/null
docker exec "$name-supervisor" curl -fsS --retry 5 --retry-connrefused http://127.0.0.1/ >/dev/null

docker run -d --name "$name-app" --network "$name" -e SUPERVISOR_TOKEN=smoke-test \
    -p 127.0.0.1::3579 "$image" >/dev/null
address=$(docker port "$name-app" 3579/tcp)
for ((attempt = 0; attempt < 45; attempt++)); do
    if curl -fsS --max-time 2 \
        -H 'X-Ingress-Path: /api/hassio_ingress/smoke' \
        "http://$address/" -o "$tmp/response.html" 2>/dev/null \
        && grep -qi '<title>Ombi' "$tmp/response.html"; then
        if ! docker exec "$name-app" sh -ec 'test -s /config/Ombi.db && test "$(id -u abc)" = 1000'; then
            docker logs "$name-app" >&2
            exit 1
        fi
        echo "Ombi startup, ingress, database initialization, and service UID verified"
        exit 0
    fi
    sleep 2
done
docker logs "$name-app" >&2
exit 1
