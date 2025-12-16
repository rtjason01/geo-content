import subprocess
import sys

def run(cmd):
    print(f"\n▶ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("❌ 命令执行失败，已停止部署")
        sys.exit(1)

def main():
    print("🚀 开始自动部署 GEO 网站到 GitHub Pages")

    # 1. 生成 HTML
    run("python build.py")

    # 2. 添加所有文件
    run("git add .")

    # 3. 提交（如果没有变化会失败，所以加上 || true）
    run('git commit -m "update site" || true')

    # 4. 推送到 GitHub
    run("git push")

    print("\n✅ 部署完成！GitHub Pages 会在几秒内自动更新。")
    print("🌐 访问你的站点： https://rtjason01.github.io/geo-content/")

if __name__ == "__main__":
    main()
