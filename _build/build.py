# -*- coding: utf-8 -*-
"""執行： python3 build.py  → 重新產生所有 HTML 頁面（在上一層資料夾）"""
import os, html
from data import SITE, VERTICALS, FILMS, PRESS

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Manrope:wght@300;400;500;600&family=Noto+Sans+TC:wght@300;400;500&family=Noto+Serif+TC:wght@400;500&display=swap" rel="stylesheet">'

def bi(en, zh):
    return f'<span data-en>{en}</span><span data-zh>{zh}</span>'

def shell(title, body, root="", active="", desc="", ogimg=""):
    nav = lambda href, key, en, zh: f'<li><a href="{root}{href}"{" class=on" if active==key else ""}>{bi(en,zh)}</a></li>'
    og = f'<meta property="og:image" content="{root}{ogimg}">' if ogimg else ""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc or 'Chin-En Gau — New York based filmmaker. Producer of vertical short-drama series for DramaBox; director and cinematographer of narrative and documentary films.')}">
<meta property="og:title" content="{html.escape(title)}">{og}
{FONTS}
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<nav class="nav">
  <a class="brand" href="{root}index.html">{bi(SITE["name"],"高靖恩")}</a>
  <button class="burger" id="burger">Menu</button>
  <ul id="menu">
    {nav("verticals/index.html","verticals","Verticals","豎屏短劇")}
    {nav("films/index.html","films","Films","電影作品")}
    {nav("press.html","press","Press","報導")}
    {nav("about.html","about","About","關於")}
    {nav("about.html#contact","contact","Contact","聯絡")}
    <li><button class="lang" id="lang">中文</button></li>
  </ul>
</nav>
<main>
{body}
</main>
<footer>
  <span>© <span id="yr"></span> {SITE["name"]} · New York</span>
  <span><a href="{SITE["imdb"]}" target="_blank" rel="noopener">IMDb</a> &nbsp;·&nbsp; <a href="{SITE["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a> &nbsp;·&nbsp; <a href="mailto:{SITE["email"]}">Email</a></span>
</footer>
<div class="modal" id="modal"><button class="x" id="closemodal">Close ✕</button><div class="box" id="modalbox"></div></div>
<script src="{root}assets/site.js"></script>
</body>
</html>'''

def write(path, content):
    p = os.path.join(OUT, path); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content); print("wrote", path)

# ---------------- HOME ----------------
posters = [v["img"] for v in VERTICALS]
film_stills = [s for f in FILMS for s in ([f["hero"]] if f["hero"] else []) + f["stills"]]
def marquee(imgs, cols, cls):
    # split images across columns; each column duplicated so the CSS loop is seamless
    out = ""
    for c in range(cols):
        col = imgs[c::cols] or imgs
        while len(col) < 4: col = col + col
        tiles = "".join(f'<img src="img/{p}" alt="" loading="lazy">' for p in col)
        out += f'<div class="col c{c%2}" style="animation-duration:{38 + c*9}s">{tiles}{tiles}</div>'
    return f'<div class="bg marquee {cls}">{out}</div>'
home = f'''
<header class="hero" id="top">
  <div class="poster"></div>
  <div id="ytwrap" class="yt"><div id="ytbg"></div></div>
  <div id="curtain" class="curtain"></div>
  <div class="shade"></div>
  <div class="txt">
    <div>
      <p class="eyebrow" style="color:var(--ink2)">{bi("Filmmaker · New York","影像創作者 · 紐約")}</p>
      <h1 style="margin-top:14px"><span data-en>Chin-En<br><em>Gau</em></span><span data-zh class="zhname">高靖恩</span></h1>
      <p class="roles">{bi("Producer · Director · Cinematographer · Editor","製片 · 導演 · 攝影 · 剪接")}</p>
    </div>
    <a class="reelbtn" href="#" data-reel><i></i>{bi("Watch reel with sound","觀看作品集（含聲音）")}</a>
  </div>
  <div class="scroll"></div>
</header>
<section class="intro rv">
  <div class="wrap">
    <p data-en>A Taiwanese filmmaker based in New York, working between two extremes: producing chart-topping vertical short dramas for DramaBox, and directing and shooting quiet films that follow immigrants, family, and the feelings that hide inside everyday life.</p>
    <p data-zh>一名台灣出生、現居紐約的影像創作者。他的作品穿梭在兩個極端：一方面為 DramaBox 打造登上榜首的豎屏短劇，另一方面則專注於執導與攝影，用溫柔的鏡頭記錄移民、家庭，以及那些藏在日常中難以言說的情感。</p>
    <a class="more" href="about.html">{bi("More about me","更多關於我")} →</a>
  </div>
