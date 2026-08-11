"""서울·경기 지역 페이지 및 메인에 유품소각 콘텐츠·SEO 추가."""
from __future__ import annotations

import re
from pathlib import Path

from generate_regions import REGIONS

INCINERATION_CSS = """
    .incineration-section { background: var(--bg); }
    .incineration-box {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 26px;
      padding: 36px;
      box-shadow: 0 10px 28px rgba(54,90,76,0.07);
    }
    .incineration-box > p { color: var(--muted); margin: 0 0 20px; }
    .incineration-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
      margin: 24px 0;
    }
    .incineration-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 15px;
    }
    .incineration-table th, .incineration-table td {
      border: 1px solid var(--line);
      padding: 14px 16px;
      text-align: left;
    }
    .incineration-table th {
      background: var(--soft);
      color: var(--main);
      font-weight: 800;
    }
    .incineration-table td { color: var(--text); }
    .box-spec {
      background: var(--soft);
      border-radius: 18px;
      padding: 24px;
    }
    .box-visual {
      display: block;
      width: 200px;
      max-width: 100%;
      height: auto;
      margin: 0 auto 16px;
      object-fit: contain;
    }
    .box-spec dl { margin: 0; display: grid; gap: 8px; }
    .box-spec dt { color: var(--main); font-weight: 800; font-size: 14px; }
    .box-spec dd { margin: 0 0 8px; color: var(--muted); font-size: 14px; }
    .box-size-line {
      margin: 0;
      text-align: center;
      color: var(--muted);
      font-size: 15px;
      line-height: 1.6;
    }
    .box-size-line strong { color: var(--main); font-weight: 800; }
    .box-size-mm { font-size: 14px; }
    .legal-notice {
      background: linear-gradient(135deg, #2a4540, #365a4c);
      color: #fff;
      border-radius: 18px;
      padding: 24px 28px;
      margin-top: 24px;
    }
    .legal-notice h3 { margin: 0 0 12px; font-size: 18px; color: #fff; }
    .legal-notice p { margin: 0; color: rgba(255,255,255,0.88); font-size: 15px; line-height: 1.8; }
    .legal-notice .fine { color: #ffb4b4; font-weight: 900; }
    @media(max-width:900px) {
      .incineration-grid { grid-template-columns: 1fr; }
    }
"""

SLUG_TO_REGION = {slug: (region_type, name) for region_type, name, slug in REGIONS}


def incineration_section(region_type: str, name: str) -> str:
    return f"""
  <section class="incineration-section" id="incineration">
    <div class="wrap">
      <div class="title">
        <span>INCINERATION</span>
        <h2>{name} 유품소각대행 서비스</h2>
        <p>{region_type} {name} 지역 유품소각·소각대행 상담을 진행합니다.</p>
      </div>
      <div class="incineration-box">
        <p>
          고인의 유품을 <strong>보관·기부·소각·폐기</strong> 3가지로 분류한 뒤,
          소각·폐기 대상 유품은 폐기물관리법에 따라 합법적으로 소각·처리하는 서비스입니다.
          {name} 유품정리 과정에서 소각이 필요한 물품이 있으면 함께 상담할 수 있습니다.
        </p>
        <div class="incineration-grid">
          <div>
            <table class="incineration-table">
              <thead>
                <tr><th>구분</th><th>비용</th></tr>
              </thead>
              <tbody>
                <tr><td>1 box 기준</td><td><strong>4만원 ~ 5만원</strong></td></tr>
              </tbody>
            </table>
            <p style="color:var(--muted);font-size:14px;margin-top:12px;">
              * 박스 수·물품 종류·처리 방식에 따라 달라질 수 있습니다.
            </p>
          </div>
          <div class="box-spec">
            <img class="box-visual" src="/image/main/incineration-box.png" alt="우체국 5호 택배상자 (유품소각 기준 박스)" />
            <strong style="color:var(--main);display:block;margin-bottom:12px;text-align:center;">우체국 5호 상자 기준</strong>
            <p class="box-size-line"><strong>가로×세로×높이</strong> 48cm × 38cm × 34cm <span class="box-size-mm">(480×380×340mm)</span></p>
          </div>
        </div>
        <div class="legal-notice">
          <h3>※ 폐기물관리법 안내</h3>
          <p>
            고인의 유품을 허가받지 않은 장소에서 소각하는 것은
            <strong>폐기물관리법 제8조 제2항 및 제32조 제1항</strong>에 따른 불법 소각에 해당할 수 있으며,
            <span class="fine">1천만원 이하의 벌금</span>이 부과될 수 있습니다.
            올바른 유품정리는 {region_type} {name} 지역에서 합법적인 소각·폐기 처리 경로로 안내합니다.
          </p>
        </div>
      </div>
    </div>
  </section>
"""


