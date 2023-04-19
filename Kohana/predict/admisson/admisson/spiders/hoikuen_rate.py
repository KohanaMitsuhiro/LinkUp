import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import logging

class HoikuenRateSpider(CrawlSpider):
    name = 'hoikuen_rate'
    allowed_domains = ['www.hokatsunomikata.com']
    start_urls = ['https://www.hokatsunomikata.com/taiki_infos/prefectures/13']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="select-bar-detail"]//a'), callback='parse_item', follow=False),
    )

    def convert_percent(self,rate):
        if rate:
            if rate == "データなし":
                return 0
            return float(rate.split("%")[0])
        return rate


    def parse_item(self, response):
        # logging.info(response.text)
        # tbodyで指定したが、response.textで確認すると、なぜかtbody要素が存在しなかった。
        yield{
            "name":response.xpath('//li[@itemprop="itemListElement"]/span[@itemprop="name"]/text()').get(),
            "rate":{"2022":self.convert_percent(response.xpath('(//table)[1]//td[contains(text(),"2022")]/following-sibling::td[1]/text()').get()),
                    "2021":self.convert_percent(response.xpath('(//table)[1]//td[contains(text(),"2021")]/following-sibling::td[1]/text()').get()),
                    "2020":self.convert_percent(response.xpath('(//table)[1]//td[contains(text(),"2020")]/following-sibling::td[1]/text()').get()),
                    "2019":self.convert_percent(response.xpath('(//table)[1]//td[contains(text(),"2019")]/following-sibling::td[1]/text()').get()),
                    "2018":self.convert_percent(response.xpath('(//table)[1]//td[contains(text(),"2018")]/following-sibling::td[1]/text()').get()),
                    },
            "capacity":{"2022":response.xpath('(//table)[2]//td[contains(text(),"2022")]/following-sibling::td[1]/text()').get(),
                    "2021":response.xpath('(//table)[2]//td[contains(text(),"2021")]/following-sibling::td[1]/text()').get(),
                    "2020":response.xpath('(//table)[2]//td[contains(text(),"2020")]/following-sibling::td[1]/text()').get(),
                    "2019":response.xpath('(//table)[2]//td[contains(text(),"2019")]/following-sibling::td[1]/text()').get(),
                    "2018":response.xpath('(//table)[2]//td[contains(text(),"2018")]/following-sibling::td[1]/text()').get(),
                    },
            "entry_num":{"2022":response.xpath('(//table)[3]//td[contains(text(),"2022")]/following-sibling::td[1]/text()').get(),
                    "2021":response.xpath('(//table)[3]//td[contains(text(),"2021")]/following-sibling::td[1]/text()').get(),
                    "2020":response.xpath('(//table)[3]//td[contains(text(),"2020")]/following-sibling::td[1]/text()').get(),
                    "2019":response.xpath('(//table)[3]//td[contains(text(),"2019")]/following-sibling::td[1]/text()').get(),
                    "2018":response.xpath('(//table)[3]//td[contains(text(),"2018")]/following-sibling::td[1]/text()').get(),
                    }
        }