</section>
<section class="doors">
  <a class="door vert" href="verticals/index.html">
    {marquee(posters, 4, "mv")}
    <span class="count">{len(VERTICALS):02d}</span>
    <div>
      <p class="eyebrow">{bi("TV Mini Series · Vertical","豎屏迷你劇集")}</p>
      <h2>Verticals</h2>
      <p>{bi("Vertical short-drama series produced for DramaBox — charting No.1 in new releases, with over two million views a day at peak.","為 DramaBox 製作的豎屏短劇，曾登上新片榜第一，單日觀看最高突破兩百萬。")}</p>
      <span class="go">{bi("Enter","進入")} →</span>
    </div>
  </a>
  <a class="door" href="films/index.html">
    {marquee(film_stills, 3, "mf")}
    <span class="count">{len(FILMS):02d}</span>
    <div>
      <p class="eyebrow">{bi("Features · Shorts · Documentary","長片 · 短片 · 紀錄片")}</p>
      <h2>Films</h2>
      <p>{bi("Narrative and documentary work as director, cinematographer and editor — Film at Lincoln Center, Tribeca, Sundance Documentary Fund.","以導演、攝影與剪接身分參與的敘事片與紀錄片——林肯中心電影協會、翠貝卡影展、日舞影展紀錄片基金。")}</p>
      <span class="go">{bi("Enter","進入")} →</span>
    </div>
  </a>
</section>'''
write("index.html", shell("Chin-En Gau — Filmmaker", home, ogimg="img/a-journey-of-jack-02.jpg"))

# ---------------- VERTICALS INDEX ----------------
cards = ""
for v in VERTICALS:
    tag = f'<span class="tag">{v["rank"]}</span>' if v["rank"] else ""
    ai = '<span class="tag ai">AI</span>' if v["ai"] else ""
    stat = f'{v["views"]} {bi("views","觀看")}' + (f' · {v["rank"]} {bi("new releases","新片榜")}' if v["rank"] else "")
    cards += f'''
  <a class="vcard rv" href="{v["slug"]}.html">
    <div class="frame"><img src="../img/{v["img"]}" alt="{html.escape(v["title"])}">{tag}{ai}</div>
    <h3>{v["title"]}</h3>
    <div class="meta">{v["year"]} · {bi("Producer","製片")}{bi(" · full AI production"," · 全 AI 製作") if v["ai"] else ""} · {v["episodes"]} {bi("episodes","集")}</div>
    <div class="stat">{stat}</div>
  </a>'''
vindex = f'''
<div class="wrap">
  <header class="phead">
    <p class="crumb"><a href="../index.html">Home</a><span>/</span>Verticals</p>
    <h1>Verticals</h1>
    <p class="lead">{bi("In-house producer at DramaBox, New York (2025–2026). Showrunner-style oversight from concept to final cut — script, casting and edit — with pacing, hooks and episode breaks shaped daily by retention and ranking data. Three titles produced with a fully AI-generated pipeline.","DramaBox 紐約內部製片（2025–2026）。以 showrunner 方式從概念到定剪全程把關——劇本、選角、剪接——並每日依留存率與榜單數據調整節奏、鉤子與分集點。其中三部以全 AI 流程製作。")}</p>
  </header>
  <div class="kpis rv">
    <div><b>10</b><span>{bi("Series produced","製作劇集")}</span></div>
    <div><b>No.1</b><span>{bi("Peak new-release rank","新片榜最高名次")}</span></div>
    <div><b>2M+</b><span>{bi("Peak views / day","單日最高觀看")}</span></div>
    <div><b>75M+</b><span>{bi("Total views, titles shown","本頁作品累計觀看")}</span></div>
  </div>
  <div class="vgrid">{cards}
  </div>