def add_css(html: str) -> str:
    if ".incineration-section" in html:
        return html
    return html.replace("  </style>", INCINERATION_CSS + "\n  </style>", 1)


def update_meta(html: str, region_type: str, name: str) -> str:
    html = re.sub(
        r"(<title>)[^<]*( · 고독사청소 · 특수청소 \| 올바른 유품정리</title>)",
        rf"\1{name} 유품정리 · 유품소각 · 고독사청소 | 올바른 유품정리</title>",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta name="description" content=")([^"]*)(")',
        lambda m: (
            f'{m.group(1)}{name} 지역 유품정리, 유품소각대행(1박스 4~5만원), 고독사청소, 특수청소. '
            f"유품 분류, 합법 소각·폐기, 공간 정리, 소독, 폐기물 반출까지 상담 가능합니다.{m.group(3)}"
        ),
        html,
        count=1,
    )
    if f"{name} 유품소각" not in html:
        html = re.sub(
            r'(<meta name="keywords" content="[^"]*)(올바른 유품정리")',
            rf"\1{name} 유품소각, {region_type} 유품소각, \2",
            html,
            count=1,
        )
    html = re.sub(
        r'(<meta property="og:title" content=")[^"]*( · 고독사청소 · 특수청소 \| 올바른 유품정리")',
        rf'\1{name} 유품정리 · 유품소각 · 고독사청소 | 올바른 유품정리"',
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta property="og:description" content=")([^"]*)(")',
        lambda m: (
            f'{m.group(1)}{name} 유품정리·유품소각대행, 고독사청소, 특수청소. '
            f"우체국 5호 박스 기준 4~5만원, 폐기물관리법 준수 합법 소각 안내.{m.group(3)}"
        ),
        html,
        count=1,
    )
    return html


def update_faq_schema(html: str, name: str) -> str:
    if f"{name} 유품소각 비용" in html:
        return html
    entry = f"""    {{
      "@type": "Question",
      "name": "{name} 유품소각 비용은 얼마인가요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "우체국 5호 박스(480×380×340mm) 1박스 기준 4만원~5만원입니다. 소각·폐기 대상 유품은 폐기물관리법에 따라 합법적으로 처리합니다."
      }}
    }},
"""
    match = re.search(
        rf'(\{{\s+"@type": "Question",\s+"name": "{re.escape(name)}[^"]*상담[^"]*")',
        html,
    )
    if match:
        return html[: match.start()] + entry + html[match.start() :]
    return html


def update_service_schema(html: str) -> str:
    if '"name": "유품소각"' in html:
        return html
    block = """      {
        "@type": "ListItem",
        "position": 6,
        "item": {
          "@type": "Service",
          "name": "유품소각",
          "description": "유품 소각대행, 우체국 5호 박스 기준 4~5만원",
          "provider": {
            "@type": "LocalBusiness",
            "name": "올바른 유품정리"
          }
        }
      }"""
    return html.replace(
        '"image": "https://www.yupum.allbarunclean.com/images/waste.jpg"\n        }\n      }\n    ]',
        '"image": "https://www.yupum.allbarunclean.com/images/waste.jpg"\n        }\n      },\n' + block + "\n    ]",
        1,
    )


def add_service_card(html: str) -> str:
    if "<strong>유품소각</strong>" in html and "소각·폐기 대상" in html:
        return html
    card = """        <div class="card">
          <strong>유품소각</strong>
          <p>소각·폐기 대상 유품을 폐기물관리법에 따라 합법적으로 소각·처리합니다.</p>
        </div>
"""
    return html.replace(
        """        <div class="card">
          <strong>특수청소</strong>
          <p>일반 청소로 어려운 오염 공간과 장기간 방치된 공간을 정리합니다.</p>
        </div>
      </div>""",
        """        <div class="card">
          <strong>특수청소</strong>
          <p>일반 청소로 어려운 오염 공간과 장기간 방치된 공간을 정리합니다.</p>
        </div>
""" + card + """      </div>""",
        1,
    )


def add_price_card(html: str, name: str) -> str:
    if '유품소각</strong>\n          <div class="price">4만원' in html:
        return html
    marker = """        <div class="card">
          <strong>특수청소</strong>
          <div class="price">상담 후 <span>안내</span></div>
          <p>오염도와 작업 범위에 따라 비용이 달라집니다.</p>
        </div>
      </div>"""
    card = """        <div class="card">
          <strong>유품소각</strong>
          <div class="price">4만원 <span>~5만원/box</span></div>
          <p>우체국 5호 박스(48×38×34cm) 1박스 기준입니다.</p>
        </div>
"""
    if marker in html:
        return html.replace(marker, marker.replace("      </div>", card + "      </div>", 1), 1)
    return html


