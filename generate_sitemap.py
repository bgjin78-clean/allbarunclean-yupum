from pathlib import Path
from datetime import date
import subprocess

BASE_URL = "https://www.yupum.allbarunclean.com"


def last_modified(root, file_path):
    """git 마지막 커밋일. 커밋 전이거나 작업 중 수정된 파일은 오늘 날짜."""
    rel = file_path.relative_to(root).as_posix()
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--", rel],
        cwd=root, capture_output=True, text=True,
    ).stdout.strip()
    if dirty:
        return date.today().isoformat()
    committed = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", rel],
        cwd=root, capture_output=True, text=True,
    ).stdout.strip()
    return committed or date.today().isoformat()


def generate():
    root = Path(__file__).resolve().parent

    pages = [("/", root / "index.html"), ("/reviews/", root / "reviews" / "index.html")]

    regions_dir = root / "regions"
    if regions_dir.exists():
        for folder in sorted(regions_dir.iterdir()):
            if folder.is_dir() and (folder / "index.html").exists():
                pages.append((f"/regions/{folder.name}/", folder / "index.html"))

    reviews_dir = root / "reviews"
    if reviews_dir.exists():
        for index_file in sorted(reviews_dir.rglob("index.html")):
            rel = index_file.parent.relative_to(reviews_dir)
            if str(rel) == ".":
                continue
            pages.append((f"/reviews/{rel.as_posix()}/", index_file))

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path, file_path in pages:
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{BASE_URL}{path}</loc>")
        sitemap.append(f"    <lastmod>{last_modified(root, file_path)}</lastmod>")
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
    print(f"총 URL 수: {len(pages)}개")


if __name__ == "__main__":
    generate()
