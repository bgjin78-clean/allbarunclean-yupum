from pathlib import Path
import re

BRAND = "올바른 유품정리"
PHONE = "010-4393-2414"
PHONE_LINK = "01043932414"

REGIONS = {
    "gangnam": "강남구", "gangdong": "강동구", "gangbuk": "강북구", "gangseo": "강서구",
    "gwanak": "관악구", "gwangjin": "광진구", "guro": "구로구", "geumcheon": "금천구",
    "nowon": "노원구", "dobong": "도봉구", "dongdaemun": "동대문구", "dongjak": "동작구",
    "mapo": "마포구", "seodaemun": "서대문구", "seocho": "서초구", "seongdong": "성동구",
    "seongbuk": "성북구", "songpa": "송파구", "yangcheon": "양천구", "yeongdeungpo": "영등포구",
    "yongsan": "용산구", "eunpyeong": "은평구", "jongno": "종로구", "jung": "중구",
    "jungnang": "중랑구", "suwon": "수원시", "seongnam": "성남시", "goyang": "고양시",
    "yongin": "용인시", "bucheon": "부천시", "ansan": "안산시", "anyang": "안양시",
    "namyangju": "남양주시", "hwaseong": "화성시", "pyeongtaek": "평택시", "uijeongbu": "의정부시",
    "siheung": "시흥시", "paju": "파주시", "gimpo": "김포시", "gwangmyeong": "광명시",
    "gwangju": "광주시", "gunpo": "군포시", "osan": "오산시", "icheon": "이천시",
    "yangju": "양주시", "guri": "구리시", "anseong": "안성시", "pocheon": "포천시",
    "uiwang": "의왕시", "hanam": "하남시", "yeoju": "여주시", "dongducheon": "동두천시",
    "gwacheon": "과천시", "gapyeong": "가평군", "yangpyeong": "양평군", "yeoncheon": "연천군",
}

PHASE3_CSS = """
    .nav-links {
      display:flex; flex-wrap:wrap; gap:14px;
      font-size:14px; font-weight:700; color:var(--muted);
    }
    .review-promo {
      background:var(--card); border:1px solid var(--line); border-radius:22px;
      padding:28px; box-shadow:0 10px 28px rgba(54,90,76,0.07);
    }
    .review-promo p { margin:0 0 18px; color:var(--muted); }
    .btn-row { display:flex; flex-wrap:wrap; gap:12px; }
    .related-section { background:var(--soft); }
    .related-grid {
      display:grid; grid-template-columns:repeat(2,1fr); gap:18px;
    }
    .related-card {
      display:block; background:var(--card); border:1px solid var(--line);
      border-radius:22px; padding:28px; box-shadow:0 10px 28px rgba(54,90,76,0.07);
    }
    .related-card h3 { margin:0 0 10px; color:var(--main); font-size:20px; }
    .related-card p { margin:0 0 14px; color:var(--muted); font-size:15px; }
    .related-card span { color:var(--main); font-weight:900; font-size:15px; }
    .footer-links a {
      display:inline-block; margin-right:10px; color:var(--main); font-weight:700;
    }
    @media(max-width:900px) {
      .nav-links { display:none; }
      .related-grid { grid-template-columns:1fr; }
    }
"""


def header_html(slug):
    return f"""<header>
  <div class="nav">
    <a href="/" class="logo">{BRAND}</a>
    <nav class="nav-links">
      <a href="/#service">서비스</a>
      <a href="/reviews/{slug}/">작업후기</a>
      <a href="/#area">지역안내</a>
      <a href="#contact">상담접수</a>
    </nav>
    <a href="tel:{PHONE_LINK}" class="call">{PHONE}</a>
  </div>
</header>"""


def review_section(name, slug):
    return f"""  <section class="soft" id="review">
    <div class="wrap">
      <div class="title">
        <span>REVIEW</span>
        <h2>{name} 유품정리 작업후기</h2>
        <p>{name} 현장에서 진행한 유품정리·고독사청소·특수청소 작업후기를 확인할 수 있습니다.</p>
      </div>
      <div class="review-promo">
        <p>작업 전·후 현장 사진과 정리 과정을 {name} 작업후기 페이지에서 확인하세요.</p>
        <div class="btn-row">
          <a href="/reviews/{slug}/" class="btn btn-primary">{name} 작업후기 보기</a>
          <a href="/reviews/" class="btn btn-outline">전체 작업후기</a>
        </div>
      </div>
    </div>
  </section>

"""


def related_section_html():
    return """
  <section class="related-section">
    <div class="wrap">
      <div class="title">
        <span>올바른 관련 서비스</span>
        <h2>서울·경기 올바른 서비스 바로가기</h2>
      </div>
      <div class="related-grid">
        <a href="https://www.allbarunclean.com/" class="related-card" target="_blank" rel="noopener">
          <h3>올바른수거</h3>
          <p>서울·경기 전 지역 쓰레기집청소, 빈집정리, 유품·고독사·특수청소 등 종합 정리 서비스를 안내합니다.</p>
          <span>www.allbarunclean.com →</span>
        </a>
        <a href="https://www.waste.allbarunclean.com/" class="related-card" target="_blank" rel="noopener">
          <h3>올바른폐기물처리</h3>
          <p>서울·경기 전 지역 가정폐기물, 이사폐기물, 빈집정리, 폐업폐기물 등 폐기물 처리 서비스를 안내합니다.</p>
          <span>www.waste.allbarunclean.com →</span>
        </a>
      </div>
    </div>
  </section>
"""


def footer_html(name, slug):
    return f"""<footer>
  <div class="footer-inner">
    <div>
      <strong>{BRAND}</strong><br />
      {name} 유품정리 · 고독사청소 · 특수청소
    </div>
    <div class="footer-links">
      대표 상담 : <a href="tel:{PHONE_LINK}">{PHONE}</a><br />
      <a href="https://www.allbarunclean.com/" target="_blank" rel="noopener">올바른수거 · allbarunclean.com</a>
      <a href="https://www.waste.allbarunclean.com/" target="_blank" rel="noopener">올바른폐기물처리 · waste.allbarunclean.com</a><br />
      <a href="/reviews/">작업후기 모음</a>
      <a href="/reviews/{slug}/">{name} 작업후기</a>
    </div>
  </div>
</footer>"""


def upgrade_html(html, slug, name):
    html = html.replace("올바른수거", BRAND)

    if ".nav-links" not in html:
        html = html.replace("</style>", PHASE3_CSS + "\n  </style>")

    html = re.sub(r"<header>.*?</header>", header_html(slug), html, count=1, flags=re.DOTALL)

    if 'id="review"' not in html:
        html = html.replace(
            '<section class="contact" id="contact">',
            review_section(name, slug) + '  <section class="contact" id="contact">',
        )

    if '<section class="related-section">' not in html:
        html = html.replace("</main>", related_section_html() + "\n</main>")

    html = re.sub(r"<footer>.*?</footer>", footer_html(name, slug), html, count=1, flags=re.DOTALL)

    return html


def upgrade():
    root = Path(__file__).resolve().parent
    regions_dir = root / "regions"
    count = 0

    for slug, name in REGIONS.items():
        file_path = regions_dir / slug / "index.html"
        if not file_path.exists():
            print(f"건너뜀: {slug}")
            continue

        html = file_path.read_text(encoding="utf-8")
        html = upgrade_html(html, slug, name)
        file_path.write_text(html, encoding="utf-8")
        print(f"완료: {name} ({slug})")
        count += 1

    print(f"\n총 {count}개 지역 페이지 3단계 업그레이드 완료")


if __name__ == "__main__":
    upgrade()
