from gc import callbacks
from ..config import BECAS_URL_SOURCE
from selenium.webdriver import Chrome,ChromeOptions
import json
from ..items import dicci
import scrapy


class Spider_Santander(scrapy.Spider):
    name = "Santander"
    start_urls = [BECAS_URL_SOURCE[4]]
    pages = 3
  
    #start_urls = ["https://api-manager.universia.net/becas-programs/api/search?page=1&originCountry=CO&tag=STUDIES&status=open,closed,ended&mode=faceToFace,online,semiFace&destinations=true"]
    custom_settings= {
        "FEEDS":{
            "DT4-Santander.csv":{
                "format":"csv",
                "overwrite":True,
                "encoding":"utf8"
                }
        },
        #'CLOSESPIDER_PAGECOUNT': 4,
        #"DOWNLOAD_DELAY" : 1
    }
    Xpath_Expressions = {
        'cookies-button':'//*[@id="onetrust-accept-btn-handler"]',
        'cards':'//santander-card',
        'title':'//h1[@class="hero-info__title"]/text()'
    }

    headers = { 
    "authority": "api-manager.universia.net",
    "method": "GET",
    "path": "/becas-programs/api/search?page=1&originCountry=CO&tag=STUDIES&status=open,closed,ended&mode=faceToFace,online,semiFace&destinations=true",
    "scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding":" gzip, deflate, br",
    "accept-language": "es",
    "cache-control":" no-cache",
    "origin":" https://app.becas-santander.com",
    "pragma": "no-cache",
    "referer": "https://app.becas-santander.com/",
    "req_uuid": "7ba4d5a0-35e0-11ed-ae12-2314f479b259",
    "sec-ch-ua": '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent":" Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }
    

    def parse(self, response):
        links = []
        for i in range(self.pages):
            page = i +1
            links.append("https://api-manager.universia.net/becas-programs/api/search?page="+str(page)+"&originCountry=CO&tag=STUDIES&status=open,closed,ended&mode=faceToFace,online,semiFace&destinations=true")
        for link in links:
            yield response.follow(link,callback=self.parse_link)

        
        
    def parse_link(self,response):
        data = {}
        data = response.json()
        item = scrapy.loader.ItemLoader(dicci(),response)
        data = data['data']
        for becas in data['hits']:
            a  = becas["name"]
            print(a)
            input()
            #a = becas['addressed'] ## nivel de estudio
            item.add_value('dic',becas['name'])
            yield item.load_item()
        