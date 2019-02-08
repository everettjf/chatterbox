# -*- coding: utf-8 -*-
import scrapy


class AppstoreSpider(scrapy.Spider):
    name = 'appstore'
    allowed_domains = ['apple.com']
    start_urls = [
        'https://itunes.apple.com/cn/app/id423084029?l=en#?platform=iphone'
    ]

    def parse(self, response):
        # app name
        app_name = response.css('header.product-header h2.product-header__identity a.link::text').get()
        print(app_name)

        # version items
        version_items = response.css('ul.version-history__items li.version-history__item')

        # each version item
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
