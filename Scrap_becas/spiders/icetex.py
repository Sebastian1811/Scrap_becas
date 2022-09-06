import scrapy
import scrapy.loader.processors  
from itemloaders.processors import MapCompose
from ..config import BECAS_URL_SOURCE
from ..items import Becas

class icetexSpider(scrapy.Spider):
    name= "icetex"
    start_urls = [BECAS_URL_SOURCE[2]]

    custom_settings= {
        "FEEDS":{
            "becas3.csv":{
                "format":"csv",
                "overwrite":True,
                "encoding":"utf8"
                }
        },
        #'CLOSESPIDER_PAGECOUNT': 4
    }

    Xpath_Expressions={
        'links':'//div[@class="resulta_do"]/div[@class="tit_resul"]/a/@href',
        'title': '//div[@class="col-12 col-md-9"]/div/h1/text()',
        'country_host':'//div[@class="indicadores_becas" and child::span[contains(.,"País")]]/text()[2]',
        'study_field':'//div[@class="indicadores_becas" and child::span[contains(.,"Área de estudio")]]/text()[2]',
        'study_level':'//div[@class="indicadores_becas" and child::span[contains(.,"Estudio:")]]/text()[2]'
    }

    def parse(self,response):
        link_becas = response.xpath(self.Xpath_Expressions['links'])

        for link in link_becas:
            yield response.follow(link,callback=self.parse_link)

    def parse_link(self,response):
        study_level = response.xpath(self.Xpath_Expressions['study_level']).get()
        study_level = self.format_link(study_level)
        item = scrapy.loader.ItemLoader(Becas(),response)
        if study_level == "" or "Docto" in study_level or "Maestr" in study_level:
            item.add_xpath('name',self.Xpath_Expressions['title'])
            item.add_xpath('country_host',self.Xpath_Expressions['country_host'],MapCompose(self.format_link))
            item.add_xpath('study_field',self.Xpath_Expressions['study_field'],MapCompose(self.format_link))
            item.add_value('study_level',study_level)
            #item.add_xpath('study_level',self.Xpath_Expressions['study_level'],MapCompose(self.format_link))
        yield item.load_item()

    def format_link (self,study_level:str):
        if "," in study_level:
            study_level.replace(",","")
            return study_level.strip()
        else:
            return study_level.strip()    

    