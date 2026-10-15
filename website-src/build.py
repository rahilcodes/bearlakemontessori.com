"""Build the Bear Lake Montessori Academy static site.

Each file in pages/ starts with a JSON front-matter block between <!--meta and -->,
followed by the page body. This script wraps the body in the shared head, header,
pre-footer CTA and footer, expands a few design-system macros, and writes the
finished HTML into ../website/.

    python build.py
"""
import json
import pathlib
import re
import hashlib

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "website"
SITE = "https://bearlakemontessori.com"

PHONE = "(407) 786-2255"
TEL = "tel:+14077862255"
EMAIL = "bearlakemontessori@gmail.com"
INSTAGRAM = "https://www.instagram.com/bearlakemontessori/"

NAV = [
    ("About", [
        ("about.html", "About us", "Our story and our new home"),
        ("team.html", "Our team", "The people who guide"),
        ("testimonials.html", "Testimonials", "Words from our families"),
    ]),
    ("Learning", [
        ("approach.html", "Our approach", "The Montessori method"),
        ("programs.html", "Programs", "Ages 1 to 6, VPK and care"),
        ("curriculum.html", "Curriculum", "The five areas of learning"),
    ]),
    ("School life", [
        ("school-life.html", "A day at Bear Lake", "Rhythm, spaces and play"),
        ("gallery.html", "Gallery", "Photographed on site"),
    ]),
    ("Admissions", [
        ("admissions.html", "Admissions", "How to enroll"),
        ("faq.html", "FAQs", "Answers for parents"),
    ]),
    ("Contact", "contact.html"),
]

CARET = '<svg class="caret" viewBox="0 0 10 10" aria-hidden="true"><path d="M1.5 3.5 5 7l3.5-3.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def header(page, cta_href):
    items = []
    for i, (label, target) in enumerate(NAV):
        if isinstance(target, str):
            cur = ' aria-current="page"' if target == page else ""
            active = " is-active" if target == page else ""
            items.append(f'<div class="nav-item{active}"><a class="nav-link" href="{target}"{cur}>{label}</a></div>')
            continue
        active = " is-active" if any(t[0] == page for t in target) else ""
        links = "".join(
            f'<a href="{href}"{" aria-current=\"page\"" if href == page else ""}>{name}<small>{desc}</small></a>'
            for href, name, desc in target
        )
        items.append(
            f'<div class="nav-item{active}" data-dropdown><button class="nav-link" type="button" aria-expanded="false" aria-controls="dd-{i}">{label}{CARET}</button>'
            f'<div class="dropdown" id="dd-{i}">{links}</div></div>'
        )
    groups = []
    for label, target in NAV:
        if isinstance(target, str):
            continue
        links = "".join(
            f'<a href="{href}"{" aria-current=\"page\"" if href == page else ""}>{name}</a>' for href, name, _ in target
        )
        groups.append(f'<div class="mgroup"><p>{label}</p>{links}</div>')
    home_cur = ' aria-current="page"' if page == "index.html" else ""
    contact_cur = ' aria-current="page"' if page == "contact.html" else ""
    groups.insert(0, f'<div class="mgroup"><p>Start here</p><a href="index.html"{home_cur}>Home</a><a href="contact.html"{contact_cur}>Contact us</a></div>')
    return f"""<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="hdr">
    <a class="brand" href="index.html" aria-label="Bear Lake Montessori Academy, home">
      <img src="img/logo.webp" alt="" width="46" height="46">
      <span>Bear Lake Montessori</span>
    </a>
    <nav class="nav" aria-label="Main">
      {''.join(items)}
      <a class="nav-cta" href="{cta_href}">Book a tour</a>
    </nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav">Menu</button>
  </div>
  <nav class="mobile-nav" id="mobile-nav" aria-label="Main" hidden>
    <div class="mgroups">{''.join(groups)}</div>
    <div class="m-cta">
      <a class="btn btn--primary btn--sm" href="{cta_href}">Book a tour</a>
      <a class="btn btn--sm btn--light" href="{TEL}">Call {PHONE}</a>
    </div>
  </nav>
</header>"""


