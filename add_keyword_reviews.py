from pathlib import Path
import re
from datetime import date

from generate_reviews import (
    BASE_URL,
    BRAND,
    PHONE,
    PHONE_LINK,
    SHARED_CSS,
    header_html,
    footer_html,
    related_section_html,
    pick_case_set_numbers,
)

# 우선순위(대표) 지역 중 해당 키워드 작업후기가 없는 곳에만 추가
# 유품정리 미보유: 강남구, 송파구, 용산구, 용인시, 고양시
# 고인집정리 전 지역 미보유 → 서초구, 마포구, 수원시, 성남시, 화성시
EXTRA_REVIEWS = [
    {
        "region_type": "서울",
        "name": "강남구",
        "slug": "gangnam",
        "path": "gangnam/yupum",
        "tag": "유품정리",
        "place": "아파트",
        "title": "강남구 아파트 유품정리 작업후기",
        "summary": "강남구 아파트에서 고인 유품을 분류하고 보관품과 정리품을 구분해 진행한 유품정리 작업후기입니다.",
        "keywords": "강남구 유품정리, 강남구 아파트 유품정리, 서울 유품정리 작업후기",
        "details": [
            "강남구 역삼동 인근 아파트 유품정리 현장이었습니다. 관리사무소 협의와 주차 위치, 엘리베이터 사용 시간을 먼저 맞춘 뒤 유품 확인 범위를 가족분과 함께 정했습니다.",
            "사진, 서류, 귀중품은 별도로 모아 보관했고, 의류·생활용품은 남길 것과 정리할 것을 구분해 방 단위로 유품정리를 진행했습니다. 물품 양이 많아 반출 동선을 복도와 화물 엘리베이터 기준으로 잡았습니다.",
            "폐기물은 종류별로 나눠 반출했고, 작업 후 거실과 방을 비운 상태를 가족분과 함께 확인했습니다. 강남구 유품정리는 단지 규정에 맞춰 조용히, 정해진 시간 안에 마무리하는 것이 중요했습니다.",
        ],
    },
    {
        "region_type": "서울",
        "name": "송파구",
        "slug": "songpa",
        "path": "songpa/yupum",
        "tag": "유품정리",
        "place": "아파트",
        "title": "송파구 아파트 유품정리 작업후기",
        "summary": "송파구 대단지 아파트에서 유품 확인부터 공간 정리, 폐기물 반출까지 단계적으로 진행한 유품정리입니다.",
        "keywords": "송파구 유품정리, 송파구 아파트 유품정리, 서울 유품정리 작업후기",
        "details": [
            "송파구 잠실·문정 권역의 대단지 아파트 유품정리 상담이었습니다. 차량 진입과 폐기물 반출 동선이 단지마다 달라, 작업 전날 관리실에 반출 가능 시간을 확인했습니다.",
            "유품정리는 안방의 서류와 사진부터 시작했습니다. 가족분이 남기고 싶은 물건을 먼저 고르신 뒤, 나머지 생활용품과 가구를 정리·반출 순서로 나눴습니다.",
            "베란다와 창고에 쌓여 있던 물품까지 포함해 공간을 비웠고, 마무리 전 각 방을 다시 확인했습니다. 송파구 유품정리는 물품 양보다 반출 동선을 얼마나 짧게 잡느냐가 작업 시간을 좌우했습니다.",
        ],
    },
    {
        "region_type": "서울",
        "name": "용산구",
        "slug": "yongsan",
        "path": "yongsan/yupum",
        "tag": "유품정리",
        "place": "빌라",
        "title": "용산구 빌라 유품정리 작업후기",
        "summary": "용산구 빌라에서 유품 분류와 공간 정리를 신중하게 진행한 유품정리 작업후기입니다.",
        "keywords": "용산구 유품정리, 용산구 빌라 유품정리, 서울 유품정리 작업후기",
        "details": [
            "용산구 후암동 인근 빌라 유품정리 현장이었습니다. 오래된 주택과 빌라가 섞인 골목이라 주차와 계단 반출이 쉽지 않아, 작업 인원과 운반 순서를 미리 나눴습니다.",
            "1층 거실의 가구와 2층 방의 의류·서류를 구분해 유품정리를 진행했습니다. 가족분이 확인이 필요하다고 하신 상자류는 열어보지 않고 그대로 옮겨 드렸습니다.",
            "계단으로만 반출해야 해서 큰 가구는 분해 후 내렸고, 남은 생활폐기물은 분류해 반출했습니다. 용산구 유품정리는 건물 구조에 맞춰 동선을 잡는 과정이 작업의 핵심이었습니다.",
        ],
    },
    {
        "region_type": "경기",
        "name": "용인시",
        "slug": "yongin",
        "path": "yongin/yupum",
        "tag": "유품정리",
        "place": "아파트",
        "title": "용인시 아파트 유품정리 작업후기",
        "summary": "용인시 아파트에서 주소지와 반출 동선을 확인한 뒤 유품 분류·정리를 진행한 작업후기입니다.",
        "keywords": "용인시 유품정리, 용인시 아파트 유품정리, 경기 유품정리 작업후기",
        "details": [
            "용인시 기흥구 아파트 유품정리 현장이었습니다. 시 면적이 넓고 단지 규모도 커서, 상담 시 정확한 동·호수와 지하 주차장 진입 가능 여부를 먼저 확인했습니다.",
            "안방과 작은방의 유품을 사진·서류·생활용품으로 나눠 정리했습니다. 가족분이 멀리 계셔서 남길 물건 목록을 미리 받아 두었고, 현장에서 목록 기준으로 유품정리를 진행했습니다.",
            "폐기물 반출은 단지 내 지정 위치로 옮긴 뒤 차량에 실었습니다. 용인시 유품정리는 물품 양과 함께 단지 규정, 주차 환경을 맞춰야 해서 사전 확인이 특히 중요했습니다.",
        ],
    },
    {
        "region_type": "경기",
        "name": "고양시",
        "slug": "goyang",
        "path": "goyang/yupum",
        "tag": "유품정리",
        "place": "아파트",
        "title": "고양시 아파트 유품정리 작업후기",
        "summary": "고양시 일산권 아파트에서 보관품 분류와 폐기물 반출을 함께 진행한 유품정리 작업후기입니다.",
        "keywords": "고양시 유품정리, 고양시 아파트 유품정리, 경기 유품정리 작업후기",
        "details": [
            "고양시 일산동구 아파트 유품정리 상담이었습니다. 일산권은 아파트 비중이 높아 관리사무소 협의와 엘리베이터 사용이 작업 전 필수 확인 항목이었습니다.",
            "거실에 쌓인 생활용품과 방 안의 옷가지, 서류 상자를 구분해 유품정리를 진행했습니다. 가족분이 남기실 앨범과 인감·통장류는 별도 상자에 담아 바로 전달했습니다.",
            "정리 과정에서 나온 폐기물은 가구와 생활쓰레기를 나눠 반출했고, 작업 후 빈 공간을 함께 확인했습니다. 고양시 유품정리는 보관품을 얼마나 빨리 가려내느냐가 이후 정리 속도를 결정했습니다.",
        ],
    },
    {
        "region_type": "서울",
        "name": "서초구",
        "slug": "seocho",
        "path": "seocho/goinjip",
        "tag": "고인집정리",
        "place": "아파트",
        "title": "서초구 아파트 고인집정리 작업후기",
        "summary": "서초구 아파트에서 고인이 살던 집의 살림살이를 비우고 공간을 정리한 고인집정리 작업후기입니다.",
        "keywords": "서초구 고인집정리, 서초구 아파트 고인집정리, 서울 고인집정리 작업후기",
        "details": [
            "서초구 방배동 아파트 고인집정리 현장이었습니다. 유품만 골라내는 작업이 아니라, 고인이 살던 집 전체를 비워 임대 반환과 매매 준비를 해야 하는 경우였습니다.",
            "가구, 가전, 주방 살림, 옷장 정리까지 방마다 순서를 정해 고인집정리를 진행했습니다. 중요 서류와 사진류는 가족분이 직접 확인하신 뒤, 나머지 생활 물품을 반출했습니다.",
            "단지 내 반출 시간이 정해져 있어 오전에 큰 가구를 먼저 내렸습니다. 서초구 고인집정리는 보관품 분류와 집 비우기를 같은 날 맞춰야 해서 작업 범위를 사전에 분명히 나누는 것이 중요했습니다.",
        ],
    },
    {
        "region_type": "서울",
        "name": "마포구",
        "slug": "mapo",
        "path": "mapo/goinjip",
        "tag": "고인집정리",
        "place": "빌라",
        "title": "마포구 빌라 고인집정리 작업후기",
        "summary": "마포구 빌라에서 고인의 살림살이와 생활 공간을 함께 비운 고인집정리 현장입니다.",
        "keywords": "마포구 고인집정리, 마포구 빌라 고인집정리, 서울 고인집정리 작업후기",
        "details": [
            "마포구 연남·성산 인근 빌라 고인집정리 현장이었습니다. 원룸·오피스텔과 달리 방이 나뉘어 있고 계단 반출이라, 집 전체를 비우는 순서를 층과 방 기준으로 잡았습니다.",
            "고인집정리는 유품 확인 후 주방, 화장실, 베란다까지 살림을 걷어내는 작업이었습니다. 가족분이 남기실 물건은 현관 쪽에 모아 두었고, 나머지는 폐기·기부로 나눠 반출했습니다.",
            "골목 주차가 어려워 차량을 가까운 공터에 두고 소량씩 옮겼습니다. 마포구 고인집정리는 건물 구조보다 반출 동선이 작업 시간을 좌우했습니다.",
        ],
    },
    {
        "region_type": "경기",
        "name": "수원시",
        "slug": "suwon",
        "path": "suwon/goinjip",
        "tag": "고인집정리",
        "place": "아파트",
        "title": "수원시 아파트 고인집정리 작업후기",
        "summary": "수원시 아파트에서 고인이 사용하던 가구·가전과 생활물품을 정리해 집을 비운 고인집정리입니다.",
        "keywords": "수원시 고인집정리, 수원시 아파트 고인집정리, 경기 고인집정리 작업후기",
        "details": [
            "수원시 영통구 아파트 고인집정리 상담이었습니다. 유품 분류만으로는 공간이 비지 않아, 가구와 가전을 포함한 집 전체 정리를 요청하신 현장이었습니다.",
            "거실 소파와 장식장, 방의 옷장, 주방 가전 순으로 고인집정리를 진행했습니다. 가족분이 남기고 싶은 가전은 따로 포장했고, 나머지는 반출 목록에 올렸습니다.",
            "단지 지하 주차장에서 화물 엘리베이터를 사용할 수 있어 큰 가구 반출이 수월했습니다. 수원시 고인집정리는 물품 양과 반출 환경에 따라 인원 구성이 달라지는 전형적인 아파트 현장이었습니다.",
        ],
    },
    {
        "region_type": "경기",
        "name": "성남시",
        "slug": "seongnam",
        "path": "seongnam/goinjip",
        "tag": "고인집정리",
        "place": "아파트",
        "title": "성남시 아파트 고인집정리 작업후기",
        "summary": "성남시 분당권 아파트에서 고인 집의 살림을 비우고 공간을 정돈한 고인집정리 작업후기입니다.",
        "keywords": "성남시 고인집정리, 성남시 아파트 고인집정리, 경기 고인집정리 작업후기",
        "details": [
            "성남시 분당구 아파트 고인집정리 현장이었습니다. 분당·수정·중원 생활권이 달라 단지 규정과 주차 환경이 제각각이라, 작업 전 관리실에 반출 가능 여부를 확인했습니다.",
            "고인이 오래 거주하신 집이라 물품이 방마다 가득했습니다. 고인집정리는 서류와 사진 분류 후, 옷장·주방·베란다 순으로 살림을 걷어내는 방식으로 진행했습니다.",
            "대형 가구는 분해 후 엘리베이터로 내렸고, 남은 생활폐기물은 분류해 반출했습니다. 성남시 고인집정리는 아파트형 현장에서 보관품 확인과 집 비우기를 같은 일정에 맞추는 것이 핵심이었습니다.",
        ],
    },
    {
        "region_type": "경기",
        "name": "화성시",
        "slug": "hwaseong",
        "path": "hwaseong/goinjip",
        "tag": "고인집정리",
        "place": "빌라",
        "title": "화성시 빌라 고인집정리 작업후기",
        "summary": "화성시 빌라에서 고인이 살던 집의 살림살이를 정리하고 공간을 비운 고인집정리 현장입니다.",
        "keywords": "화성시 고인집정리, 화성시 빌라 고인집정리, 경기 고인집정리 작업후기",
        "details": [
            "화성시 동탄 인근 빌라 고인집정리 현장이었습니다. 신도시 아파트와 달리 엘리베이터 없는 빌라라, 계단 반출과 골목 주차부터 계획을 세웠습니다.",
            "고인집정리는 1층 거실 가구부터 시작해 방과 주방, 다용도실까지 살림을 정리하는 순서로 진행했습니다. 가족분이 확인이 필요하다고 하신 상자만 남기고 나머지는 반출했습니다.",
            "큰 장롱은 현장에서 분해해 내렸고, 마당에 있던 잡동사니까지 함께 치웠습니다. 화성시 고인집정리는 주거 형태가 다양해 빌라형 현장은 반출 동선을 먼저 보는 것이 안전했습니다.",
        ],
    },
]


