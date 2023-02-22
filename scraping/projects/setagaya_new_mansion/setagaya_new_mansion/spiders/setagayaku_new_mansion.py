import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging 


class SetagayakuNewMansionSpider(CrawlSpider):
    name = 'setagayaku_new_mansion'
    allowed_domains = ['suumo.jp']
    start_urls = ['https://suumo.jp/ms/shinchiku/tokyo/sc_setagaya/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2/a'), callback='parse', follow=False), #各物件への詳細ページへ
        # Rule(LinkExtractor(restrict_xpaths='(//a[contains(text(),"次へ")])[1]')) #2ぺージ目以降へ
    )

    def get_price(self, price):
        if price:
            return price.replace('\r\n\t\t\t\t\t\t\t', '')
        return price

    def get_measure(self, measure):
        if measure:
            return float(measure.replace('m','').replace('\r\n\t\t\t\t\t', ''))
        return measure
    
    def get_madori(self, madori):
        if madori:
            return madori.replace('\r\n\t\t\t\t\t', '')
        return madori
    
    def get_hikiwatashi(self, hikiwatashi):
         if hikiwatashi:
              return hikiwatashi.replace('\r\n\t\t\t\t\t', '')
         return hikiwatashi

    # def get_kanseijiki(self, kanseijiki):
    #      if kanseijiki:
    #           return kanseijiki.replace('\r\n\t\t\t', '')
    #      return kanseijiki

    # def get_floor(self, floor):
    #      if floor:
    #           return int(floor.replace('階', '').replace('\r\n\t\t\t', ''))
    #      return floor
    
    # def get_building(self, building):
    #      if building:
    #           return building.replace('\r\n\t\t\t', '')
        #  return building

    # def get_koutsuu(self, koutsuu):
    #      if koutsuu:
    #           return koutsuu.replace('\r\n\t\t\t', '')
    #      return koutsuu

    def get_nearest_line(self,nearest_line):
        if nearest_line:
            return nearest_line.split("「")[0].replace('\r\n\t\t\t\t\t', '')
        return nearest_line
    
    def get_nearest_station(self,nearest_station):
        if nearest_station:
            return nearest_station.split("「")[1].split("」")[0]
        return nearest_station

    def get_walk_time(self,walk_time):
        if walk_time:
            return int(walk_time.split("」")[-1].replace("歩","").replace("分",""))
        return walk_time

    def get_adress(self,adress):
         if adress:
              return adress.replace('\r\n\t\t\t\t\t\t\t', '')
    


    def parse(self, response):
            logging.info(response.url)
            yield{
                'name': response.xpath('(//span[@class="section_h1-title"])[1]/text()').get(),
                # 'category':response.xpath('//li[@class="fl mt5 mr10 pct01"][1]/text()').get(),
                'price':self.get_price(response.xpath('(//span[@class="overview-txt_emplasis"])[1]/text()').get()),
                'measure': self.get_measure(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[3]/text()').get()),
                'madori': self.get_madori(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[2]/text()').get()),
                'hikiwatashi': self.get_hikiwatashi(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[4]/text()').get()),
                # 'kanseijiki': self.get_kanseijiki(response.xpath('(//td[@class="w299 bdCell"])[14]/text()').get()),
                # 'floor': self.get_floor(response.xpath('(//td[@class="w299 bdCell"])[15]/text()').get()),
                # 'building': self.get_building(response.xpath('(//td[@class="w299 bdCell"])[22]/text()').get()),
                'adress': self.get_adress(response.xpath('(//div[@class="overview_table-flexitem"])[1]/text()').get()),
                'nearest_line': self.get_nearest_line(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[1]/text()').get()),
                'nearest_station': self.get_nearest_station(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[1]/text()').get()),
                'walk_time': self.get_walk_time(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[1]/text()').get()),
                'url': response.request.url,
                }


