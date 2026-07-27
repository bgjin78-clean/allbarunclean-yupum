from pathlib import Path
from datetime import date
import random
import json

BASE_URL = "https://www.yupum.allbarunclean.com"
PHONE = "010-4393-2414"
PHONE_LINK = "01043932414"

REGIONS = [
    ("서울", "강남구", "gangnam"), ("서울", "강동구", "gangdong"), ("서울", "강북구", "gangbuk"),
    ("서울", "강서구", "gangseo"), ("서울", "관악구", "gwanak"), ("서울", "광진구", "gwangjin"),
    ("서울", "구로구", "guro"), ("서울", "금천구", "geumcheon"), ("서울", "노원구", "nowon"),
    ("서울", "도봉구", "dobong"), ("서울", "동대문구", "dongdaemun"), ("서울", "동작구", "dongjak"),
    ("서울", "마포구", "mapo"), ("서울", "서대문구", "seodaemun"), ("서울", "서초구", "seocho"),
    ("서울", "성동구", "seongdong"), ("서울", "성북구", "seongbuk"), ("서울", "송파구", "songpa"),
    ("서울", "양천구", "yangcheon"), ("서울", "영등포구", "yeongdeungpo"), ("서울", "용산구", "yongsan"),
    ("서울", "은평구", "eunpyeong"), ("서울", "종로구", "jongno"), ("서울", "중구", "jung"),
    ("서울", "중랑구", "jungnang"),

    ("경기", "수원시", "suwon"), ("경기", "성남시", "seongnam"), ("경기", "고양시", "goyang"),
    ("경기", "용인시", "yongin"), ("경기", "부천시", "bucheon"), ("경기", "안산시", "ansan"),
    ("경기", "안양시", "anyang"), ("경기", "남양주시", "namyangju"), ("경기", "화성시", "hwaseong"),
    ("경기", "평택시", "pyeongtaek"), ("경기", "의정부시", "uijeongbu"), ("경기", "시흥시", "siheung"),
    ("경기", "파주시", "paju"), ("경기", "김포시", "gimpo"), ("경기", "광명시", "gwangmyeong"),
    ("경기", "광주시", "gwangju"), ("경기", "군포시", "gunpo"), ("경기", "오산시", "osan"),
    ("경기", "이천시", "icheon"), ("경기", "양주시", "yangju"), ("경기", "구리시", "guri"),
    ("경기", "안성시", "anseong"), ("경기", "포천시", "pocheon"), ("경기", "의왕시", "uiwang"),
    ("경기", "하남시", "hanam"), ("경기", "여주시", "yeoju"), ("경기", "동두천시", "dongducheon"),
    ("경기", "과천시", "gwacheon"), ("경기", "가평군", "gapyeong"), ("경기", "양평군", "yangpyeong"),
    ("경기", "연천군", "yeoncheon"),
]

SEO_INTROS = [
    "유품정리는 단순히 물건을 치우는 일이 아니라 남겨진 물품을 확인하고 가족분들이 필요한 물건을 구분하는 과정입니다.",
    "갑작스럽게 정리가 필요한 상황에서는 어디서부터 시작해야 할지 막막할 수 있습니다. 올바른 유품정리는 현장 상황을 먼저 확인하고 필요한 작업만 안내합니다.",
    "공간의 크기, 물품의 양, 반출 환경, 특수청소 필요 여부에 따라 작업 범위와 비용은 달라질 수 있습니다.",
    "고독사청소나 특수청소가 함께 필요한 경우 일반 정리와는 다른 절차가 필요합니다. 오염 정리, 소독, 냄새 저감까지 현장에 맞춰 진행합니다.",
]

def get_related_links(current_slug, current_type):
    same_area = [r for r in REGIONS if r[0] == current_type and r[2] != current_slug]
    other_area = [r for r in REGIONS if r[0] != current_type]

    random.seed(current_slug)
    selected = random.sample(same_area, min(8, len(same_area))) + random.sample(other_area, min(4, len(other_area)))

    links = []
    for _, name, slug in selected:
        links.append(f'<a href="/regions/{slug}/">{name} 유품정리</a>')
    return "\n".join(links)

