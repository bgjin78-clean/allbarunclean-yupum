"""서울·경기 유품정리업체 키워드 SEO 보강."""
from __future__ import annotations

import re
from pathlib import Path

from generate_regions import REGIONS

SLUG_TO_REGION = {slug: (region_type, name) for region_type, name, slug in REGIONS}

INDEX_FAQ_SCHEMA = """
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "서울·경기 유품정리업체는 어떻게 선택하나요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "유품정리업체 선택 시 현장 상황 확인, 유품 분류 기준, 고독사·특수청소 가능 여부, 비용 안내 방식, 폐기물 반출까지 포함되는지 확인하는 것이 좋습니다. 올바른 유품정리는 서울 25개 구·경기 31개 시·군에서 상담 후 작업 범위와 비용을 먼저 안내합니다."
      }
    },
    {
      "@type": "Question",
      "name": "서울·경기 유품정리업체 비용은 얼마부터인가요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "유품정리는 기본 45만원부터 시작하며, 유품·물품 양, 공간 크기, 층수, 특수청소 필요 여부에 따라 달라질 수 있습니다. 사진과 주소를 알려주시면 대략적인 범위 안내가 가능합니다."
      }
    },
    {
      "@type": "Question",
      "name": "서울·경기 유품정리업체에서 고독사청소도 가능한가요?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "가능합니다. 오염 정리, 소독, 냄새 저감, 폐기물 반출까지 현장 상황에 맞춰 유품정리와 함께 상담할 수 있습니다."
      }
    }
  ]
}
</script>"""


