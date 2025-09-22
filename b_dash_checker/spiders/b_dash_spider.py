import scrapy
import pandas as pd

class BDashSpider(scrapy.Spider):
    name = 'b_dash'

    def __init__(self, *args, **kwargs):
        super(BDashSpider, self).__init__(*args, **kwargs)
        # 顧客リストのCSVファイルを読み込む
        try:
            # このファイルパスをあなたのCSVファイルの正確なパスに変更してください
            df = pd.read_csv('merged_target_site_domain.csv')
            self.start_urls = [f'http://{domain}' for domain in df['domain']]
        except FileNotFoundError:
            self.logger.error("customer_list.csv not found! Please check the file path.")
            self.start_urls = []

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_zyte_api.handler.ScrapyZyteAPIDownloadHandler',
            'https': 'scrapy_zyte_api.handler.ScrapyZyteAPIDownloadHandler',
        },
        'ZYTE_API_KEY': 'YOUR_API_KEY', '3852e5cef3c84163a2ec69ac249d0c67'
        'ZYTE_API_DOWNLOAD_HANDLERS_HTTP_TIMEOUT': 600,
        'CONCURRENT_REQUESTS': 16, # 並列リクエスト数を増やす
        'DOWNLOAD_DELAY': 0, # Zyte APIを使用する場合は不要
    }

    def parse(self, response):
        # ページのHTMLをすべて文字列として取得
        html_content = response.text

        basic_tag = 'btm.js' in html_content
        data_logging = 'bdash_log.js' in html_content
        normal_recommend = '/recommend-script/' in html_content
        ai_recommend = '/ai-recommend-script/' in html_content

        yield {
            'domain': response.url,
            'basic_tag': 1 if basic_tag else 0,
            'data_logging': 1 if data_logging else 0,
            'normal_recommend': 1 if normal_recommend else 0,
            'ai_recommend': 1 if ai_recommend else 0,
        }