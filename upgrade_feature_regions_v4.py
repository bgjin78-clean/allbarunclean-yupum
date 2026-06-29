from pathlib import Path
import re

FEATURE_REGIONS = [
    ("강남구", "gangnam", 1),
    ("송파구", "songpa", 2),
    ("서초구", "seocho", 3),
    ("마포구", "mapo", 4),
    ("용산구", "yongsan", 5),
    ("수원시", "suwon", 6),
    ("성남시", "seongnam", 7),
    ("용인시", "yongin", 8),
    ("고양시", "goyang", 9),
    ("화성시", "hwaseong", 10),
    ("남양주시", "namyangju", 11),
]

def case_section(region_name, num):
    n = f"{num:02d}"

    return f"""
  <section>
    <div class="wrap">
      <div class="title">
        <span>CASE</span>
        <h2>{region_name} 유품정리 작업 사례</h2>
        <p>현장 확인부터 소독·연무 작업, 정리 완료까지 단계별로 신중하게 진행합니다.</p>
      </div>

      <div class="case-timeline">
        <div class="case-step">
          <div class="case-text">
            <b>STEP 01</b>
            <h3>작업 전 현장 확인</h3>
            <p>
              유품의 양, 보관이 필요한 물품, 폐기물 반출 범위, 건물 구조와 이동 동선을 먼저 확인합니다.
              현장 상황을 확인한 뒤 필요한 작업 인원과 절차를 안내합니다.
            </p>
          </div>
          <img src="/image/main/before-{n}.jpg" alt="{region_name} 유품정리 작업 전 현장">
        </div>

        <div class="case-step reverse">
          <div class="case-text">
            <b>STEP 02</b>
            <h3>소독·연무 작업 과정</h3>
            <p>
              고독사청소나 특수청소가 필요한 경우 오염 정리 후 소독과 냄새 저감 작업을 함께 진행합니다.
              공간 상태에 따라 연무 작업과 마무리 소독을 단계적으로 진행합니다.
            </p>
          </div>
          <img src="/image/main/process-{n}.jpg" alt="{region_name} 유품정리 소독 연무 작업 과정">
        </div>

        <div class="case-step">
          <div class="case-text">
            <b>STEP 03</b>
            <h3>작업 후 정리 완료</h3>
            <p>
              유품 분류와 폐기물 반출 후 공간을 정돈하고 마무리 확인을 진행합니다.
              가족분들이 확인해야 할 물품은 별도로 구분하여 안내드립니다.
            </p>
          </div>
          <img src="/image/main/after-{n}.jpg" alt="{region_name} 유품정리 작업 후 정리 완료">
        </div>
      </div>
    </div>
  </section>
"""

def add_css(html):
    css = """
    .case-timeline {
      display:flex;
      flex-direction:column;
      gap:26px;
    }

    .case-step {
      display:grid;
      grid-template-columns:0.9fr 1.1fr;
      gap:28px;
      align-items:center;
      background:var(--card);
      border:1px solid var(--line);
      border-radius:26px;
      padding:28px;
      box-shadow:0 10px 28px rgba(54,90,76,0.07);
    }

    .case-step.reverse {
      grid-template-columns:1.1fr 0.9fr;
    }

    .case-step.reverse .case-text {
      order:2;
    }

    .case-step.reverse img {
      order:1;
    }

    .case-step img {
      width:100%;
      height:320px;
      object-fit:cover;
      border-radius:20px;
      display:block;
      background:#d8d0c3;
    }

    .case-text b {
      display:inline-block;
      color:var(--point);
      font-size:14px;
      font-weight:900;
      margin-bottom:8px;
    }

    .case-text h3 {
      color:var(--main);
      font-size:26px;
      margin:0 0 12px;
      letter-spacing:-0.8px;
    }

    .case-text p {
      color:var(--muted);
      margin:0;
    }

    @media(max-width:900px) {
      .case-step,
      .case-step.reverse {
        grid-template-columns:1fr;
      }

      .case-step.reverse .case-text,
      .case-step.reverse img {
        order:initial;
      }

      .case-step img {
        height:240px;
      }
    }
"""

    if ".case-timeline" in html:
        return html

    return html.replace("    .case-box {\n", css + "\n    .case-box {\n")

def replace_case(html, region_name, num):
    new_case = case_section(region_name, num)

    pattern = re.compile(
        r'\s*<section>\s*<div class="wrap">\s*<div class="title">\s*<span>CASE</span>.*?</section>',
        re.DOTALL
    )

    match = pattern.search(html)

    if not match:
        print(f"CASE 섹션을 찾지 못했습니다: {region_name}")
        return html

    html = html[:match.start()] + "\n" + new_case + "\n" + html[match.end():]
    html = add_css(html)

    return html

def upgrade():
    root = Path(__file__).resolve().parent

    for region_name, slug, num in FEATURE_REGIONS:
        file_path = root / "regions" / slug / "index.html"

        if not file_path.exists():
            print(f"파일 없음: {file_path}")
            continue

        html = file_path.read_text(encoding="utf-8")
        html = replace_case(html, region_name, num)
        file_path.write_text(html, encoding="utf-8")

        print(f"V4 작업사례 적용 완료: {region_name}")

    print("\n완료: 대표지역 11개 V4 작업사례 섹션 적용")

if __name__ == "__main__":
    upgrade()