import scrapy
from ..config import BECAS_URL_SOURCE
from ..items import Becas


class Spider_SinFronteras(scrapy.Spider):
    name = "SinFronteras"
    start_urls = [BECAS_URL_SOURCE[1]]

    custom_settings= {
        "FEEDS":{
            "DT2-SFront.csv":{
                "format":"csv",
                "overwrite":True,
                "encoding":"utf8"
                }
        },
        #'CLOSESPIDER_PAGECOUNT': 4
    }

    Xpath_Expressions = {
        'links':'//div[@class="tb-grid-column"]/div/a/@href',
        'title': '//h1/strong/text()',
        'next_page': '//div[@class="wpv-pagination-nav-links colour titulo_beca acm_container_width"]//a[@class="wpv-archive-pagination-links-next-link js-wpv-archive-pagination-links-next-link page-link"]/@href',
        'study_level':'//div[@class="tb-fields-and-text acm_container_width" and child::p[child::a]]/p/a[contains(.,"Posdoctorado") or contains(.,"Doctorado") or contains(.,"Maestría") or contains(.,"Especialidad") or contains(.,"Grado")]/text()',
        'study_field':'//div[@class="tb-fields-and-text acm_container_width" and child::p[child::a]]/p/a[contains(.,"computación") or contains(.,"Ingeniería")]/text()',
        'country-host':'//div[@class="tb-fields-and-text acm_container_width" and child::p[child::a[child::img]]][1]/p/a/@title',
        'requirements':'//h2[@id="08-requisitos"]/../p[child::br]/text()'
    }
    
    def parse(self,response):
        links_becas = response.xpath(self.Xpath_Expressions['links']).getall()

        for link in links_becas:
            yield response.follow(link,callback=self.parse_link)

        next_page = response.xpath(self.Xpath_Expressions['next_page']).get()
        yield response.follow(next_page,callback=self.parse)


    def parse_link(self,response):
        study_level= response.xpath(self.Xpath_Expressions['study_level']).getall()
        study_level=self.format_study_level(study_level)
        study_field = response.xpath(self.Xpath_Expressions['study_field']).getall()
        study_field = self.format_study_field(study_field)
        country_host = response.xpath(self.Xpath_Expressions['country-host']).getall()
        country_host = self.format_country_host(country_host)
        requirements = response.xpath(self.Xpath_Expressions['requirements']).getall()
        requirements = self.format_requirements(requirements)
        item = scrapy.loader.ItemLoader(Becas(),response)
        if len(study_field)  !=0 and len(study_level) !=0:
            item.add_xpath('name',self.Xpath_Expressions['title'])
            item.add_value('study_level',study_level)
            item.add_value('study_field',study_field)
            item.add_value('country_host',country_host)
            item.add_value('requirements',requirements)
        yield item.load_item()
        

    def format_study_level(self,studylevels:list[str]):
        separator = ','
        if len(studylevels) > 1:
            return separator.join(studylevels)
        elif len(studylevels)==1:
            return studylevels[0]
        return []

    def format_study_field(self,studyfields:list[str]):
        if len(studyfields) >1:
            return ["ciencias de la computación","Ingeniería"]
        elif len(studyfields)==1:
            return["ciencias de la computación"]
        return []

    def format_country_host(self,countryhosts:list[str]):
        for i in range(len(countryhosts)):
            country= countryhosts[i]
            if "online" in countryhosts[i]:
                countryhosts[i] =country[20:].strip()
            else:
                countryhosts[i] =country[22:].strip()
        return countryhosts
    
    def format_requirements(self,requirements:list[str]):
        for i in range(len(requirements)):
            requirements[i] = requirements[i].strip()
            #requirements[i] = requirements[i].replace("")
        return requirements

#test boar

