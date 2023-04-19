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

    def get_min_price(self, min_price):
        if min_price:
            try:
                return int(min_price.replace('\r\n\t\t\t\t\t\t\t', '').replace('億', '').replace('万', '').replace('円', '').replace('台', '').split('～')[0])
            except:
                return min_price.replace('\r\n\t\t\t\t\t\t\t', '')
        return min_price
    
    def get_max_price(self, max_price):
        if max_price:
            try:
                return int(max_price.replace('\r\n\t\t\t\t\t\t\t', '').replace('億', '').replace('万', '').replace('円', '').replace('台', '').split('～')[-1])
            except:
                return max_price.replace('\r\n\t\t\t\t\t\t\t', '')
        return max_price

    def get_measure(self, measure):
        if measure:
            return '・'.join(measure).replace('\r\n\t\t\t\t\t', '').replace('・', '').replace('m', '')
        return measure
    
    def get_min_measure(self, min_measure):
        if min_measure:
            return float('・'.join(min_measure).replace('\r\n\t\t\t\t\t', '').replace('・', '').replace('m', '').split('～')[0])
        return min_measure
    
    def get_max_measure(self, max_measure):
        if max_measure:
            return float('・'.join(max_measure).replace('\r\n\t\t\t\t\t', '').replace('・', '').replace('m', '').split('～')[-1])
        return max_measure
        
    
    def get_madori(self, madori):
        if madori:
            return madori.replace('\r\n\t\t\t\t\t', '')
        return madori
    
    def get_min_madori(self, min_madori):
        if min_madori:
            return min_madori.replace('\r\n\t\t\t\t\t', '').split('～')[0]
        return min_madori
    
    def get_max_madori(self, max_madori):
        if max_madori:
            return max_madori.replace('\r\n\t\t\t\t\t', '').split('～')[-1]
        return max_madori
    
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
                'min_price': self.get_min_price(response.xpath('(//span[@class="overview-txt_emplasis"])[1]/text()').get()),
                'max_price': self.get_max_price(response.xpath('(//span[@class="overview-txt_emplasis"])[1]/text()').get()),
                'measure': self.get_measure(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[3]/text()').getall()),
                'min_measure':self.get_min_measure(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[3]/text()').getall()),
                'max_measure':self.get_max_measure(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[3]/text()').getall()),
                'madori': self.get_madori(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[2]/text()').get()),
                'min_madori': self.get_min_madori(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[2]/text()').get()),
                'max_madori': self.get_max_madori(response.xpath('(//td[@class="overview_table-body overview_table-body--singleline"])[2]/text()').get()),
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


