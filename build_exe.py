#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller安装成功！")
        return True
    except subprocess.CalledProcessError:
        print("PyInstaller安装失败！")
        return False

def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # PyInstaller命令参数
    cmd = [
        "pyinstaller",
        "--onefile",                    # 打包成单个文件
        "--windowed",                   # 不显示控制台窗口
        "--name=微博爬虫工具",           # 可执行文件名称
        "--icon=icon.ico",              # 图标文件（如果存在）
        "--add-data=weibo_spider;weibo_spider",  # 包含weibo_spider模块
        "--add-data=run_spider.py;.",   # 包含运行脚本
        "--add-data=使用说明.md;.",      # 包含使用说明
        "--hidden-import=weibo_spider",
        "--hidden-import=weibo_spider.spider",
        "--hidden-import=weibo_spider.parser",
        "--hidden-import=weibo_spider.downloader",
        "--hidden-import=weibo_spider.writer",
        "weibo_spider_gui.py"
    ]
    
    # 如果没有图标文件，移除图标参数
    if not os.path.exists("icon.ico"):
        cmd = [arg for arg in cmd if not arg.startswith("--icon")]
    
    try:
        subprocess.check_call(cmd)
        print("可执行文件构建成功！")
        
        # 检查输出文件
        exe_path = os.path.join("dist", "微博爬虫工具.exe")
        if os.path.exists(exe_path):
            print(f"可执行文件位置: {os.path.abspath(exe_path)}")
            
            # 复制使用说明到dist目录
            if os.path.exists("使用说明.md"):
                shutil.copy("使用说明.md", "dist/")
                print("使用说明已复制到输出目录")
            
            return True
        else:
            print("构建失败：找不到输出文件")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"构建失败：{e}")
        return False

def create_icon():
    """创建简单的图标文件（SVG格式）"""
    icon_svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect width="64" height="64" rx="8" fill="#1DA1F2"/>
  <text x="32" y="40" font-family="Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="white">微</text>
</svg>'''
    
    with open("icon.svg", "w", encoding="utf-8") as f:
        f.write(icon_svg)
    print("已创建图标文件: icon.svg")

def main():
    print("=" * 50)
    print("微博爬虫可视化工具 - 可执行文件构建器")
    print("=" * 50)
    
    # 检查是否安装了PyInstaller
    try:
        import PyInstaller
        print("PyInstaller已安装")
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        if not install_pyinstaller():
            print("安装失败，请手动安装PyInstaller")
            return
    
    # 创建图标
    create_icon()
    
    # 构建可执行文件
    if build_executable():
        print("\n" + "=" * 50)
        print("构建完成！")
        print("可执行文件位于 dist/ 目录中")
        print("您可以将整个 dist/ 目录分发给其他用户")
        print("=" * 50)
    else:
        print("\n构建失败，请检查错误信息")

if __name__ == "__main__":
    main()