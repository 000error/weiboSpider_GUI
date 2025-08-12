#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os
import argparse

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 创建一个模拟的FLAGS对象来避免absl flags的问题
class MockFlags:
    def __init__(self):
        self.user_id_list = None
        self.u = None
        self.config_path = None
        self.output_dir = None

# 在导入spider模块之前设置模拟的FLAGS
import weibo_spider.spider as spider_module
spider_module.FLAGS = MockFlags()

from weibo_spider.spider import Spider
from weibo_spider import config_util
import json
import shutil

def load_config(config_path=None):
    """加载配置文件，不依赖FLAGS"""
    if config_path and os.path.exists(config_path):
        # 使用指定的配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    else:
        # 使用默认配置文件
        current_dir = os.getcwd()
        default_config_path = os.path.join(current_dir, 'config.json')
        
        if not os.path.exists(default_config_path):
            # 复制示例配置文件
            spider_dir = os.path.dirname(os.path.abspath(__file__))
            sample_config = os.path.join(spider_dir, 'weibo_spider', 'config_sample.json')
            if os.path.exists(sample_config):
                shutil.copy(sample_config, default_config_path)
                print(f"已创建默认配置文件: {default_config_path}")
                print("请编辑配置文件后重新运行")
                return None
        
        with open(default_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config

def main():
    parser = argparse.ArgumentParser(description='微博爬虫')
    parser.add_argument('--config_path', help='配置文件路径')
    parser.add_argument('--output_dir', help='输出目录')
    
    args = parser.parse_args()
    
    try:
        # 读取配置文件
        config = load_config(args.config_path)
        if config is None:
            return
        
        # 验证配置
        try:
            config_util.validate_config(config)
        except Exception as e:
            print(f"配置验证失败: {str(e)}")
            return
        
        # 设置输出目录
        if args.output_dir:
            os.chdir(args.output_dir)
        
        print(f"开始爬取微博数据...")
        print(f"用户ID: {config.get('user_id_list', [])}")
        print(f"时间范围: {config.get('since_date')} 到 {config.get('end_date')}")
        print(f"输出格式: {config.get('write_mode', [])}")
        print("-" * 50)
        
        # 创建爬虫实例并开始爬取
        wb = Spider(config)
        wb.start()
        
        print("-" * 50)
        print("爬取完成！")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()