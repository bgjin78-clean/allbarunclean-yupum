from pathlib import Path
from datetime import datetime, timezone

BASE_URL = "https://yupum.allbarunclean.com"
SITE_TITLE = "올바른 유품정리"
SITE_DESC = "서울·경기 유품정리, 고독사청소, 특수청소 전문 사이트"

def get_title(html, fallback):
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start + 7:end].strip()
    return fallback

def generate():
    root = Path(__file__).resolve().parent
    regions_dir = root / "regions"

    items = []

    index_html = (root / "index.html").read_text(encoding="utf-8")
    items.append((SITE_TITLE, BASE_URL + "/", SITE_DESC))

    items.append(("서울·경기 유품정리 작업후기 | 올바른 유품정리", BASE_URL + "/reviews/", "지역별 유품정리 작업후기 모음"))

    reviews_dir = root / "reviews"
    if reviews_dir.exists():
        for folder in sorted(reviews_dir.iterdir()):
            index_file = folder / "index.html"
            if folder.is_dir() and index_file.exists():
                html = index_file.read_text(encoding="utf-8")
                title = get_title(html, f"{folder.name} 작업후기 | 올바른 유품정리")
                link = f"{BASE_URL}/reviews/{folder.name}/"
                desc = title.replace(f"| {SITE_TITLE}", "").replace("| 올바른 유품정리", "").strip()
                items.append((title, link, desc))

    for folder in sorted(regions_dir.iterdir()):
        index_file = folder / "index.html"
        if index_file.exists():
            html = index_file.read_text(encoding="utf-8")
            title = get_title(html, f"{folder.name} 유품정리 | 올바른수거")
            link = f"{BASE_URL}/regions/{folder.name}/"
            desc = title.replace("| 올바른수거", "").strip()
            items.append((title, link, desc))

    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    rss = []
    rss.append('<?xml version="1.0" encoding="UTF-8"?>')
    rss.append('<rss version="2.0">')
    rss.append("<channel>")
    rss.append(f"<title>{SITE_TITLE}</title>")
    rss.append(f"<link>{BASE_URL}/</link>")
    rss.append(f"<description>{SITE_DESC}</description>")
    rss.append("<language>ko</language>")
    rss.append(f"<lastBuildDate>{now}</lastBuildDate>")

    for title, link, desc in items:
        rss.append("<item>")
        rss.append(f"<title>{title}</title>")
        rss.append(f"<link>{link}</link>")
        rss.append(f"<guid>{link}</guid>")
        rss.append(f"<description>{desc}</description>")
        rss.append(f"<pubDate>{now}</pubDate>")
        rss.append("</item>")

    rss.append("</channel>")
    rss.append("</rss>")

    (root / "rss.xml").write_text("\n".join(rss), encoding="utf-8")

    print(f"완료: rss.xml 생성")
    print(f"총 RSS 항목: {len(items)}개")

if __name__ == "__main__":
    generate()