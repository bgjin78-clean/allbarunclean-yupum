"""유품소각 비용 4~5만원 → 5만원 일괄 수정."""
from __future__ import annotations

from pathlib import Path

REPLACEMENTS = [
    ("4만원 <span>~5만원/box</span>", "5만원 <span>/box</span>"),
    ("4만원 ~ 5만원", "5만원"),
    ("4만원~5만원", "5만원"),
    ("4~5만원", "5만원"),
]

TARGETS = [
    "index.html",
    "generate_regions.py",
    "upgrade_yupum_incineration.py",
]


def apply(text: str) -> str:
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    return text


def main() -> None:
    root = Path(__file__).resolve().parent
    count = 0
    paths = [root / name for name in TARGETS]
    paths.extend(sorted((root / "regions").glob("*/index.html")))

    for path in paths:
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = apply(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            count += 1
            print(f"updated: {path.relative_to(root)}")

    print(f"\n완료: {count}개 파일 유품소각 비용 5만원으로 수정")


if __name__ == "__main__":
    main()
