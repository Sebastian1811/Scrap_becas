import scrapy
from scrapy.loader.processors  import MapCompose
from ..config import BECAS_URL_SOURCE
from ..items import Becas


class Spider_SinFronteras(scrapy.Spider):
    name = "SinFronteras"
    start_urls = [BECAS_URL_SOURCE]

    custom_settings= {
        "FEEDS":{
            "becas.csv":{
                "format":"csv",
                "overwrite":True,
                "encoding":"utf8"
                }
        },
        'CLOSESPIDER_PAGECOUNT': 4
    }


    Xpath_Expressions = {
        'links':'//div[@class="tb-grid-column"]/div/a/@href',
        'title': '//h1/strong/text()',
        'next_page': '//div[@class="wpv-pagination-nav-links colour titulo_beca acm_container_width"]//a[@class="wpv-archive-pagination-links-next-link js-wpv-archive-pagination-links-next-link page-link"]/@href',
        'study_level':'//div[@class="tb-fields-and-text acm_container_width" and child::p[child::a]]/p/a[contains(.,"Posdoctorado") or contains(.,"Doctorado") or contains(.,"Maestría") or contains(.,"Especialidad")]/text()'
    }
    

    def parse(self,response):

        links_becas = response.xpath(self.Xpath_Expressions['links']).getall()

        for link in links_becas:
            yield response.follow(link,callback=self.parse_link)

        next_page = response.xpath(self.Xpath_Expressions['next_page']).get()
        yield response.follow(next_page,callback=self.parse)


    def parse_link(self,response):
        #study_level= response.xpath(self.Xpath_Expressions['study_level']).getall()
        #study_level=self.format_study_level(study_level)
        item = scrapy.loader.ItemLoader(Becas(),response)
        item.add_xpath('name',self.Xpath_Expressions['title'])
        #item.add_xpath('requisito',Xpath_number_awards_Expression)
        #item.add_value('study_level',study_level)
        item.add_xpath('study_level',self.Xpath_Expressions['study_level'])
        yield item.load_item()

    def format_study_level(self,studylevels:list[str]):
        separator = ','
        if len(studylevels) > 1:
            return separator.join(studylevels)
        else:
            return studylevels[0]

