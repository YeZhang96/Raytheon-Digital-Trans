# -*- coding: utf-8 -*-
import scrapy
import json
from os import path

class TechcrunchSpider(scrapy.Spider):
    name = 'techcrunch'
    allowed_domains = ['techcrunch.com']
    start_urls = ['https://search.techcrunch.com/search?p=acquisition&fr3=sb-top&fr=techcrunch'+'&pz=10&b='+str(b) for b in range(1,10001,10)]
    page_count = 0
    article_count = 0

    def parse(self, response):
        # xpath of articles url
        axp = "//*[@class='compArticleList']//h4/a/@href" 
        # xpath of next page url
        nxp = "//*[@class='compPagination']/a[@class='next']/@href"

        # extract urls
        a_urls = response.xpath(axp).extract()
        n_url = response.xpath(nxp).extract_first()

        # request articles, parse article page
        for url in a_urls:
            yield scrapy.Request(url=url, callback=self.parse_article)
            self.article_count += 1
        # # request next page, parse it by the same way
        # self.page_count += 1
        # # if page_count < 10:
        # yield scrapy.Request(url=n_url, callback=self.parse)

    def parse_article(self, response):
        # save json data of article into 'techcrunch.json'
        text = response.xpath("//*[@type='application/ld+json']/text()").extract_first() 
        fname = './techcrunch.json'
        if path.exists(fname) and self.article_count == 0:
            with open(fname, 'w') as f:
                f.write(text[2:-2]+'\n')
                
        else:
            with open(fname, 'a') as f:
                f.write(text[2:-2]+'\n')
        
        return 



