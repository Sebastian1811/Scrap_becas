import scrapy
from scrapy.loader.processors  import MapCompose
from ..config import BECAS_URL_SOURCE
from ..items import Becas

class Spider_SinFronteras(scrapy.Spider):
    name = "SinFronteras"
    start_urls = [BECAS_URL_SOURCE]

    custom_settings = {
        'FEED_URI':'becas.csv',
        'FEED_FORMAT':'csv',
        'FEED_EXPORT_ENCODING':'utf-8',
        #'CLOSESPIDER_PAGECOUNT': 2
    }

    Xpath_Expressions = {
        'links':'//div[@class="tb-grid-column"]/div/a/@href',
        'title': '//h1/strong/text()',
        'next_page': '//div[@class="wpv-pagination-nav-links colour titulo_beca acm_container_width"]//a/@href'
    }

    def parse(self,response):
        links_becas = response.xpath(self.Xpath_Expressions['links']).getall()

        for link in links_becas:
            yield response.follow(link,callback=self.parse_link)

        next_page = response.xpath(self.Xpath_Expressions['next_page']).get()
        yield response.follow(next_page,callback=self.parse)

    def parse_link(self,response):
        #name = response.xpath(self.Xpath_Expressions['title']).get()
        item = scrapy.loader.ItemLoader(Becas(),response)
        item.add_xpath('name',self.Xpath_Expressions['title'])
        #item.add_xpath('requisito',Xpath_number_awards_Expression)
        #item.add_xpath('study_level',self.Xpath_Expressions['study_level'])
        yield item.load_item()

    def LimpiarTexto(self,texto:str):
        newText= texto.replace('"','')
