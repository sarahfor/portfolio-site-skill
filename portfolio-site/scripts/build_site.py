#!/usr/bin/env python3
import argparse
import base64
import html
import json
import re
import shutil
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "assets" / "site-template"


DEFAULTS = {
    "name": "Your Name",
    "role": "creative technologist",
    "audience": "teams, communities, and collaborators",
    "tagline": "I build clear, useful work for the people I want to reach.",
    "about": "Use this space to explain who you are, what kind of work you do, and what you want people to understand after spending one minute on the site.",
    "hero_lead_in": "Build your",
    "hero_emphasis": "personal website",
    "hero_trailing": "",
    "contact_email": "hello@example.com",
    "partners": ["Partner 1", "Partner 2", "Partner 3", "Partner 4", "Partner 5", "Partner 6"],
    "partner_categories": ["strategy", "education", "creative work", "community programs"],
    "gallery_title": "Selected moments",
    "partners_kicker": "Clients, partners, and projects include:",
    "future_report": {
        "title": "Add Your Signature Insight",
        "subtitle": "Use this section to make your point visually.",
        "lead": "Replace this with the trend, belief, result, or opportunity you want visitors to remember.",
        "eyebrow": "Your signal",
        "headline": "Make your point,<br><span>with a clear signal.</span>",
        "summary": "Add the context, audience, change, or outcome that explains why this matters.",
        "metrics": [
            {"label": "Add metric 1", "detail": "What this number shows", "value": "Value"},
            {"label": "Add metric 2", "detail": "What this comparison means", "value": "Value"},
            {"label": "Add metric 3", "detail": "What changed or improved", "value": "Value"},
        ],
    },
}


DEFAULT_WORK = [
    {
        "title": "Featured project",
        "source": "Organization",
        "type": "Project",
        "summary": "A concise sentence explaining the work and why it matters.",
        "url": "#",
        "cta": "View project",
        "image_alt": "Project preview",
    },
    {
        "title": "Press or publication",
        "source": "Publication",
        "type": "Feature",
        "summary": "A concise sentence explaining the feature, article, talk, or public proof point.",
        "url": "#",
        "cta": "Read more",
        "image_alt": "Feature preview",
    },
    {
        "title": "Program or talk",
        "source": "Community",
        "type": "Program",
        "summary": "A concise sentence explaining the audience, outcome, or collaboration.",
        "url": "#",
        "cta": "Explore work",
        "image_alt": "Program preview",
    },
]


SOCIAL_LABELS = {
    "linkedin": "LinkedIn",
    "instagram": "Instagram",
    "resume": "Resume",
    "github": "GitHub",
    "newsletter": "Notes",
    "substack": "Substack",
    "website": "Website",
    "booking": "Book",
    "youtube": "YouTube",
    "tiktok": "TikTok",
    "x": "X",
}


def esc(value):
    return html.escape(str(value or ""), quote=True)


def read_answers(path):
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_intake_link(link):
    if not link:
        return {}
    match = re.search(r"(?:answers|data)=([^&\s]+)", link)
    if not match:
        raise ValueError("No answers payload found in intake link.")
    payload = match.group(1)
    padding = "=" * (-len(payload) % 4)
    decoded = base64.urlsafe_b64decode((payload + padding).encode("ascii"))
    return json.loads(decoded.decode("utf-8"))


def ask(prompt, default=""):
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value or default


def interactive_answers():
    partners = ask("Clients, partners, employers, or credibility signals (comma-separated)", "")
    links = {}
    for key in ["linkedin", "instagram", "resume", "website", "github", "newsletter", "booking"]:
        value = ask(f"{SOCIAL_LABELS[key]} URL or file path", "")
        if value:
            links[key] = value
    return {
        "name": ask("Name", DEFAULTS["name"]),
        "role": ask("What do you do in one line", DEFAULTS["role"]),
        "audience": ask("Who should the site attract", DEFAULTS["audience"]),
        "tagline": ask("Short tagline", DEFAULTS["tagline"]),
        "about": ask("About paragraph", DEFAULTS["about"]),
        "contact_email": ask("Contact email", DEFAULTS["contact_email"]),
        "profile_image": ask("Portrait/headshot path", ""),
        "partners": [p.strip() for p in partners.split(",") if p.strip()],
        "links": links,
    }


