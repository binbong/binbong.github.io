#!/usr/bin/env python3
"""Generate route detail pages and update travel.html from routes data."""

import re
import urllib.request
from pathlib import Path

from routes_data import ROUTES

ROOT = Path(__file__).resolve().parent.parent
ROUTES_DIR = ROOT / "routes"
IMAGES_DIR = ROOT / "images" / "routes"
UA = "CheXingTianXia/1.0 (personal travel site; contact@tahoo.me)"


def download(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 5000:
        return str(dest.relative_to(ROOT)).replace("\\", "/")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) < 1000:
            raise ValueError("image too small")
        dest.write_bytes(data)
        return str(dest.relative_to(ROOT)).replace("\\", "/")
    except Exception as e:
        print(f"WARN download failed {dest.name}: {e}")
        return url


def image_ref(path_or_url: str) -> str:
    if path_or_url.startswith("http"):
        return path_or_url
    return f"../{path_or_url}"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_detail(route: dict, paths: dict) -> str:
    hero = paths["hero"]
    gallery_html = "".join(
        f'<figure class="detail-gallery-item"><img src="{image_ref(p["path"])}" alt="{esc(p["caption"])}">'
        f'<figcaption>{esc(p["caption"])}</figcaption></figure>'
        for p in paths["gallery"]
    )
    overview_html = "".join(
        f'<p class="detail-overview-p">{esc(p)}</p>' for p in route.get("overview", [])
    )
    days_html = "".join(
        f"""<article class="detail-day">
            <div class="detail-day-head">
                <span class="detail-day-num">{esc(d["day"])}</span>
                <h3 class="detail-day-title">{esc(d["title"])}</h3>
            </div>
            <p class="detail-day-meta">{esc(d.get("drive", ""))}{" · " if d.get("drive") and d.get("stay") else ""}{esc(d.get("stay", ""))}</p>
            <p class="detail-day-text">{esc(d["text"])}</p>
        </article>"""
        for d in route.get("days", [])
    )
    spots_html = "".join(
        f"""<div class="detail-spot">
            <h3 class="detail-spot-name">{esc(s["name"])}</h3>
            <p class="detail-spot-text">{esc(s["text"])}</p>
        </div>"""
        for s in route.get("spots", [])
    )
    stops_html = "".join(
        f"""<div class="route-stop">
            <span class="route-stop-num">{i + 1}</span>
            <div>
                <strong>{esc(s["name"])}</strong><span class="route-stop-km">{esc(s["km"])}</span>
                <p>{esc(s["note"])}</p>
                {f'<p class="route-stop-detail">{esc(s["detail"])}</p>' if s.get("detail") else ""}
            </div>
        </div>"""
        for i, s in enumerate(route["stops"])
    )
    practical_html = "".join(f"<li>{esc(t)}</li>" for t in route.get("practical", []))
    ev_html = "".join(f"<li>{esc(t)}</li>" for t in route["ev_tips"])
    tags_html = "".join(f'<span class="route-tag">{esc(t)}</span>' for t in route["tags"])

    route_map_html = ""
    if paths.get("route_map"):
        rm = paths["route_map"]
        route_map_html = f"""
        <section class="detail-section">
            <p class="section-eyebrow">Route Map</p>
            <h2 class="section-title">路线示意图</h2>
            <figure class="detail-route-map">
                <img src="{image_ref(rm["path"])}" alt="{esc(rm["caption"])}">
                <figcaption>{esc(rm["caption"])}</figcaption>
            </figure>
        </section>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="darkreader-lock">
    <style id="theme-lock">
      html {{ color-scheme: only dark; background: #0a0a0a; color: #f5f5f7; }}
      body {{ background: #0a0a0a; color: #f5f5f7; }}
      .hero-title, .detail-hero .hero-title {{ color: #fff !important; -webkit-text-fill-color: #fff !important; }}
      .hero-subtitle, .detail-hero .hero-subtitle {{ color: rgba(255,255,255,.9) !important; -webkit-text-fill-color: rgba(255,255,255,.9) !important; }}
      .detail-stat-val, .detail-stat-lbl {{ color: #fff !important; -webkit-text-fill-color: #fff !important; }}
      .detail-lead-text {{ color: #f5f5f7 !important; -webkit-text-fill-color: #f5f5f7 !important; }}
    </style>
    <script src="../theme-guard.js" defer></script>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="dark">
    <title>{esc(route["name"])} — 车行天下</title>
    <meta name="description" content="{esc(route["summary"])}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css?v=4">
    <link rel="stylesheet" href="../route-detail.css?v=4">
</head>
<body>

<nav class="nav" id="nav">
    <a href="../index.html" class="nav-logo">车行<span>天下</span></a>
    <ul class="nav-links" id="navLinks">
        <li><a href="../index.html">首页</a></li>
        <li><a href="../travel.html" class="active">自驾游</a></li>
        <li><a href="../index.html#vehicle">我的座驾</a></li>
        <li><a href="../index.html#care">养护指南</a></li>
        <li><a href="../index.html#about">关于</a></li>
    </ul>
    <button class="nav-toggle" id="navToggle" aria-label="菜单">
        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
</nav>

<section class="detail-hero">
    <div class="detail-hero-bg" style="background-image:url('{image_ref(hero)}')"></div>
    <div class="hero-overlay"></div>
    <div class="detail-hero-content">
        <a href="../travel.html" class="detail-back">← 返回路线列表</a>
        <span class="hero-eyebrow">{esc(route["tagline"])}</span>
        <h1 class="hero-title">{esc(route["name"])}</h1>
        <p class="hero-subtitle">{esc(route["summary"])}</p>
        <div class="detail-stats">
            <div><span class="detail-stat-val">{esc(route["distance"])}</span><span class="detail-stat-lbl">总里程</span></div>
            <div><span class="detail-stat-val">{esc(route["duration"])}</span><span class="detail-stat-lbl">建议天数</span></div>
            <div><span class="detail-stat-val">{esc(route["season"])}</span><span class="detail-stat-lbl">最佳季节</span></div>
        </div>
    </div>
</section>

<article class="detail-body">
    <div class="detail-inner">
        <div class="detail-lead">
            <p class="detail-lead-text">{esc(route["intro"])}</p>
            <div class="detail-overview">{overview_html}</div>
            <div class="route-highlights detail-tags">{tags_html}</div>
        </div>

        <section class="detail-section">
            <p class="section-eyebrow">Itinerary</p>
            <h2 class="section-title">分日行程</h2>
            <div class="detail-days">{days_html}</div>
        </section>

        <section class="detail-section">
            <p class="section-eyebrow">Photo Essay</p>
            <h2 class="section-title">沿途影像</h2>
            <div class="detail-gallery detail-gallery-wide">{gallery_html}</div>
        </section>

        <section class="detail-section">
            <p class="section-eyebrow">Highlights</p>
            <h2 class="section-title">核心景点</h2>
            <div class="detail-spots">{spots_html}</div>
        </section>

        <section class="detail-section">
            <p class="section-eyebrow">Route</p>
            <h2 class="section-title">途经站点</h2>
            <div class="route-stops route-stops-full">{stops_html}</div>
        </section>
        {route_map_html}

        <section class="detail-section">
            <p class="section-eyebrow">Practical</p>
            <h2 class="section-title">实用信息</h2>
            <ul class="detail-list">{practical_html}</ul>
        </section>

        <section class="detail-section detail-ev">
            <p class="section-eyebrow">EV Tips</p>
            <h2 class="section-title">新能源出行提示</h2>
            <p class="section-desc">驾驶腾势 N7 等纯电 SUV 出发前，请特别注意以下事项：</p>
            <ul class="detail-list detail-ev-list">{ev_html}</ul>
        </section>
    </div>
</article>

<section class="detail-nav-bottom">
    <div class="detail-inner detail-nav-inner">
        <a href="../travel.html" class="btn btn-ghost">← 全部路线</a>
    </div>
</section>

<footer class="footer">
    <div class="footer-inner">
        <div>
            <div class="footer-brand">车行<span>天下</span></div>
            <p class="footer-desc">新能源自驾与用车笔记。驾驶腾势 N7，探索中国之美。</p>
        </div>
        <div class="footer-links">
            <div class="footer-col">
                <h4>栏目</h4>
                <ul>
                    <li><a href="../travel.html">自驾游</a></li>
                    <li><a href="../index.html#vehicle">我的座驾</a></li>
                    <li><a href="../index.html#care">养护指南</a></li>
                </ul>
            </div>
        </div>
    </div>
    <div class="footer-bottom"><p>© 2026 车行天下 · tahoo.me</p></div>
</footer>

<script>
    const nav = document.getElementById('nav');
    window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 50));
    document.getElementById('navToggle').addEventListener('click', () => document.getElementById('navLinks').classList.toggle('open'));
</script>
</body>
</html>"""