def insert_incineration_section(html: str, region_type: str, name: str) -> str:
    if 'id="incineration"' in html:
        return html
    match = re.search(
        r"(<section class=\"soft\">\s*<div class=\"wrap\">\s*<div class=\"title\">\s*<span>PRICE</span>.*?</section>)",
        html,
        re.DOTALL,
    )
    if not match:
        return html
    return html[: match.end()] + incineration_section(region_type, name) + html[match.end() :]


def update_hero(html: str) -> str:
    return html.replace(
        "유품정리, 고독사청소, 특수청소를",
        "유품정리, 유품소각, 고독사청소, 특수청소를",
    )


def update_contact_form(html: str, name: str) -> str:
    option = f"          <option>{name} 유품소각</option>\n"
    if f"{name} 유품소각</option>" in html:
        return html
    return html.replace(
        f"          <option>{name} 특수청소</option>\n",
        f"          <option>{name} 특수청소</option>\n{option}",
        1,
    )


def add_content_heading(html: str, name: str) -> str:
    heading = f"""
        <h3>{name} 유품소각(소각대행) 안내</h3>
        <p>
          {name} 유품소각은 유품정리 과정에서 소각·폐기가 필요한 물품을 분류한 뒤,
          우체국 5호 박스(480×380×340mm) 기준 1박스당 4만원~5만원으로 합법 처리 경로를 안내합니다.
          무단 소각은 폐기물관리법 위반으로 최대 1천만원 이하 벌금이 부과될 수 있으므로
          반드시 허가된 방식으로 진행해야 합니다.
        </p>
"""
    if f"{name} 유품소각(소각대행)" in html:
        return html
    for marker in (
        "        <h3>고독사청소와 특수청소가 필요한 경우</h3>",
        f"        <h3>{name} 지역 상담 안내</h3>",
    ):
        if marker in html:
            return html.replace(marker, heading + marker, 1)
    return html


def fix_og_title(html: str) -> str:
    return html.replace('올바른 유품정리\\" />', '올바른 유품정리" />')


