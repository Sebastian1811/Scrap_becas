import scrapy
import scrapy.loader.processors  
from itemloaders.processors import MapCompose
from ..config import BECAS_URL_SOURCE
from ..items import Becas


class SpiderWeMakeScholars(scrapy.Spider):
    name = "WeMakeScholars"
    start_urls = [BECAS_URL_SOURCE[3]]

    custom_settings = {
        "FEEDS":{
            "DT3-WeMakeScholars.csv":{
                "format":"csv",
                "overwrite":True,
                "encoding":"utf8"
            }
        },
    }