def asset_path(source, output_dir, fallback):
    if not source:
        return fallback
    if re.match(r"^(assets|image assets)/", str(source)):
        return str(source)
    source_path = Path(source).expanduser()
    if not source_path.exists():
        return source if re.match(r"^https?://", str(source)) else fallback
    asset_dir = output_dir / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    target = asset_dir / f"custom-{source_path.name}"
    counter = 2
    while target.exists():
        target = asset_dir / f"custom-{counter}-{source_path.name}"
        counter += 1
    shutil.copy2(source_path, target)
    return f"assets/{target.name}"


def external_href(value, output_dir):
    if not value:
        return ""
    if re.match(r"^(https?://|mailto:|#)", value):
        return value
    return asset_path(value, output_dir, value)


def replace_block(pattern, text, replacement):
    next_text, count = re.subn(pattern, replacement, text, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"Expected one match for pattern: {pattern}")
    return next_text


def render_social_links(links, output_dir):
    items = []
    for key, label in SOCIAL_LABELS.items():
        href = external_href(links.get(key, ""), output_dir)
        if href:
            items.append(f'<a href="{esc(href)}" target="_blank" rel="noopener noreferrer"><span class="social-label">{esc(label)}</span></a>')
    if not items:
        return '<div class="social-links"></div>'
    return '<div class="social-links">\n                        ' + "\n                        ".join(items) + "\n                    </div>"


def render_partners(partners):
    clean = [p for p in partners if p][:6] or DEFAULTS["partners"]
    clean = (clean + DEFAULTS["partners"])[:6]
    group = "\n                    ".join(f'<span class="partner-logo">{esc(p)}</span>' for p in clean)
    return (
        '<div class="partnerships-logos ticker-group">\n                    '
        + group
        + '\n                </div>\n                <div class="partnerships-logos ticker-group" aria-hidden="true">\n                    '
        + group
        + "\n                </div>"
    )


def render_news_cards(items, output_dir):
    cards = []
    merged = (items or [])[:4]
    merged = merged + DEFAULT_WORK[len(merged):]
    while len(merged) < 4:
        merged.append(DEFAULT_WORK[len(merged) % len(DEFAULT_WORK)])
    for item in merged[:4]:
        image = asset_path(item.get("image"), output_dir, "assets/landscape-placeholder.svg")
        url = item.get("url") or "#"
        cards.append(
            f'''<article class="news-card news-card-compact">
                <a class="news-card-media" href="{esc(url)}" target="_blank" rel="noopener noreferrer">
                    <img src="{esc(image)}" alt="{esc(item.get("image_alt") or item.get("title") or "Work preview")}" loading="lazy" decoding="async">
                </a>
                <div class="news-card-body">
                    <div>
                        <div class="news-meta">
                            <span class="news-badge">{esc(item.get("type", "Work"))}</span>
                            <span class="news-source">{esc(item.get("source", "Selected work"))}</span>
                        </div>
                        <h3><a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(item.get("title", "Featured work"))}</a></h3>
                        <p>{esc(item.get("summary", "A concise sentence explaining why this work matters."))}</p>
                    </div>
                    <a class="news-link" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(item.get("cta", "View work"))}</a>
                </div>
            </article>'''
        )
    return "\n            ".join(cards)


def render_gallery(images, output_dir):
    entries = images or []
    placeholders = [
        ("assets/landscape-placeholder.svg", "Gallery image 1"),
        ("assets/square-placeholder.svg", "Gallery image 2"),
        ("assets/landscape-placeholder.svg", "Gallery image 3"),
        ("assets/square-placeholder.svg", "Gallery image 4"),
        ("assets/landscape-placeholder.svg", "Gallery image 5"),
        ("assets/square-placeholder.svg", "Gallery image 6"),
    ]
    tiles = []
    for index in range(max(6, len(entries))):
        item = entries[index] if index < len(entries) else {}
        if isinstance(item, str):
            item = {"path": item}
        fallback_src, fallback_alt = placeholders[index % len(placeholders)]
        src = asset_path(item.get("path"), output_dir, fallback_src)
        alt = item.get("alt") or fallback_alt
        tiles.append(
            f'<div class="image-tile"><a href="{esc(src)}" class="image-lightbox-trigger" data-full-image="{esc(src)}" data-image-alt="{esc(alt)}"><img src="{esc(src)}" alt="{esc(alt)}"></a></div>'
        )
    group = "\n                        ".join(tiles)
    return (
        '<div class="ticker-group">\n                        '
        + group
        + '\n                    </div>\n                    <div class="ticker-group" aria-hidden="true">\n                        '
        + group
        + "\n                    </div>"
    )


