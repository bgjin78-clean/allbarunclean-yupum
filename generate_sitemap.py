from pathlib import Path
from datetime import date

BASE_URL = "https://www.yupum.allbarunclean.com"

def generate():
    root = Path(__file__).resolve().parent
    regions_dir = root / "regions"

    urls = [BASE_URL + "/", BASE_URL + "/reviews/"]

    if regions_dir.exists():
        for folder in sorted(regions_dir.iterdir()):
            if folder.is_dir() and (folder / "index.html").exists():
                urls.append(f"{BASE_URL}/regions/{folder.name}/")

    reviews_dir = root / "reviews"
    if reviews_dir.exists():
        for index_file in sorted(reviews_dir.rglob("index.html")):
            rel = index_file.parent.relative_to(reviews_dir)
            if str(rel) == ".":
                continue
            urls.append(f"{BASE_URL}/reviews/{rel.as_posix()}/")

    today = date.today().isoformat()

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url in urls:
        priority = "1.0" if url == BASE_URL + "/" else "0.8"
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{url}</loc>")
        sitemap.append(f"    <lastmod>{today}</lastmod>")
        sitemap.append("    <changefreq>weekly</changefreq>")
        sitemap.append(f"    <priority>{priority}</priority>")
        sitemap.append("  </url>")

    sitemap.append("</urlset>")

    (root / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    robots = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    (root / "robots.txt").write_text(robots, encoding="utf-8")

    print(f"완료: sitemap.xml 생성")
    print(f"완료: robots.txt 생성")
    print(f"총 URL 수: {len(urls)}개")

if __name__ == "__main__":
    generate()