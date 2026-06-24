# -*- coding: utf-8 -*-
"""
个人简历在线展示网站 — Flask 后端
==================================
本地运行方式：
    python app.py
    浏览器访问 -> http://127.0.0.1:5000
"""

import sys
import os

# ============================================================
# Windows GBK 终端 UTF-8 兼容（必须在最前面执行）
# ============================================================
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ============================================================
# 配置变量区（统一放在文件顶部，方便修改）
# ============================================================
HOST = "127.0.0.1"                    # 监听地址
PORT = 5000                           # 监听端口
DEBUG = True                          # 调试模式（生产环境改为 False）
TEMPLATE_FOLDER = "templates"         # 前端模板目录
STATIC_FOLDER = "static"              # 静态资源目录

# 清华镜像源配置
TSUINGHUA_INDEX = "https://pypi.tuna.tsinghua.edu.cn/simple"
TSUINGHUA_HOST = "pypi.tuna.tsinghua.edu.cn"


# ============================================================
# 第1步：自动安装依赖（清华镜像源）
# ============================================================
def auto_install_dependencies():
    """检测并自动安装 Flask，使用清华镜像源避免超时"""
    import subprocess

    print("=" * 50)
    print("[依赖检测] 检查 Flask 是否已安装...")
    print("=" * 50)

    need_install = False
    try:
        import flask  # noqa: F401
        print("  [OK] Flask 已安装，跳过")
    except ImportError:
        need_install = True

    if need_install:
        print("  [>>] 正在从清华镜像安装 Flask ...")
        cmd = [
            sys.executable, "-m", "pip", "install", "flask",
            "-i", TSUINGHUA_INDEX,
            "--trusted-host", TSUINGHUA_HOST,
            "--default-timeout=120",
            "--retries=5",
        ]
        try:
            subprocess.check_call(cmd)
            print("  [OK] Flask 安装成功")
        except subprocess.CalledProcessError:
            # 备用：阿里云镜像
            print("  [>>] 清华镜像失败，尝试阿里云备用源...")
            cmd_backup = [
                sys.executable, "-m", "pip", "install", "flask",
                "-i", "https://mirrors.aliyun.com/pypi/simple/",
                "--trusted-host", "mirrors.aliyun.com",
                "--default-timeout=120",
                "--retries=5",
            ]
            subprocess.check_call(cmd_backup)
            print("  [OK] Flask 安装成功（备用源）")

        # 清除 import 缓存，重新导入
        import importlib
        importlib.invalidate_caches()

    print()


# 先执行依赖安装
auto_install_dependencies()

# ============================================================
# 第2步：创建 Flask 应用
# ============================================================
from flask import Flask, render_template

# 获取当前文件所在目录作为项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, TEMPLATE_FOLDER),
    static_folder=os.path.join(BASE_DIR, STATIC_FOLDER),
)

# 强制 Flask 使用 UTF-8 编码
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


# ============================================================
# 路由：简历首页
# ============================================================
@app.route("/")
def resume():
    """
    简历主页面
    所有文本内容在 HTML 模板中硬编码，确保一字不差
    """
    return render_template("index.html")


@app.route("/cad")
def cad():
    """CAD 蓝图线上图纸展示页面"""
    return render_template("cad.html")


# ============================================================
# 启动入口
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("  个人简历在线展示网站")
    print(f"  访问地址 -> http://{HOST}:{PORT}")
    print("  按 Ctrl+C 停止服务")
    print("=" * 50)
    app.run(host=HOST, port=PORT, debug=DEBUG)
