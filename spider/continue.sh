# !/bin/bash

today=`date +%Y%m%d`
outputdir=data/${today}

scrapy crawl appinfo
