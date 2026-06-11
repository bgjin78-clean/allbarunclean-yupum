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

def image_case_section(region_name, num):
    n = f"{num:02d}"

    return f"""
  <section>
    <div class="wrap">
      <div class="title">
        <span>CASE</span>
        <h2>{region_name} 유품정리 작업 사례</h2>
        <p>현장 상황에 따라 유품 분류, 소독·연무 작업, 정리 완료 과정을 단계별로 진행합니다.</p>
      </div>

      <div class="case-box">
        <div class="card">
          <img class="case-photo" src="/image/cases/before-{n}.jpg" alt="{region_name} 유품정리 작업 전 현장">
          <strong>작업 전 현장</strong>
          <p>정리가 필요한 공간의 물품 상태와 반출 범위를 확인합니다.</p>
        </div>

        <div class="card">
          <img class="case-photo" src="/image/cases/process-{n}.jpg" alt="{region_name} 유품정리 소독 연무 작업 과정">
          <strong>소독·연무 작업 과정</strong>
          <p>필요한 경우 오염 정리 후 소독과 냄새 저감 작업을 함께 진행합니다.</p>
        </div>

        <div class="card">
          <img class="case-photo" src="/image/cases/after-{n}.jpg" alt="{region_name} 유품정리 작업 후 정리 완료">
          <strong>작업 후 정리 완료</strong>
          <p>유품 분류와 폐기물 반출 후 공간을 정돈하고 마무리 확인을 진행합니다.</p>
        </div>
      </div>
    </div>
  </section>
"""

def ensure_photo_css(html):
    css = """
    .case-photo {
      width:100%;
      height:210px;
      object-fit:cover;
      border-radius:18px;
      display:block;
      margin-bottom:16px;
      background:#d8d0c3;
    }
"""
    if ".case-photo" in html:
        return html

    return html.replace(
        "    .case-img {\n",
        css + "\n    .case-img {\n"
    )

def replace_case_section(html, region_name, num):
    new_section = image_case_section(region_name, num)

    pattern = re.compile(
        r'\s*<section>\s*<div class="wrap">\s*<div class="title">\s*<span>CASE</span>.*?</section>',
        re.DOTALL
    )

    matches = list(pattern.finditer(html))
    if not matches:
        print(f"CASE 섹션을 찾지 못했습니다: {region_name}")
        return html

    # 첫 번째 CASE 섹션만 교체
    start, end = matches[0].span()
    html = html[:start] + "\n" + new_section + "\n" + html[end:]
    html = ensure_photo_css(html)
    return html

def upgrade():
    root = Path(__file__).resolve().parent

    for region_name, slug, num in FEATURE_REGIONS:
        file_path = root / "regions" / slug / "index.html"

        if not file_path.exists():
            print(f"파일 없음: {file_path}")
            continue

        html = file_path.read_text(encoding="utf-8")
        html = replace_case_section(html, region_name, num)
        file_path.write_text(html, encoding="utf-8")

        print(f"이미지 적용 완료: {region_name} / before-{num:02d}, process-{num:02d}, after-{num:02d}")

    print("\n완료: 대표지역 11개 작업 사례 이미지 적용")

if __name__ == "__main__":
    upgrade()