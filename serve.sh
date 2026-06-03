#!/bin/bash
# 本地预览静态站。勿用 8080（本机常被 Spring Boot 占用 → Whitelabel 404）
set -e
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if [[ ! -f index.html ]]; then
  echo "错误：请在项目根目录运行（应包含 index.html）"
  exit 1
fi

if [[ ! -f data/routes.json ]] || [[ ! -f routes-data.js ]]; then
  echo "正在生成 data/routes.json 与 routes-data.js …"
  python3 scripts/build_site.py
fi

pick_port() {
  local p=$1
  while lsof -nP -iTCP:"$p" -sTCP:LISTEN >/dev/null 2>&1; do
    echo "端口 $p 已被占用，尝试 $((p + 1)) …" >&2
    p=$((p + 1))
  done
  echo "$p"
}

PORT=$(pick_port 8765)
BASE="http://127.0.0.1:${PORT}"

echo ""
echo "  站点目录: $ROOT"
echo "  ─────────────────────────────────────"
echo "  首页:     ${BASE}/index.html"
echo "  路线列表: ${BASE}/travel.html"
echo "  川藏攻略: ${BASE}/route.html?slug=chuanzang"
echo "  ─────────────────────────────────────"
echo "  不要用 http://localhost:8080 （那是 Java/Spring）"
echo "  按 Ctrl+C 停止"
echo ""

if command -v open >/dev/null 2>&1; then
  (sleep 0.8 && open "${BASE}/travel.html") &
fi

exec python3 -m http.server "$PORT" --bind 127.0.0.1
