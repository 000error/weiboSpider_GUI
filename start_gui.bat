@echo off
chcp 65001
title 微博爬虫可视化工具
echo 正在启动微博爬虫可视化工具...
echo.
python weibo_spider_gui.py
if errorlevel 1 (
    echo.
    echo 启动失败，请检查Python环境是否正确安装
    echo 按任意键退出...
    pause >nul
)