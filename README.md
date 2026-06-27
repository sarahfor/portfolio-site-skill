# Portfolio Site Skill

A reusable skill for building a polished one-page personal website from a beginner-friendly form.

## What it includes

- Codex version: `portfolio-site/`
- Claude version: `claude-portfolio-site/`
- Intake form: `Build a Personal Website`
- Static HTML site generator
- Upload-style fields for resume and images
- A reusable portfolio template with profile, links, work cards, gallery, and contact sections

## Install for Codex

Copy the Codex skill folder:

```bash
cp -R portfolio-site ~/.codex/skills/
```

Then restart Codex.

Run the form:

```bash
~/.codex/skills/portfolio-site/scripts/open_intake_form.sh
```

Fill out the form, copy the generated link, and paste it into Codex.

## Install for Claude

Copy the Claude skill folder:

```bash
mkdir -p ~/.claude/skills
cp -R claude-portfolio-site ~/.claude/skills/
```

Then restart Claude.

Run the form:

```bash
~/.claude/skills/claude-portfolio-site/scripts/open_intake_form.sh
```

Fill out the form, copy the generated link, and paste it into Claude.
