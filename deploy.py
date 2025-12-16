import os
import subprocess

def run(cmd):
    print(f"\n▶️ 运行：{cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ 命令失败：{cmd}")
        exit(1)

def main():
    print("🚀 开始部署流程…")

    # 1. 运行 build.py
    run("python build.py")

    # 2. 添加所有修改
    run("git add .")

    # 3. 提交
    run('git commit -m "update site"')

    # 4. 推送到 GitHub
    run("git push")

    print("\n✅ 部署完成！网站已更新。")

if __name__ == "__main__":
    main()
