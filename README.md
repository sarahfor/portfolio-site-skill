# Portfolio Site Skill

A reusable skill for building a polished one-page personal website from a beginner-friendly form.

## What it includes

- Codex version: `portfolio-site/`
- Claude version: `claude-portfolio-site/`
- Public static form source: `docs/index.html`
- Intake form: `Build a Personal Website`
- Static HTML site generator
- Upload-style fields for resume and images
- Browser-only package download with `answers.json`, selected files, and instructions
- A reusable portfolio template with profile, links, work cards, gallery, and contact sections
- Cross-platform form opener for macOS, Linux, and Windows-style shells

## Public form

The form can be published with GitHub Pages from the `docs/` folder. Once Pages is enabled, people can use the form without a GitHub account.

The form runs in the browser. It can download a zip package with:

- `answers.json`
- selected resume/images in `assets/`
- `README.txt` with next steps

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

Fill out the form, copy the generated link, and paste it into Codex. You can also download a package with your answers and selected files. If your computer does not open the browser automatically, the script will print the form file path so you can open it manually.

Once the site is generated, you will still need to chat with your LLM to customize it. Have fun!

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

Fill out the form, copy the generated link, and paste it into Claude. You can also download a package with your answers and selected files. If your computer does not open the browser automatically, the script will print the form file path so you can open it manually.

Once the site is generated, you will still need to chat with your LLM to customize it. Have fun!
