import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging
from setagaya.items import KodateItem
from scrapy.loader import ItemLoader

class SetagayaSpider(CrawlSpider):
    name = 'kodate'
    allowed_domains = ['suumo.jp']
    start_urls = ['https://suumo.jp/ikkodate/tokyo/sc_setagaya/','https://suumo.jp/chukoikkodate/tokyo/sc_setagaya/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//h2[@class="property_unit-title"]/a'), callback='parse_item', follow=False),
        Rule(LinkExtractor(restrict_xpaths='//a[contains(text(),"次へ")]')),
    )

    def parse_item(self, response):
        # logging.info(response.url)
        loader = ItemLoader(item=KodateItem(),response=response)

        loader.add_xpath('name','//h1/text()')
        loader.add_xpath('category','//div[@class="cf mt10"]/div[@class="fl w420"]/ul/li[1]/text()')
        
        loader.add_xpath('price','(//div[contains(text(),"価格")]/../following-sibling::td[1]/p)[1]/text()')
        loader.add_xpath('min_price','(//div[contains(text(),"価格")]/../following-sibling::td[1]/p)[1]/text()')
        loader.add_xpath('max_price','//div[contains(text(),"価格")]/../following-sibling::td[1]/p[contains(text(),"万円")]/text()')
        
        tochi = response.xpath('(//div[@class="fl" and contains(text(),"土地面積")])[1]/../following-sibling::td[1]/text()').getall()
        loader.add_value('tochi_measure',"".join(tochi))
        loader.add_value('min_tochi_measure',"".join(tochi))
        loader.add_value('max_tochi_measure',"".join(tochi))

        tatemono = response.xpath('(//div[@class="fl" and contains(text(),"建物面積")])[1]/../following-sibling::td[1]/text()').getall()
        loader.add_value('tatemono_measure',"".join(tatemono))
        loader.add_value('min_tatemono_measure',"".join(tatemono))        
        loader.add_value('max_tatemono_measure',"".join(tatemono))
        
        loader.add_xpath('madori','//div[contains(text(),"間取り")]/../following-sibling::td/p/text()')
        loader.add_xpath('min_madori','//div[contains(text(),"間取り")]/../following-sibling::td/p/text()')        
        loader.add_xpath('max_madori','//div[contains(text(),"間取り")]/../following-sibling::td/p/text()')
        
        loader.add_xpath('hikiwatashi','//div[contains(text(),"引渡可能時期")]/../following-sibling::td[1]/text()')
        loader.add_xpath('kanseijiki','//div[contains(text(),"完成時期(築年月)")]/../following-sibling::td[1]/text()')
        # loader.add_xpath('floor','')
        loader.add_xpath('building','//div[contains(text(),"構造・工法")]/../following-sibling::td[1]/text()')
        loader.add_xpath('adress','//div[contains(text(),"所在地")]/../following-sibling::td[1]/text()')
        loader.add_xpath('nearest_line','//th[contains(text(),"交通")]/following-sibling::td/div[1]/text()')
        loader.add_xpath('nearest_station','//th[contains(text(),"交通")]/following-sibling::td/div[1]/text()')
        loader.add_xpath('walk_time','//th[contains(text(),"交通")]/following-sibling::td/div[1]/text()')
        loader.add_xpath('nearest_bus_station','//th[contains(text(),"交通")]/following-sibling::td/div[1]/text()')
        loader.add_xpath('bus_time','//th[contains(text(),"交通")]/following-sibling::td/div[1]/text()')
        loader.add_value('url',response.request.url)

        yield loader.load_item()