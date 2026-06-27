# Intake Guide

Use this reference when turning a short interview into a polished personal website.

## Beginner form flow

Default to this flow for nontechnical users:

1. Have the user open `assets/intake-form/index.html`.
2. The user fills out the form-based intake.
3. The user selects resume and portrait/gallery files in upload boxes. Browser security means the form can capture filenames but cannot move the files.
4. The form generates a `claude-portfolio-site://build?answers=...` intake link.
5. The user copies the link and pastes it into Claude.
6. Decode the link with `scripts/build_site.py --intake-link`.
7. After the site is generated, have the user copy the selected files into the generated `assets` folder. The builder creates `assets/ADD-YOUR-FILES-HERE.txt` listing exact filenames.

The form also offers a JSON download backup for cases where the copied link is too long or gets mangled.

## Minimum questions

Ask these first, and infer the rest when the user gives enough material.

1. What is your name and one-line role?
2. What do you do, and who do you want the site to attract?
3. What should people do next: email, book a call, download a resume, follow, hire, subscribe, or view work?
4. Which links should appear? LinkedIn, Instagram, website, GitHub, newsletter/Substack, press, booking, or portfolio links.
5. Which clients, partners, employers, communities, or credibility signals should appear in the ticker?
6. What 3-6 work samples, press mentions, programs, talks, articles, or projects should be featured?
7. Which images should be used? Include a portrait/headshot, hero/background if available, and gallery images or screenshots.
8. What contact email should the site use?
9. What personal, industry, or field-level insight should power the signature section?

## Answer JSON shape

`scripts/build_site.py` accepts this shape. Omit unknown fields.

```json
{
  "name": "Jordan Lee",
  "role": "AI workflow designer and educator",
  "audience": "founders, operators, and teams adopting AI",
  "tagline": "I help teams turn AI curiosity into practical workflow changes.",
  "about": "Short paragraph in first person or third person.",
  "hero_lead_in": "It's a",
  "hero_emphasis": "builder's world",
  "contact_email": "hello@example.com",
  "profile_image": "/absolute/path/headshot.jpg",
  "links": {
    "linkedin": "https://linkedin.com/in/example",
    "instagram": "https://instagram.com/example",
    "resume": "assets/resume.pdf",
    "website": "https://example.com",
    "github": "https://github.com/example",
    "newsletter": "https://example.substack.com",
    "booking": "https://cal.com/example"
  },
  "partners": ["Client 1", "Project 2", "Community 3", "Publication 4"],
  "partner_categories": ["strategy", "education", "creative work", "community programs"],
  "cta": {
    "label": "Work with me",
    "prompts": [
      "Bring me in for a practical AI workshop.",
      "Turn a messy process into a clearer workflow.",
      "Build a public-facing program or resource."
    ],
    "primary": "Start a conversation",
    "supporting_line": "Share the work you are trying to move."
  },
  "work_items": [
    {
      "title": "Flagship program or press title",
      "source": "Organization or publication",
      "type": "Program build",
      "summary": "One concise sentence about the work.",
      "url": "https://example.com",
      "cta": "Explore work",
      "image": "/absolute/path/image.png",
      "image_alt": "Short alt text"
    }
  ],
  "gallery_title": "In the room",
  "gallery_images": [
    {
      "path": "/absolute/path/photo.jpg",
      "alt": "Person facilitating a workshop"
    }
  ],
  "future_report": {
    "title": "Add Your Signature Insight",
    "subtitle": "Use this section to make your point visually.",
    "lead": "One sentence explaining the trend, belief, result, or opportunity you want visitors to remember.",
    "eyebrow": "Your signal",
    "headline": "Make your point,<br><span>with a clear signal.</span>",
    "summary": "Short explanation of why this matters.",
    "metrics": [
      {"label": "Add metric 1", "detail": "What this number shows", "value": "Value"},
      {"label": "Add metric 2", "detail": "What this comparison means", "value": "Value"},
      {"label": "Add metric 3", "detail": "What changed or improved", "value": "Value"}
    ]
  }
}
```

## Copy style

- Use specific, concrete positioning over generic claims.
- Make the hero short and memorable. Keep the longer explanation in the about section.
- Use proof items as credibility, not a full resume.
- Use partner/client names only when the user gave them or they are already public on the user's materials.
- Prefer direct CTA language: "Start a conversation", "Book a workshop", "View resume", "Invite me to speak".
- Keep the site first-person if the user sounds like an independent creator or consultant; use third-person if it is an event bio, speaker page, or agency-style site.
