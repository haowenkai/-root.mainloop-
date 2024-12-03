import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
from src.crawler.web_crawler import WebCrawler

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("豆瓣电影抓取工具")
        self.root.geometry("700x500")
        self.root.configure(bg="#ffffff")

        # 创建主框架
        self.main_frame = tk.Frame(root, bg="#ffffff")
        self.main_frame.pack(pady=20)

        # 输入网址的标签和输入框
        self.url_entry = tk.Entry(self.main_frame, width=50, font=("Helvetica", 12))
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        self.url_entry.insert(0, "https://movie.douban.com/top250")  # 默认网址

        # 抓取数据按钮
        self.fetch_button = tk.Button(self.main_frame, text="抓取数据", command=self.crawl, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), relief=tk.FLAT)
        self.fetch_button.grid(row=0, column=2, padx=10, pady=10)

        # 保存结果按钮
        self.save_button = tk.Button(self.main_frame, text="保存结果", command=self.save_results, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), relief=tk.FLAT)
        self.save_button.grid(row=1, column=2, padx=10, pady=10)

        # 结果区域
        self.result_area = scrolledtext.ScrolledText(self.main_frame, width=70, height=20, font=("Helvetica", 12))
        self.result_area.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # 状态栏
        self.status_bar = tk.Label(root, text="状态: 等待操作", bd=1, relief=tk.SUNKEN, anchor=tk.W, bg="#ffffff")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 进度条
        self.progress_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def crawl(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showwarning("警告", "请输入网址！")
            return
        self.status_bar.config(text="状态: 正在抓取数据...")
        self.progress_bar.start()  # 启动进度条

        crawler = WebCrawler(url)
        html = crawler.fetch_data()
        if html:
            data = crawler.parse_data(html)  # 只传递 HTML 内容
            if data:  # 确保数据不为空
                self.result_area.delete(1.0, tk.END)  # 清空文本区域
                self.result_area.insert(tk.END, "\n".join(data))
            else:
                self.result_area.insert(tk.END, "未能解析到任何数据")
            self.status_bar.config(text="状态: 数据抓取成功")
        else:
            self.result_area.insert(tk.END, "无法获取数据")
            self.status_bar.config(text="状态: 数据抓取失败")

        self.progress_bar.stop()  # 停止进度条
        self.progress_bar['value'] = 100  # 设置进度条为完成状态

    def save_results(self):
        results = self.result_area.get(1.0, tk.END).strip()
        if not results:
            messagebox.showwarning("警告", "没有数据可保存！")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(results)
            messagebox.showinfo("成功", "结果已保存！") 