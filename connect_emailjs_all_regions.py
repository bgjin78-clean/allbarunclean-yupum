from pathlib import Path
import re

PUBLIC_KEY = "JKsVOKPtnWHIr2BCV"
SERVICE_ID = "allbarunclean-waste"
TEMPLATE_ID = "template_b4ox5js"

EMAILJS_SCRIPT = f"""
<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
<script>
  emailjs.init("{PUBLIC_KEY}");

  function checkPrivacy() {{
    const checked = document.getElementById("privacyCheck").checked;

    if (!checked) {{
      alert("개인정보 수집 및 이용 동의가 필요합니다.");
      return false;
    }}

    const form = document.querySelector("form");
    const inputs = form.querySelectorAll("input");

    const params = {{
      service: form.querySelector("select").value,
      name: inputs[0].value,
      phone: inputs[1].value,
      region: inputs[2].value,
      message: form.querySelector("textarea").value
    }};

    emailjs.send("{SERVICE_ID}", "{TEMPLATE_ID}", params)
      .then(function () {{
        alert("상담 신청이 접수되었습니다. 확인 후 연락드리겠습니다.");
        form.reset();
      }})
      .catch(function (error) {{
        console.error("EmailJS 오류:", error);
        alert("접수 중 오류가 발생했습니다. 전화 상담을 이용해 주세요.");
      }});

    return false;
  }}
</script>
"""

def replace_emailjs(html):
    # 기존 EmailJS / checkPrivacy 스크립트 제거
    html = re.sub(
        r'<script src="https://cdn\.jsdelivr\.net/npm/@emailjs/browser@4/dist/email\.min\.js"></script>\s*',
        '',
        html,
        flags=re.DOTALL
    )

    html = re.sub(
        r'<script>\s*emailjs\.init\(.*?</script>\s*',
        '',
        html,
        flags=re.DOTALL
    )

    html = re.sub(
        r'<script>\s*function checkPrivacy\(\).*?</script>',
        EMAILJS_SCRIPT,
        html,
        flags=re.DOTALL
    )

    return html

def run():
    root = Path(__file__).resolve().parent

    files = []

    # 유품 메인
    files.append(root / "index.html")

    # 전체 지역 페이지
    regions_dir = root / "regions"
    for path in regions_dir.glob("*/index.html"):
        files.append(path)

    count = 0

    for file in files:
        if not file.exists():
            continue

        html = file.read_text(encoding="utf-8")

        if "checkPrivacy" not in html:
            print(f"건너뜀: checkPrivacy 없음 - {file}")
            continue

        new_html = replace_emailjs(html)
        file.write_text(new_html, encoding="utf-8")
        print(f"메일 연결 완료: {file}")
        count += 1

    print(f"\n완료: 총 {count}개 페이지 EmailJS 연결")

if __name__ == "__main__":
    run()