</div>'''
write("verticals/index.html", shell("Verticals — Chin-En Gau", vindex, root="../", active="verticals"))

# ---------------- VERTICAL DETAIL ----------------
for i, v in enumerate(VERTICALS):
    prev = VERTICALS[i-1]; nxt = VERTICALS[(i+1) % len(VERTICALS)]
    facts = f'''
    <dl><dt>{bi("Role","職務")}</dt><dd><b>{bi("Producer","製片")}</b>{bi(" — full AI production"," — 全 AI 製作") if v["ai"] else ""}</dd></dl>
    <dl><dt>{bi("Platform","平台")}</dt><dd>DramaBox · {v["year"]}</dd></dl>
    <dl><dt>{bi("Episodes","集數")}</dt><dd>{v["episodes"]}</dd></dl>
    <dl><dt>{bi("Views","總觀看")}</dt><dd><b>{v["views"]}</b></dd></dl>'''
    if v["rank"]:
        facts += f'<dl><dt>{bi("Chart","榜單")}</dt><dd><b>{v["rank"]}</b> {bi("in new releases","新片榜")}{(" · "+v["peak"]) if v["peak"] else ""}{(" · "+bi(v["extra_en"],v["extra_zh"])) if v["extra_en"] else ""}</dd></dl>'
    facts += f'<dl><dt>{bi("Genre","類型")}</dt><dd>{" · ".join(v["genres"])}</dd></dl>'
    body = f'''
<div class="vwork">
<header class="work-hero"><div class="wrap txt">
  <p class="crumb"><a href="../index.html">Home</a><span>/</span><a href="index.html">Verticals</a><span>/</span>{v["year"]}</p>
  <h1>{v["title"]}</h1>
</div></header>
<div class="wrap work-body">
  <aside>
    <div class="poster"><img src="../img/{v["img"]}" alt="{html.escape(v["title"])}"></div>
  </aside>
  <div class="syn">
    <h2>{bi("Synopsis","劇情簡介")}</h2>
    <p data-en>{v["syn_en"]}</p><p data-zh>{v["syn_zh"]}</p>
    <div class="facts">{facts}</div>
    <a class="back" href="index.html">← {bi("All verticals","回到所有短劇")}</a>
  </div>
</div>
<nav class="pn">
  <a href="{prev["slug"]}.html"><p class="eyebrow">← {bi("Previous","上一部")}</p><b>{prev["title"]}</b></a>
  <a class="next" href="{nxt["slug"]}.html"><p class="eyebrow">{bi("Next","下一部")} →</p><b>{nxt["title"]}</b></a>
</nav>
</div>'''
    write(f"verticals/{v['slug']}.html", shell(f'{v["title"]} — Chin-En Gau', body, root="../", active="verticals", desc=v["syn_en"], ogimg="img/"+v["img"]))

# ---------------- FILMS INDEX ----------------
fcards = ""
for f in FILMS:
    media = f'<div class="media"><img src="../img/{f["hero"]}" alt=""></div>' if f["hero"] else ""
    laur = "".join(f"<span>{l}</span>" for l in f["laurels"][:3])
    syn = f'<p>{bi(f["syn_en"], f["syn_zh"])}</p>' if f["syn_en"] else ""
    fcards += f'''
  <a class="fcard rv{'' if f["hero"] else ' noimg'}" href="{f["slug"]}.html">
    {media}
    <div>
      <div class="yr">{(str(f["year"])+" · ") if f["year"] else ""}{bi(f["kind_en"], f["kind_zh"])}</div>
      <h3>{f["title"]}</h3>
      <div class="role">{bi(f["role_en"], f["role_zh"])}</div>
      {syn}
      <div class="laurels">{laur}</div>
      <span class="go">{bi("View project","查看作品")} →</span>
    </div>
  </a>'''
findex = f'''
<div class="wrap">
  <header class="phead">
    <p class="crumb"><a href="../index.html">Home</a><span>/</span>Films</p>
    <h1>Films</h1>
    <p class="lead">{bi("Director, writer, cinematographer and editor on independent narrative work; director of photography on feature documentary and theatre-film. Screened at Film at Lincoln Center, Tribeca (WIP) and Fargo; supported by the Sundance Institute Documentary Fund and The Gotham.","獨立敘事作品的導演、編劇、攝影與剪接；紀錄長片與劇場電影的攝影指導。作品曾於林肯中心電影協會、翠貝卡影展（WIP）與法戈影展放映，並獲日舞影展紀錄片基金與 The Gotham 支持。")}</p>
  </header>
  <div class="flist">{fcards}
  </div>
