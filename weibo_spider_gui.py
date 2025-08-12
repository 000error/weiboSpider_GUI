#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import threading
import subprocess
import sys
from datetime import datetime, date

class WeiboSpiderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("微博爬虫可视化工具")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 创建界面元素
        self.create_widgets(main_frame)
        
        # 初始化配置
        self.load_default_config()
        
    def create_widgets(self, parent):
        # 标题
        title_label = ttk.Label(parent, text="微博爬虫可视化工具", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 用户ID配置
        ttk.Label(parent, text="用户ID列表:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.user_id_var = tk.StringVar(value="1669879400")
        user_id_entry = ttk.Entry(parent, textvariable=self.user_id_var, width=50)
        user_id_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        ttk.Label(parent, text="(多个ID用逗号分隔)", font=('Arial', 8)).grid(row=1, column=2, sticky=tk.W, padx=(5, 0))
        
        # 时间范围配置
        ttk.Label(parent, text="开始日期:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.since_date_var = tk.StringVar(value="2023-01-01")
        since_date_entry = ttk.Entry(parent, textvariable=self.since_date_var, width=20)
        since_date_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        ttk.Label(parent, text="结束日期:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.end_date_var = tk.StringVar(value="now")
        end_date_entry = ttk.Entry(parent, textvariable=self.end_date_var, width=20)
        end_date_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 过滤选项
        ttk.Label(parent, text="微博类型:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.filter_var = tk.IntVar(value=0)
        filter_frame = ttk.Frame(parent)
        filter_frame.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        ttk.Radiobutton(filter_frame, text="全部微博", variable=self.filter_var, value=0).pack(side=tk.LEFT)
        ttk.Radiobutton(filter_frame, text="仅原创", variable=self.filter_var, value=1).pack(side=tk.LEFT, padx=(20, 0))
        
        # 下载选项
        download_frame = ttk.LabelFrame(parent, text="下载选项", padding="10")
        download_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.pic_download_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(download_frame, text="下载图片", variable=self.pic_download_var).pack(side=tk.LEFT)
        
        self.video_download_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(download_frame, text="下载视频", variable=self.video_download_var).pack(side=tk.LEFT, padx=(20, 0))
        
        # 输出格式
        ttk.Label(parent, text="输出格式:").grid(row=6, column=0, sticky=tk.W, pady=5)
        format_frame = ttk.Frame(parent)
        format_frame.grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        self.csv_var = tk.BooleanVar(value=True)
        self.txt_var = tk.BooleanVar(value=True)
        self.json_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(format_frame, text="CSV", variable=self.csv_var).pack(side=tk.LEFT)
        ttk.Checkbutton(format_frame, text="TXT", variable=self.txt_var).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Checkbutton(format_frame, text="JSON", variable=self.json_var).pack(side=tk.LEFT, padx=(10, 0))
        
        # Cookie配置
        ttk.Label(parent, text="Cookie:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.cookie_var = tk.StringVar(value="your cookie")
        cookie_entry = ttk.Entry(parent, textvariable=self.cookie_var, width=50, show="*")
        cookie_entry.grid(row=7, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # 输出目录
        ttk.Label(parent, text="输出目录:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.output_dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "weibo_data"))
        output_dir_frame = ttk.Frame(parent)
        output_dir_frame.grid(row=8, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        output_dir_frame.columnconfigure(0, weight=1)
        
        output_dir_entry = ttk.Entry(output_dir_frame, textvariable=self.output_dir_var)
        output_dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(output_dir_frame, text="浏览", command=self.browse_output_dir).grid(row=0, column=1, padx=(5, 0))
        
        # 按钮框架
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=9, column=0, columnspan=3, pady=20)
        
        self.start_button = ttk.Button(button_frame, text="开始爬取", command=self.start_crawling)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="停止爬取", command=self.stop_crawling, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="保存配置", command=self.save_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="加载配置", command=self.load_config).pack(side=tk.LEFT)
        
        # 日志输出区域
        log_frame = ttk.LabelFrame(parent, text="运行日志", padding="5")
        log_frame.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置主框架的行权重
        parent.rowconfigure(10, weight=1)
        
        # 进程变量
        self.process = None
        
    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
    
    def load_default_config(self):
        """加载默认配置"""
        self.log_message("已加载默认配置")
    
    def save_config(self):
        """保存配置到JSON文件"""
        config = self.get_config()
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="保存配置文件"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=4)
                self.log_message(f"配置已保存到: {file_path}")
                messagebox.showinfo("成功", "配置文件保存成功！")
            except Exception as e:
                self.log_message(f"保存配置失败: {str(e)}")
                messagebox.showerror("错误", f"保存配置失败: {str(e)}")
    
    def load_config(self):
        """从JSON文件加载配置"""
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="选择配置文件"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.set_config(config)
                self.log_message(f"配置已从 {file_path} 加载")
                messagebox.showinfo("成功", "配置文件加载成功！")
            except Exception as e:
                self.log_message(f"加载配置失败: {str(e)}")
                messagebox.showerror("错误", f"加载配置失败: {str(e)}")
    
    def get_config(self):
        """获取当前配置"""
        write_mode = []
        if self.csv_var.get():
            write_mode.append("csv")
        if self.txt_var.get():
            write_mode.append("txt")
        if self.json_var.get():
            write_mode.append("json")
        
        if not write_mode:
            write_mode = ["csv", "txt"]
        
        user_ids = [uid.strip() for uid in self.user_id_var.get().split(',') if uid.strip()]
        
        config = {
            "user_id_list": user_ids,
            "filter": self.filter_var.get(),
            "since_date": self.since_date_var.get(),
            "end_date": self.end_date_var.get(),
            "random_wait_pages": [1, 5],
            "random_wait_seconds": [6, 10],
            "global_wait": [[1000, 3600], [500, 2000]],
            "write_mode": write_mode,
            "pic_download": 1 if self.pic_download_var.get() else 0,
            "video_download": 1 if self.video_download_var.get() else 0,
            "file_download_timeout": [5, 5, 10],
            "result_dir_name": 0,
            "cookie": self.cookie_var.get()
        }
        
        return config
    
    def set_config(self, config):
        """设置配置到界面"""
        if "user_id_list" in config:
            self.user_id_var.set(",".join(config["user_id_list"]))
        
        if "filter" in config:
            self.filter_var.set(config["filter"])
        
        if "since_date" in config:
            self.since_date_var.set(config["since_date"])
        
        if "end_date" in config:
            self.end_date_var.set(config["end_date"])
        
        if "write_mode" in config:
            write_mode = config["write_mode"]
            self.csv_var.set("csv" in write_mode)
            self.txt_var.set("txt" in write_mode)
            self.json_var.set("json" in write_mode)
        
        if "pic_download" in config:
            self.pic_download_var.set(bool(config["pic_download"]))
        
        if "video_download" in config:
            self.video_download_var.set(bool(config["video_download"]))
        
        if "cookie" in config:
            self.cookie_var.set(config["cookie"])
    
    def validate_config(self):
        """验证配置"""
        if not self.user_id_var.get().strip():
            messagebox.showerror("错误", "请输入至少一个用户ID")
            return False
        
        if self.cookie_var.get().strip() == "your cookie":
            result = messagebox.askyesno("警告", "您还没有设置Cookie，这可能导致爬取失败。是否继续？")
            if not result:
                return False
        
        return True
    
    def start_crawling(self):
        """开始爬取"""
        if not self.validate_config():
            return
        
        # 创建输出目录
        output_dir = self.output_dir_var.get()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成配置文件
        config = self.get_config()
        config_path = os.path.join(output_dir, "config.json")
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("错误", f"创建配置文件失败: {str(e)}")
            return
        
        # 启动爬虫进程
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        self.log_message("开始爬取微博数据...")
        self.log_message(f"配置文件: {config_path}")
        self.log_message(f"输出目录: {output_dir}")
        
        # 在新线程中运行爬虫
        thread = threading.Thread(target=self.run_spider, args=(config_path, output_dir))
        thread.daemon = True
        thread.start()
    
    def run_spider(self, config_path, output_dir):
        """运行爬虫"""
        try:
            # 构建命令
            cmd = [
                sys.executable, "run_spider.py",
                "--config_path", config_path,
                "--output_dir", output_dir
            ]
            
            # 启动进程
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # 实时读取输出
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.root.after(0, self.log_message, line.strip())
            
            self.process.wait()
            
            if self.process.returncode == 0:
                self.root.after(0, self.log_message, "爬取完成！")
                self.root.after(0, messagebox.showinfo, "完成", "微博数据爬取完成！")
            else:
                self.root.after(0, self.log_message, f"爬取失败，退出码: {self.process.returncode}")
                
        except Exception as e:
            self.root.after(0, self.log_message, f"运行错误: {str(e)}")
            self.root.after(0, messagebox.showerror, "错误", f"运行失败: {str(e)}")
        finally:
            self.root.after(0, self.reset_buttons)
    
    def stop_crawling(self):
        """停止爬取"""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.log_message("爬取已停止")
        self.reset_buttons()
    
    def reset_buttons(self):
        """重置按钮状态"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
    
    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = WeiboSpiderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()