def extra_card_html(content):
    return f"""
        <article class="review-card">
          <span class="review-tag">{content["tag"]}</span>
          <h3>{content["title"]}</h3>
          <p>{content["summary"]}</p>
          <a href="/reviews/{content["path"]}/" class="review-link">자세히 보기 →</a>
        </article>"""


def extra_detail_page_html(content):
    before_imgs = "\n".join(
        f'          <img src="/image/cases/before-{n:03d}.jpg" alt="{content["name"]} {content["tag"]} 작업 전 현장">'
        for n in content["before_nums"]
    )
    after_imgs = "\n".join(
        f'          <img src="/image/cases/after-{n:03d}.jpg" alt="{content["name"]} {content["tag"]} 작업 후 현장">'
        for n in content["after_nums"]
    )
    detail_paragraphs = "\n".join(f"        <p>{p}</p>" for p in content["details"])
    page_url = f"{BASE_URL}/reviews/{content['path']}/"
    title = f"{content['title']} | {BRAND}"
    desc = content["summary"]
    keywords = content["keywords"]

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="canonical" href="{page_url}" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="keywords" content="{keywords}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{page_url}" />
  <link rel="icon" href="/favicon-allbarun.png" />
  <style>{SHARED_CSS}</style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{content['title']}",
    "description": "{desc}",
    "author": {{ "@type": "Organization", "name": "{BRAND}" }},
    "publisher": {{ "@type": "Organization", "name": "{BRAND}" }},
    "mainEntityOfPage": "{page_url}",
    "dateModified": "{date.today().isoformat()}"
  }}
  </script>
