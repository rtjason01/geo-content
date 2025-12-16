import pandas as pd
from pathlib import Path
import json
from datetime import datetime

INPUT_FILE = "content.xlsx"
OUTPUT_HTML = "docs/index.html"
OUTPUT_SITEMAP = "docs/sitemap.xml"
OUTPUT_ROBOTS = "docs/robots.txt"

SITE_URL = "https://rtjason01.github.io/geo-content/"

def load_content():
    df = pd.read_excel(INPUT_FILE)
    return df.to_dict(orient="records")

def generate_schema(records):
    """生成 schema.org FAQPage 结构化数据"""
    faq_items = []

    for r in records:
        faq_items.append({
            "@type": "Question",
            "name": r["question"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": r["answer"]
            },
            "ai_summary": r.get("ai_summary", "")
        })

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_items
    }

def generate_html(records, schema_json):
    """生成 HTML 页面"""
    html_parts = []

    html_parts.append(f"""
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>GEO 内容库</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="{SITE_URL}">
<script type="application/ld+json">
{json.dumps(schema_json, ensure_ascii=False)}
</script>
</head>
<body>
<h1>GEO 内容库</h1>
""")

    for r in records:
        html_parts.append(f"""
<section>
  <h2>{r['question']}</h2>
  <p><strong>摘要：</strong>{r['summary']}</p>
  <p>{r['answer']}</p>
  <p><strong>关键词：</strong>{r['keywords']}</p>
  <p><strong>AI 摘要：</strong>{r.get('ai_summary', '')}</p>
</section>
<hr>
""")

    html_parts.append("</body></html>")

    Path(OUTPUT_HTML).write_text("\n".join(html_parts), encoding="utf-8")
    print(f"✅ 已生成 HTML：{OUTPUT_HTML}")

def generate_sitemap():
    """生成 sitemap.xml"""
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}</loc>
    <lastmod>{datetime.utcnow().date()}</lastmod>
  </url>
</urlset>
"""
    Path(OUTPUT_SITEMAP).write_text(content, encoding="utf-8")
    print(f"✅ 已生成 sitemap.xml")

def generate_robots():
    """生成 robots.txt"""
    content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}sitemap.xml
"""
    Path(OUTPUT_ROBOTS).write_text(content, encoding="utf-8")
    print(f"✅ 已生成 robots.txt")

def main():
    records = load_content()
    schema_json = generate_schema(records)
    generate_html(records, schema_json)
    generate_sitemap()
    generate_robots()
    print("✅ build.py 已完成所有生成任务")

if __name__ == "__main__":
    main()
