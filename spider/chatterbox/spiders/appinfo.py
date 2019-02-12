# -*- coding: utf-8 -*-
import scrapy
from chatterbox import settings
import os
import json
from datetime import datetime
from urllib.parse import urlparse

class AppinfoSpider(scrapy.Spider):
    name = 'appinfo'

    def __init__(self):
        now = datetime.now()
        today = now.strftime("%Y%m%d")
        self.today_string = today

    def format_app_url(self, id):
        return "https://itunes.apple.com/cn/app/" + id

    def get_apps_txt_path(self):
        return os.path.join(settings.PROJECT_ROOT,'..','apps.txt')
    
    def get_apps_txt_ids(self):
        ids = []

        apps_txt_path = self.get_apps_txt_path()
        print('apps.txt : {}'.format(apps_txt_path))

        with open(apps_txt_path) as fp:
            for line in fp:
                line = line.strip()
                if line == '' or line.startswith('#'):
                    continue
                ids.append(line)
        return ids

    def get_today_directory(self):
        return os.path.join(settings.PROJECT_ROOT,'..','data',self.today_string)

    def get_today_topapp_json_path(self):
        return os.path.join(self.get_today_directory(),'topapp.json')

    def get_today_topapp_ids(self):
        ids = []

        today_topapp_json_path = self.get_today_topapp_json_path()
        print('today topapp.json : {}'.format(today_topapp_json_path))

        with open(today_topapp_json_path) as fp:
            items = json.load(fp)
            for item in items:
                ids.append(item['id'])

        return ids

    def get_ignore_idset(self):
        result_dir = os.path.join(self.get_today_directory(),'appinfo')
        if not os.path.exists(result_dir):
            return set()

        ids = set()
        filenames = os.listdir(result_dir)
        for filename in filenames:
            id = filename.split('.')[0]
            ids.add(id)

        return ids

    def get_urls(self):
        # apps.txt
        ids = []
        ids.extend(self.get_apps_txt_ids())

        # data/${today}/topapp.json
        ids.extend(self.get_today_topapp_ids())

        # make unique
        ids = list(set(ids))

        # remove ignore
        ignoreset = self.get_ignore_idset()
        print('ignore ids : {}'.format(ignoreset))
        ids = [id for id in ids if id not in ignoreset ]
        
        return [self.format_app_url(id) for id in ids]
    


    def start_requests(self):
        urls = self.get_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        app = {}

        if response.status != 200:
            print('result ignored because response status : {}'.format(response.status))
            return

        print('*' * 80)
        url = urlparse(response.url)
        product_id = url.path.split('/')[-1]

        # app name
        app_name = response.css('header.product-header h1.product-header__title::text').get()
        app_name = app_name.strip()
        if app_name == '':
            print('!!!!! can not get app name for {}'.format(response.url))
            return

        # version items
        version_history = []
        version_items = response.css('ul.version-history__items li.version-history__item')
        for item in version_items:
            version = item.css('h4.version-history__item__version-number::text').get()
            release_date = item.css('time.version-history__item__release-date::text').get()

            version_history.append({
                'version': version,
                'release_date': release_date
            })
        
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

        headerlist = response.css('ul.app-header__list')
        rank_desc = headerlist.xpath('li[1]/ul/li/text()').get()
        rating_desc = headerlist.css('figcaption.we-rating-count::text').get()

        if rank_desc:
            rank_desc = rank_desc.strip()
        if rating_desc:
            rating_desc = rating_desc.strip()

        appinfo = {
            'url': response.url,
            'id': product_id,
            'app_name': app_name,
            'rank_desc': rank_desc,
            'rating_desc': rating_desc,
            'info_list': info_dict,
            'version_history': version_history,
        }

        result_dir = os.path.join(self.get_today_directory(),'appinfo')
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)

        result_path = os.path.join(result_dir, product_id+'.json')
        with open(result_path,'w') as fp:
            json.dump(appinfo, fp, indent=2)
        