</head>
<body>
{header_html()}
<main>
  <section class="hero">
    <div class="hero-inner">
      <div class="breadcrumb"><a href="/">홈</a> · <a href="/reviews/">작업후기</a> · {content["name"]} · {content["tag"]}</div>
      <div class="badge">{content["tag"]}</div>
      <h1>{content["title"]}</h1>
      <p>{content["summary"]}</p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="article-box">
        <h1>{content["title"]}</h1>
        <p class="lead">{content["summary"]}</p>
{detail_paragraphs}

        <div class="photo-block">
          <h2>작업 전 현장</h2>
          <div class="photo-grid">
{before_imgs}
          </div>

          <h2>작업 후 정리</h2>
          <div class="photo-grid">
{after_imgs}
          </div>
        </div>

        <div class="cta-box">
          <h2>{content["name"]} {content["tag"]} 상담</h2>
          <p>비슷한 현장 상담이 필요하시면 사진과 주소를 남겨주시면 확인 후 연락드립니다.</p>
          <div class="btn-row">
            <a href="tel:{PHONE_LINK}" class="btn btn-primary">전화 상담 {PHONE}</a>
            <a href="/regions/{content["slug"]}/" class="btn btn-outline">{content["name"]} 유품정리 안내</a>
            <a href="/reviews/" class="btn btn-outline">작업후기 목록</a>
            <a href="/#contact" class="btn btn-outline">상담 접수</a>
          </div>
        </div>
      </div>
    </div>
  </section>
{related_section_html()}
</main>
{footer_html()}
</body>
</html>
"""


def extra_section_html(contents):
    cards = "".join(extra_card_html(c) for c in contents)
    return f"""<!-- extra-keyword-reviews-start -->
      <div class="area-block">
        <h3>유품정리 · 고인집정리 작업후기</h3>
        <div class="review-grid">
{cards}
        </div>
      </div>
      <!-- extra-keyword-reviews-end -->"""


def update_list_page(contents):
    root = Path(__file__).resolve().parent
    list_path = root / "reviews" / "index.html"
    html = list_path.read_text(encoding="utf-8")
    block = extra_section_html(contents)
    start = "<!-- extra-keyword-reviews-start -->"
    end = "<!-- extra-keyword-reviews-end -->"

    if start in html and end in html:
        html = re.sub(
            re.escape(start) + r".*?" + re.escape(end),
            block,
            html,
            count=1,
            flags=re.S,
        )
    else:
        needle = '      <div class="area-block">\n        <h3>서울특별시 25개 구</h3>'
        if needle not in html:
            raise RuntimeError("작업후기 목록에서 서울 섹션을 찾지 못했습니다.")
        html = html.replace(needle, block + "\n\n" + needle, 1)

    list_path.write_text(html, encoding="utf-8")


def generate():
    root = Path(__file__).resolve().parent
    reviews_dir = root / "reviews"

    contents = []
    for item in EXTRA_REVIEWS:
        content = dict(item)
        nums = pick_case_set_numbers(content["path"], 2)
        content["before_nums"] = nums
        content["after_nums"] = nums
        contents.append(content)

        page_dir = reviews_dir / content["path"]
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(
            extra_detail_page_html(content),
            encoding="utf-8",
        )

    update_list_page(contents)

    print(f"완료: 키워드 작업후기 {len(contents)}개 생성")
    for content in contents:
        print(f"  /reviews/{content['path']}/  [{content['tag']}] {content['title']}")


if __name__ == "__main__":
    generate()
