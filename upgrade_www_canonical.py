from pathlib import Path
import re

OLD_BASE = "https://yupum.allbarunclean.com"
NEW_BASE = "https://www.yupum.allbarunclean.com"


def canonical_url(html, file_path, root):
    rel = file_path.relative_to(root).as_posix()
    if rel == "index.html":
        return NEW_BASE + "/"
    if rel.startswith("regions/") and rel.endswith("/index.html"):
        slug = rel.split("/")[1]
        return f"{NEW_BASE}/regions/{slug}/"
    if rel == "reviews/index.html":
        return f"{NEW_BASE}/reviews/"
    if rel.startswith("reviews/") and rel.endswith("/index.html"):
        slug = rel.split("/")[1]
        return f"{NEW_BASE}/reviews/{slug}/"
    match = re.search(r'<meta property="og:url" content="([^"]+)"', html)
    if match:
        return match.group(1).replace(OLD_BASE, NEW_BASE)
    return None


def add_canonical(html, url):
    if 'rel="canonical"' in html:
        html = re.sub(
            r'<link rel="canonical" href="[^"]+"\s*/?>',
            f'<link rel="canonical" href="{url}" />',
            html,
            count=1,
        )
        return html

    marker = '<meta name="viewport" content="width=device-width, initial-scale=1.0" />'
    canonical_tag = f'{marker}\n\n  <link rel="canonical" href="{url}" />'
    if marker in html:
        return html.replace(marker, canonical_tag, 1)
    return html


def upgrade_file(file_path, root):
    html = file_path.read_text(encoding="utf-8")
    original = html

    html = html.replace(OLD_BASE, NEW_BASE)
    url = canonical_url(html, file_path, root)
    if url:
        html = add_canonical(html, url)

    if html != original:
        file_path.write_text(html, encoding="utf-8")
        return True
    return False


def upgrade():
    root = Path(__file__).resolve().parent
    targets = [root / "index.html"]
    targets.extend((root / "regions").glob("*/index.html"))
    targets.extend((root / "reviews").glob("**/index.html"))

    count = 0
    for file_path in sorted(targets):
        if file_path.exists() and upgrade_file(file_path, root):
            count += 1
            print(f"updated: {file_path.relative_to(root)}")

    print(f"\n완료: {count}개 HTML 파일 www + canonical 적용")


if __name__ == "__main__":
    upgrade()
