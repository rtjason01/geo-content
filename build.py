import pandas as pd
from pathlib import Path
from html import escape

EXCEL_FILE = "content.xlsx"
OUTPUT_HTML = Path("docs/index.html")
PAGE_TITLE = "GEO 知识库"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
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

def main():
    df = load_content()
    html_body = generate_html(df)

    OUTPUT_HTML.parent.mkdir(exist_ok=True)
    OUTPUT_HTML.write_text(
        HTML_TEMPLATE.format(title=PAGE_TITLE, content=html_body),
        encoding="utf-8"
    )

    print(f"✅ HTML 已生成：{OUTPUT_HTML.resolve()}")

if __name__ == "__main__":
    main()