def upgrade_region_file(path: Path) -> bool:
    slug = path.parent.name
    if slug not in SLUG_TO_REGION:
        return False
    region_type, name = SLUG_TO_REGION[slug]
    html = path.read_text(encoding="utf-8")
    original = html

    html = fix_og_title(html)

    if 'id="incineration"' not in html:
        html = add_css(html)
        html = update_meta(html, region_type, name)
        html = update_faq_schema(html, name)
        html = update_service_schema(html)
        html = update_hero(html)
        html = add_service_card(html)
        html = add_price_card(html, name)
        html = insert_incineration_section(html, region_type, name)
        html = update_contact_form(html, name)

    html = add_content_heading(html, name)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def upgrade_index(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html

    html = fix_og_title(html)
    if 'id="incineration"' not in html:
        css = INCINERATION_CSS.replace("    ", "    ")
        html = html.replace("  </style>", css + "\n  </style>", 1)

        section = """
  <section class="incineration-section" id="incineration">
    <div class="wrap">
      <div class="title">
        <span>유품소각</span>
        <h2>서울·경기 유품소각대행 서비스</h2>
        <p>56개 지역(서울 25구·경기 31시·군) 유품소각·소각대행 상담을 진행합니다.</p>
      </div>
      <div class="incineration-box">
        <p>
          고인의 유품을 <strong>보관·기부·소각·폐기</strong> 3가지로 분류한 뒤,
          소각·폐기 대상 유품은 폐기물관리법에 따라 합법적으로 소각·처리하는 서비스입니다.
          서울·경기 전 지역에서 유품정리와 함께 유품소각 상담이 가능합니다.
        </p>
        <div class="incineration-grid">
          <div>
            <table class="incineration-table">
              <thead>
                <tr><th>구분</th><th>비용</th></tr>
              </thead>
              <tbody>
                <tr><td>1 box 기준</td><td><strong>4만원 ~ 5만원</strong></td></tr>
              </tbody>
            </table>
            <p style="color:var(--muted);font-size:14px;margin-top:12px;">
              * 박스 수·물품 종류·처리 방식에 따라 달라질 수 있습니다.
            </p>
          </div>
          <div class="box-spec">
            <img class="box-visual" src="/image/main/incineration-box.png" alt="우체국 5호 택배상자 (유품소각 기준 박스)" />
            <strong style="color:var(--main);display:block;margin-bottom:12px;text-align:center;">우체국 5호 상자 기준</strong>
            <p class="box-size-line"><strong>가로×세로×높이</strong> 48cm × 38cm × 34cm <span class="box-size-mm">(480×380×340mm)</span></p>
          </div>
        </div>
        <div class="legal-notice">
          <h3>※ 폐기물관리법 안내</h3>
          <p>
            고인의 유품을 허가받지 않은 장소에서 소각하는 것은
            <strong>폐기물관리법 제8조 제2항 및 제32조 제1항</strong>에 따른 불법 소각에 해당할 수 있으며,
            <span class="fine">1천만원 이하의 벌금</span>이 부과될 수 있습니다.
            올바른 유품정리는 서울·경기 전 지역에서 합법적인 소각·폐기 처리 경로로 안내합니다.
          </p>
        </div>
      </div>
    </div>
  </section>
"""
        html = html.replace(
            '  <section>\n    <div class="wrap">\n      <div class="title">\n        <span>비용 기준</span>',
            section + '\n  <section>\n    <div class="wrap">\n      <div class="title">\n        <span>비용 기준</span>',
            1,
        )

    html = re.sub(
        r"<title>서울 경기 유품정리 · 고독사청소 · 특수청소 \| 올바른 유품정리</title>",
        "<title>서울·경기 유품정리 · 유품소각 · 고독사청소 | 올바른 유품정리</title>",
        html,
    )
    html = re.sub(
        r'content="올바른 유품정리는 서울·경기 전 지역 유품정리, 고독사청소, 특수청소를',
        'content="올바른 유품정리는 서울·경기 전 지역 유품정리, 유품소각대행(1박스 4~5만원), 고독사청소, 특수청소를',
        html,
    )
    if "서울 유품소각" not in html:
        html = html.replace(
            'content="서울 유품정리, 경기 유품정리,',
            'content="서울 유품소각, 경기 유품소각, 서울 유품정리, 경기 유품정리,',
            1,
        )

    if "<h3>유품소각</h3>" not in html and "<h3>서울·경기 유품소각" not in html:
        html = html.replace(
            "        <h3>유품정리와 폐기물처리의 차이</h3>",
            """        <h3>서울·경기 유품소각(소각대행) 안내</h3>
        <p>
          유품소각은 유품정리 과정에서 소각·폐기가 필요한 물품을 분류한 뒤,
          우체국 5호 박스(480×380×340mm) 기준 1박스당 4만원~5만원으로 합법 처리하는 서비스입니다.
          강남·송파·수원·성남 등 지역별로 <a href="/regions/gangnam/#incineration">강남구 유품소각</a>,
          <a href="/regions/suwon/#incineration">수원시 유품소각</a> 페이지에서 상세 안내를 확인할 수 있습니다.
          무단 소각은 폐기물관리법 위반으로 최대 1천만원 이하 벌금이 부과될 수 있습니다.
        </p>

        <h3>유품정리와 폐기물처리의 차이</h3>""",
            1,
        )

    if "<h3>유품소각</h3>" not in html.replace("서울·경기 유품소각", ""):
        html = html.replace(
            """        <div class="service-card">
          <b>05</b>
          <h3>폐기물 반출</h3>""",
            """        <div class="service-card">
          <b>05</b>
          <h3>유품소각</h3>
          <p>소각·폐기 대상 유품을 폐기물관리법에 따라 합법적으로 소각·처리합니다. 1박스 4~5만원.</p>
        </div>
        <div class="service-card">
          <b>06</b>
          <h3>폐기물 반출</h3>""",
            1,
        )

    html = html.replace(
        "<option>특수청소</option>\n          <option>유품정리 + 특수청소</option>",
        "<option>특수청소</option>\n          <option>유품소각</option>\n          <option>유품정리 + 특수청소</option>",
        1,
    )
    html = html.replace(
        "<li>✓ 특수청소 · 유품정리 + 특수청소</li>",
        "<li>✓ 유품소각 · 특수청소 · 유품정리 + 특수청소</li>",
        1,
    )
    html = html.replace(
        "유품정리·고독사청소·특수청소까지",
        "유품정리·유품소각·고독사청소·특수청소까지",
        1,
    )

    if '"name": "유품소각"' not in html:
        html = update_service_schema(html)

    if "유품소각 비용은" not in html:
        html = html.replace(
            """        <div class="faq">
          <strong>가족이 현장에 꼭 있어야 하나요?</strong>""",
            """        <div class="faq">
          <strong>서울·경기 유품소각 비용은 얼마인가요?</strong>
          <p>우체국 5호 박스(480×380×340mm) 1박스 기준 4만원~5만원입니다. 폐기물관리법에 따라 합법적으로 처리합니다.</p>
        </div>
        <div class="faq">
          <strong>가족이 현장에 꼭 있어야 하나요?</strong>""",
            1,
        )

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def upgrade():
    root = Path(__file__).resolve().parent
    count = 0

    index_path = root / "index.html"
    if upgrade_index(index_path):
        count += 1
        print(f"updated: index.html")

    for path in sorted((root / "regions").glob("*/index.html")):
        if upgrade_region_file(path):
            count += 1
            print(f"updated: {path.relative_to(root)}")

    print(f"\n완료: {count}개 파일 유품소각 콘텐츠·SEO 적용")


if __name__ == "__main__":
    upgrade()
