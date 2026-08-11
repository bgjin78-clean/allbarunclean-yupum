from pathlib import Path

root = Path(__file__).resolve().parent

OLD_CSS = """    .box-visual {
      width: 120px;
      height: 90px;
      margin: 0 auto 16px;
      background: linear-gradient(145deg, #c4a574, #a8844f);
      border-radius: 4px;
      box-shadow: 4px 6px 0 rgba(0,0,0,0.12);
    }"""

NEW_CSS = """    .box-visual {
      display: block;
      width: 200px;
      max-width: 100%;
      height: auto;
      margin: 0 auto 16px;
      object-fit: contain;
    }"""

OLD_HTML = '<div class="box-visual" aria-hidden="true"></div>'
NEW_HTML = (
    '<img class="box-visual" src="/image/main/incineration-box.png" '
    'alt="우체국 5호 택배상자 (유품소각 기준 박스)" />'
)

targets = [root / "index.html", *sorted((root / "regions").glob("*/index.html"))]
count = 0
for path in targets:
    text = path.read_text(encoding="utf-8")
    updated = text.replace(OLD_CSS, NEW_CSS).replace(OLD_HTML, NEW_HTML)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        count += 1
        print(f"updated: {path.relative_to(root)}")

print(f"\n완료: {count}개 파일")
