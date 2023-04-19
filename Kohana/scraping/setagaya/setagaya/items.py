# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.loader import ItemLoader

def strip_r(element):
    if element:
        return element.replace("\r","")
    return element

def strip_n(element):
    if element:
        return element.replace("\n","")
    return element

def strip_t(element):
    if element:
        return element.replace("\t","")
    return element


def nearest_line(element):
    if element:
        return element.split("「")[0]
    return element

def nearest_station(element):
    if element:
        return element.split("「")[1].split("」")[0]
    return element

def walk_time(element):
    if element:
        return element.split("歩")[1].replace("分","").split("～")[-1]
    return element

def nearest_bus_station(element):
    if element:
        if len(element.split("バス"))==1:
            return ""
        else:
            return element.split("分")[1].split("歩")[0]
    return element

def bus_time(element):
    if element:
        if len(element.split("バス"))==1:
            return ""
        else:
            return element.split("バス")[1].split("分")[0]
    return element

def convert_integer(element):
    if element:
        try:
            return int(element)
        except:
            return element
    return element

def convert_float(element):
    if element:
        try:
            return float(element)
        except:
            return element
    return element

def convert_100million(element):
    if element:
        if len(element.split("億"))!=1:
            buf = int(element.split("億")[1])
            if buf < 1000:
                return element.split("億")[0] + "0" + str(buf)
            elif buf < 100:
                return element.split("億")[0] + "00" + str(buf)
            elif buf < 10:
                return element.split("億")[0] + "000" + str(buf)
            else:
                return element.replace("億","")
    return element

def min_price(element):
    if element:
        if len(element.split("～"))==1 and len(element.split("・"))==1:
            return element.split("万円")[0]
        else:
            return element.split("～")[0].split("・")[0].split("万円")[0]
    return element


def max_price(element):
    if element:
        if len(element.split("～"))==1 and len(element.split("・"))==1:
            return element.split("万円")[0]
        else:
            return element.split("～")[-1].split("・")[-1].split("万円")[0]
    return element

def min_measure(element):
    if element:
        if len(element.split("～")) == 1 and len(element.split("・")) == 1:
            return element.split("m")[0]
        else:
            return element.split("～")[0].split("・")[0].split("m")[0]
    return element

def max_measure(element):
    if element:
        if len(element.split("～")) == 1 and len(element.split("・")) == 1:
            return element.split("m")[0]
        elif len(element.split("～")) != 1:
            return element.split("～")[1].split("m")[0]
        elif len(element.split("・")) != 1:
            return element.split("・")[1].split("m")[0]
    return element


def min_madori(element):
    if element:
        if len(element.split("～")) == 1 and len(element.split("・")) == 1:
            return element.replace("（納戸）","")
        elif len(element.split("～")) != 1:
            return element.split("～")[0].replace("（納戸）","")
        elif len(element.split("・")) != 1:
            return element.split("・")[0].replace("（納戸）","")
    return element

def max_madori(element):
    if element:
        if len(element.split("～")) == 1 and len(element.split("・")) == 1:
            return element.replace("（納戸）","")
        elif len(element.split("～")) != 1:
            return element.split("～")[1].split("※")[0].replace("（納戸）","")
        elif len(element.split("・")) != 1:
            return element.split("・")[1].split("※")[0].replace("（納戸）","")
    return element


class KodateItem(scrapy.Item):  

    name = scrapy.Field(
        output_processor = TakeFirst()
    )
    category = scrapy.Field(
        output_processor = TakeFirst()
    )
    price = scrapy.Field(
        output_processor = TakeFirst()
    )
    min_price = scrapy.Field(
        input_processor = MapCompose(min_price,convert_100million,convert_integer),
        output_processor = TakeFirst()
    )

    max_price = scrapy.Field(
        input_processor = MapCompose(max_price,convert_100million,convert_integer),
        output_processor = TakeFirst()
    )

    tochi_measure = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t),
        output_processor = Join(' ')
    )
    min_tochi_measure = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,min_measure,convert_float),
        output_processor = TakeFirst()
    )
    max_tochi_measure = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,max_measure,convert_float),
        output_processor = TakeFirst()
    )

    tatemono_measure = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t),
        output_processor = Join(' ')
    )
    min_tatemono_measure = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,min_measure,convert_float),
        output_processor = TakeFirst()    
    )

    max_tatemono_measure = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,max_measure,convert_float),
        output_processor = TakeFirst()
    )
    
    madori = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t),
        output_processor = TakeFirst()
    )
    min_madori = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,min_madori),
        output_processor = TakeFirst()        
    )
    max_madori = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,max_madori),
        output_processor = TakeFirst()       
    )
    

    hikiwatashi = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t),
        output_processor = TakeFirst()
    )
    kanseijiki = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t),
        output_processor = TakeFirst()
    )
    floor = scrapy.Field()
    building = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t),
        output_processor = TakeFirst()
    )
    adress = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t),
        output_processor = TakeFirst()
    )
    nearest_line = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,nearest_line),
        output_processor = TakeFirst()
    )
    nearest_station = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,nearest_station),
        output_processor = TakeFirst()
    )
    walk_time = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,walk_time,convert_integer),
        output_processor = TakeFirst()
    )
    nearest_bus_station = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,nearest_bus_station),
        output_processor = TakeFirst()
    )
    bus_time = scrapy.Field(
        input_processor = MapCompose(strip_r,strip_n,strip_t,bus_time,convert_integer),
        output_processor = TakeFirst()
    )

    url = scrapy.Field(
        output_processor = TakeFirst()
    )