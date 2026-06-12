from pathlib import Path
import re

def case_section(region_name, before_num, process_num, after_num):
    b = f"{before_num:02d}"
    p = f"{process_num:02d}"
    a = f"{after_num:02d}"

    return f"""
  <section>
    <div class="wrap">
      <div class="title">
        <span>CASE</span>
        <h2>{region_name} 유품정리 작업 사례</h2>
        <p>작업 전 현장 확인부터 소독·연무 과정, 작업 후 정리 완료까지 단계별로 진행합니다.</p>
      </div>

      <div class="case-timeline">
        <div class="case-step">
          <div class="case-text">
            <b>STEP 01</b>
            <h3>작업 전 현장 확인</h3>
            <p>유품의 양, 보관 물품, 폐기물 반출 범위와 이동 동선을 확인합니다.</p>
          </div>
          <img src="/image/cases/before-{b}.jpg" alt="{region_name} 유품정리 작업 전 현장">
        </div>

        <div class="case-step reverse">
          <div class="case-text">
            <b>STEP 02</b>
            <h3>소독·연무 작업 과정</h3>
            <p>필요한 경우 오염 정리 후 소독과 냄새 저감 작업을 함께 진행합니다.</p>
          </div>
          <img src="/image/cases/process-{p}.jpg" alt="{region_name} 유품정리 소독 연무 작업 과정">
        </div>

        <div class="case-step">
          <div class="case-text">
            <b>STEP 03</b>
            <h3>작업 후 정리 완료</h3>
            <p>유품 분류와 폐기물 반출 후 공간을 정돈하고 마무리 확인을 진행합니다.</p>
          </div>
          <img src="/image/cases/after-{a}.jpg" alt="{region_name} 유품정리 작업 후 정리 완료">
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

    if ".case-box" in html:
        return html.replace("    .case-box {\n", css + "\n    .case-box {\n")

    return html.replace("</style>", css + "\n  </style>")

def get_region_name(html, slug):
    title_match = re.search(r"<title>(.*?) 유품정리", html)
    if title_match:
        return title_match.group(1).strip()

    h1_match = re.search(r"<h1>(.*?) 유품정리", html)
    if h1_match:
        return h1_match.group(1).strip()

    return slug

def replace_or_insert_case(html, region_name, before_num, process_num, after_num):
    new_case = case_section(region_name, before_num, process_num, after_num)

    pattern = re.compile(
        r'\s*<section>\s*<div class="wrap">\s*<div class="title">\s*<span>CASE</span>.*?</section>',
        re.DOTALL
    )

    if pattern.search(html):
        html = pattern.sub("\n" + new_case + "\n", html, count=1)
    else:
        # 상담 섹션 앞에 CASE 삽입
        contact_pos = html.find('<section class="contact"')
        if contact_pos != -1:
            html = html[:contact_pos] + "\n" + new_case + "\n" + html[contact_pos:]
        else:
            html = html.replace("</main>", new_case + "\n</main>")

    return add_css(html)

def upgrade():
    root = Path(__file__).resolve().parent
    regions_dir = root / "regions"

    if not regions_dir.exists():
      print("regions 폴더가 없습니다.")
      return

    folders = sorted([p for p in regions_dir.iterdir() if p.is_dir()])

    count = 0

    for idx, folder in enumerate(folders, start=1):
        file_path = folder / "index.html"

        if not file_path.exists():
            continue

        before_num = ((idx - 1) % 30) + 1
        after_num = ((idx - 1) % 30) + 1
        process_num = ((idx - 1) % 25) + 1

        html = file_path.read_text(encoding="utf-8")
        region_name = get_region_name(html, folder.name)

        html = replace_or_insert_case(html, region_name, before_num, process_num, after_num)

        file_path.write_text(html, encoding="utf-8")

        print(
            f"{region_name} 적용 완료: "
            f"before-{before_num:02d}, process-{process_num:02d}, after-{after_num:02d}"
        )

        count += 1

    print(f"\n완료: 총 {count}개 지역 페이지 이미지 적용")

if __name__ == "__main__":
    upgrade()