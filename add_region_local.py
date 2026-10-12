from pathlib import Path
import re

from generate_reviews import REGIONS, review_content
from add_keyword_reviews import EXTRA_REVIEWS
from region_local import REGION_LOCAL

START = "<!-- region-local-start -->"
END = "<!-- region-local-end -->"
ANCHOR = '<section class="soft" id="review">'


def region_local_html(region_type, name, slug):
    base = review_content(region_type, name, slug)
    links = [(f"/reviews/{slug}/", base["title"])]
    links += [
        (f"/reviews/{e['path']}/", e["title"])
        for e in EXTRA_REVIEWS
        if e["slug"] == slug
    ]
    link_html = "\n".join(f'        <a href="{href}">{title}</a>' for href, title in links)
    return f"""{START}
  <section class="seo-plus">
    <div class="wrap">
      <div class="title">
        <span>LOCAL</span>
        <h2>{name} 지역 특징과 작업 참고사항</h2>
        <p>{REGION_LOCAL[slug]}</p>
      </div>
      <div class="related-links">
{link_html}
      </div>
    </div>
  </section>
  {END}

  """


def generate():
    root = Path(__file__).resolve().parent
    updated = 0
    for region_type, name, slug in REGIONS:
        path = root / "regions" / slug / "index.html"
        html = path.read_text(encoding="utf-8")
        block = region_local_html(region_type, name, slug)

        if START in html:
            html = re.sub(
                re.escape(START) + r".*?" + re.escape(END) + r"\s*",
                lambda _: block,
                html,
                count=1,
                flags=re.S,
            )
        else:
            if ANCHOR not in html:
                raise RuntimeError(f"{slug}: 작업후기 섹션을 찾지 못했습니다.")
            html = html.replace(ANCHOR, block + ANCHOR, 1)

        path.write_text(html, encoding="utf-8")
        updated += 1

    print(f"완료: 지역 페이지 {updated}개에 지역 특징 섹션 반영")


if __name__ == "__main__":
    generate()