def render_travel_card(route: dict, thumb: str) -> str:
    tags = "".join(f'<span class="route-tag">{esc(t)}</span>' for t in route["tags"])
    return f"""
            <a href="routes/{route["slug"]}.html" class="route-card route-card-link" data-region="{esc(route["region"])}">
                <div class="route-card-image">
                    <img src="{thumb}" alt="{esc(route["name"])}">
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


def normalize_gallery(route: dict) -> list:
    gallery = route["images"]["gallery"]
    out = []
    for item in gallery:
        if isinstance(item, dict):
            out.append(item)
        else:
            out.append({"url": item, "caption": route["name"]})
    return out


def main():
    ROUTES_DIR.mkdir(exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    card_html = []

    for route in ROUTES:
        slug = route["slug"]
        slug_dir = IMAGES_DIR / slug
        hero_path = download(route["images"]["hero"], slug_dir / "hero.jpg")
        gallery_paths = []
        for i, item in enumerate(normalize_gallery(route)):
            gallery_paths.append(
                {
                    "path": download(item["url"], slug_dir / f"gallery-{i + 1}.jpg"),
                    "caption": item["caption"],
                }
            )

        paths = {"hero": hero_path, "gallery": gallery_paths}
        if route.get("route_map"):
            rm = route["route_map"]
            ext = ".svg" if rm["url"].lower().endswith(".svg") else ".jpg"
            rm_path = download(rm["url"], slug_dir / f"route-map{ext}")
            if not rm_path.startswith("http"):
                paths["route_map"] = {"path": rm_path, "caption": rm["caption"]}

        detail_path = ROUTES_DIR / f"{slug}.html"
        detail_path.write_text(render_detail(route, paths), encoding="utf-8")
        card_html.append(render_travel_card(route, hero_path))
        print(f"OK {slug}")

    travel_path = ROOT / "travel.html"
    content = travel_path.read_text(encoding="utf-8")
    new_grid = "\n".join(card_html) + "\n"
    content = re.sub(
        r'(<div class="route-grid" id="routeGrid">).*?(</div>\s*</div>\s*</section>)',
        rf"\1{new_grid}        \2",
        content,
        count=1,
        flags=re.DOTALL,
    )
    content = re.sub(
        r"(class=\"page-hero\">[\s\S]*?background-image: url\(')[^']+('\);)",
        r"\1images/routes/qinggan/hero.jpg\2",
        content,
        count=1,
    )
    content = re.sub(
        r"(class=\"quote-banner-bg\" style=\"background-image: url\(')[^']+('\);)",
        r"\1images/routes/chuanzang/hero.jpg\2",
        content,
        count=1,
    )
    travel_path.write_text(content, encoding="utf-8")
    print("Updated travel.html")


if __name__ == "__main__":
    main()
