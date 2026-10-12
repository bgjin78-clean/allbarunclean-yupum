from pathlib import Path
import re
from io import BytesIO
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
LAZY_RE = re.compile(r"<img (?![^>]*\bloading=)")


def kb(n):
    return f"{n / 1024:,.0f}KB"


def optimize_favicon():
    fav = ROOT / "favicon-allbarun.png"
    with Image.open(fav) as im:
        if im.size[0] <= 192:
            return
        before = fav.stat().st_size
        small = im.convert("RGBA").resize((192, 192), Image.LANCZOS)
    small.save(fav, optimize=True)
    print("favicon", kb(before), "->", kb(fav.stat().st_size))


def hero_to_jpg():
    src = ROOT / "yupum-main.png"
    dst = ROOT / "yupum-main.jpg"
    if dst.exists():
        return
    with Image.open(src) as im:
        im.convert("RGB").save(dst, "JPEG", quality=80, optimize=True, progressive=True)
    print("hero", kb(src.stat().st_size), "->", kb(dst.stat().st_size))


def recompress_photos():
    saved = changed = 0
    photos = sorted((ROOT / "image" / "main").glob("*.jpg")) + sorted((ROOT / "image" / "cases").glob("*.jpg"))
    for p in photos:
        orig = p.read_bytes()
        with Image.open(BytesIO(orig)) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            im.thumbnail((1280, 1280), Image.LANCZOS)
            buf = BytesIO()
            im.save(buf, "JPEG", quality=80, optimize=True, progressive=True)
        new = buf.getvalue()
        if len(new) < len(orig) * 0.85:
            p.write_bytes(new)
            saved += len(orig) - len(new)
            changed += 1
    print(f"photos: {changed}/{len(photos)} recompressed, saved {saved / 1024 / 1024:,.1f}MB")


def patch_markup():
    files = [p for p in ROOT.rglob("*.html") if "regions_backup" not in p.parts]
    files += list(ROOT.glob("*.py"))
    touched = 0
    for p in files:
        if p.name == Path(__file__).name:
            continue
        text = p.read_text(encoding="utf-8")
        new = text.replace("yupum-main.png", "yupum-main.jpg")
        new = LAZY_RE.sub('<img loading="lazy" decoding="async" ', new)
        if new != text:
            p.write_text(new, encoding="utf-8")
            touched += 1
    print("files updated (hero ref / lazy):", touched)


if __name__ == "__main__":
    optimize_favicon()
    hero_to_jpg()
    recompress_photos()
    patch_markup()