def upgrade_index(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    original = html

    html = html.replace(
        "<title>서울·경기 유품정리 · 유품소각 · 고독사청소 | 올바른 유품정리</title>",
        "<title>서울·경기 유품정리업체 · 유품정리 · 고독사청소 | 올바른 유품정리</title>",
    )
    html = html.replace(
        'content="올바른 유품정리는 서울·경기 전 지역 유품정리, 유품소각대행(1박스 4~5만원), 고독사청소, 특수청소를',
        'content="올바른 유품정리는 서울·경기 유품정리업체로 유품정리, 유품소각대행(1박스 4~5만원), 고독사청소, 특수청소를',
    )
    html = html.replace(
        'content="서울 유품소각, 경기 유품소각, 서울 유품정리, 경기 유품정리,',
        'content="서울 경기 유품정리업체, 서울 유품정리업체, 경기 유품정리업체, 서울 유품소각, 경기 유품소각, 서울 유품정리, 경기 유품정리,',
    )
    html = html.replace(
        '<meta property="og:title" content="서울 경기 유품정리 전문 | 올바른 유품정리" />',
        '<meta property="og:title" content="서울·경기 유품정리업체 | 올바른 유품정리" />',
    )
    html = html.replace(
        'content="서울·경기 유품정리, 고독사청소, 특수청소 전문 상담. 유품 분류부터 정리, 청소, 소독까지 책임감 있게 진행합니다."',
        'content="서울·경기 유품정리업체 전문 상담. 유품정리, 고독사청소, 특수청소, 유품소각까지 현장 상황에 맞춰 안내합니다."',
    )
    html = html.replace(
        '"description": "서울·경기 유품정리, 고독사청소, 특수청소 전문 상담. 유품 분류, 공간 정리, 소독, 폐기물 반출까지 안내합니다."',
        '"description": "서울·경기 유품정리업체. 유품정리, 고독사청소, 특수청소, 유품소각 전문 상담. 유품 분류, 공간 정리, 소독, 폐기물 반출까지 안내합니다."',
    )
    html = html.replace(
        '<div class="badge">서울 · 경기 유품정리 45만원부터</div>',
        '<div class="badge">서울·경기 유품정리업체 · 45만원부터</div>',
    )
    html = html.replace(
        "<h1>서울·경기 유품정리<br />올바른 유품정리</h1>",
        "<h1>서울·경기 유품정리업체<br />올바른 유품정리</h1>",
    )
    html = html.replace(
        "유품정리·유품소각·고독사청소·특수청소까지",
        "유품정리업체로서 유품정리·유품소각·고독사청소·특수청소까지",
    )

    if 'name="서울·경기 유품정리업체는 어떻게 선택하나요?"' not in html:
        html = html.replace(
            "        <h3>서울·경기 유품정리란 무엇인가요?</h3>",
            """        <h3>서울·경기 유품정리업체란?</h3>
        <p>
          서울·경기 유품정리업체는 고인의 유품을 분류·정리하고, 필요 시 고독사청소·특수청소·유품소각·폐기물 반출까지
          현장 상황에 맞춰 진행하는 전문 업체입니다. 올바른 유품정리는 서울 25개 구와 경기 31개 시·군을 대상으로
          유품정리, 유품소각, 고독사청소, 특수청소 상담을 진행합니다.
        </p>
        <p>
          유품정리업체를 선택할 때는 <strong>현장 확인 후 비용 안내</strong>, <strong>유품 분류 기준</strong>,
          <strong>고독사·특수청소 가능 여부</strong>, <strong>폐기물 반출 포함 범위</strong>를 함께 확인하는 것이 좋습니다.
        </p>

        <h3>서울·경기 유품정리란 무엇인가요?</h3>""",
        )

    if "서울·경기 유품정리업체는 어떻게 선택" not in html:
        html = html.replace(
            """        <div class="faq">
          <strong>서울·경기 전 지역 유품정리 비용은 얼마부터인가요?</strong>""",
            """        <div class="faq">
          <strong>서울·경기 유품정리업체는 어떻게 선택하나요?</strong>
          <p>현장 상황 확인, 유품 분류 기준, 고독사·특수청소 가능 여부, 비용·폐기물 반출 포함 범위를 확인하세요. 올바른 유품정리는 상담 후 작업 범위와 비용을 먼저 안내합니다.</p>
        </div>
        <div class="faq">
          <strong>서울·경기 전 지역 유품정리 비용은 얼마부터인가요?</strong>""",
        )

    if '"@type": "FAQPage"' not in html:
        html = html.replace("</head>", INDEX_FAQ_SCHEMA + "\n</head>", 1)

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def upgrade_region(path: Path) -> bool:
    slug = path.parent.name
    if slug not in SLUG_TO_REGION:
        return False
    region_type, name = SLUG_TO_REGION[slug]
    html = path.read_text(encoding="utf-8")
    original = html

    html = re.sub(
        r"(<title>)[^<]*( · 유품소각 · 고독사청소 \| 올바른 유품정리</title>)",
        rf"\1{name} 유품정리업체 · 유품소각 · 고독사청소 | 올바른 유품정리</title>",
        html,
        count=1,
    )
    if f"{name} 유품정리업체" not in html.split("<meta name=\"keywords\"")[1][:300]:
        html = re.sub(
            r'(<meta name="keywords" content="[^"]*)(올바른 유품정리")',
            rf"\1{name} 유품정리업체, {region_type} 유품정리업체, \2",
            html,
            count=1,
        )
    html = re.sub(
        r'(<meta name="description" content=")([^"]*유품정리, )',
        rf"\1\2{name} 유품정리업체, ",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta property="og:title" content=")[^"]*( · 유품소각 · 고독사청소 \| 올바른 유품정리")',
        rf'\1{name} 유품정리업체 · 유품소각 · 고독사청소 | 올바른 유품정리"',
        html,
        count=1,
    )

    faq_entry = f"""    {{
      "@type": "Question",
      "name": "{name} 유품정리업체는 어떻게 선택하나요?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "현장 확인, 유품 분류 기준, 고독사·특수청소 가능 여부, 비용·폐기물 반출 범위를 확인하세요. 올바른 유품정리는 {name} 지역에서 상담 후 작업 범위를 안내합니다."
      }}
    }},
"""
    if f"{name} 유품정리업체는 어떻게" not in html:
        match = re.search(
            rf'(\{{\s+"@type": "Question",\s+"name": "{re.escape(name)}[^"]*상담[^"]*")',
            html,
        )
        if match:
            html = html[: match.start()] + faq_entry + html[match.start() :]

    heading = f"""
        <h3>{name} 유품정리업체 선택 시 확인할 점</h3>
        <p>
          {name} 유품정리업체를 찾을 때는 유품 분류·보관 기준, 고독사·특수청소 가능 여부,
          비용 산정 방식, 폐기물 반출 포함 범위를 함께 확인하는 것이 좋습니다.
          올바른 유품정리는 {region_type} {name} 지역에서 유품정리, 유품소각, 고독사청소, 특수청소 상담을 진행합니다.
        </p>
"""
    if f"{name} 유품정리업체 선택" not in html:
        for marker in (
            f"        <h3>{name} 유품소각(소각대행) 안내</h3>",
            f"        <h3>{name} 지역 상담 안내</h3>",
            "        <h3>고독사청소와 특수청소가 필요한 경우</h3>",
        ):
            if marker in html:
                html = html.replace(marker, heading + marker, 1)
                break

    if html != original:
        path.write_text(html, encoding="utf-8")
        return True
    return False


def upgrade():
    root = Path(__file__).resolve().parent
    count = 0
    if upgrade_index(root / "index.html"):
        count += 1
        print("updated: index.html")
    for path in sorted((root / "regions").glob("*/index.html")):
        if upgrade_region(path):
            count += 1
            print(f"updated: {path.relative_to(root)}")
    print(f"\n완료: {count}개 파일 유품정리업체 SEO 적용")


if __name__ == "__main__":
    upgrade()