def footer():
    return f"""<footer class="site-footer" data-hide-mbar>
  <div class="footer-scallop" aria-hidden="true"></div>
  <div class="footer-sun" aria-hidden="true"></div>
  <div class="footer-horizon" aria-hidden="true"></div>
  <div class="footer-in">
    <a class="footer-logo" href="index.html" aria-label="Back to the homepage"><img src="img/logo.webp" alt="" width="104" height="104"></a>
    <p class="footer-name">Bear Lake Montessori Academy</p>
    <p class="footer-tagline">Respect · Freedom · Independence</p>
    <div class="footer-cols">
      <div>
        <h2>Visit</h2>
        <address>843 N SR 434<br>Altamonte Springs, FL 32714</address>
        <p style="margin-top:8px"><a href="contact.html#map">Get directions</a></p>
      </div>
      <div>
        <h2>Talk to us</h2>
        <ul>
          <li><a href="{TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}" style="overflow-wrap:anywhere">{EMAIL}</a></li>
          <li><a href="{INSTAGRAM}" rel="noopener" target="_blank">Instagram @bearlakemontessori</a></li>
        </ul>
      </div>
      <div>
        <h2>School hours</h2>
        <p>Monday to Friday<br>7:15am to 6:00pm<br>Closed weekends</p>
      </div>
      <div class="fc-explore">
        <h2>Explore</h2>
        <ul>
          <li><a href="approach.html">Our approach</a></li>
          <li><a href="programs.html">Programs</a></li>
          <li><a href="admissions.html">Admissions</a></li>
          <li><a href="faq.html">FAQs</a></li>
        </ul>
      </div>
    </div>
    <nav class="footer-pills" aria-label="Footer">
      <a href="about.html">About us</a>
      <a class="fp-extra" href="approach.html">Our approach</a>
      <a class="fp-extra" href="programs.html">Programs</a>
      <a href="curriculum.html">Curriculum</a>
      <a href="school-life.html">School life</a>
      <a href="gallery.html">Gallery</a>
      <a href="team.html">Our team</a>
      <a href="testimonials.html">Testimonials</a>
      <a class="fp-extra" href="admissions.html">Admissions</a>
      <a class="fp-extra" href="faq.html">FAQs</a>
      <a href="contact.html">Contact</a>
    </nav>
    <p class="footer-legal">Florida DCF Lic. C18SE0374 · © <span data-year>2026</span> Bear Lake Montessori Academy</p>
    <p class="footer-credit"><span class="fc-star" aria-hidden="true"></span><span>Designed &amp; developed by</span><a href="https://creativals.com" target="_blank" rel="noopener">creativals.com<svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true"><path d="M2 8 8 2M3.5 2H8v4.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></a></p>
  </div>
</footer>"""


def cta_block(title, text, page):
    if not title:
        return ""
    return f"""<section class="section" aria-label="Book a tour">
  <div class="cta-card" data-reveal>
    <div>
      <p class="tag bg-white">Visit us</p>
      <h2 class="h2">{title}</h2>
    </div>
    <div class="cta-side">
      <p>{text}</p>
      <div class="btn-row">
        <a class="btn btn--primary" href="contact.html#tour">Book a tour</a>
        <a class="btn btn--light" href="{TEL}">Call {PHONE}</a>
      </div>
    </div>
  </div>
</section>"""


# ---------- Macros ----------
WAVE_PATH = "M0 24 C90 0 270 0 360 24 C450 48 630 48 720 24 C810 0 990 0 1080 24 C1170 48 1350 48 1440 24"


def wave(m):
    pos, fill = m.group(1), m.group(2)
    bg = m.group(3)
    style = f' style="background:{bg}"' if bg else ""
    return (f'<svg class="wave wave--{pos}" aria-hidden="true" viewBox="0 0 1440 48" preserveAspectRatio="none"{style}>'
            f'<path d="{WAVE_PATH} V48 H0 Z" fill="{fill}"></path>'
            f'<path d="{WAVE_PATH}" fill="none" stroke="#3a2a1f" stroke-width="2" vector-effect="non-scaling-stroke"></path></svg>')


def deco(m):
    kind, color, pos, drift = [x.strip() for x in m.group(1).split("|")]
    d = f' data-drift="{drift}"' if drift else ""
    if kind == "star":
        inner = f'<span class="star" style="--c:{color};--r:8deg"></span>'
    elif kind == "dot":
        inner = f'<span class="dot" style="--c:{color}"></span>'
    elif kind == "squiggle":
        inner = (f'<svg class="squiggle" width="64" height="22" viewBox="0 0 64 22" style="--r:-6deg"><path d="M2 12 C 10 2, 16 2, 22 12 S 34 22, 40 12 S 52 2, 62 12" '
                 f'fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round"></path></svg>')
    elif kind == "ring":
        inner = (f'<svg class="ring" width="56" height="56" viewBox="0 0 56 56"><circle cx="28" cy="28" r="22" fill="none" stroke="{color}" '
                 f'stroke-width="4" stroke-dasharray="6 10" stroke-linecap="round"></circle></svg>')
    else:
        raise ValueError(kind)
    return f'<span class="deco" aria-hidden="true"{d} style="{pos}">{inner}</span>'


