from pathlib import Path

root = Path(__file__).resolve().parent

OLD_BLOCK = """            <dl>
              <dt>크기</dt>
              <dd>480 × 380 × 340 mm</dd>
              <dt>가로 × 세로 × 높이</dt>
              <dd>48cm × 38cm × 34cm</dd>
            </dl>"""

NEW_BLOCK = """            <p class="box-size-line"><strong>가로×세로×높이</strong> 48cm × 38cm × 34cm <span class="box-size-mm">(480×380×340mm)</span></p>"""

OLD_CSS = """    .box-spec dl { margin: 0; display: grid; gap: 8px; }
    .box-spec dt { color: var(--main); font-weight: 800; font-size: 14px; }
    .box-spec dd { margin: 0 0 8px; color: var(--muted); font-size: 14px; }"""

NEW_CSS = """    .box-spec dl { margin: 0; display: grid; gap: 8px; }
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
    .box-size-mm { font-size: 14px; }"""

OLD_HTML = '<div class="box-visual" aria-hidden="true"></div>'
NEW_HTML = (
    '<img class="box-visual" src="/image/main/incineration-box.png" '
    'alt="우체국 5호 택배상자 (유품소각 기준 박스)" />'
)

targets = [root / "index.html", *sorted((root / "regions").glob("*/index.html"))]
count = 0
for path in targets:
    text = path.read_text(encoding="utf-8")
    updated = text.replace(OLD_BLOCK, NEW_BLOCK)
    if ".box-size-line" not in updated:
        updated = updated.replace(OLD_CSS, NEW_CSS)
    if updated != text:
        path.write_text(updated, encoding="utf-8")
        count += 1
        print(f"updated: {path.relative_to(root)}")

print(f"\n완료: {count}개 파일")
