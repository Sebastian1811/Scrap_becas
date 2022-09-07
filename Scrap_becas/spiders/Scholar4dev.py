from time import sleep
import scrapy
import scrapy.loader.processors  
from itemloaders.processors import MapCompose
from ..config import BECAS_URL_SOURCE
from ..items import Becas
from bs4 import BeautifulSoup
import bs4

class Spider_Scholar4dev(scrapy.Spider):

    name = "Scholar4dev"
    start_urls = [BECAS_URL_SOURCE[0]]

    custom_settings= {
        "FEEDS":{
            "becas2.csv":{
                "format":"csv",
                "overwrite":True,
                "encoding":"utf8"
                }
        },
        #'CLOSESPIDER_PAGECOUNT': 4
    }

    Xpath_Expressions = {
        "links": '//div[contains(@id,"post-")]/div[@class="entry clearfix"]//h2/a/@href',
        "title": '//div[contains(@id,"post-")]/h1/text()',
        "next_page":'//div[@class="wp-pagenavi"]/a[@class="page larger"]/@href',
        "study_level":'//div[@class="post_column_1"]/p[contains(.,"Master") or contains(.,"PhD") or contains(.,"Postdoctoral") or contains(.,"Bachelor") or contains(.,"BS") or contains(.,"MS")]/text()',
        "study_field":'',
        "country-host":'//div[@class="post_column_1"][2]/p/text()'
    }
    

    def parse(self,response):

        links_becas = response.xpath(self.Xpath_Expressions['links']).getall()

        for link in links_becas:
            yield response.follow(link,callback=self.parse_link)

        next_page = response.xpath(self.Xpath_Expressions['next_page']).get()
        if next_page != None:
            yield response.follow(next_page,callback=self.parse)


    def parse_link(self,response):
        country_host = response.xpath(self.Xpath_Expressions['country-host']).getall()
        country_host = self.formar_country(country_host)

        study_level =  response.xpath(self.Xpath_Expressions['study_level']).getall()
        item = scrapy.loader.ItemLoader(Becas(),response)

        requisitos = self.soup_parser(response)

        if len(study_level)!=0:
            item.add_xpath('name',self.Xpath_Expressions['title'])
            item.add_value('requirements',"")
            item.add_xpath('study_level',self.Xpath_Expressions['study_level'],MapCompose(self.format_level))
            item.add_value('country_host',country_host,MapCompose(self.format_level))
        yield item.load_item()

    def formar_country(self,country:list[str]):
        country_aux=''
        for i in range(len(country)):
            if 'Study in:' in country[i]:
                country_aux = country[i]
        if ',' in country_aux:
            return country_aux.split(',',1)[1]
        else: 
            return country_aux.split(':',1)[1]       
    
    def format_level (self,study_level:str):
        if "," in study_level:
            study_level.replace(",","")
            return study_level.strip()
        else:
            return study_level.strip()      

#un comentario furtivo 
    def change(self,iterable,result_type):
        return [item for item in iterable if isinstance(item, result_type)]
        
    def soup_parser(self,response):
        
        requisitos = 0 # variable de control para hayar posicion de los requisitos
        soup = BeautifulSoup(response.body,'html.parser') 
        div = soup.find_all(attrs={'class':'entry clearfix'}) #Traigo el div padre de los requisitos
        lista = list()
        mlist = self.change(div[0],bs4.element.Tag) # Filtro la lista a solo tags
        for i in mlist:
            if i.strong != None: #El tag strong tiene los requisitos
                a = i.strong # hallo el strong
                b = a.contents #guardo el contenido del strong
                if "Eligibility" in b[0]: # pregunto si el strong son los requisitos
                    requisitos = 1 #ya puedo recopilar los requisitos
            
            if requisitos and i.strong == None:
                print("eyyyyyy")
                lista.append(i.contents)
                print(i.contents)
                sleep(3)
                if i.strong != None:
                    requisitos = 0


            #sleep(2)
        sleep(5)
       
        