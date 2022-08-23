import scrapy
import scrapy.loader.processors  
from ..config import BECAS_URL_SOURCE
from ..items import Becas

class Spider_Scholar4dev(scrapy.Spider):

    name = "Scholar4dev"
    start_urls = [BECAS_URL_SOURCE[0]]

    custom_settings = {
        'FEED_URI':'becas.csv',
        'FEED_FORMAT':'csv',
        'FEED_EXPORT_ENCODING':'utf-8',
        #'CLOSESPIDER_PAGECOUNT': 2
    }

    Xpath_Expressions = {
        "links": '//div[contains(@id,"post-")]/div[@class="entry clearfix"]//h2/a/@href',
        "title": '//div[contains(@id,"post-")]/h1/text()',
        "next_page":'//div[@class="wp-pagenavi"]/a[@class="page larger"]/@href',
        "study_level":'//div[@class="post_column_1"]/p[contains(.,"Master") or contains(.,"PhD") or contains(.,"Postdoctoral") or contains(.,"Bachelor")]/text()'
    }
    

    def parse(self,response):

        links_becas = response.xpath(self.Xpath_Expressions['links']).getall()

        for link in links_becas:
            yield response.follow(link,callback=self.parse_link)

        next_page = response.xpath(self.Xpath_Expressions['next_page']).get()
        yield response.follow(next_page,callback=self.parse)


    def parse_link(self,response):
        item = scrapy.loader.ItemLoader(Becas(),response)
        item.add_xpath('name',self.Xpath_Expressions['title'])
        #item.add_xpath('requisito',Xpath_number_awards_Expression)
        item.add_xpath('study_level',self.Xpath_Expressions['study_level'])
        yield item.load_item()