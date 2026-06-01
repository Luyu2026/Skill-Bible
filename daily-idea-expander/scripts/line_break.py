#!/usr/bin/env python3
"""
机械断行脚本：原版文案 → 剪辑版（≤9字断行，不删不改任何字词标点）。

核心规则：
- 原句照搬，不删、不加、不改任何一个字或标点
- 每行 ≤9 字（中文字符）
- 优先在标点后断开
- 如果第9字正好是标点前一个字，允许带入标点（行长为10）

用法:
  python3 line_break.py <原文文件>
  echo "原文内容" | python3 line_break.py -
"""

import sys


PUNCT = set('。！？；：，、」』）')


def break_paragraph(para, max_chars=9):
    """将一段文字机械断行，不改变任何内容。"""
    lines = []
    para = para.strip()
    while len(para) > max_chars:
        cut = max_chars
        # 在倒数4个字内找标点，优先在标点后断开（标点归上一行）
        for i in range(max_chars - 1, max(0, max_chars - 4) - 1, -1):
            if para[i] in PUNCT:
                cut = i + 1  # 标点归入当前行
                break
        # 如果第 max_chars 位刚好是标点，也带入当前行
        if cut == max_chars and len(para) > max_chars and para[max_chars] in PUNCT:
            cut = max_chars + 1
        lines.append(para[:cut])
        para = para[cut:].lstrip()
    if para:
        lines.append(para)
    return lines


def break_lines(text, max_chars=9):
    text = text.strip()
    result = []
    for para in text.split('\n'):
        para = para.strip()
        if not para:
            result.append('')
        else:
            result.extend(break_paragraph(para, max_chars))
    return '\n'.join(result)


def main():
    if len(sys.argv) < 2 or sys.argv[1] == '-':
        text = sys.stdin.read()
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            text = f.read()
    print(break_lines(text))


if __name__ == '__main__':
    main()
