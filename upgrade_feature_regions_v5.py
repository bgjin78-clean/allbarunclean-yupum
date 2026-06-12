from pathlib import Path
import re

FEATURE_REGIONS = [
    ("강남구", "gangnam"),
    ("송파구", "songpa"),
    ("서초구", "seocho"),
    ("마포구", "mapo"),
    ("용산구", "yongsan"),
    ("수원시", "suwon"),
    ("성남시", "seongnam"),
    ("용인시", "yongin"),
    ("고양시", "goyang"),
    ("화성시", "hwaseong"),
    ("남양주시", "namyangju"),
]

AREA_FEATURES = {
    "강남구": "아파트, 오피스텔, 빌라 등 다양한 주거 형태가 많아 관리사무소 협의, 주차 위치, 엘리베이터 사용 여부 확인이 중요합니다.",
    "송파구": "대단지 아파트와 오피스텔이 함께 있는 지역으로, 폐기물 반출 동선과 차량 진입 가능 여부를 먼저 확인하는 것이 좋습니다.",
    "서초구": "아파트와 고급 주거시설 비중이 높아 보관품 분류, 중요 서류 확인, 반출 절차를 신중하게 진행하는 것이 중요합니다.",
    "마포구": "원룸, 오피스텔, 빌라, 상가주택이 혼재되어 있어 공간 구조에 따라 작업 방식과 반출 방식이 달라질 수 있습니다.",
    "용산구": "아파트, 빌라, 오래된 주택이 함께 있어 현장 구조와 주차 환경을 먼저 확인한 뒤 작업 범위를 안내합니다.",
    "수원시": "아파트와 빌라, 단독주택 상담이 고르게 발생하며 물품 양과 반출 환경에 따라 작업 인원과 차량이 달라질 수 있습니다.",
    "성남시": "분당, 수정, 중원 등 생활권 차이가 있어 아파트형 현장과 빌라형 현장에 맞춰 정리 방식이 달라질 수 있습니다.",
    "용인시": "면적이 넓고 주거 형태가 다양해 상담 시 주소지와 건물 구조, 반출 동선을 함께 확인하는 것이 중요합니다.",
    "고양시": "일산권 아파트와 빌라, 단독주택 상담이 많아 보관품 분류와 폐기물 반출 계획을 함께 안내합니다.",
    "화성시": "신도시 아파트와 외곽 단독주택, 빌라 등 현장 유형이 다양해 작업 범위 확인이 중요합니다.",
    "남양주시": "서울 동북권과 경기 북동부를 잇는 지역으로 아파트, 빌라, 단독주택 유품정리 상담이 고르게 발생합니다.",
}

