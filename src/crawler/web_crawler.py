import requests
from bs4 import BeautifulSoup
from tkinter import messagebox

class WebCrawler:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()  # 检查请求是否成功
            print("数据抓取成功")
            return response.text
        except requests.RequestException as e:
            messagebox.showerror("错误", f"请求失败: {e}")
            return None

    def parse_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        results = []

        # 抓取豆瓣排名前二十的电影
        movie_items = soup.find_all('div', class_='item', limit=20)
        for item in movie_items:
            title = item.find('span', class_='title').get_text()  # 电影标题
            rating = item.find('span', class_='rating_num').get_text()  # 电影评分
            results.append(f"{title} - 评分: {rating}")
            print(f"抓取到的电影: {title} - 评分: {rating}")  # 打印抓取到的电影信息

        print(f"解析到的数据: {results}")  # 打印解析到的数据
        return results 