def schema_json(region_type, name, slug, title, desc):
    url = f"{BASE_URL}/regions/{slug}/"

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"{name} 유품정리 비용은 어떻게 결정되나요?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "유품의 양, 공간 크기, 폐기물 반출량, 엘리베이터 유무, 특수청소 필요 여부에 따라 달라집니다."
                }
            },
            {
                "@type": "Question",
                "name": f"{name} 고독사청소도 가능한가요?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "가능합니다. 오염 정리, 소독, 냄새 저감, 폐기물 반출까지 현장 상황에 맞춰 진행합니다."
                }
            },
            {
                "@type": "Question",
                "name": f"{name} 유품정리 상담은 어떻게 진행되나요?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "전화 또는 온라인 상담 접수 후 지역, 현장 상황, 필요한 서비스 범위를 확인하고 안내드립니다."
                }
            }
        ]
    }

    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {
            "@type": "Organization",
            "name": "올바른 유품정리"
        },
        "publisher": {
            "@type": "Organization",
            "name": "올바른 유품정리"
        },
        "mainEntityOfPage": url,
        "dateModified": date.today().isoformat()
    }

    business_schema = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "올바른 유품정리",
        "url": BASE_URL,
        "telephone": PHONE,
        "areaServed": f"{region_type} {name}",
        "description": desc,
        "priceRange": "450000KRW~"
    }

    return f"""
  <script type="application/ld+json">
{json.dumps(faq_schema, ensure_ascii=False, indent=2)}
  </script>

  <script type="application/ld+json">
{json.dumps(article_schema, ensure_ascii=False, indent=2)}
  </script>

  <script type="application/ld+json">
{json.dumps(business_schema, ensure_ascii=False, indent=2)}
  </script>
"""