def extra_section(region_name):
    feature = AREA_FEATURES.get(region_name, "지역 내 주거 형태와 현장 구조에 따라 유품정리 방식과 반출 절차가 달라질 수 있습니다.")

    return f"""
  <section class="seo-plus">
    <div class="wrap">
      <div class="title">
        <span>CONSULTING</span>
        <h2>{region_name} 유품정리 최근 문의 유형</h2>
        <p>{region_name} 지역에서 자주 접수되는 상담 유형을 기준으로 필요한 작업 범위를 안내드립니다.</p>
      </div>

      <div class="plus-grid">
        <div class="plus-card">
          <strong>임대 종료 전 정리</strong>
          <p>원룸, 오피스텔, 빌라 등에서 임대 종료 전 유품과 생활물품을 정리해야 하는 경우 상담이 많습니다.</p>
        </div>

        <div class="plus-card">
          <strong>가족 방문이 어려운 현장</strong>
          <p>타지역 거주, 일정 문제 등으로 가족분들이 직접 정리하기 어려운 경우 현장 확인 후 진행 방향을 안내합니다.</p>
        </div>

        <div class="plus-card">
          <strong>장기간 방치된 공간</strong>
          <p>오랜 기간 비어 있던 공간이나 오염, 냄새가 동반된 공간은 유품정리와 특수청소를 함께 검토합니다.</p>
        </div>

        <div class="plus-card">
          <strong>폐기물 반출이 많은 현장</strong>
          <p>가구, 가전, 생활폐기물이 많은 경우 작업 인원, 차량, 반출 동선을 함께 확인해야 합니다.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="seo-plus soft">
    <div class="wrap">
      <div class="title">
        <span>COST DETAIL</span>
        <h2>{region_name} 유품정리 비용을 결정하는 요소</h2>
        <p>정확한 비용은 현장 상태를 확인한 뒤 안내드리는 것이 가장 좋습니다.</p>
      </div>

      <div class="content">
        <p>
          {region_name} 유품정리 비용은 단순히 평수만으로 정해지지 않습니다.
          정리해야 할 유품의 양, 폐기물 반출량, 가구와 가전의 크기, 엘리베이터 사용 가능 여부,
          주차 위치, 차량 진입 가능 여부, 특수청소 필요 여부에 따라 달라질 수 있습니다.
        </p>
        <p>
          일반적인 유품정리는 기본 정리와 반출을 중심으로 진행되지만, 고독사청소나 악취·오염 정리가 필요한 경우
          소독, 연무, 냄새 저감 작업이 추가될 수 있습니다. 따라서 상담 시 현장 사진이나 대략적인 물품 양을 알려주시면
          보다 빠르게 예상 범위를 안내드릴 수 있습니다.
        </p>
      </div>
    </div>
  </section>

  <section class="seo-plus">
    <div class="wrap">
      <div class="title">
        <span>LOCAL POINT</span>
        <h2>{region_name} 유품정리 작업 시 확인할 점</h2>
        <p>지역별 주거 형태와 반출 환경에 따라 작업 전 확인 사항이 달라질 수 있습니다.</p>
      </div>

      <div class="content">
        <p>
          {feature}
          유품정리 작업 전에는 보관해야 할 물품, 중요 서류, 사진, 통장, 도장, 귀중품 등을 가능한 범위에서 먼저 확인하는 것이 좋습니다.
        </p>
        <p>
          직접 확인이 어렵다면 상담 단계에서 분류 기준을 정하고, 현장에서 발견되는 주요 물품은 별도로 구분해 안내받는 방식으로 진행할 수 있습니다.
          올바른수거는 {region_name} 지역 현장 상황을 확인한 뒤 유품정리, 고독사청소, 특수청소가 필요한 범위를 나누어 안내합니다.
        </p>
      </div>
    </div>
  </section>
"""

def add_css(html):
    css = """
    .seo-plus .plus-grid {
      display:grid;
      grid-template-columns:repeat(4,1fr);
      gap:18px;
    }

    .seo-plus .plus-card {
      background:var(--card);
      border:1px solid var(--line);
      border-radius:22px;
      padding:24px;
      box-shadow:0 10px 28px rgba(54,90,76,0.07);
    }

    .seo-plus .plus-card strong {
      display:block;
      color:var(--main);
      font-size:18px;
      margin-bottom:8px;
    }

    .seo-plus .plus-card p {
      color:var(--muted);
      margin:0;
      font-size:15px;
    }

    @media(max-width:900px) {
      .seo-plus .plus-grid {
        grid-template-columns:1fr;
      }
    }
"""

    if ".seo-plus .plus-grid" in html:
        return html

    return html.replace("</style>", css + "\n  </style>")

def insert_extra_sections(html, region_name):
    # 이미 V5가 들어갔으면 중복 삽입 방지
    if "최근 문의 유형" in html and "COST DETAIL" in html:
        return html

    section = extra_section(region_name)

    # 작업 사례 CASE 섹션 뒤에 삽입
    case_pattern = re.compile(
        r'(<section>\s*<div class="wrap">\s*<div class="title">\s*<span>CASE</span>.*?</section>)',
        re.DOTALL
    )

    match = case_pattern.search(html)

    if match:
        insert_pos = match.end()
        html = html[:insert_pos] + "\n" + section + "\n" + html[insert_pos:]
    else:
        # CASE가 없으면 상담 섹션 앞에 삽입
        contact_pos = html.find('<section class="contact"')
        if contact_pos != -1:
            html = html[:contact_pos] + "\n" + section + "\n" + html[contact_pos:]
        else:
            html = html.replace("</main>", section + "\n</main>")

    return add_css(html)

def upgrade():
    root = Path(__file__).resolve().parent

    for region_name, slug in FEATURE_REGIONS:
        file_path = root / "regions" / slug / "index.html"

        if not file_path.exists():
            print(f"파일 없음: {region_name} / {file_path}")
            continue

        html = file_path.read_text(encoding="utf-8")
        html = insert_extra_sections(html, region_name)
        file_path.write_text(html, encoding="utf-8")

        print(f"SEO V5 적용 완료: {region_name}")

    print("\n완료: 대표지역 11개 SEO 강화 섹션 적용")

if __name__ == "__main__":
    upgrade()