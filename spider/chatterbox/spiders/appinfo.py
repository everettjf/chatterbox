# -*- coding: utf-8 -*-
import scrapy


class AppinfoSpider(scrapy.Spider):
    name = 'appinfo'

    def start_requests(self):
        urls = [
            # 'https://itunes.apple.com/cn/app/id423084029?l=en#?platform=iphone',
            'https://itunes.apple.com/cn/app/%E6%8A%96%E9%9F%B3%E7%9F%AD%E8%A7%86%E9%A2%91-%E5%A5%BD%E7%8E%A9%E7%9A%84%E4%BA%BA%E9%83%BD%E5%9C%A8%E8%BF%99/id1142110895?mt=8&v0=WWW-GCCN-ITSTOP100-FREEAPPS&l=&ign-mpt=uo%3D4',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # app name
        app_name = response.css('header.product-header h2.product-header__identity a.link::text').get()
        print(app_name)

        # version items
        version_items = response.css('ul.version-history__items li.version-history__item')
        for item in version_items:
            version = item.css('h4.version-history__item__version-number::text').get()
            release_date = item.css('time.version-history__item__release-date::text').get()

            print(version)
            print(release_date)
        
        # info dictionary
        info_dict = {
            'Seller': '',
            'Size': '',
            'Copyright': '',
        }
        info_section = response.css('dl.information-list--app')
        info_items = info_section.css('div.information-list__item')
        for item in info_items:
            k = item.css('dt.information-list__item__term::text').get()
            v = item.css('dd.information-list__item__definition::text').get()
            if not k or not v:
                continue

            k = k.strip('\n ')
            v = v.strip('\n ')

            if v == '':
                continue
            
            info_dict[k] = v

        print(info_dict)

        headerlist = response.css('ul.app-header__list')
        rank_desc = headerlist.xpath('li[1]/ul/li/text()').get()
        rating_desc = headerlist.css('figcaption.we-rating-count::text').get()

        if rank_desc:
            rank_desc = rank_desc.strip()
        if rating_desc:
            rating_desc = rating_desc.strip()

        print(rank_desc)
        print(rating_desc)

        