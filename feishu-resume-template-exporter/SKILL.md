---
name: feishu-resume-template-exporter
description: Convert a structured Feishu resume document into a Word document and PDF that follow a supplied resume sample's layout. Use when the user wants Word/PDF output in the same visual format as a resume template, not a plain Feishu export.
---

# Feishu Resume Template Exporter

Use this skill to turn a student's completed Feishu resume document into a polished `.docx` and matching PDF based on the provided sample resume.

## What This Skill Does

The Feishu document is the editable source of truth. The bundled Word sample is the visual authority. Do not export the Feishu document directly: normalize its content into the JSON shape described in [input-schema.md](references/input-schema.md), then run the builder against the template.

Use this skill only for resumes that follow the sample's structure. It does not invent, embellish, or alter factual experience.

## Workflow

1. Read the student's Feishu document with `lark-cli docs +fetch --as user --doc <URL> --detail full --format json`.
2. Confirm it contains, at minimum: name/contact, personal summary, experience entries, education, and skills. If a section is intentionally absent, use an empty array instead of inventing content.
3. Map the document into the JSON schema. Preserve all facts, dates, and numbers exactly. Treat lines in the form `公司/项目｜角色　时间` as one experience header.
4. If the user has not supplied a headshot, create or use an explicitly labeled generic simulated avatar for a demo only. Do not present it as the student's real photo.
5. Run `scripts/build_resume.py` with the JSON, the bundled `assets/resume-template.docx`, and the avatar. The script emits a `.docx`.
6. Render the PDF with `scripts/build_resume_pdf.py` from the same JSON and avatar. This is the default path: it avoids font substitution and table reflow that can occur when a DOCX is converted by a different office suite. If Microsoft Word is installed, native Word export is an acceptable alternative after visual verification. Do not use LibreOffice as the primary PDF path.
7. Upload both final files to the requested Feishu folder or attach them to the source document when the user authorizes it.

## Invocation

```bash
python3 scripts/build_resume.py \
  --input /path/to/resume.json \
  --template assets/resume-template.docx \
  --avatar /path/to/avatar.png \
  --output /path/to/姓名-简历.docx
```

Create the delivery PDF with:

```bash
python3 scripts/build_resume_pdf.py \
  --input /path/to/resume.json \
  --avatar /path/to/avatar.png \
  --output /path/to/姓名-简历.pdf
```

## Output Rules

- Match the sample's compact Chinese resume layout: top identity block, black divider rules, concise section headers, organization/role on the left and date on the right.
- Keep the source template unchanged. Work from a copy or use it only as a style reference.
- Keep all body copy factual and compact. If material runs long, preserve the facts and let the resume continue to page two; do not silently shrink type below readable size.
- A simulated avatar must carry the label “模拟头像（示意）” in the Feishu source and must never replace a real supplied photo.
- The final Word and PDF must contain the same content. PDF is the primary delivery artifact and must be visually inspected page by page before delivery.

Read [input-schema.md](references/input-schema.md) before creating or modifying the content JSON.
