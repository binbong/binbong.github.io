#!/usr/bin/env python3
"""Build deployable site under docs/ from routes_data.py."""

import json
import re
from pathlib import Path

from routes_data import ROUTES

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT
DATA_DIR = SITE_DIR / "data"
ASSETS_JS = SITE_DIR / "assets" / "js"
TRAVEL_HTML = SITE_DIR / "travel.html"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_travel_card(route: dict) -> str:
    slug = route["slug"]
    thumb = f"images/routes/{slug}/hero.jpg"
    tags = "".join(f'<span class="route-tag">{esc(t)}</span>' for t in route["tags"])
    href = f"route.html?slug={slug}"
    return f"""            <a href="{href}" class="route-card route-card-link" data-region="{esc(route["region"])}">
                <div class="route-card-image">
                    <img src="{thumb}" alt="{esc(route["name"])}" loading="lazy">
                </div>
                <div class="route-card-body">
                    <p class="route-card-region">{esc(route["tagline"])}</p>
                    <h3 class="route-card-title">{esc(route["name"])}</h3>
                    <p class="route-card-desc">{esc(route["summary"])}</p>
                    <div class="route-meta">
                        <span class="route-meta-item"><strong>里程</strong> {esc(route["distance"])}</span>
                        <span class="route-meta-item"><strong>建议</strong> {esc(route["duration"])}</span>
                        <span class="route-meta-item"><strong>最佳</strong> {esc(route["season"])}</span>
                    </div>
                    <div class="route-highlights">{tags}</div>
                    <span class="route-card-cta">查看详情 →</span>
                </div>
            </a>"""


def normalize_route(route: dict) -> dict:
    slug = route["slug"]
    gallery = []
    for i, item in enumerate(route["images"]["gallery"]):
        caption = item["caption"] if isinstance(item, dict) else route["name"]
        gallery.append(
            {
                "src": f"images/routes/{slug}/gallery-{i + 1}.jpg",
                "caption": caption,
            }
        )
    return {
        "slug": route["slug"],
        "name": route["name"],
        "region": route["region"],
        "tagline": route["tagline"],
        "distance": route["distance"],
        "duration": route["duration"],
        "season": route["season"],
        "tags": route["tags"],
        "summary": route["summary"],
        "intro": route["intro"],
        "overview": route.get("overview", []),
        "days": route.get("days", []),
        "spots": route.get("spots", []),
        "stops": route.get("stops", []),
        "practical": route.get("practical", []),
        "ev_tips": route["ev_tips"],
        "images": {
            "hero": f"images/routes/{slug}/hero.jpg",
            "gallery": gallery,
        },
    }


def export_data_files() -> tuple[Path, Path]:
    """Write JSON (for fetch) and JS bundle (for file:// without a server)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data = [normalize_route(r) for r in ROUTES]
    json_path = DATA_DIR / "routes.json"
    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    ASSETS_JS.mkdir(parents=True, exist_ok=True)
    js_path = ASSETS_JS / "routes-data.js"
    js_path.write_text(
        "window.ROUTES_DATA=" + json.dumps(data, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    return json_path, js_path


def update_travel_html() -> None:
    cards = "\n".join(render_travel_card(r) for r in ROUTES) + "\n"
    content = TRAVEL_HTML.read_text(encoding="utf-8")
    content = re.sub(
        r'(<div class="route-grid" id="routeGrid">).*?(</div>\s*</div>\s*</section>)',
        rf"\1\n{cards}        \2",
        content,
        count=1,
        flags=re.DOTALL,
    )
    TRAVEL_HTML.write_text(content, encoding="utf-8")


def main():
    if not SITE_DIR.is_dir():
        raise SystemExit(f"缺少发布目录 {SITE_DIR}")
    json_path, js_path = export_data_files()
    update_travel_html()
    print(f"Site output: {SITE_DIR} (repository root, GitHub Pages /)")
    print(f"Wrote {json_path} ({len(ROUTES)} routes)")
    print(f"Wrote {js_path}")


if __name__ == "__main__":
    main()
