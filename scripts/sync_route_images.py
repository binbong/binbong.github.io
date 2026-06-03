#!/usr/bin/env python3
"""Download missing route images; search Wikimedia Commons on failure."""

import json
import re
import shutil
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from routes_data import ROUTES

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "images" / "routes"
UA = "CheXingTianXia/1.0 (https://tahoo.me; contact@tahoo.me)"
CTX = ssl.create_default_context()


def fetch(url: str, timeout: int = 60) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
        return resp.read()


def commons_search(query: str) -> str | None:
    params = urllib.parse.urlencode(
        {
            "action": "query",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": 6,
            "gsrlimit": 5,
            "prop": "imageinfo",
            "iiprop": "url",
            "iiurlwidth": 1280,
            "format": "json",
        }
    )
    try:
        data = json.loads(fetch(f"https://commons.wikimedia.org/w/api.php?{params}", 30))
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            info = page.get("imageinfo", [{}])[0]
            url = info.get("thumburl") or info.get("url")
            if url and url.startswith("https://"):
                return url
    except Exception as e:
        print(f"  API search failed for {query!r}: {e}")
    return None


def save_url(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = fetch(url)
        if len(data) < 800:
            return False
        if url.lower().endswith(".svg") or ".svg" in url.lower():
            dest = dest.with_suffix(".svg")
        elif url.lower().endswith(".png") or "/png" in url.lower().split("?")[0]:
            dest = dest.with_suffix(".png")
        dest.write_bytes(data)
        print(f"  saved {dest.relative_to(ROOT)} ({len(data)//1024} KB)")
        return True
    except Exception as e:
        print(f"  download error: {e}")
        return False


def is_ok(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 5000


def local_fallback(slug_dir: Path, dest: Path) -> bool:
    for name in ("gallery-1.jpg", "gallery-2.jpg", "hero.jpg"):
        src = slug_dir / name
        if is_ok(src) and src != dest:
            shutil.copy2(src, dest)
            print(f"  copied fallback {name} -> {dest.name}")
            return True
    return False


def ensure_image(slug: str, dest: Path, url: str, caption: str) -> Path | None:
    slug_dir = dest.parent
    if is_ok(dest):
        return dest
    print(f"{slug}/{dest.name}: trying URL...")
    if save_url(url, dest) and is_ok(dest):
        return dest
    print(f"{slug}/{dest.name}: searching Commons for {caption!r}...")
    alt = commons_search(caption) or commons_search(f"{caption} China")
    if alt and save_url(alt, dest) and is_ok(dest):
        return dest
    if local_fallback(slug_dir, dest):
        return dest
    print(f"  FAILED {slug}/{dest.name}")
    return None


def ensure_hero(slug_dir: Path, url: str, slug: str) -> None:
    dest = slug_dir / "hero.jpg"
    if is_ok(dest):
        return
    print(f"{slug}/hero: downloading...")
    if not save_url(url, dest) or not is_ok(dest):
        local_fallback(slug_dir.parent / slug, dest)


def main():
    updated = {}
    for route in ROUTES:
        slug = route["slug"]
        slug_dir = IMAGES_DIR / slug
        slug_dir.mkdir(parents=True, exist_ok=True)
        ensure_hero(slug_dir, route["images"]["hero"], slug)
        gallery_paths = []
        for i, item in enumerate(route["images"]["gallery"]):
            url = item["url"] if isinstance(item, dict) else item
            caption = item.get("caption", route["name"]) if isinstance(item, dict) else route["name"]
            dest = slug_dir / f"gallery-{i + 1}.jpg"
            result = ensure_image(slug, dest, url, caption)
            if result:
                gallery_paths.append(str(result.relative_to(ROOT)).replace("\\", "/"))
            time.sleep(0.3)
        updated[slug] = gallery_paths
    out = ROOT / "scripts" / "local_image_paths.json"
    out.write_text(json.dumps(updated, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
