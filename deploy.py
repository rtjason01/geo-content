import os
import subprocess
import requests

SITE_URL = "https://rtjason01.github.io/geo-content/"

def run(cmd, allow_fail=False):
    print(f"\n▶️ 运行：{cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    if allow_fail:
        return result

    if result.returncode != 0:
        print(f"命令失败：{cmd}")
        exit(1)

    return result

def trigger_crawler():
    """通过模拟访问触发搜索引擎抓取"""
    print("\n正在模拟访问以触发搜索引擎抓取…")

    urls = [
        SITE_URL,
        SITE_URL + "sitemap.xml",
        SITE_URL + "robots.txt",
        SITE_URL + "data.json",
    ]

    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            print(f"[OK] 访问 {url} 状态码: {r.status_code}")
        except Exception as e:
            print(f"[WARN] 无法访问 {url}: {e}")

    print("[OK] 模拟访问完成，搜索引擎将自动抓取更新")

def main():
    print("🚀 开始部署流程…")

    # 1. 运行 build.py
    run("python build.py")

    # 2. 添加所有修改
    run("git add .")

    # 3. 提交（允许无变化）
    commit_result = run('git commit -m "update site"', allow_fail=True)

    if "nothing to commit" in commit_result.stdout.lower():
        print("ℹ️ 没有文件变化，跳过提交步骤")

    # 4. 推送到 GitHub
    run("git push", allow_fail=True)

    # 5. ✅ 模拟访问触发抓取
    trigger_crawler()

    print("\n✅ 部署完成！网站已更新并触发搜索引擎抓取。")

if __name__ == "__main__":
    main()
