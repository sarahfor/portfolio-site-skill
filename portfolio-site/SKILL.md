---
name: portfolio-site
description: Build a one-page portfolio or professional personal website from a beginner-friendly form intake named Build a Personal Website. Use when someone downloads the skill, wants a polished form-based questionnaire, fills in what they do, audience, links such as Instagram, LinkedIn, press/work samples, partners/clients, email, uploads resume and image filenames through upload boxes, then copies a generated intake link into Codex. Produces a scaffolded HTML/CSS/JS site with cinematic hero, profile card, social links, partner ticker, work/features cards, tappable gallery, contact CTA, and instructions for adding selected files to the generated assets folder.
---

# Portfolio Site

Use this skill to build a polished one-page personal site with the user's own positioning, links, work samples, and images.

## What this skill provides

- A reusable single-page template in `assets/site-template/`
- Placeholder image assets in `assets/site-template/assets/`
- A beginner-friendly intake form in `assets/intake-form/index.html`
- A scaffold script in `scripts/scaffold_template.sh`
- An intake-driven generator in `scripts/build_site.py`
- Intake guidance in `references/intake.md`
- A browser-only package download that bundles `answers.json`, selected resume/images, and instructions
- A reusable signature-site pattern:
  cinematic hero, scroll cue, AI-inspector profile card, partner ticker, selected work/news cards, generic signature insight panel, moving field-image gallery with lightbox, and contact section

## Default workflow

1. For beginners, send them to the packaged intake form first:

```bash
${CODEX_HOME:-$HOME/.codex}/skills/portfolio-site/scripts/open_intake_form.sh
```

Tell them to fill out the form, use the upload boxes for resume and portrait/gallery images, click `Generate my Codex link`, copy the generated `portfolio-site://build?...` link, and paste it into Codex. They can also click `Download package` to save a zip with `answers.json`, selected files under `assets/`, and a short README. The form does not publish or upload files; after the site is generated, tell the user to copy selected files into the generated site's `assets` folder. The builder writes `assets/ADD-YOUR-FILES-HERE.txt` with the exact filenames.

2. When the user pastes a generated intake link, build from it:

```bash
python3 ${CODEX_HOME:-$HOME/.codex}/skills/portfolio-site/scripts/build_site.py \
  --intake-link 'portfolio-site://build?answers=...' \
  --output /absolute/path/to/new-site
```

3. Use JSON only as a fallback when the user downloads the form's JSON backup or gives answers directly:

```bash
python3 ${CODEX_HOME:-$HOME/.codex}/skills/portfolio-site/scripts/build_site.py \
  --answers /absolute/path/to/answers.json \
  --output /absolute/path/to/new-site
```

For a terminal interview:

```bash
python3 ${CODEX_HOME:-$HOME/.codex}/skills/portfolio-site/scripts/build_site.py \
  --interactive \
  --output /absolute/path/to/new-site
```

4. Use the plain scaffold only when the user explicitly wants a blank template:

```bash
${CODEX_HOME:-$HOME/.codex}/skills/portfolio-site/scripts/scaffold_template.sh /absolute/path/to/new-site
```

5. Open the scaffolded `index.html` and polish any generated copy. If using the plain scaffold, replace bracketed placeholders such as:

- `[SITE TITLE]`
- `[YOUR NAME]`
- `[YOUR TAGLINE]`
- `[YOUR ABOUT PARAGRAPH]`
- `[PARTNER CATEGORY 1]`
- `[PROMPT 1]`
- `[NEWS STORY 1 TITLE]`
- `[CONTACT EMAIL]`

6. Replace placeholder SVGs in `assets/` with the user's photos, screenshots, press images, or logo marks when available. Copy any uploaded resume/CV file into `assets/` using the filename listed in `ADD-YOUR-FILES-HERE.txt`.

7. Verify the output before final delivery:

```bash
rg "\\[[A-Z0-9 _.-]+\\]" /absolute/path/to/new-site/index.html
```

If the site is static, opening `index.html` is enough. If testing browser behavior, use a local server and check desktop and mobile widths.

## Intake-driven content rules

- Ask for the user's name, what they do, who the site should attract, preferred CTA, contact email, public links, and image set.
- Treat LinkedIn, Instagram, resume/CV upload, website, GitHub, Substack/newsletter, press, and booking links as optional social links. Do not show empty links.
- Use 3-6 proof items for the work/features cards: press, client projects, talks, programs, articles, case studies, or flagship portfolio items.
- Use 4-8 image assets for the gallery when available. Include a portrait/headshot first if the user provides one. For form-uploaded images, preserve the generated `assets/<filename>` references and remind the user to add the image files to the generated `assets` folder.
- Do not reuse source-site-specific copy, photos, client names, emails, links, or personal names.
- Keep the generic signature structure: cinematic hero, scroll cue, AI-inspector profile card, social link row, partner/client ticker, selected work cards, signature insight panel, field-image carousel, and contact card.

## Template rules

- Preserve the one-page structure unless the user asks for multiple pages.
- Keep the hero, partner ticker, profile-inspector modal, gallery lightbox, signature insight panel, and contact interactions unless the user asks to remove them.
- Replace placeholder logos and photos with the user's assets.
- If the user wants the exact look with different content, edit the scaffolded template rather than rebuilding from scratch.
- Keep class names and section structure unless redesigning deliberately. The CSS and JS behaviors assume those hooks exist.

## Files to use

- Main template: `assets/site-template/index.html`
- Placeholder media: `assets/site-template/assets/`
- Scaffold helper: `scripts/scaffold_template.sh`
- Form opener: `scripts/open_intake_form.sh`
- Intake generator: `scripts/build_site.py`
- Beginner intake form: `assets/intake-form/index.html`
- Intake guide and answer schema: `references/intake.md`
