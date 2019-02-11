# -*- coding: utf-8 -*-
import scrapy


class TopappSpider(scrapy.Spider):
    name = 'topapp'

    def start_requests(self):
        urls = [
            'https://www.apple.com/cn/itunes/charts/free-apps/',
            'https://www.apple.com/cn/itunes/charts/paid-apps/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        appsection = response.css('section.apps')
        apps = appsection.css('li')
        for app in apps:
            # img = app.css('a img::attr(src)').get()
            # img = response.urljoin(img)

            # name = app.css('h3 a::text').get()
            url = app.css('h3 a::attr(href)').get()
            # category = app.css('h4 a::text').get()

            yield({
                'url': url,
            })
        
        

    