def underline(m, draw=False):
    cls = "u u--draw" if draw else "u"
    path = '<path d="M3 10 C 40 2, 70 15, 110 8 S 170 4, 197 9" pathLength="1"></path>' if draw else '<path d="M3 10 C 40 2, 70 15, 110 8 S 170 4, 197 9"></path>'
    return f'<span class="{cls}">{m.group(1)}<svg aria-hidden="true" viewBox="0 0 200 16" preserveAspectRatio="none">{path}</svg></span>'


def tail():
    return ('<svg class="tail" aria-hidden="true" width="46" height="32" viewBox="0 0 46 32"><path d="M4 0 C 10 12, 12 22, 6 31 C 20 26, 30 14, 36 0" '
            'fill="#fff" stroke="#3a2a1f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path><path d="M3 0 H37" stroke="#fff" stroke-width="4"></path></svg>')


def expand(html):
    html = re.sub(r"\{\{wave:(top|bottom):([^:}]+)(?::([^}]+))?\}\}", wave, html)
    html = re.sub(r"\{\{deco:([^}]+)\}\}", deco, html)
    html = re.sub(r"\{\{ud:([^}]+)\}\}", lambda m: underline(m, True), html)
    html = re.sub(r"\{\{u:([^}]+)\}\}", underline, html)
    html = html.replace("{{tail}}", tail())
    html = html.replace("{{PHONE}}", PHONE).replace("{{TEL}}", TEL).replace("{{EMAIL}}", EMAIL).replace("{{INSTAGRAM}}", INSTAGRAM)
    return html


def asset_version():
    h = hashlib.md5()
    for name in ("site.css", "site.js"):
        h.update((OUT / "assets" / name).read_bytes())
    return h.hexdigest()[:8]


def head(meta, page):
    url = SITE + "/" + ("" if page == "index.html" else page)
    title = meta["title"]
    desc = meta["description"]
    image = SITE + "/img/" + meta.get("image", "building-front.jpg")
    extra = meta.get("head", "")
    VER = asset_version()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Bear Lake Montessori Academy">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#fff8ea">
<link rel="icon" href="img/logo.webp" type="image/webp">
<link rel="apple-touch-icon" href="img/logo.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css?v={VER}">
{extra}
</head>"""


def build():
    pages = sorted((ROOT / "pages").glob("*.html"))
    sitemap = []
    for p in pages:
        raw = p.read_text(encoding="utf-8")
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
        if not m:
            raise SystemExit(f"{p.name}: missing meta block")
        meta = json.loads(m.group(1))
        body = raw[m.end():]
        page = p.name
        cta_href = meta.get("cta_href", "contact.html#tour")
        cta = cta_block(meta.get("cta_title"), meta.get("cta_text", ""), page)
        VER = asset_version()
        mbar = ("" if page == "404.html" else
                f'\n<div class="m-bar" aria-label="Quick actions"><a class="btn btn--light" href="{TEL}">Call us</a>'
                f'<a class="btn btn--primary" href="{cta_href}">Book a tour</a></div>')
        html = (head(meta, page) + "\n<body>\n" + header(page, cta_href) +
                f'\n<main id="main">\n{body.strip()}\n{cta}\n</main>\n' + footer() + mbar +
                f'\n<script src="assets/site.js?v={VER}" defer></script>\n</body>\n</html>\n')
        html = expand(html)
        leftover = re.findall(r"\{\{[^}]*\}\}", html)
        if leftover:
            raise SystemExit(f"{page}: unexpanded macros {leftover[:5]}")
        (OUT / page).write_text(html, encoding="utf-8")
        if page != "404.html":
            sitemap.append(SITE + "/" + ("" if page == "index.html" else page))
        print("built", page)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{u}</loc></url>\n" for u in sitemap) + "</urlset>\n"
    (OUT / "sitemap.xml").write_text(xml, encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    build()
