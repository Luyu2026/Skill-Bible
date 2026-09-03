# Input Schema

The builder accepts UTF-8 JSON. All arrays may be empty; omit no facts only because a field is inconvenient to map.

```json
{
  "name": "姓名",
  "contact": "手机号｜邮箱",
  "summary": ["优势一", "优势二"],
  "sections": [
    {
      "title": "工作经历",
      "entries": [
        {
          "organization": "公司或项目",
          "role": "职位",
          "period": "2021年05月 - 至今",
          "intro": "一句职责概述，可为空",
          "bullets": [
            {"text": "一级要点", "children": ["对应细项一", "对应细项二"]},
            "普通单层要点"
          ]
        }
      ]
    }
  ],
  "education": [
    {
      "school": "大学",
      "period": "2017年06月 - 2021年06月",
      "detail": "专业｜本科｜学院",
      "bullets": ["绩点、排名、奖项"]
    }
  ],
  "skills": ["SQL", "Excel", "Axure"]
}
```

## Mapping Notes

- `summary` is displayed as short bullet points.
- Each `sections` item is an experience group such as “工作经历” or “校园经历”.
- `intro` is a one-sentence role summary. Do not turn it into a bullet unless the source itself is a bullet.
- `bullets` may contain factual strings or nested objects with `text` and `children`. Preserve the source hierarchy and metrics exactly.
- `skills` renders as one compact line separated by Chinese commas.
