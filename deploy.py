import os
import subprocess
import requests
import json

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/search"
SITE_URL = "https://rtjason01.github.io/geo-content/"

def run(cmd, allow_fail=False):
    print(f"\n▶️ 运行：{cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # 打印输出
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)

    # 如果允许失败（例如 git commit 无变化），则不退出
    if allow_fail:
        return result

    # 不允许失败的命令
    if result.returncode != 0:
        print(f"❌ 命令失败：{cmd}")
        exit(1)

    return result

def trigger_deepseek():
    """通过 DeepSeek 搜索接口触发抓取（使用环境变量中的 API Key）"""
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        print("⚠️ 未检测到环境变量 DEEPSEEK_API_KEY，跳过 DeepSeek 抓取触发")
        return

    print("\n🌐 正在通知 DeepSeek 抓取最新内容…")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "query": f"site:{SITE_URL}"
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            print("✅ DeepSeek 已收到抓取请求（搜索接口触发成功）")
        else:
            print(f"⚠️ DeepSeek 返回状态码：{response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"⚠️ 无法连接 DeepSeek API：{e}")

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

    # 4. 推送到 GitHub（即使没有 commit 也不会报错）
    run("git push", allow_fail=True)

    # 5. ✅ 触发 DeepSeek 抓取
    trigger_deepseek()

    print("\n✅ 部署完成！网站已更新并通知 DeepSeek 抓取。")

if __name__ == "__main__":
    main()
