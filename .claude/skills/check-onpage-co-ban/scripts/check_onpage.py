#!/usr/bin/env python3
"""
check_onpage.py - Kiem tra onpage co ban cho mot URL: Domain, Kha nang index
(robots.txt), Website metadata (OG tags, Viewport, Charset, Hreflang).
Chi dung thu vien chuan Python (khong can pip install).

Usage:
    python check_onpage.py https://example.com
"""

import sys
import re
import ssl
import urllib.request
import urllib.error
from collections import Counter
from urllib.parse import urlparse, urljoin
from html.parser import HTMLParser

TIMEOUT = 12
UA = "Mozilla/5.0 (compatible; SEONGON-OnpageChecker/1.0)"

PASS, WARN, FAIL, ERROR = "PASS", "WARN", "FAIL", "ERROR"


def fetch(url, method="GET"):
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method=method)
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            return {
                "ok": True,
                "status": resp.status,
                "final_url": resp.geturl(),
                "body": resp.read(),
            }
    except urllib.error.HTTPError as e:
        return {
            "ok": True,
            "status": e.code,
            "final_url": e.geturl() if hasattr(e, "geturl") else url,
            "body": e.read() if e.fp else b"",
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.metas = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "meta":
            self.metas.append(d)
        elif tag == "link":
            self.links.append(d)


def get_meta(metas, key, attr="name"):
    for m in metas:
        if m.get(attr, "").lower() == key.lower():
            return m
    return None


def row(label, status, detail):
    return {"label": label, "status": status, "detail": detail}


def check_domain(base_url):
    parsed = urlparse(base_url)
    host = parsed.netloc.split(":")[0]
    bare = host[4:] if host.startswith("www.") else host
    variants = [
        f"http://{bare}",
        f"https://{bare}",
        f"http://www.{bare}",
        f"https://www.{bare}",
    ]
    results = {}
    finals = []
    for v in variants:
        r = fetch(v)
        if r["ok"]:
            results[v] = r["final_url"]
            finals.append(r["final_url"].rstrip("/"))
        else:
            results[v] = f"LOI: {r['error']}"

    cnt = Counter(finals)
    top_final, top_count = (cnt.most_common(1)[0] if cnt else (None, 0))
    detail_lines = [f"{v} -> {results[v]}" for v in variants]
    if top_count >= 3:
        status = PASS
        note = f"{top_count}/4 phien ban redirect ve cung 1 URL: {top_final}"
    elif top_count == 2:
        status = WARN
        note = f"Chi {top_count}/4 phien ban thong nhat ve {top_final} - can ra soat redirect"
    else:
        status = FAIL
        note = "Cac phien ban www/non-www, http/https khong thong nhat ve 1 URL duy nhat"
    return [row("www & non-www / http & https", status,
                 note + "\n      " + "\n      ".join(detail_lines))]


def check_index(base_url):
    parsed = urlparse(base_url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    robots_url = urljoin(root, "/robots.txt")
    r = fetch(robots_url)
    if not (r.get("ok") and r["status"] == 200):
        return [row("Robots.txt", FAIL,
                     f"Khong tim thay /robots.txt (status: {r.get('status', r.get('error'))}).")]

    text = r["body"].decode("utf-8", errors="ignore")
    has_sitemap = bool(re.search(r"(?im)^sitemap:\s*\S+", text))
    blocks_root = bool(re.search(r"(?im)^disallow:\s*/\s*$", text))
    detail = "Co robots.txt."
    detail += " Co khai bao Sitemap:." if has_sitemap else " KHONG khai bao dong Sitemap:."
    if blocks_root:
        return [row("Robots.txt", FAIL, detail + " CANH BAO: co dong 'Disallow: /' chan toan bo site khoi index.")]
    status = PASS if has_sitemap else WARN
    return [row("Robots.txt", status, detail)]


def check_metadata(page):
    rows = []

    og_keys = ["og:locale", "og:type", "og:title", "og:description", "og:url", "og:image"]
    found = [k for k in og_keys if get_meta(page.metas, k, attr="property")]
    missing = [k for k in og_keys if k not in found]
    if not missing:
        rows.append(row("OG tags (Open Graph)", PASS,
                         f"Du 6 tag: {', '.join(found)}. Nen verify hien thi thuc te bang Facebook Debugger."))
    elif found:
        rows.append(row("OG tags (Open Graph)", WARN,
                         f"Thieu: {', '.join(missing)}. Da co: {', '.join(found)}."))
    else:
        rows.append(row("OG tags (Open Graph)", FAIL, "Khong tim thay OG tag nao."))

    viewport = get_meta(page.metas, "viewport")
    if viewport and "width=device-width" in viewport.get("content", "").replace(" ", ""):
        rows.append(row("Viewport", PASS, f'content="{viewport.get("content")}"'))
    elif viewport:
        rows.append(row("Viewport", WARN,
                         f'Co viewport nhung thieu width=device-width: content="{viewport.get("content")}"'))
    else:
        rows.append(row("Viewport", FAIL, 'Khong tim thay <meta name="viewport">.'))

    charset_meta = None
    for m in page.metas:
        if "charset" in m:
            charset_meta = m["charset"]
        elif m.get("http-equiv", "").lower() == "content-type" and "charset=" in m.get("content", "").lower():
            charset_meta = m["content"].lower().split("charset=")[-1]
    if charset_meta and "utf-8" in charset_meta.lower():
        rows.append(row("Charset", PASS, f"charset={charset_meta}"))
    elif charset_meta:
        rows.append(row("Charset", WARN, f"Co charset nhung khong phai UTF-8: {charset_meta}"))
    else:
        rows.append(row("Charset", FAIL, "Khong tim thay khai bao charset."))

    hreflangs = [l for l in page.links if l.get("rel", "").lower() == "alternate" and l.get("hreflang")]
    if hreflangs:
        detail = ", ".join(f'{l.get("hreflang")} -> {l.get("href")}' for l in hreflangs)
        rows.append(row("Hreflang", PASS, f"Co {len(hreflangs)} the hreflang: {detail}"))
    else:
        rows.append(row("Hreflang", WARN,
                         "Khong co the hreflang. Chi bat buoc neu site co nhieu phien ban ngon ngu/khu vuc - "
                         "xac nhan lai voi khach hang xem site co yeu cau da ngon ngu khong."))
    return rows


def print_report(url, sections):
    icon = {PASS: "[PASS]", WARN: "[WARN]", FAIL: "[FAIL]", ERROR: "[ERROR]"}
    print("=" * 78)
    print(f"BAO CAO CHECK ONPAGE CO BAN: {url}")
    print("=" * 78)
    counts = {PASS: 0, WARN: 0, FAIL: 0, ERROR: 0}
    for sec_name, rows in sections:
        print(f"\n### {sec_name}")
        for r in rows:
            counts[r["status"]] += 1
            print(f'  {icon[r["status"]]} {r["label"]}')
            for line in str(r["detail"]).split("\n"):
                print(f"      {line}")
    print("\n" + "-" * 78)
    print(f"Tong ket: PASS={counts[PASS]}  WARN={counts[WARN]}  FAIL={counts[FAIL]}  ERROR={counts[ERROR]}")
    print("-" * 78)


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_onpage.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    if not url.startswith("http"):
        url = "https://" + url

    r = fetch(url)
    if not r.get("ok"):
        print(f"Khong the tai trang {url}: {r.get('error')}")
        sys.exit(1)
    final_url = r["final_url"]
    html_text = r["body"].decode("utf-8", errors="ignore")
    page = MetaParser()
    page.feed(html_text)

    sections = [
        ("01. Domain", check_domain(final_url)),
        ("02. Kha nang index (robots.txt)", check_index(final_url)),
        ("03. Website metadata", check_metadata(page)),
    ]
    print_report(final_url, sections)


if __name__ == "__main__":
    main()