def write_asset_instructions(data, output_dir):
    files = data.get("image_asset_files") or []
    if not files:
        return
    asset_dir = output_dir / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "Files to add",
        "",
        "Copy the selected files into this folder using these exact filenames:",
        "",
    ]
    for item in files:
        label = item.get("label", "File")
        file_name = item.get("fileName") or Path(item.get("path", "")).name
        if file_name:
            lines.append(f"- {label}: {file_name}")
    lines.extend([
        "",
        "The generated HTML already points at assets/<filename>.",
        "If an image does not appear, confirm the file is in this folder and the filename matches exactly.",
    ])
    (asset_dir / "ADD-YOUR-FILES-HERE.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_site(answers, output_dir):
    data = {**DEFAULTS, **answers}
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE_DIR, output_dir, dirs_exist_ok=True)
    index_path = output_dir / "index.html"
    text = index_path.read_text(encoding="utf-8")

    name = data.get("name", DEFAULTS["name"])
    first_name = name.split()[0] if name.split() else "Person"
    role = data.get("role", DEFAULTS["role"])
    audience = data.get("audience", DEFAULTS["audience"])
    cta = data.get("cta", {}) or {}
    code_demo = data.get("code_demo", {}) or {}
    categories = (data.get("partner_categories") or DEFAULTS["partner_categories"])[:4]
    categories = (categories + DEFAULTS["partner_categories"])[:4]
    contact_email = data.get("contact_email", DEFAULTS["contact_email"])
    profile_src = asset_path(data.get("profile_image"), output_dir, "assets/portrait-placeholder.svg")
    future = {**DEFAULTS["future_report"], **(data.get("future_report") or {})}
    metrics = future.get("metrics") or DEFAULTS["future_report"]["metrics"]
    metrics = (metrics + DEFAULTS["future_report"]["metrics"])[:3]

    prompts = cta.get("prompts") or []
    prompts = (prompts + [
        f"Bring {name.split()[0]} in for a practical session.",
        f"Turn {audience} needs into a clear plan.",
        "Build a useful public-facing resource.",
    ])[:3]

    replacements = {
        "[SITE TITLE]": f"{name} - Portfolio",
        "[HERO LEAD-IN]": data.get("hero_lead_in") or "It's a",
        "[HERO EMPHASIS]": data.get("hero_emphasis") or f"{role} world",
        "[HERO TRAILING]": data.get("hero_trailing", ""),
        "[YOUR NAME]": name,
        "[FIRST NAME]": first_name,
        "[YOUR TAGLINE]": data.get("tagline", DEFAULTS["tagline"]),
        "[YOUR ABOUT PARAGRAPH. Explain who you are, what kind of work you do, and what you want the site to make people curious about.]": data.get("about", DEFAULTS["about"]),
        "[YOUR ABOUT PARAGRAPH]": data.get("about", DEFAULTS["about"]),
        "[YOUR PARTNERS HEADLINE]": data.get("partners_headline") or "Work shaped with teams, partners, and communities",
        "[PARTNERS KICKER]": data.get("partners_kicker", DEFAULTS["partners_kicker"]),
        "[PARTNER CATEGORY 1]": categories[0],
        "[PARTNER CATEGORY 2]": categories[1],
        "[PARTNER CATEGORY 3]": categories[2],
        "[PARTNER CATEGORY 4]": categories[3],
        "[CTA LABEL]": cta.get("label", "Work with me"),
        "[PROMPT 1]": prompts[0],
        "[PROMPT 2]": prompts[1],
        "[PROMPT 3]": prompts[2],
        "[CONTACT EMAIL]": contact_email,
        "[PRIMARY CTA]": cta.get("primary", "Start a conversation"),
        "[CTA SUPPORTING LINE]": cta.get("supporting_line", "Share the work you are trying to move."),
        "[NEWS SECTION TITLE]": data.get("work_section_title", "Selected Work & Features"),
        "[GALLERY SECTION TITLE]": data.get("gallery_title", DEFAULTS["gallery_title"]),
        "[FUTURE SECTION TITLE]": future.get("title", ""),
        "[FUTURE SUBTITLE]": future.get("subtitle", ""),
        "[FUTURE LEAD]": future.get("lead", ""),
        "[FUTURE EYEBROW]": future.get("eyebrow", ""),
        "[FUTURE HEADLINE]": future.get("headline", ""),
        "[FUTURE SUMMARY]": future.get("summary", ""),
        "[METRIC 1 LABEL]": metrics[0].get("label", ""),
        "[METRIC 1 DETAIL]": metrics[0].get("detail", ""),
        "[METRIC 1 VALUE]": metrics[0].get("value", ""),
        "[METRIC 2 LABEL]": metrics[1].get("label", ""),
        "[METRIC 2 DETAIL]": metrics[1].get("detail", ""),
        "[METRIC 2 VALUE]": metrics[1].get("value", ""),
        "[METRIC 3 LABEL]": metrics[2].get("label", ""),
        "[METRIC 3 DETAIL]": metrics[2].get("detail", ""),
        "[METRIC 3 VALUE]": metrics[2].get("value", ""),
        "[PROFILE INSPECTOR CAPTION]": data.get("profile_inspector_caption", "Object detection software identifies objects in an image and estimates confidence scores for each match."),
        "[CODE SECTION LABEL]": code_demo.get("label", "Interactive lab"),
        "[CODE HEADLINE LINE 1]": code_demo.get("headline_line_1", "Try a small"),
        "[CODE HEADLINE LINE 2]": code_demo.get("headline_line_2", "working demo"),
        "[Explain what the code demo is for and what someone should try first.]": code_demo.get("lead", "Use this space for a small code demo, calculator, quiz, prompt, or interactive proof point connected to the person's work."),
        "[EDITOR HINT]": code_demo.get("hint", "Edit and run"),
        "[CONTACT LABEL]": data.get("contact_label", "Connect"),
        "[CONTACT HEADLINE]": data.get("contact_headline", f"Build something useful with {name.split()[0]}"),
        "[CONTACT DESCRIPTION]": data.get("contact_description", "For collaborations, workshops, speaking, or selected projects, reach out by email."),
        "[FOOTER NOTE]": data.get("footer_note", f"&copy; 2026 {name}. All rights reserved."),
    }
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, esc(value) if placeholder != "[FOOTER NOTE]" else str(value))

    text = text.replace('src="assets/portrait-placeholder.svg"', f'src="{esc(profile_src)}"')
    text = text.replace('srcset="assets/portrait-placeholder.svg 900w"', f'srcset="{esc(profile_src)} 900w"')
    text = replace_block(r'<div class="social-links"[^>]*>.*?</div>', text, render_social_links(data.get("links", {}) or {}, output_dir))
    text = replace_block(r'<div class="partnerships-logos ticker-group">.*?</div>\s*<div class="partnerships-logos ticker-group" aria-hidden="true">.*?</div>', text, render_partners(data.get("partners") or []))
    text = replace_block(r'(?s)<div class="news-grid">\s*(?:<article class="news-card.*?</article>\s*)+</div>', text, '<div class="news-grid">\n            ' + render_news_cards(data.get("work_items") or [], output_dir) + '\n        </div>')
    text = replace_block(r'(?s)<div class="future-image-track">\s*<div class="ticker-group">.*?</div>\s*<div class="ticker-group" aria-hidden="true">.*?</div>\s*</div>', text, '<div class="future-image-track">\n                    ' + render_gallery(data.get("gallery_images") or [], output_dir) + '\n                </div>')
    text = re.sub(r'\n\s*<section class="learning-library-section".*?</section>\s*', '\n\n', text, count=1, flags=re.DOTALL)

    if code_demo.get("starter_code"):
        text = text.replace('print("Hello, World!")', esc(code_demo["starter_code"]))

    leftover = sorted(set(re.findall(r"\[[A-Z0-9 _./-]+\]", text)))
    index_path.write_text(text, encoding="utf-8")
    write_asset_instructions(data, output_dir)
    return {"index": str(index_path), "leftover_placeholders": leftover}


def main():
    parser = argparse.ArgumentParser(description="Build a signature personal website from intake answers.")
    parser.add_argument("--answers", help="Path to JSON answers file")
    parser.add_argument("--intake-link", help="Generated portfolio-site:// intake link")
    parser.add_argument("--interactive", action="store_true", help="Prompt for a short intake")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()

    answers = read_answers(args.answers)
    if args.intake_link:
        answers = {**answers, **read_intake_link(args.intake_link)}
    if args.interactive:
        answers = {**answers, **interactive_answers()}
    result = build_site(answers, Path(args.output).expanduser().resolve())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
