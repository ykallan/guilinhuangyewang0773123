import scrapy
import pandas as pd
import chardet
import re


class GlSpider(scrapy.Spider):
    name = 'gl'
    # allowed_domains = ['guilin.com']
    start_urls = ['http://www.0773123.com/index.asp']

    def parse(self, response):
        links = response.xpath('//p[@style="margin-left: 20px"]/a/@href').getall()
        for link in links:
            # print(link)
            yield response.follow(url=link, callback=self.parse_lists)

    def parse_lists(self, response):
        links = response.xpath('//td[@width="555"]/a/@href').getall()
        print(links)
        for link in links:
            yield response.follow(url=link, callback=self.parse_detail)

        next_pages = response.xpath('//td[@style="font-size: 16px"]/a/@href').getall()
        if next_pages:
            for next_page in next_pages:
                yield response.follow(url=next_page, callback=self.parse_lists)
                # break

    def parse_detail(self, response):
        # print(response.encoding)
        # tables = pd.read_html(response.text.encode(response.encoding).decode(response.encoding))
        # print(chardet.detect(response.text.encode(response.encoding)))
        tables = pd.read_html(response.text.encode(response.encoding).decode('GB2312'))
        # tables = pd.read_html(response.text)
        # for i, table in enumerate(tables):
        #     print('第', i, '个 table：')
        #     print(table)
        # print(tables[2])
        # print(tables[2][0][2])
        info = tables[2][0][2]

        com_name = tables[2][0][0].strip()
        # print(com_name)
        conn_name = re.findall(r'联系人：(.*?)职位', info)[0]
        # print(conn_name)
        try:
            tele = re.findall(r'.*?(\d{11}).*?', info)[0]
        except Exception as e:
            print(e)
            tele = 0
        # print(tele)
        item = {}
        item['com_name'] = com_name
        item['conn_name'] = conn_name
        item['tele'] = tele
        item['info'] = info
        yield item