</div>'''
write("films/index.html", shell("Films — Chin-En Gau", findex, root="../", active="films"))

# ---------------- FILM DETAIL ----------------
for i, f in enumerate(FILMS):
    prev = FILMS[i-1]; nxt = FILMS[(i+1) % len(FILMS)]
    hero = f'<img src="../img/{f["hero"]}" alt="">' if f["hero"] else ""
    facts = f'''
    <dl><dt>{bi("Role","職務")}</dt><dd><b>{bi(f["role_en"], f["role_zh"])}</b></dd></dl>
    <dl><dt>{bi("Format","形式")}</dt><dd>{bi(f["kind_en"], f["kind_zh"])}{(" · "+f["runtime"]) if f.get("runtime") and f["runtime"] not in f["kind_en"] else ""}</dd></dl>
'''
    if f["year"]: facts += f'<dl><dt>{bi("Year","年份")}</dt><dd>{f["year"]}</dd></dl>'
    if f.get("status_en"): facts += f'<dl><dt>{bi("Notes","備註")}</dt><dd>{bi(f["status_en"], f["status_zh"])}</dd></dl>'
    for k, val in f.get("credits", []): facts += f'<dl><dt>{k}</dt><dd>{val}</dd></dl>'
    laur = "".join(f"<span>{l}</span>" for l in f["laurels"])
    poster = f'<div class="poster" style="aspect-ratio:2/3;max-width:320px"><img src="../img/{f["poster"]}" alt=""></div>' if f.get("poster") else ""
    syn = f'<p data-en>{f["syn_en"]}</p><p data-zh>{f["syn_zh"]}</p>' if f["syn_en"] else f'<p class="note">{bi("Synopsis coming soon.","劇情簡介近期更新。")}</p>'
    note = f'<p class="note">{bi(f["note_en"], f["note_zh"])}</p>' if f.get("note_en") else ""
    gal = ""
    if f["stills"]:
        imgs = "".join(f'<img src="../img/{s}" alt="" class="{"wide" if j==0 and len(f["stills"])%3==1 else ""}">' for j, s in enumerate(f["stills"]))
        gal = f'<div class="wrap"><div class="gallery rv">{imgs}</div></div>'
    body = f'''
<header class="work-hero">{hero}<div class="wrap txt">
  <p class="crumb"><a href="../index.html">Home</a><span>/</span><a href="index.html">Films</a>{("<span>/</span>"+str(f["year"])) if f["year"] else ""}</p>
  <h1>{f["title"]}</h1>
</div></header>
<div class="wrap work-body">
  <aside>{poster}<div class="facts">{facts}</div></aside>
  <div class="syn">
    <h2>{bi("Synopsis","劇情簡介")}</h2>
    {syn}{note}
    <div class="laurels">{laur}</div>
    <a class="back" href="index.html">← {bi("All films","回到所有電影")}</a>
  </div>
</div>
{gal}
<nav class="pn">
  <a href="{prev["slug"]}.html"><p class="eyebrow">← {bi("Previous","上一部")}</p><b>{prev["title"]}</b></a>
  <a class="next" href="{nxt["slug"]}.html"><p class="eyebrow">{bi("Next","下一部")} →</p><b>{nxt["title"]}</b></a>
