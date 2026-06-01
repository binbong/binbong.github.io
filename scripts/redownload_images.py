#!/usr/bin/env python3
"""Re-download all route images from routes_data.py."""

import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

from routes_data import ROUTES

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "images" / "routes"
UA = "CheXingTianXia/1.0 (https://tahoo.me; contact@tahoo.me) Python-urllib"


def download(url: str, dest: Path, force: bool = False) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not force and dest.exists() and dest.stat().st_size > 5000:
        return True
    ext = dest.suffix.lower()
    if url.lower().endswith(".svg") and ext != ".svg":
        dest = dest.with_suffix(".svg")
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": UA,
                    "Accept": "image/*,*/*",
                },
            )
            ctx = ssl.create_default_context()
            with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                data = resp.read()
            if len(data) < 800:
                raise ValueError(f"too small ({len(data)} bytes)")
            dest.write_bytes(data)
            print(f"OK  {dest.relative_to(ROOT)} ({len(data)//1024} KB)")
            return True
        except Exception as e:
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))
            else:
                print(f"FAIL {dest.name}: {e}")
                print(f"     {url[:100]}...")
                return False
    return False


def main():
    ok = fail = skip = 0
    for route in ROUTES:
        slug = route["slug"]
        slug_dir = IMAGES_DIR / slug
        if download(route["images"]["hero"], slug_dir / "hero.jpg"):
            ok += 1
        else:
            fail += 1
        for i, item in enumerate(route["images"]["gallery"]):
            url = item["url"] if isinstance(item, dict) else item
            if download(url, slug_dir / f"gallery-{i + 1}.jpg"):
                ok += 1
            else:
                fail += 1
        if route.get("route_map"):
            rm = route["route_map"]
            dest = slug_dir / ("route-map.svg" if rm["url"].endswith(".svg") else "route-map.jpg")
            if download(rm["url"], dest):
                ok += 1
            else:
                fail += 1
    print(f"\nDone: {ok} ok, {fail} failed")


if __name__ == "__main__":
    main()