def html_template(region_type, name, slug):
    intro = random.choice(SEO_INTROS)
    related_links = get_related_links(slug, region_type)

    title = f"{name} 유품정리 · 고독사청소 · 특수청소 | 올바른 유품정리"
    desc = f"올바른 유품정리는 {name} 지역 유품정리, 고독사청소, 특수청소를 진행합니다. 유품 분류, 공간 정리, 소독, 폐기물 반출까지 상담 가능합니다."
    schemas = schema_json(region_type, name, slug, title, desc)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="canonical" href="{BASE_URL}/regions/{slug}/" />
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{name} 유품정리, {name} 고독사청소, {name} 특수청소, {region_type} 유품정리, 올바른 유품정리" />

  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{BASE_URL}/regions/{slug}/" />

  <link rel="icon" href="/favicon-allbarun.png" />
{schemas}
  <style>
    :root {{
      --main:#365a4c;
      --sub:#61786b;
      --point:#c2a86f;
      --bg:#f1eee6;
      --card:#fffaf1;
      --text:#26362f;
      --muted:#68776e;
      --line:#ddd4c5;
      --soft:#e6dfd2;
    }}

    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{
      margin:0;
      font-family:"Pretendard","Noto Sans KR",Arial,sans-serif;
      background:var(--bg);
      color:var(--text);
      line-height:1.75;
    }}
    a {{ color:inherit; text-decoration:none; }}

    header {{
      position:sticky;
      top:0;
      z-index:100;
      background:rgba(241,238,230,0.95);
      border-bottom:1px solid var(--line);
      backdrop-filter:blur(10px);
    }}

    .nav {{
      max-width:1180px;
      margin:0 auto;
      padding:16px 20px;
      display:flex;
      justify-content:space-between;
      align-items:center;
      gap:16px;
    }}

    .logo {{
      font-size:24px;
      font-weight:900;
      color:var(--main);
    }}

    .call {{
      background:var(--main);
      color:#fff;
      padding:10px 18px;
      border-radius:999px;
      font-weight:900;
      white-space:nowrap;
    }}

    .hero {{
      background:linear-gradient(120deg,rgba(54,90,76,0.95),rgba(97,120,107,0.82));
      color:#fff;
      padding:98px 20px 84px;
    }}

    .wrap {{
      max-width:1180px;
      margin:0 auto;
    }}

    .badge {{
      display:inline-block;
      background:rgba(255,255,255,0.14);
      border:1px solid rgba(255,255,255,0.28);
      border-radius:999px;
      padding:8px 15px;
      font-size:14px;
      margin-bottom:22px;
    }}

    h1 {{
      font-size:46px;
      line-height:1.25;
      margin:0 0 22px;
      letter-spacing:-1.6px;
    }}

    .hero p {{
      max-width:760px;
      font-size:18px;
      color:rgba(255,255,255,0.9);
      margin:0 0 32px;
    }}

    .btns {{
      display:flex;
      flex-wrap:wrap;
      gap:12px;
    }}

    .btn {{
      display:inline-block;
      padding:14px 22px;
      border-radius:13px;
      font-weight:900;
    }}

    .btn-primary {{
      background:var(--point);
      color:#26362f;
    }}

    .btn-outline {{
      color:#fff;
      border:1px solid rgba(255,255,255,0.38);
      background:rgba(255,255,255,0.13);
    }}

    section {{
      padding:72px 20px;
    }}

    .title {{
      margin-bottom:30px;
    }}

    .title span {{
      color:var(--point);
      font-weight:900;
      font-size:14px;
    }}

    .title h2 {{
      color:var(--main);
      font-size:32px;
      margin:8px 0 10px;
      letter-spacing:-1px;
    }}

    .title p {{
      color:var(--muted);
      margin:0;
    }}

    .grid {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:20px;
    }}

    .card {{
      background:var(--card);
      border:1px solid var(--line);
      border-radius:22px;
      padding:28px;
      box-shadow:0 10px 28px rgba(54,90,76,0.07);
    }}

    .card strong {{
      display:block;
      color:var(--main);
      font-size:20px;
      margin-bottom:10px;
    }}

    .card p {{
      color:var(--muted);
      margin:0;
    }}

    .soft {{
      background:var(--soft);
    }}

    .content {{
      background:var(--card);
      border:1px solid var(--line);
      border-radius:26px;
      padding:36px;
    }}

    .content h2, .content h3 {{
      color:var(--main);
    }}

    .content p {{
      color:var(--muted);
    }}

    .price-grid {{
      display:grid;
      grid-template-columns:repeat(3,1fr);
      gap:20px;
    }}

    .price {{
      font-size:38px;
      color:var(--main);
      font-weight:900;
      margin:10px 0;
    }}

    .price span {{
      font-size:16px;
      color:var(--muted);
    }}

    .related-links {{
      display:flex;
      flex-wrap:wrap;
      gap:9px;
    }}

    .related-links a {{
      background:#e9e1d3;
      color:#40584d;
      padding:8px 12px;
      border-radius:999px;
      font-size:14px;
      font-weight:800;
    }}

    .contact {{
      background:linear-gradient(135deg,#365a4c,#61786b);
      color:#fff;
    }}

    .contact-box {{
      display:grid;
      grid-template-columns:0.9fr 1.1fr;
      gap:40px;
    }}

    .contact h2 {{
      font-size:34px;
      margin:0 0 14px;
    }}

    .contact p {{
      color:rgba(255,255,255,0.86);
    }}

    form {{
      background:var(--card);
      color:var(--text);
      border-radius:24px;
      padding:30px;
    }}

    input, select, textarea {{
      width:100%;
      padding:14px;
      border:1px solid var(--line);
      border-radius:12px;
      margin-bottom:14px;
      background:#fffdf8;
      font-size:15px;
    }}

    textarea {{
      min-height:120px;
      resize:vertical;
    }}

    .agree {{
      display:flex;
      gap:10px;
      color:var(--muted);
      font-size:14px;
      margin:4px 0 18px;
    }}

    .agree input {{
      width:auto;
      margin-top:6px;
    }}

    button {{
      width:100%;
      border:none;
      background:var(--main);
      color:#fff;
      padding:15px;
      border-radius:12px;
      font-size:17px;
      font-weight:900;
      cursor:pointer;
    }}

    footer {{
      background:#dcd4c6;
      color:#4d5d54;
      padding:38px 20px;
    }}

    .footer-inner {{
      max-width:1180px;
      margin:0 auto;
      display:flex;
      justify-content:space-between;
      flex-wrap:wrap;
      gap:20px;
    }}

    .floating {{
      position:fixed;
      right:18px;
      bottom:18px;
      background:var(--main);
      color:#fff;
      padding:14px 18px;
      border-radius:999px;
      font-weight:900;
      box-shadow:0 12px 30px rgba(54,90,76,0.28);
    }}

    @media(max-width:900px) {{
      h1 {{ font-size:34px; }}
      .grid, .price-grid, .contact-box {{ grid-template-columns:1fr; }}
      .floating {{ left:18px; right:18px; text-align:center; }}
    }}
  </style>
</head>

<body>

<header>
  <div class="nav">
    <a href="/" class="logo">올바른 유품정리</a>
    <a href="tel:{PHONE_LINK}" class="call">{PHONE}</a>
  </div>
</header>

<main>
  <section class="hero">
    <div class="wrap">
      <div class="badge">{region_type} {name} 유품정리 전문</div>
      <h1>{name} 유품정리,<br />고독사청소와 특수청소까지</h1>
      <p>
        올바른 유품정리는 {name} 지역에서 유품정리, 고독사청소, 특수청소를 진행합니다.
        유품 분류부터 공간 정리, 오염 정리, 소독, 폐기물 반출까지 현장 상황에 맞춰 차분히 도와드립니다.
      </p>
      <div class="btns">
        <a href="#contact" class="btn btn-primary">상담 접수하기</a>
        <a href="tel:{PHONE_LINK}" class="btn btn-outline">전화 상담 {PHONE}</a>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="title">
        <span>SERVICE</span>
        <h2>{name} 유품정리 서비스</h2>
        <p>{name} 지역 현장 상황에 따라 필요한 작업 범위를 안내드립니다.</p>
      </div>

      <div class="grid">
        <div class="card">
          <strong>유품정리</strong>
          <p>보관할 물품, 중요 서류, 정리 대상 물품을 구분하고 공간을 정돈합니다.</p>
        </div>
        <div class="card">
          <strong>고독사청소</strong>
          <p>오염 정리, 소독, 냄새 저감, 폐기물 반출까지 현장에 맞춰 진행합니다.</p>
        </div>
        <div class="card">
          <strong>특수청소</strong>
          <p>일반 청소로 어려운 오염 공간과 장기간 방치된 공간을 정리합니다.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="soft">
    <div class="wrap">
      <div class="title">
        <span>PRICE</span>
        <h2>{name} 유품정리 가격 가이드</h2>
        <p>아래 금액은 기본 시작 가격이며, 현장 상황에 따라 달라질 수 있습니다.</p>
      </div>

      <div class="price-grid">
        <div class="card">
          <strong>유품정리</strong>
          <div class="price">45만원 <span>부터~</span></div>
          <p>유품 분류와 공간 정리 기준 시작 금액입니다.</p>
        </div>
        <div class="card">
          <strong>고독사 특수청소</strong>
          <div class="price">80만원 <span>부터~</span></div>
          <p>오염 정리, 소독, 냄새 저감이 필요한 경우입니다.</p>
        </div>
        <div class="card">
          <strong>특수청소</strong>
          <div class="price">상담 후 <span>안내</span></div>
          <p>오염도와 작업 범위에 따라 비용이 달라집니다.</p>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="content">
        <h2>{name} 유품정리, 올바른 유품정리가 신중하게 도와드립니다</h2>
        <p>{intro}</p>
        <p>
          {name} 유품정리는 공간의 크기, 물품의 양, 엘리베이터 유무, 주차 가능 여부,
          폐기물 반출량, 특수청소 필요 여부에 따라 작업 범위가 달라질 수 있습니다.
        </p>
        <p>
          고독사청소나 특수청소가 함께 필요한 현장은 일반적인 정리보다 더 신중한 절차가 필요합니다.
          오염 정리와 소독, 냄새 저감 작업을 함께 고려해야 하며 작업자의 안전과 주변 환경도 함께 확인해야 합니다.
        </p>
        <h3>{name} 지역 상담 안내</h3>
        <p>
          올바른 유품정리는 {name} 지역의 아파트, 빌라, 단독주택, 오피스텔, 원룸 등 다양한 주거 공간의
          유품정리 상담을 진행합니다.
        </p>
      </div>
    </div>
  </section>

  <section class="soft">
    <div class="wrap">
      <div class="title">
        <span>REGION</span>
        <h2>함께 확인하면 좋은 지역</h2>
        <p>{region_type} 인근 지역과 서울·경기 주요 지역 유품정리 안내입니다.</p>
      </div>
      <div class="related-links">
        {related_links}
      </div>
    </div>
  </section>

  <section class="contact" id="contact">
    <div class="wrap contact-box">
      <div>
        <h2>{name} 유품정리 상담</h2>
        <p>성함, 연락처, 지역, 필요한 서비스를 남겨주시면 확인 후 연락드립니다.</p>
        <a href="tel:{PHONE_LINK}" class="btn btn-outline">{PHONE}</a>
      </div>

      <form onsubmit="return checkPrivacy();">
        <select required>
          <option value="">필요한 서비스를 선택하세요</option>
          <option>{name} 유품정리</option>
          <option>{name} 고독사청소</option>
          <option>{name} 특수청소</option>
          <option>{name} 유품정리 + 특수청소</option>
        </select>

        <input type="text" placeholder="성함" required />
        <input type="tel" placeholder="연락처" required />
        <input type="text" value="{name}" required />
        <textarea placeholder="상담 내용을 간단히 적어주세요"></textarea>

        <label class="agree">
          <input type="checkbox" id="privacyCheck" />
          <span>개인정보 수집 및 이용에 동의합니다. 수집항목은 성함, 연락처, 지역, 상담내용이며 상담 및 견적 안내 목적으로만 사용됩니다.</span>
        </label>

        <button type="submit">상담 신청하기</button>
      </form>
    </div>
  </section>
</main>

<footer>
  <div class="footer-inner">
    <div>
      <strong>올바른 유품정리</strong><br />
      {name} 유품정리 · 고독사청소 · 특수청소
    </div>
    <div>
      대표 상담 : <a href="tel:{PHONE_LINK}">{PHONE}</a><br />
      메인 : <a href="/">yupum.allbarunclean.com</a>
    </div>
  </div>
</footer>

<a href="tel:{PHONE_LINK}" class="floating">전화 상담 {PHONE}</a>

<script>
  function checkPrivacy() {{
    const checked = document.getElementById("privacyCheck").checked;

    if (!checked) {{
      alert("개인정보 수집 및 이용 동의가 필요합니다.");
      return false;
    }}

    alert("상담 신청이 확인되었습니다. EmailJS 연결 코드를 적용해 주세요.");
    return false;
  }}
</script>

</body>
</html>
"""

def generate():
    root = Path(__file__).resolve().parent
    regions_dir = root / "regions"
    regions_dir.mkdir(exist_ok=True)

    for region_type, name, slug in REGIONS:
        folder = regions_dir / slug
        folder.mkdir(parents=True, exist_ok=True)

        html = html_template(region_type, name, slug)
        (folder / "index.html").write_text(html, encoding="utf-8")

    print(f"완료: {len(REGIONS)}개 지역 페이지 업그레이드 생성")
    print("포함 항목: 내부링크 + FAQ Schema + Article Schema + LocalBusiness Schema")

if __name__ == "__main__":
    generate()