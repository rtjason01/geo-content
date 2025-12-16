import pandas as pd
from pathlib import Path
from html import escape
from datetime import datetime

EXCEL_FILE = "content.xlsx"
OUTPUT_DIR = Path("docs")
OUTPUT_HTML = OUTPUT_DIR / "index.html"
SITEMAP_FILE = OUTPUT_DIR / "sitemap.xml"
ROBOTS_FILE = OUTPUT_DIR / "robots.txt"

SITE_URL = "https://rtjason01.github.io/geo-content/"
PAGE_TITLE = "GEO 内容库"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="description" content="GEO 内容库，结构化知识，自动部署，适合 AI 抓取和 SEO 优化。">
<meta name="keywords" content="GEO, AI, 内容库, SEO, GitHub Pages">
<link rel="canonical" href="{site_url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="结构化内容，适合 AI 抓取和搜索引擎优化。">
<meta property="og:url" content="{site_url}">
<script type="application/ld+json">
{schema_json}
</script>
<style>
body {{
    font-family: system-ui, sans-serif;
    max-width: 860px;
    margin: 0 auto;
    padding: 24px;
    background: #fafafa;
    line-height: 1.7;
}}
h1 {{
    font-size: 32px;
    border-bottom: 2px solid #eee;
    padding-bottom: 8px;
}}
h2 {{
    margin-top: 40px;
    padding-left: 10px;
    border-left: 4px solid #3b82f6;
}}
.faq-block {{
    background: #fff;
    padding: 16px;
    margin: 20px 0;
    border-radius: 8px;
    border: 1px solid #eee;
}}
.summary {{
    font-weight: 600;
}}
.keywords {{
    margin-top: 12px;
    font-size: 14px;
    color: #666;
}}
</style>
</head>
<body>

<h1>{title}</h1>

<main>
{content}
</main>

</body>
</html>
"""

def load_content():
    df = pd.read_excel(EXCEL_FILE)
    df.columns = [c.strip() for c in df.columns]
    return df

def generate_html(df):
    grouped = df.groupby("category")
    html_parts = []

    for category, group in grouped:
        html_parts.append(f"<h2>{escape(str(category))}</h2>")

        for _, row in group.iterrows():
            html_parts.append('<div class="faq-block">')
            html_parts.append(f"<h3>{escape(str(row['question']))}</h3>")

            if pd.notna(row.get("summary", "")):
                html_parts.append(f"<p class='summary'>{escape(str(row['summary']))}</p>")

            answer = str(row["answer"]).split("\n")
            for para in answer:
                if para.strip():
                    html_parts.append(f"<p>{escape(para.strip())}</p>")

            if pd.notna(row.get("keywords", "")):
                html_parts.append(
                    f"<div class='keywords'>关键词：{escape(str(row['keywords']))}</div>"
                )

            html_parts.append("</div>")

    return "\n".join(html_parts)

def generate_schema(df):
    items = []
    for _, row in df.iterrows():
        items.append({
            "@type": "Question",
            "name": str(row["question"]),
            "acceptedAnswer": {
                "@type": "Answer",
                "text": str(row["answer"])
            }
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": items
    }

    import json
    return json.dumps(schema, ensure_ascii=False, indent=2)

def generate_sitemap():
    today = datetime.today().strftime("%Y-%m-%d")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{SITE_URL}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    SITEMAP_FILE.write_text(xml, encoding="utf-8")

def generate_robots():
    txt = f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}sitemap.xml
"""
    ROBOTS_FILE.write_text(txt, encoding="utf-8")

def main():
    df = load_content()
    html_body = generate_html(df)
    schema_json = generate_schema(df)

    OUTPUT_DIR.mkdir(exist_ok=True)

    OUTPUT_HTML.write_text(
        HTML_TEMPLATE.format(
            title=PAGE_TITLE,
            content=html_body,
            schema_json=schema_json,
            site_url=SITE_URL
        ),
        encoding="utf-8"
    )

    generate_sitemap()
    generate_robots()

    print("✅ HTML 已生成：docs/index.html")
    print("✅ sitemap.xml 已生成")
    print("✅ robots.txt 已生成")
    print("✅ schema.org FAQ 已自动嵌入")
    print("🚀 SEO / AI 抓取优化全部完成")

if __name__ == "__main__":
    main()