</nav>'''
    write(f"films/{f['slug']}.html", shell(f'{f["title"]} — Chin-En Gau', body, root="../", active="films", desc=f["syn_en"], ogimg=("img/"+f["hero"]) if f["hero"] else ""))

# ---------------- ABOUT + CONTACT ----------------
about = f'''
<div class="wrap">
  <header class="phead">
    <p class="crumb"><a href="index.html">Home</a><span>/</span>About</p>
    <h1>{bi("Taiwanese-born,<br>New York based.","生於台灣，<br>現居紐約。")}</h1>
  </header>
  <section class="about">
    <div class="photo"><img src="img/picture-of-me.jpg" alt="Chin-En Gau"></div>
    <div>
      <p data-en>Chin-En Gau is a filmmaker with an MFA in Directing from Stony Brook University and ten years of production experience across commercial and independent work. As in-house producer at DramaBox he produced ten vertical short-drama series — several reaching No.1 in new releases with more than a million daily views — including three made with a fully AI-generated pipeline.</p>
      <p data-en>His cinematography and editing credits include work supported by the Sundance Institute Documentary Fund and fiscally sponsored by The Gotham, with screenings at Film at Lincoln Center, Tribeca (Work-in-Progress) and the Fargo Film Festival. He has taught filmmaking at Stony Brook University and Taiwan Public Television, and his own films focus on cultural difference and self-identity.</p>
      <p data-zh>Chin-En Gau 畢業於石溪大學電影導演藝術碩士，擁有十年橫跨商業與獨立製作的經驗。任職 DramaBox 內部製片期間製作十部豎屏短劇，多部登上新片榜第一、單日觀看破百萬，其中三部以全 AI 流程完成。</p>
      <p data-zh>攝影與剪接作品曾獲日舞影展紀錄片基金支持與 The Gotham 財務贊助，並於林肯中心電影協會、翠貝卡影展（WIP）與法戈影展放映。曾於石溪大學與台灣公共電視教授電影製作；個人創作聚焦於文化差異與自我認同。</p>
      <div class="cred">
        <div><b>{bi("Education","學歷")}</b><ul>
          <li>{bi("MFA, Film Directing — Stony Brook University","電影導演藝術碩士 — 石溪大學")}</li>
          <li>{bi("BFA, Film Technology (Editing) — Taipei National University of the Arts","電影創作學系學士（剪接）— 國立臺北藝術大學")}</li>
        </ul></div>
        <div><b>{bi("Selected recognition","獲獎與支持")}</b><ul>
          <li>Jacob Burns Film Center Artist-in-Residence 2026</li>
          <li>Jury Award — MAX3MIN Very Short Film Festival 2025</li>
          <li>FilmNorth Inclusive & Socially Conscious Filmmaking Lab 2025</li>
          <li>Sundance Institute Documentary Fund (as cinematographer)</li>
        </ul></div>
        <div><b>{bi("Teaching","教學")}</b><ul>
          <li>{bi("Instructor, Stony Brook University Film Minor (FLM 101 / 102), 2023–2025","石溪大學電影輔系講師（FLM 101 / 102），2023–2025")}</li>
          <li>{bi("Instructor, Documentary Summer Camp — Taiwan Public Television Service","台灣公共電視紀錄片夏令營講師")}</li>
        </ul></div>
        <div><b>{bi("Tools","工具")}</b><ul>
          <li>Adobe Premiere Pro · DaVinci Resolve</li>
          <li>{bi("AI pipeline: image & video prompting, Seedance 2.0","AI 流程：圖像／影片提示設計、Seedance 2.0")}</li>
        </ul></div>
      </div>
    </div>
  </section>
</div>
<section class="contact" id="contact">
  <div class="wrap">
    <p class="eyebrow">{bi("Contact","聯絡")}</p>
    <h2 class="mail"><a href="mailto:{SITE["email"]}">{SITE["email"]}</a></h2>
    <div class="links">
      <a href="{SITE["imdb"]}" target="_blank" rel="noopener">IMDb</a>
      <a href="{SITE["linkedin"]}" target="_blank" rel="noopener">LinkedIn</a>
      <a href="{SITE["instagram"]}" target="_blank" rel="noopener">Instagram</a>
      <a href="#" data-reel>Reel</a>
      <a href="{SITE["resume"]}" target="_blank">{bi("Resume (PDF)","履歷（PDF）")}</a>
    </div>
  </div>
</section>'''
write("about.html", shell("About — Chin-En Gau", about, active="about"))

# ---------------- PRESS ----------------
items = ""
for a in sorted(PRESS, key=lambda a: a["date"] or "0000", reverse=True):
    q = f'<blockquote>{bi(a["quote_en"] or a["quote_zh"], a["quote_zh"] or a["quote_en"])}</blockquote>' if (a["quote_en"] or a["quote_zh"]) else ""
    date = a["date"] if a["date"] else ""
    items += f'''
  <a class="press rv" href="{a["url"]}" target="_blank" rel="noopener">
    <div class="pmeta"><span class="outlet">{a["outlet"]}</span><span class="date">{date}</span></div>
    <div>
      <h3>{bi(a["title_en"], a["title_zh"])}</h3>
      <p>{bi(a["blurb_en"], a["blurb_zh"])}</p>
      {q}
      <span class="go">{bi("Read","閱讀")} ↗</span>
    </div>
  </a>'''
press = f'''
<div class="wrap">
  <header class="phead">
    <p class="crumb"><a href="index.html">Home</a><span>/</span>Press</p>
    <h1>{bi("Press &amp; Interviews","報導與專訪")}</h1>
    <p class="lead">{bi("Features, interviews and podcasts.","媒體報導、專訪與 Podcast。")}</p>
  </header>
  <div class="plist">{items}
  </div>
</div>'''
write("press.html", shell("Press — Chin-En Gau", press, active="press"))

print("done")
