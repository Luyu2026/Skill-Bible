#!/usr/bin/env python3
"""Render a stable, sample-style PDF resume directly from the normalized JSON."""

import argparse
import json
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


CJK_FONT = "ResumeSongti"
CJK_BOLD_FONT = "ResumeSongtiBold"
FONT_PATH = "/System/Library/Fonts/Supplemental/Songti.ttc"
BODY_SIZE = 7.2
LINE_HEIGHT = 9.2
LEFT = 1.15 * cm
RIGHT = 1.15 * cm
TOP = 0.9 * cm
BOTTOM = 0.85 * cm
PHOTO_SIZE = 2.0 * cm


def register_fonts():
    # Embed a real Chinese font instead of relying on a reader's CJK language
    # pack. This keeps the PDF stable across macOS, Windows, and web previews.
    pdfmetrics.registerFont(TTFont(CJK_FONT, FONT_PATH, subfontIndex=2))
    pdfmetrics.registerFont(TTFont(CJK_BOLD_FONT, FONT_PATH, subfontIndex=5))


def wrap_text(text, font, size, max_width):
    """Wrap CJK and mixed-language copy using the actual PDF font metrics."""
    lines, current = [], ""
    for paragraph in str(text).split("\n"):
        for char in paragraph:
            candidate = current + char
            if current and pdfmetrics.stringWidth(candidate, font, size) > max_width:
                lines.append(current)
                current = char
            else:
                current = candidate
        if current:
            lines.append(current)
            current = ""
    return lines or [""]


class ResumePDF:
    def __init__(self, output, data, avatar=None):
        self.data = data
        self.avatar = avatar
        self.page_width, self.page_height = A4
        self.pdf = canvas.Canvas(str(output), pagesize=A4)
        self.y = self.page_height - TOP

    @property
    def content_width(self):
        return self.page_width - LEFT - RIGHT

    def font(self, size=BODY_SIZE, bold=False):
        self.pdf.setFont(CJK_BOLD_FONT if bold else CJK_FONT, size)

    def new_page(self):
        self.pdf.showPage()
        self.y = self.page_height - TOP

    def ensure(self, height):
        if self.y - height < BOTTOM:
            self.new_page()

    def text_center(self, text, y, size, bold=False):
        self.font(size, bold)
        self.pdf.drawCentredString(self.page_width / 2, y, text)

    def draw_header(self):
        photo_top = self.y
        photo_bottom = photo_top - PHOTO_SIZE
        if self.avatar and self.avatar.exists():
            image = ImageReader(str(self.avatar))
            width, height = image.getSize()
            scale = min(PHOTO_SIZE / width, PHOTO_SIZE / height)
            draw_w, draw_h = width * scale, height * scale
            photo_x = self.page_width - RIGHT - draw_w
            photo_y = photo_top - draw_h
            self.pdf.drawImage(image, photo_x, photo_y, width=draw_w, height=draw_h, mask="auto")

        # Match the sample: the identity block is centered on the page;
        # the photo sits separately in the right rail.
        self.text_center(self.data["name"], photo_top - 21, 14.5, bold=True)
        self.text_center(self.data["contact"], photo_top - 39, 8.1)
        self.y = photo_bottom - 10

    def draw_section_title(self, title):
        self.ensure(18)
        self.y -= 2.5
        self.font(9.0, bold=True)
        self.pdf.drawString(LEFT, self.y, title)
        self.y -= 3.2
        self.pdf.setLineWidth(0.7)
        self.pdf.line(LEFT, self.y, self.page_width - RIGHT, self.y)
        self.y -= 9.2

    def draw_wrapped(self, text, x, max_width, size=BODY_SIZE, bullet=False):
        prefix = "•  " if bullet else ""
        indent = pdfmetrics.stringWidth(prefix, CJK_FONT, size) if bullet else 0
        lines = wrap_text(text, CJK_FONT, size, max_width - indent)
        self.ensure(len(lines) * LINE_HEIGHT + 1)
        self.font(size)
        for index, line in enumerate(lines):
            if index == 0 and bullet:
                self.pdf.drawString(x, self.y, prefix)
            self.pdf.drawString(x + indent, self.y, line)
            self.y -= LINE_HEIGHT

    def draw_entry(self, entry):
        self.ensure(16)
        label = entry["organization"] + (f"｜{entry['role']}" if entry.get("role") else "")
        date = entry.get("period", "")
        self.font(7.9, bold=True)
        self.pdf.drawString(LEFT, self.y, label)
        self.font(7.2)
        self.pdf.drawRightString(self.page_width - RIGHT, self.y, date)
        self.y -= 10.5
        if entry.get("intro"):
            self.draw_wrapped(entry["intro"], LEFT, self.content_width)
        for item in entry.get("bullets", []):
            self.draw_wrapped(item, LEFT, self.content_width, bullet=True)
        self.y -= 1.3

    def build(self):
        self.draw_header()
        self.draw_section_title("个人总结")
        for item in self.data.get("summary", []):
            self.draw_wrapped(item, LEFT, self.content_width, bullet=True)
        for section in self.data.get("sections", []):
            entries = section.get("entries", [])
            if not entries:
                continue
            self.draw_section_title(section["title"])
            for entry in entries:
                self.draw_entry(entry)
        if self.data.get("education"):
            self.draw_section_title("教育经历")
            for edu in self.data["education"]:
                self.draw_entry({
                    "organization": edu["school"],
                    "period": edu.get("period", ""),
                    "intro": edu.get("detail", ""),
                    "bullets": edu.get("bullets", []),
                })
        if self.data.get("skills"):
            self.draw_section_title("精通技能")
            self.draw_wrapped("、".join(self.data["skills"]), LEFT, self.content_width)
        self.pdf.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--avatar", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    for key in ("name", "contact"):
        if not data.get(key):
            raise ValueError(f"Missing required field: {key}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    register_fonts()
    ResumePDF(args.output, data, args.avatar).build()


if __name__ == "__main__":
    main()
